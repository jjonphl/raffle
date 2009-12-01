import sys
import os

sys.path.append(os.path.join(sys.path[0], 'webpy'))

import web
import sqlite3
import json
from sqlalchemy.pool import SingletonThreadPool

from find_num import find_num

urls = ('/', 'Raffle',
        '/query', 'Query',
        '/setup', 'Setup')

app = web.application(urls, globals())
render = web.template.render('templates')
pool = SingletonThreadPool(lambda: sqlite3.connect('numbers.db'))

class Raffle(object):
    def GET(self):
        return render.raffle()

class Query(object):
    def GET(self):
        num = web.input(num='').num
        result = find_num(pool.connect(), str(num))
        return json.dumps({'status': status, 'results':[r[0] for r in result]})

class Setup(object):
    def GET(self):
        pass

if __name__ == '__main__':
    app.run()
