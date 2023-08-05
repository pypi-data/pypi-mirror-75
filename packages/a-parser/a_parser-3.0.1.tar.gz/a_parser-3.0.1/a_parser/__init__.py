# AParser Python v3 API
from urllib import request
import json, time

class AParser:
    def __init__(self, uri, password):
        self.password = password
        self.uri = uri

    def doRequest(self, action, data = None, options = {}):
        params = { 'password': self.password, 'action': action }

        if data:
            data.update(options)
            params['data'] = data

        body = bytes(json.dumps(params), 'utf-8')
        headers = { 'Content-Type': 'application/json; charset=utf-8' }
        req = request.Request(self.uri, data=body, headers=headers)
        response = request.urlopen(req).read().decode('utf-8')
        responseData = json.loads(response)
        return responseData

    def ping(self):
        return self.doRequest('ping')

    def info(self):
        return self.doRequest('info')

    def getProxies(self):
        return self.doRequest('getProxies')

    def getParserPreset(self, parser, preset):
        data = { 'parser': parser, 'preset': preset }
        return self.doRequest('getParserPreset', data)

    def oneRequest(self, parser, preset, query, **kwargs):
        data = { 'parser': parser, 'preset': preset, 'query': query }
        return self.doRequest('oneRequest', data, kwargs)

    def bulkRequest(self, parser, preset, configPreset, threads, queries, **kwargs):
        data = { 'parser': parser, 'preset': preset, 'configPreset': configPreset, 'threads': threads, 'queries': queries }
        return self.doRequest('bulkRequest', data, kwargs)

    def addTask(self, parsers, configPreset, queriesFrom, queries, **kwargs):
        data = {
            'parsers': parsers, 'configPreset': configPreset, 'queriesFrom': queriesFrom,
            'queries' if queriesFrom == 'text' else 'queriesFile': queries
        }

        return self.doRequest('addTask', data, kwargs)

    def getTaskState(self, task_id):
        data = { 'taskUid': task_id }
        return self.doRequest('getTaskState', data)

    def getTaskConf(self, task_id):
        data = { 'taskUid': task_id }
        return self.doRequest('getTaskConf', data)

    def changeTaskStatus(self, task_id, to_status):
        # starting|pausing|stopping|deleting
        data = { 'taskUid': task_id, 'toStatus': to_status }
        return self.doRequest('changeTaskStatus', data)

    def waitForTask(self, task_id, interval = 5):
        while True:
            response = self.getTaskState(task_id)
            if 'data' not in response:
                return response
            state = response['data']
            if state['status'] == 'completed':
                return state
            time.sleep(interval)

    def moveTask(self, task_id, direction):
        # start|end|up|down
        data = { 'taskUid': task_id, 'direction': direction }
        return self.doRequest('moveTask', data)

    def getTaskResultsFile(self, task_id):
        data = { 'taskUid': task_id }
        return self.doRequest('getTaskResultsFile', data)

    def deleteTaskResultsFile(self, task_id):
        data = { 'taskUid': task_id }
        return self.doRequest('deleteTaskResultsFile', data)

    def getTasksList(self):
        return self.doRequest('getTasksList')

    def getParserInfo(self, parser):
        data = { 'parser': parser }
        return self.doRequest('getParserInfo', data)

    def getAccountsCount(self):
        return self.doRequest('getAccountsCount')

    def update(self):
        return self.doRequest('update')
