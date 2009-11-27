#!/usr/bin/python

import sqlite3
import sys

def find_num(con, num):
    if not type(num) == str:
        raise 'This is crazy'
    digits = len(num)
    cols = ','.join(['c' + str(n+1) for n in range(digits)])
    parm = ','.join(['?'] * digits)
    where_clause = ' and '.join(['c' + str(n+1) + '=?' for n in range(digits)])
    params = [int(i) for i in num]
    cu = con.cursor()
    cu.execute('select c1||c2||c3||c4||c5||c6 from numbers where %s' %
            where_clause, params)
    ret = cu.fetchall()
    cu.close()
    print ret
    return ret

if __name__ == '__main__':
    con = sqlite3.connect('numbers.db')
    ret = find_num(con, sys.argv[1])
    print '\n'.join([s[0] for s in ret])
