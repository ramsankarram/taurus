import os
import time
import json

LOGGING_ON = False
LOG_DIR = '/tmp/bm_data'


class DataLogger(object):
    def __init__(self, clean=False):
        self.file_name = os.path.join(LOG_DIR, 'data')
        if clean and os.path.exists(self.file_name):
            os.remove(self.file_name)

    def save(self, req, resp):
        with open(self.file_name, 'a') as _file:
            _file.write('request: {}\n'
                        'response status_code: {}\n'
                        'response reason: {}\n'
                        'response content: {}\n\n'.format(
                            req, resp.status_code, resp.reason, json.dumps(json.loads(resp.content))))


class TimeLogger(object):
    def __init__(self, clean=False):
        self.file_name = os.path.join(LOG_DIR, 'timer')
        if clean and os.path.exists(self.file_name):
            os.remove(self.file_name)

    def my_time(self):
        t = time.time()
        with open(self.file_name, 'a') as _file:
            _file.write('{}\n'.format(t))
        return t


class DataReader(object):
    def __init__(self):
        self.file_name = os.path.join(LOG_DIR, 'data')
        self.data = []
        self.read()

    def read(self):
        with open(self.file_name) as _file:
            content = _file.read().split('\n')[:-1]
            while content:
                request = content.pop(0)[len('request: '):]
                resp_status_code = int(content.pop(0)[len('response status_code: '):])
                resp_reason = content.pop(0)[len('response reason: '):]
                resp_content = content.pop(0)[len("response content:"):]

                content.pop(0)  # empty line
                response = MockResponse(content=resp_content, status_code=resp_status_code, reason=resp_reason)
                self.data.append({'request': request, 'response': response})

    def get(self):
        transaction = self.data.pop(0)
        return transaction['request'], transaction['response']


class TimeReader(object):
    def __init__(self):
        self.file_name = os.path.join(LOG_DIR, 'timer')
        self.times = []
        self.read()

    def read(self):
        with open(self.file_name) as _file:
            content = _file.read().split('\n')[:-1]
            while content:
                t = float(content.pop(0))
                self.times.append(t)

    def my_time(self):
        t = self.times.pop(0)
        return t


class MockResponse(object):
    def __init__(self, content, status_code, reason):
        self.content = content
        self.status_code = status_code
        self.reason = reason


if LOGGING_ON:
    s_data = DataLogger(clean=True)
    s_time = TimeLogger(clean=True).my_time
else:
    s_data = DataReader()
    s_time = TimeReader().my_time
