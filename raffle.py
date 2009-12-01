import sys
import os

sys.path.append(os.path.join(sys.path[0], 'webpy'))

import web
import json
import dao

urls = ('/', 'Raffle',
        '/query', 'Query',
        '/setup', 'Setup')

app = web.application(urls, globals())
render = web.template.render('templates')

class Raffle(object):
    def GET(self):
        return render.raffle()

class Query(object):
    def GET(self):
        num = web.input(num='').num
        if len(num) == 0:
            return json.dumps({'status': 'empty'})

        result = dao.find_num(str(num))
        status = 'ok'
        return json.dumps({'status': status, 
                           'count': result['count'],
                           'numbers':[r[0] for r in result['numbers']]})

class Setup(object):
    def GET(self):
        pass

if __name__ == '__main__':
    app.run()
