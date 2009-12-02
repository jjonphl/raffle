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
            next = dao.find_first_digits()
            return json.dumps({'status': 'empty', 'next': next})

        result = dao.find_num(str(num))
        status = 'ok'
        return json.dumps({'status': status, 
            'count': result['count'], 'next': result['next'],
            'numbers':[r[0] for r in result['numbers']]})

class Setup(object):
    def GET(self):
        return render.setup(dao.numbers_count())
    def POST(self):
        form = web.input(_unicode=True, numbers={})
        error = None
        web.debug(form)
        if 'numbers' in form:
            errors = dao.load_numbers(form.numbers.file)
            if errors > 0:
                error = 'Error in %d lines.' % errors
        else:
            error = 'No file uploaded'
        msg = None if error else ('Successfully uploaded %s.' % form.numbers.filename)
        return render.setup(dao.numbers_count(), msg, error)


if __name__ == '__main__':
    app.run()
