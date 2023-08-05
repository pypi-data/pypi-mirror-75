Python module for working with A-Parser API.
Compatible with Python version 2.7.* and >=3.8.

# Usage
```
# example
from a_parser import AParser

aparser = AParser('http://127.0.0.1:9091/API', 'your pass')
print(aparser.ping())

# output
# { 'success': 1, 'data': 'pong' }

taskId = aparser.addTask(
    [['SE::Google', 'default',
        {
            'type': 'override',
            'id': 'formatresult',
            'value': '$serp.format("$anchor\\n")'
        }, {
            'type': 'override',
            'id': 'pagecount',
            'value': 1
        }, {
            'type': 'override',
            'id': 'useproxy',
            'value': False
        }
    ]],
    'default',
    'text',
    'diamond',
    resultsFormat= '$p1.preset',
    uniqueQueries= False,
    queryFormat= ['$query'],
    resultsUnique= 'no',
    resultsSaveTo= 'file',
    resultsFileName= '$datefile.format().txt',
    doLog= 'no',
    keepUnique= 'No',
    moreOptions= False,
    resultsPrepend= '',
    resultsAppend= '',
    configOverrides= [],
    queryBuilders= []
)['data']

aparser.waitForTask(taskId)
print(aparser.getTaskResultsFile(taskId))

# output
# {'success': 1, 'data': 'http://127.0.0.1:9091/downloadResults?fileName=Jul-29_17-33-37.txt&token=utmxidbc'}

print(aparser.oneRequest('SE::Yahoo::Suggest', 'default', 'spider'))

# output
# {'success': 1, 'data': {'resultString': 'spider - spider:\nspider solitaire\nspiderman\nspider bites\nspider bite pictures\nspider solitaire two suits\nspider plant\nspider-man\nspider solitaire free\nspider bites pictures and symptoms\nspider monkey\n', 'logs': [[0, 1596033005, 'Parser SE::Yahoo::Suggest::0 parse query spider'], [0, 1596033005, 'Use proxy http://51.255.55.144:28466'], [0, 1596033006, 'GET(1): http://sugg.search.yahoo.com/gossip-us-fp/?nresults=10&amp;output=yjson&amp;version=&amp;command=spider - 200 OK (0.3 KB)'], [3, 1596033006, 1], [0, 1596033006, 'Thread complete work']]}}
```

# Documentation
https://a-parser.com/wiki/user-api/
