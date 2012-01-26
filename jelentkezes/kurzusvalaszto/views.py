#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# using UTF-8 charset

from django.template import Context, loader
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from kurzusvalaszto.models import Felhasznalo
from kurzusvalaszto.forms import UsernameForm

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
    
    
    # Ha nincs kitöltve a név, akkor átdobjuk a kitöltős view-ra
    user = User.objects.get(username=request.user)
    if (user.last_name=='') or (user.first_name==''):
        return name_load(request, user)
    else:
        return render_to_response('kurzusvalaszto/user_start.html',
                              { 'user': user, },
                              context_instance = RequestContext(request))
