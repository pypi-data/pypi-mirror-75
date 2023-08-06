import json
import logging
import os

import requests

from faas import __version__ as version
from faas.core import Configuration


class FaasAPIClient:

    def __init__(self, access_token=None,
                 endpoint='https://api.sonra.io', refresh_token=None):
        # defaults
        self.password = None
        self.username = None
        self.user_agent = f'FaaS SDK v{version}'
        # load logger
        self.logger = logging.getLogger('root')
        self.logger.setLevel(logging.INFO)
        # endpoint
        _config = Configuration()
        setattr(_config, 'config', _config.load_config())
        if _config.config is not None and 'endpoint' in _config.config:
            self.endpoint = _config.config['endpoint']
        else:
            self.endpoint = endpoint

        if access_token is None:
            self.access_token = '' if _config.config is None else _config['access_token']
        else:
            self.access_token = access_token

        if refresh_token is None:
            self.refresh_token = '' if _config.config is None else _config['refresh_token']
        else:
            self.refresh_token = refresh_token

    def _send_request(self, endpoint, data=None, files=None,
                      method='get', multipart=False):
        url = self._generate_url(endpoint)
        headers = {}
        headers.update(self._generate_bearer_header())
        headers.update(self._generate_user_agent())
        self.logger.debug('Sending request [%s] [%s] [%s]',
                          url, data, headers)

        if (data or files) and method == 'get':
            method = 'post'

        params = {
            'headers': headers
        }

        if data:
            if multipart:
                params['data'] = data
            else:
                params['json'] = data

        if files:
            params['files'] = files

        response = requests.request(method=method, url=url, **params)
        if response.status_code != 200:
            if response.content:
                self.logger.debug(response.json())

            _errors = response.json()['errors']
            for _error in _errors:
                raise Exception(_error)

        if response.content:
            try:
                return response.json()
            except json.decoder.JSONDecodeError:
                pass
            return response.text
        else:
            return True

    def _generate_bearer_header(self):
        try:
            return {
                'authorization': 'Bearer ' + self.access_token,
            }
        except TypeError as ex:
            raise ValueError("Access token is not defined, please use FaasAPIClient.get_access_token(...) "
                             "to get access token using username and password. \n"
                             "Or define access_token, using FaaSAPIClient(access_token='...')")

    def _generate_user_agent(self):
        return {
            'User-Agent': self.user_agent
        }

    def _generate_url(self, endpoint):
        return self.endpoint + '/' + endpoint

    # authentication
    def get_access_token(self, username=None, password=None):
        if username is None:
            data = {
                'username': self.username,
                'password': self.password
            }
        else:
            data = {
                'username': username,
                'password': password
            }

        headers = {}
        headers.update(self._generate_user_agent())
        response = requests.post(self._generate_url('oauth/token'),
                                 data=data, headers=headers)
        if response.status_code != 200:
            return False

        response_json = response.json()

        if self.access_token is None:
            self.access_token = response_json['access_token']
        if self.refresh_token is None:
            self.refresh_token = response_json['refresh_token']

        return response_json['access_token'], response_json['refresh_token']

    # Schema source
    def list_schema_sources(self, _limit=None):
        if _limit is not None:
            return self._send_request(
                f'schema_sources?limit={_limit}')
        else:
            return self._send_request(
                'schema_sources')

    def get_schema_source(self, name):
        return self._send_request('schema_sources/{}'.format(name))

    def delete_schema_source(self, name):
        return self._send_request('schema_sources/{}'.format(name),
                                  method='delete')

    # ---> New option - allows multiply files and folders
    def create_file_schema_source(self, name, file):
        if isinstance(file, str):
            _file = [file]
        _files = list()
        for _f in _file:
            # Check whether source is a folder
            if os.path.isdir(_f):
                _files_in_folder = self.prepare_folder_as_source(
                    _f, 'xsd')
                for _curr_file in _files_in_folder:
                    _files.append(_curr_file)
            elif os.path.isfile(_f):
                _files.append(_f)

        data = {
            'source_type': 'uploaded_file'
        }
        if not _files:
            raise FileNotFoundError(_f)
        _file_pointers = list()
        for _f in _files:
            # check whether the file exists
            if not os.path.exists(_f):
                raise FileNotFoundError(_f)

            _file_pointers.append(('file', open(_f, 'rb')))

        _r = self._send_request('schema_sources/{}'.format(name),
                                data=data, files=_file_pointers,
                                multipart=True)
        for _f in _file_pointers:
            _f[1].close()
        return _r

    def create_s3_schema_source(self, name, path, role_arn):
        data = {
            'path': path,
            'role_arn': role_arn,
            'source_type': 's3'
        }
        return self._send_request('schema_sources/{}'.format(name),
                                  data=data, multipart=True)

    def create_http_schema_source(self, name, url):
        data = {'url': url,
                'source_type': 'http'}
        return self._send_request('schema_sources/{}'.format(name),
                                  data=data, multipart=True)

    # Data Source
    def list_data_sources(self, _limit=None):
        if _limit is not None:
            return self._send_request(
                f'data_sources?limit={_limit}')
        else:
            return self._send_request(
                'data_sources')

    def get_data_source(self, name):
        return self._send_request('data_sources/{}'.format(name))

    def delete_data_source(self, name):
        return self._send_request('data_sources/{}'.format(name),
                                  method='delete')

    # ---> Get all files of certain type from the folder
    def prepare_folder_as_source(self, _folder, _type):
        with os.scandir(_folder) as _entries:
            _fffs = [_entry.path for _entry in _entries
                     if self.check_extension(_entry, _type)
                     or self.check_extension(_entry, 'zip')]
        return _fffs

    # ---> Returns file's type
    def check_extension(self, _name, _ext):
        if not os.path.isfile(_name.path):
            return False
        _extension = _name.name.split('.')[-1]
        if _extension in _ext:
            return True

    # ---> File(s) as data_source creation
    def create_file_data_source(self, name, _type, _file):
        if isinstance(_file, str):
            _file = [_file]
        _files = list()
        for _f in _file:
            # Check whether source is a folder
            if os.path.isdir(_f):
                _files_in_folder = self.prepare_folder_as_source(
                    _f, _type)
                for _curr_file in _files_in_folder:
                    _files.append(_curr_file)
            elif os.path.isfile(_f):
                _files.append(_f)

        data = {
            'data_type': _type,
            'source_type': 'uploaded_file'
        }
        # checking existence of all files
        if not _files:
            raise Exception(
                f'FileNotFoundError {" ~ ".join(_file)}')

        _file_pointers = list()
        for _f in _files:
            if not os.path.exists(_f):
                raise FileNotFoundError(_f)

            _file_pointers.append(('file', open(_f, 'rb')))

        _r = self._send_request('data_sources/{}'.format(name),
                                data=data, files=_file_pointers,
                                multipart=True)
        for _f in _file_pointers:
            _f[1].close()
        return _r

    def create_s3_data_source(self, name, _type, path, role_arn):
        data = {
            'path': path,
            'role_arn': role_arn,
            'data_type': _type,
            'source_type': 's3'
        }
        return self._send_request('data_sources/{}'.format(name),
                                  data=data, multipart=True)

    # -------> HTTP data_source creation
    def create_source_http(self, _name, _url, _type):
        data = {
            'url': _url,
            'data_type': _type,
            'source_type': 'http'
        }
        return self._send_request('data_sources/{}'.format(_name),
                                  data=data, multipart=True)

    # Conversions
    def create_conversion(self, name, data_source, schema_source=None,
                          target="download_link", _append=None,
                          _use_stats='true', _prefix=None, _suffix=None):
        data = {
            'data_source': data_source,
            'schema_source': schema_source,
            'target': target,
            'append': _append,
            'use_stats': _use_stats,
            'prefix': _prefix,
            'suffix': _suffix
        }
        return self._send_request('conversions/{}'.format(name),
                                  data=data, multipart=True)

    def execute_conversion(self, name, data_flow, data_source=None,
                           target="download_link", _append=None,
                           _format='tsv', _prefix=None, _suffix=None):
        data = {
            "data_flow": data_flow
        }

        if data_source is not None:
            data.update({'data_source': data_source})
        if target is not None:
            data.update({'target': target})
        if _append is not None:
            data.update({'append': _append})
        if _prefix is not None:
            data.update({'prefix': _prefix})
        if _suffix is not None:
            data.update({'suffix': _suffix})
        if _format is not None:
            data.update({'format': _format.lower()})

        #     'schema_source': schema_source,
        #     'target': target,
        #     'append': _append,
        #     'use_stats': _use_stats,
        #     'prefix': _prefix,
        #     'suffix': _suffix
        # }
        return self._send_request('conversions/execute/{}'.format(name),
                                  data=data, multipart=True)

    def list_conversions(self, args):
        _expr = 'conversions?'
        if args.limit is not None:
            _expr += f'limit={args.limit}&'
        if args.filter_df is not None:
            _expr += f'filter_df={args.filter_df}&'
        return self._send_request(_expr)

    def get_conversion(self, name):
        return self._send_request('conversions/{}'.format(name))

    def delete_conversion(self, name):
        return self._send_request('conversions/{}'.format(name),
                                  method='delete')

    # DataFlow
    def create_dataflow(self, name,
                        source_data=None,
                        schema=None, optimize=True):
        data = {}
        if schema is not None:
            data.update({'schema_source': schema})
        if source_data is not None:
            data.update({'data_source': source_data})
        if optimize:
            data.update({'optimize': optimize})
        # if target is not None:
        #     data.update({'target': target})
        # if _format is not None:
        #     data.update({'format': _format})
        # if _prefix is not None:
        #     data.update({'prefix': _prefix})
        # if _suffix is not None:
        #     data.update({'suffix': _suffix})
        return self._send_request('dataflows/{}'.format(name),
                                  data=data, multipart=True)

    def list_dataflows(self, _limit=None):
        if _limit is not None:
            return self._send_request(
                f'dataflows?limit={_limit}')
        else:
            return self._send_request(
                'dataflows')

    def get_dataflow(self, name):
        return self._send_request('dataflows/{}'.format(name))

    def delete_dataflow(self, name):
        return self._send_request('dataflows/{}'.format(name),
                                  method='delete')

    def trigger_dataflow(self, _args):
        if _args.append is not None:
            data = {
                'append': _args.append
            }
        else:
            data = {
                'append': True
            }

        if _args.target is not None:
            data.update({'target':
                             _args.target})
        if _args.format is not None:
            data.update({'format':
                             _args.format})

        return self._send_request('dataflows/{}/conversion'.
                                  format(_args.name),
                                  data=data, multipart=True)

    # webhooks
    def create_webhook(self, name, url):
        data = {
            'url': url
        }
        return self._send_request('webhooks/{}'.format(name),
                                  data=data, multipart=True)

    def list_webhooks(self, _limit=None):
        if _limit is not None:
            return self._send_request(
                f'webhooks?limit={_limit}')
        else:
            return self._send_request(
                'webhooks')

    def get_webhook(self, name):
        return self._send_request('webhooks/{}'.format(name))

    def delete_webhook(self, name):
        return self._send_request('webhooks/{}'.format(name),
                                  method='delete')

    # Target connections
    def list_target_connections(self, _limit=None):
        if _limit is not None:
            return self._send_request(
                f'target_connections?limit={_limit}')
        else:
            return self._send_request(
                'target_connections')

    def get_target_connection(self, name):
        return self._send_request('target_connections/{}'.format(name))

    def delete_target_connection(self, name):
        return self._send_request('target_connections/{}'.format(name),
                                  method='delete')

    def create_s3_target_connection(self, name, path, role_arn):
        data = {
            'path': path,
            'role_arn': role_arn,
            'target_type': 's3'
        }
        return self._send_request('target_connections/{}'.
                                  format(name), data=data, multipart=True)

    def create_postgresql_target_connection(self, name, host,
                                            username, password, database, schema):
        data = {
            'host': host,
            'username': username,
            'password': password,
            'database': database,
            'schema': schema,
            'target_type': 'postgresql'
        }
        return self._send_request('target_connections/{}'.format(name),
                                  data=data, multipart=True)

    def create_mysql_target_connection(self, name, host, username,
                                       password, database):
        data = {
            'host': host,
            'username': username,
            'password': password,
            'database': database,
            'target_type': 'mysql'
        }
        return self._send_request('target_connections/{}'.format(name),
                                  data=data, multipart=True)

    def create_snowflake_target_connection(self, name, host,
                                           username, password, database, schema=None, warehouse=None,
                                           role=None):
        data = {
            'host': host,
            'username': username,
            'password': password,
            'database': database,
            'schema': schema,
            'warehouse': warehouse,
            'role': role,
            'target_type': 'snowflake'
        }
        return self._send_request('target_connections/{}'.format(name),
                                  data=data, multipart=True)

    def create_sqlserver_target_connection(self, name, host, username,
                                           password, database):
        data = {
            'host': host,
            'username': username,
            'password': password,
            'database': database,
            'target_type': 'sqlserver'
        }
        return self._send_request('target_connections/{}'.format(name),
                                  data=data, multipart=True)

    def create_oracle_target_connection(self, name, host, username,
                                        password, database):
        data = {
            'host': host,
            'username': username,
            'password': password,
            'database': database,
            'target_type': 'oracle'
        }
        return self._send_request('target_connections/{}'.
                                  format(name), data=data, multipart=True)

    def create_redshift_target_connection(self, name, host,
                                          username, password, database):
        data = {
            'host': host,
            'username': username,
            'password': password,
            'database': database,
            'target_type': 'redshift'
        }

        return self._send_request('target_connections/{}'.
                                  format(name), data=data, multipart=True)

    def create_bigquery_target_connection(self, name, dataset, storage, credentials):
        data = {
            'dataset': dataset,
            'storage': storage,
            'target_type': 'bigquery'
        }

        fp = open(credentials, 'rb')
        files = [
            ('file', fp)
        ]

        resp = self._send_request('target_connections/{}'.
                                  format(name), data=data, multipart=True, files=files)
        fp.close()
        return resp
