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
from django.conf import settings

from django.utils.datastructures import MultiValueDictKeyError

from kurzusvalaszto.models import Felhasznalo, Targy, Kurzus

def index(request):
    return render_to_response('kurzusvalaszto/index.html',
                              {},
                              context_instance = RequestContext(request))

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
                                'error': error },
                              context_instance = RequestContext(request))
        else:
            user.last_name = user_last_name
            user.first_name = user_first_name
            user.save()
            return start(request)
    else:
        user_last_name = user.last_name
        user_first_name = user.first_name
    
    return render_to_response('kurzusvalaszto/username.html',
                              { 'user_last_name': user_last_name,
                                'user_first_name': user_first_name,
                                'error': error },
                              context_instance = RequestContext(request))


@login_required
def start(request):
    
    # Ha nincs kitöltve a név, tárgy akkor átdobjuk a kitöltős view-ra
    user = User.objects.get(username=request.user)
    if ((user.last_name=='') or (user.first_name=='')):
        return name_load(request)
    else:
        
        targy = get_user_targy(user)
        kurzus = get_user_kurzus(user)
        
        return render_to_response('kurzusvalaszto/start.html',
                              { 'user': user,
                                'targy': targy,
                                'kurzus': kurzus },
                              context_instance = RequestContext(request))



def get_user_targy(user):
    try:
        user = User.objects.get(username=user)
        felhasznalo = Felhasznalo.objects.get(user = user)
        aktualis_targy = felhasznalo.targy
    except Felhasznalo.DoesNotExist:
        aktualis_targy = None
    return aktualis_targy

def get_user_kurzus(user):
    try:
        user = User.objects.get(username=user)
        felhasznalo = Felhasznalo.objects.get(user = user)
        aktualis_kurzus = felhasznalo.kurzus
    except Felhasznalo.DoesNotExist:
        aktualis_kurzus = None
    return aktualis_kurzus

@login_required
def kurzusvalasztas(request):
    kji_kezd = settings.KURZUS_JELENTKEZESI_IDOSZAK_K
    kji_vege = settings.KURZUS_JELENTKEZESI_IDOSZAK_V
    
    # Ellenőrizzük, hogy van-e kurzus felvételi időszak:
    most = datetime.datetime.now()
                
    if ((most > kji_kezd) and (most < kji_vege)):
        kji = True
    else:
        kji = False
        
    modositas = False
    
    targyak = Targy.objects.all()
    kurzusok = Kurzus.objects.all()
    
    user = User.objects.get(username=request.user)
    
    a_targy = get_user_targy(request.user)
    a_kurzus = get_user_kurzus(request.user)
    if ((a_targy != None) or (a_kurzus != None)):
        felhasznalo = Felhasznalo.objects.get(user = user)
        modositas = True
    else:
        felhasznalo = None
        
    if modositas:
        return kurzus_modositas(request, user, kji, targyak, kurzusok, felhasznalo, a_targy, a_kurzus)
    else:
        return kurzus_jelentkezes(request, user, kji, targyak, kurzusok)
       
@login_required
def kurzus_modositas(request, user, kji, targyak, kurzusok, felhasznalo, a_targy, a_kurzus):
    error = ''
    error_van = False
    valasztott_targy = a_targy
    valasztott_kurzus = a_kurzus
    if not kji:
        error = u'Nincs kurzus jelentkezési időszak!'
        error_van = True
    if request.method == 'POST':
        
        valasztott_targy = Targy.objects.get(kod=request.POST['targyak'])
        valasztott_kurzus = Kurzus.objects.get(pk=request.POST['kurzus_radio'])
        
        if (valasztott_targy != a_targy):
            felhasznalo.targy = valasztott_targy
            a_targy = valasztott_targy
            felhasznalo.save()
        
        if (valasztott_kurzus != a_kurzus):
            if (valasztott_kurzus.hallgatok < valasztott_kurzus.ferohely):
                fi = datetime.datetime.now()
                valasztott_kurzus.hallgatok = valasztott_kurzus.hallgatok + 1
                a_kurzus.hallgatok = a_kurzus.hallgatok - 1
                valasztott_kurzus.save()
                a_kurzus.save()
                felhasznalo.kurzus = valasztott_kurzus
                felhasznalo.felvetel_ideje = fi
                felhasznalo.save()
            else:
                error = 'A kurzus már betelt!'
                error_van = True
            
        if error_van:
            return render_to_response('kurzusvalaszto/kurzusvalasztas.html',
                                    { 'targyak': targyak,
                                      'kurzusok': kurzusok,
                                      'aktualis_kurzus': a_kurzus,
                                      'aktualis_targy': a_targy,
                                      'error': error },
                                      context_instance = RequestContext(request))
        else:
            return start(request)
                
    return render_to_response('kurzusvalaszto/kurzusvalasztas.html',
                              {'targyak': targyak,
                               'kurzusok': kurzusok,
                               'aktualis_kurzus': valasztott_kurzus,
                               'aktualis_targy': valasztott_targy,
                               'error': error},
                              context_instance = RequestContext(request))

@login_required
def kurzus_jelentkezes(request, user, kji, targyak, kurzusok):
    error = ''
    error_van = False
    valasztott_targy = None
    valasztott_kurzus = None
    if not kji:
        error = u'Nincs kurzus jelentkezési időszak!'
        error_van = True
    if request.method == 'POST':
        try:
            valasztott_targy = Targy.objects.get(kod=request.POST['targyak'])
        except Targy.DoesNotExist:
            error = 'Nem adtál meg tárgyat!'
            error_van = True
        try:
            valasztott_kurzus = Kurzus.objects.get(pk=request.POST['kurzus_radio'])
        except MultiValueDictKeyError:
            error = 'Nem adtál meg kurzust!'
            error_van = True
        if error_van:
            return render_to_response('kurzusvalaszto/kurzusvalasztas.html',
                          { 'targyak': targyak,
                            'kurzusok': kurzusok,
                            'aktualis_kurzus': valasztott_kurzus,
                            'aktualis_targy': valasztott_targy,
                            'error': error },
                          context_instance = RequestContext(request))
        else:
            if (valasztott_kurzus.hallgatok < valasztott_kurzus.ferohely):
                fi = datetime.datetime.now()
                valasztott_kurzus.hallgatok = valasztott_kurzus.hallgatok + 1
                valasztott_kurzus.save()
                felhasznalo = Felhasznalo(targy=valasztott_targy,
                                          user=user,
                                          kurzus=valasztott_kurzus,
                                          felvetel_ideje=fi)
                felhasznalo.save()
                return start(request)
            else:
                error = 'A kurzus már betelt!'
                return render_to_response('kurzusvalaszto/kurzusvalasztas.html',
                              { 'targyak': targyak,
                                'kurzusok': kurzusok,
                                'aktualis_kurzus': valasztott_kurzus,
                                'aktualis_targy': valasztott_targy,
                                'error': error },
                                context_instance = RequestContext(request))
            
    return render_to_response('kurzusvalaszto/kurzusvalasztas.html',
                              {'targyak': targyak,
                               'kurzusok': kurzusok,
                               'aktualis_kurzus': valasztott_kurzus,
                               'aktualis_targy': valasztott_targy,
                               'error': error},
                              context_instance = RequestContext(request))
