import sys
import os

sys.path.append(os.path.join(sys.path[0], 'webpy'))

import web

urls = ('/', 'Raffle',
        '/setup', 'Setup')

app = web.application(urls, globals())

class Raffle(object):
    def GET(self):
        return 'hello fucking world'

class Setup(object):
    def GET(self):
        pass

if __name__ == '__main__':
    app.run()
