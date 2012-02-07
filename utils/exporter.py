#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# using UTF-8 charset

import math
import os
import ConfigParser

import MySQLdb
from xlwt import Workbook, easyxf

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

OSZLOP_SZ_EGYSEG = 1000/0.77
SOR_M_EGYSEG = 1000/1.76

config = ConfigParser.ConfigParser()
config.read(PROJECT_PATH + '/../jelentkezes/server_host.cfg')

db_name = config.get('database_settings', 'name')
db_user = config.get('database_settings', 'user')
db_password = config.get('database_settings', 'password')

def get_kurzus_infok(db, id):
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM kurzusvalaszto_kurzus WHERE id='{0}'""".format(id))
    r = cursor.fetchall()
    
    if r[0][2] == 'H':
        nap = u'Hétfő'
    elif r[0][2] == 'K':
        nap = u'Kedd'
    elif r[0][2] == 'S':
        nap = u'Szerda'
    elif r[0][2] == 'C':
        nap = u'Csütörtök'
    elif r[0][2] == 'P':
        nap = u'Péntek'      
    
    return {'id': r[0][0],'nev': r[0][1].encode('utf-8'),'nap': nap.encode('utf-8'),'sav': r[0][3],'ferohely': r[0][4],'hallgatok_szama': r[0][5]}

def get_kurzus_hallgatok(db, id):
    kurzus_hallgatok = []
    cursor = db.cursor()
    cursor.execute("""SELECT username, last_name, first_name FROM \
        kurzusvalaszto_felhasznalo kf INNER JOIN auth_user au ON \
        kf.user_id = au.id WHERE kurzus_id='{0}';""".format(id))
    for row in cursor.fetchall():
        kurzus_hallgatok.append({'neptun': row[0].upper(), 'nev': "{0} {1}".format(row[1].encode('utf8'), row[2].encode('utf8'))})
    return kurzus_hallgatok
    
def create_shit_head(sheet, kurzus):
    sheet.write(0,1,'Nap/óra')
    sheet.col(1).width = int(math.ceil(OSZLOP_SZ_EGYSEG*2.04))
    
    sheet.write(1,1,'{0}/{1}'.format(kurzus['nap'],kurzus['sav']),easyxf(
        'font: bold True'
        ))

    sheet.write(0,2,'Tárgy-kurzus')
    sheet.col(2).width = int(math.ceil(OSZLOP_SZ_EGYSEG*4.08))
    sheet.write(1,2,'{0}'.format(kurzus['nev']),easyxf(
        'font: bold True'
        ))

    sheet.write_merge(0,0,18,19,'Oktató')
    sheet.col(18).width = int(math.ceil(OSZLOP_SZ_EGYSEG*0.84))

    sheet.write(4,0,'Ssz',easyxf(
        'borders: left thick, right thick, top thick, bottom thick;'
        ))
    sheet.col(0).width = int(math.ceil(OSZLOP_SZ_EGYSEG*0.81))

    sheet.write(4,1,'Azonosító',easyxf(
        'borders: left thick, right thick, top thick, bottom thick;'
        ))

    sheet.write(4,2,'Név',easyxf(
        'borders: left thick, right thick, top thick, bottom thick; alignment: horizontal center;'
        ))

    sheet.write(4,3,'Képzés',easyxf(
        'borders: left thick, right thick, top thick, bottom thick; alignment: horizontal center;'
        ))
    sheet.col(3).width = int(math.ceil(OSZLOP_SZ_EGYSEG*1.54))


    sheet.write(4,18,'A',easyxf(
        'borders: left thick, right thick, top thick, bottom thick; alignment: horizontal center;'
        ))

    sheet.write(4,19,'Megjegyzés',easyxf(
        'borders: left thick, right thick, top thick, bottom thick; alignment: horizontal center;'
        ))
    sheet.col(19).width = int(math.ceil(OSZLOP_SZ_EGYSEG*2.77))

    for i in xrange(4,18):
        sheet.col(i).width = int(math.ceil(OSZLOP_SZ_EGYSEG*0.53))
    
    for i in xrange(0,4):
        sheet.row(i).height = int(math.ceil(SOR_M_EGYSEG*0.52))

    for r in xrange(4,50):
        sheet.row(r).height = int(math.ceil(SOR_M_EGYSEG*0.56))
    
    for c in xrange(4,18):
        sheet.write(4,c,'',easyxf(
        'borders: left thick, right thick, top thick, bottom thick; alignment: horizontal center;'
        ))
    
    return sheet

def create_excel_file(db, kurzus):
    book = Workbook(encoding='utf-8')
    #sheet = book.add_sheet('{0} - {1} - {2}'.format(kurzus['nev'],kurzus['nap'],kurzus['sav']))
    sheet = book.add_sheet('Névsor')

    sheet = create_shit_head(sheet, kurzus_infok)
    
    kurzus_hallgatok = get_kurzus_hallgatok(db, kurzus['id'])
    
    sorszam = 1
    
    for user in kurzus_hallgatok:
        sheet.write(sorszam+4,0,sorszam,easyxf(
        'borders: left thick, right thick, top thick, bottom thick;'
        ))
        sheet.write(sorszam+4,1,user['neptun'],easyxf(
        'borders: left thick, right thick, top thick, bottom thick;'
        ))
        sheet.write(sorszam+4,2,user['nev'],easyxf(
        'borders: left thick, right thick, top thick, bottom thick;'
        ))
        for i in xrange(3,20):
            sheet.write(sorszam+4,i,'',easyxf(
        'borders: left thick, right thick, top thick, bottom thick;'
        ))
        sorszam = sorszam + 1
    
    book.save('{0}_{1}_{2}.xls'.format(ekezet_eltunteto(kurzus['nev'].lower()),
        ekezet_eltunteto(kurzus['nap'].lower()),
        kurzus['sav']))

def ekezet_eltunteto(s):
    s = s.replace('á', 'a')
    s = s.replace('é', 'e')
    s = s.replace('í', 'i')
    s = s.replace('ó', 'o')
    s = s.replace('ö', 'o')
    s = s.replace('ő', 'o')
    s = s.replace('ú', 'u')
    s = s.replace('Ú', 'u')
    s = s.replace('ü', 'u')
    s = s.replace('ű', 'u')
    return s

db = MySQLdb.connect(host="localhost", port=3306, user=db_user, passwd=db_password, db=db_name, charset="utf8", use_unicode=True)
cursor = db.cursor()
cursor.execute("""SELECT * FROM kurzusvalaszto_kurzus""")

kurzus_id = 0

for i in cursor.fetchall():
    kurzus_id = kurzus_id + 1
    kurzus_infok = get_kurzus_infok(db, kurzus_id)
    print(kurzus_infok['nev'])

    create_excel_file(db, kurzus_infok)