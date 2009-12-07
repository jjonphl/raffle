import sqlite3
import os
from sqlalchemy.pool import SingletonThreadPool

__db__ = 'numbers.db'

def __fail_safe_setup():
    con = sqlite3.connect(__db__)
    cu  = con.cursor()
    cu.execute('''
       select count(*) from sqlite_master 
       where type='table' and name='numbers' ''')
    res = cu.fetchone()
    if res[0] == 0:
        cu.execute('''
            create table numbers(
              c1 int, c2 int, c3 int, c4 int, c5 int, c6 int, 
              name text, employer text,
              primary key(c1, c2, c3, c4, c5, c6))            ''')
    cu.execute('''
       select count(*) from sqlite_master 
       where type='table' and name='status' ''')
    res = cu.fetchone()
    if res[0] == 0:
        cu.execute('create table status(status text)')
        cu.execute("insert into status(status) values ('unlocked')")
    con.commit()
    cu.close()
    con.close()
    
def __get_connection():
    return pool.connect()

__fail_safe_setup()
pool = SingletonThreadPool(lambda: sqlite3.connect(__db__))

def find_num(num, limit=60):
    if not type(num) == str:
        raise 'Parameter should be a string!'
    if len(num) > 6:
        num = num[0:6]
    if len(num) == 0:
        return []
    digits = len(num)
    cols = ','.join(['c' + str(n+1) for n in range(digits)])
    parm = ','.join(['?'] * digits)
    where_clause = ' and '.join(['c' + str(n+1) + '=?' for n in range(digits)])
    params = list(num)
    con = __get_connection()
    cu = con.cursor()
    count = cu.execute('select count(*) from numbers where %s' % where_clause,
                params).fetchone()
    cu.execute('''
        select c1||c2||c3||c4||c5||c6 from numbers where %s 
        order by c1,c2,c3,c4,c5,c6 limit ?''' % where_clause, params + [limit])
    numbers = cu.fetchall()
    if len(num) < 6:
        n = len(num) + 1
        next = cu.execute('select distinct(c%d) from numbers where %s' %
                (n, where_clause), params).fetchall()
        next = [n[0] for n in next]
    else:
        next = []
    ret = {'count': count[0], 'numbers': numbers, 'next': next}
    cu.close()
    return ret

def find_first_digits():
    con = __get_connection()
    cu = con.cursor()
    next = cu.execute('select distinct(c1) from numbers').fetchall()
    cu.close()
    return [n[0] for n in next]

def numbers_count():
    con = __get_connection()
    cu = con.cursor()
    count = cu.execute('select count(*) from numbers').fetchone()
    cu.close()
    return count[0]

def is_db_locked():
    con = __get_connection()
    cu  = con.cursor()
    res = cu.execute('select status from status limit 1')
    ret = cu.fetchone()
    try:
        if not res:
            raise RuntimeError('Database in unknown state: no status record found.')
        if ret[0] == 'locked':
            return True
        elif ret[0] == 'unlocked':
            return False
        else:
            raise RuntimeError('Database in unknown state: status (%s).' % res[0])
    finally:
        cu.close()

def lock_db(lock):
    con = __get_connection()
    cu  = con.cursor()
    status = 'locked' if lock else 'unlocked'
    res = cu.execute('update status set status=?', (status,))
    con.commit()

def load_numbers(lines):
    con = __get_connection()
    cu  = con.cursor()
    errors = 0
    cu.execute('delete from numbers')
    for line in lines:
        num, name, emp = line[0], line[1], line[2]
        try:
            params = [int(i) for i in num] + [name, emp]
            cu.execute('insert into numbers(c1,c2,c3,c4,c5,c6,name,employer) values(?,?,?,?,?,?,?,?)',
                    params)
        except:
            errors = errors + 1

    con.commit()
    cu.close()
    return errors
