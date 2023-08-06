import os


class Job(object):
    def __init__(self, id=0, driver='', site='', worker='', container='', host='', token=''):
        self.id = id
        self.driver = driver
        self.site = site
        self.worker = worker
        self.container = container
        self.host = host
        self.token = token

    def get_image_volumes_and_command(self):
        return ('patrikpihlstrom/anna-' + self.driver + ':latest', {'/tmp/anna/': {'bind': '/tmp', 'mode': 'rw'}},
                'python3 /home/seluser/anna/anna/__main__.py -v -H -d ' + self.driver + ' -s ' + self.site + ' --host ' +
                self.host + ' --token "' + self.token + '" -i ' + self.id)

    def dict(self):
        result = {}
        for attribute in attributes:
            value = self.__getattribute__(attribute)
            if value is not None:
                if attribute == 'log':
                    value = '""' + value + '""'
                result[attribute] = value
        return result


attributes = ('container', 'driver', 'site', 'worker')
