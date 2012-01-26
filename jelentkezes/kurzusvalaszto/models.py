#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# using UTF-8 charset

from django.db import models
from django.contrib.auth.models import User

class Targy(models.Model):
    nev = models.CharField(max_length=30, verbose_name=u'Tárgynév')   
    kod = models.CharField(max_length=15, verbose_name=u'Tárgykód')

    def __unicode__(self):
        return u'{0} ({1})'.format(self.nev, self.kod)

    class Meta:
        verbose_name = u'Tárgy'
        verbose_name_plural = u'Tárgyak'
    
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
    
    nev = models.CharField(max_length=30, verbose_name=u'Kurzus neve')
    idopont_nap = models.CharField(max_length=1, choices=NAP_CHOICES,
        verbose_name=u'Nap')
    idopont_sav = models.CharField(max_length=2, choices=SAV_CHOICES,
        verbose_name=u'Sáv')
    ferohely = models.IntegerField(verbose_name=u'Férőhely')
    hallgatok = models.IntegerField(
        verbose_name=u'Jelentkezett hallgatók száma')

    def __unicode__(self):
        return u'{0} - {1} - {2}'.format(self.nev, self.idopont_nap,
            self.idopont_sav)


    class Meta:
        verbose_name = u'Kurzus'
        verbose_name_plural = u'Kurzusok'
    
class Felhasznalo(models.Model):
    user = models.OneToOneField(User)
    targy = models.ForeignKey(Targy)
    kurzus = models.ForeignKey(Kurzus)
    felvetel_ideje = models.DateTimeField(
        verbose_name = u'a kurzus felvételének ideje')

    class Meta:
        verbose_name = u'Felhasználó'
        verbose_name = u'Felhasználók'

