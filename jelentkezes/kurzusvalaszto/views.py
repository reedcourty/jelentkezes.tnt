#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# using UTF-8 charset

import datetime

from django.template import Context, loader
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from django.utils.datastructures import MultiValueDictKeyError

from kurzusvalaszto.models import Felhasznalo, Targy, Kurzus

def index(request):
    return HttpResponse("Hello, world.")

@login_required
def name_load(request):
    user = User.objects.get(username=request.user)

    error = ''
    
    if request.method == 'POST':
        user_last_name = request.POST['user_last_name']
        user_first_name = request.POST['user_first_name']
        
        if ((user_last_name == '') or (user_first_name == '')):
            error = 'Hiányzó adatok!'
            return render_to_response('kurzusvalaszto/username.html',
                              { 'user_last_name': user_last_name,
                                'user_first_name': user_first_name,
                                'targyak': targyak,
                                'error': error },
                              context_instance = RequestContext(request))
        else:
            user.last_name = user_last_name
            user.first_name = user_first_name
            user.save()
            return user_start(request)
    else:
        user_last_name = user.last_name
        user_first_name = user.first_name
    
    return render_to_response('kurzusvalaszto/username.html',
                              { 'user_last_name': user_last_name,
                                'user_first_name': user_first_name,
                                'error': error },
                              context_instance = RequestContext(request))


@login_required
def user_start(request):
    
    # Ha nincs kitöltve a név, tárgy akkor átdobjuk a kitöltős view-ra
    user = User.objects.get(username=request.user)
    if ((user.last_name=='') or (user.first_name=='')):
        return name_load(request)
    else:
        return render_to_response('kurzusvalaszto/user_start.html',
                              { 'user': user, },
                              context_instance = RequestContext(request))

@login_required
def kurzusvalasztas(request):
    user = User.objects.get(username=request.user)
    targyak = Targy.objects.all()
    kurzusok = Kurzus.objects.all()
        
    try:
        felhasznalo = Felhasznalo.objects.get(user = user)
        aktualis_targy = valasztott_targy = felhasznalo.targy
        aktualis_kurzus = valasztott_kurzus = felhasznalo.kurzus
        modositas = True
    except Felhasznalo.DoesNotExist:
        felhasznalo = None
        valasztott_targy = None
        valasztott_kurzus = None    
    
    error = ''
    
    if request.method == 'POST':
        print(request.POST)

        try:
            valasztott_kurzus = request.POST['kurzus_radio']
            valasztott_targy = request.POST['targyak']
        except MultiValueDictKeyError:
            valasztott_kurzus = None
        
        if (valasztott_kurzus == None):
            error = 'Hiányzó adatok!'
            return render_to_response('kurzusvalaszto/kurzusvalasztas.html',
                              { 'targyak': targyak,
                                'kurzusok': kurzusok,
                                'valasztott_kurzus': valasztott_kurzus,
                                'error': error },
                              context_instance = RequestContext(request))
        else:
            if (not modositas):
                vk = Kurzus.objects.get(pk=valasztott_kurzus)
                vt = Targy.objects.get(kod=valasztott_targy)
                vk.hallgatok = vk.hallgatok + 1
                print(u"módosít",vk.hallgatok)
                fi = datetime.datetime.now()
                felhasznalo = Felhasznalo.objects.create(kurzus=vk, user=user, targy=vt, felvetel_ideje=fi)
                felhasznalo.save()
            else:
                
                vk = Kurzus.objects.get(pk=valasztott_kurzus)
                if (vk.hallgatok < vk.ferohely):
                    aktualis_kurzus.hallgatok = aktualis_kurzus.hallgatok - 1
                    vk.hallgatok = vk.hallgatok + 1
                    print(vk.hallgatok, vk.ferohely)
                else:
                    error = 'Betelt a kurzus!'
                    return render_to_response('kurzusvalaszto/kurzusvalasztas.html',
                              { 'targyak': targyak,
                                'kurzusok': kurzusok,
                                'valasztott_kurzus': valasztott_kurzus,
                                'error': error },
                              context_instance = RequestContext(request))
                vt = Targy.objects.get(kod=valasztott_targy)
                
                fi = datetime.datetime.now()
                felhasznalo.kurzus = vk
                felhasznalo.targy = vt
                felhasznalo.felvetel_ideje = fi
                felhasznalo.save()

            return user_start(request)
    else:
           
        return render_to_response('kurzusvalaszto/kurzusvalasztas.html',
                              { 'targyak': targyak,
                                'kurzusok': kurzusok,
                                'valasztott_kurzus': valasztott_kurzus,
                                'error': error },
                              context_instance = RequestContext(request))
