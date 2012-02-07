import os
import ConfigParser

import MySQLdb

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
print(PROJECT_PATH)

config = ConfigParser.ConfigParser()
config.read(PROJECT_PATH + '/../jelentkezes/server_host.cfg')

db_name = config.get('database_settings', 'name')
db_user = config.get('database_settings', 'user')
db_password = config.get('database_settings', 'password')

db = MySQLdb.connect(host="localhost", port=3306, user=db_user, passwd=db_password, db=db_name)
cursor = db.cursor()
cursor.execute("""SELECT * FROM kurzusvalaszto_felhasznalo""")
print(u"Eddig targyat/kurzus felvett: {0} fo".format(len(cursor.fetchall())))

cursor.execute("""SELECT * FROM auth_user WHERE first_name!=''""")
print(u"Eddig sikeresen belepett: {0} fo".format(len(cursor.fetchall())))

cursor.execute("""SELECT * FROM auth_user""")
print(u"Eddig regisztralt: {0} fo".format(len(cursor.fetchall())))

bad = 0
good = 0
    
ft = open('nk.hszk.users', 'rb')
for line in ft.readlines():
    neptunmail = line.split('@')[0]
    cursor.execute("""SELECT * FROM auth_user WHERE email LIKE '{0}@nc.hszk.bme.hu'""".format(neptunmail))
    r = cursor.fetchall()
    bad = bad + 1
    if (len(r) != 0):
        good = good + 1
    
ft.close()

print('nk.hszk-s userek: {0}/{1}'.format(good,bad))
