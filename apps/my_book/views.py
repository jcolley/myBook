# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from ..login.models import User


# Create your views here.
def index(request):
    user = User.objects.get(id=request.session.get('id'))
    context = {
        'user': user,
    }
    return render(request, 'my_book/index.html', context)


def addBlog(request):
    return render(request, 'my_book/addBlog.html')

