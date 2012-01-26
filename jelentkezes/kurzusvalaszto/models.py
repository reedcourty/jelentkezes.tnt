#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# using UTF-8 charset

from django.db import models
from django.contrib.auth.models import User

class Targy(models.Model):
    nev = models.CharField(max_length=30)   
    kod = models.CharField(max_length=15)
    
class Kurzus(models.Model):
    
    NAP_CHOICES = (
        (u'H', u'Hétfő'),
        (u'K', u'Kedd'),
        (u'S', u'Szerda'),
        (u'C', u'Csütörtök'),
        (u'P', u'Péntek'),
    )
    
    SAV_CHOICES = (
        (u'07',u'07:00-08:00'),
        (u'08',u'08:00-10:00'),
        (u'10',u'10:00-12:00'),
        (u'12',u'12:00-14:00'),
        (u'14',u'14:00-15:30'),
    )
    
    nev = models.CharField(max_length=30)
    idopont_nap = models.CharField(max_length=1, choices=NAP_CHOICES)
    idopont_sav = models.CharField(max_length=2, choices=SAV_CHOICES)
    ferohely = models.IntegerField()
    hallgatok = models.IntegerField()
    
class Felhasznalo(models.Model):
    user = models.OneToOneField(User)
    targy = models.ForeignKey(Targy)
    kurzus = models.ForeignKey(Kurzus)
    felvetel_ideje = models.DateTimeField(u'a kurzus felvételének ideje')
