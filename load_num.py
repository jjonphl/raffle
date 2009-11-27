#!/usr/bin/python

import sqlite3

con = sqlite3.connect('numbers.db')
cu  = con.cursor()

cu.execute("select count(*) from sqlite_master where type='table' and name='numbers'")
res = cu.fetchone()
print res[0]
if res[0] == 0:
    cu.execute('create table numbers(c1 int, c2 int, c3 int, c4 int, c5 int, c6 int, primary key(c1, c2, c3, c4, c5, c6))')
else:
    cu.execute('delete from numbers')

f = open('numbers.txt')
for line in f:
    line = line.strip()
    digits = [int(i) for i in line]
    try:
        cu.execute('insert into numbers(c1,c2,c3,c4,c5,c6) values(?,?,?,?,?,?)',
                digits)
    finally:
        pass

con.commit()
con.close()
