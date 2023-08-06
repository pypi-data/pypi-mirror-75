import json
import os


class Configuration:
    def __init__(self):
        self.config = dict()
        self.config_directory = os.path.sep.join(
                    [os.path.expanduser("~"), ".faas"])
        self.config_file = os.path.sep.join([self.config_directory,
                                             "config.json"])

    def create_dir(self):
        if not os.path.exists(self.config_directory):
            os.mkdir(self.config_directory)

    def touch_config(self):
        if not os.path.exists(self.config_file
                ) or os.path.getsize(self.config_file) < 21:
            return False
        with open(self.config_file, "a") as f:
            if not f.writable():
                return False
        return True

    @staticmethod
    def fill_config(_client):
        _conf = {'username ': _client.username,
                'access_token': _client.access_token,
                'refresh_token': _client.refresh_token}
        if hasattr(_client, 'endpoint'):
            _conf.update({'endpoint': _client.endpoint})
        return _conf

    def load_config(self):
        if not os.path.exists(self.config_file
                ) or os.path.getsize(self.config_file) < 21:
            return None
        with open(self.config_file, 'r') as f:
            try:
                return json.loads(f.read())
            except:
                return False

    def __getitem__(self, item):
        if item in self.config:
            return self.config[item]
        else:
            return None

    def __setitem__(self, key, value):
        self.config[key] = value
        self.save_config()

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.config)

    def __iter__(self):
        return iter(self.config)

    def save_config(self):
        if not os.path.exists(self.config_directory):
            self.create_dir()
        with open(self.config_file, "w") as f:
            f.write(json.dumps(self.config))

    def delete_config(self):
        if os.path.exists(self.config_file):
            os.remove(self.config_file)
