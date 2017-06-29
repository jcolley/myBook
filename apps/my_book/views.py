# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import Blog, User, Comment


# Create your views here.
def index(request):

    if not checkAuth(request):
        return redirect('/')

    user = User.objects.get(id=request.session.get('id'))
    blogs = Blog.objects.all().order_by('-created_at')[:5]
    comments = Comment.objects.all().order_by('-created_at')
    context = {
        'user': user,
        'blogs': blogs,
        'comments': comments
    }
    return render(request, 'my_book/index.html', context)

def showBlog(request, id): 
    if not checkAuth(request):
        return redirect('/')
    blog = Blog.objects.filter(id=id)
    comments = Comment.objects.filter(blog_id=id)
    context = {
        'blog': blog,
        'comments': comments,
        'id': id
    }
    print context
    return render(request, 'my_book/showBlog.html', context)

def showAll(request):
    if not checkAuth(request):
        return redirect('/')

    user = User.objects.get(id=request.session.get('id'))
    blogs = Blog.objects.all().order_by('-created_at')
    comments = Comment.objects.all().order_by('-created_at')
    context = {
        'user': user,
        'blogs': blogs,
        'comments': comments
    }
    return render(request, 'my_book/index.html', context)
    

def addBlog(request):
    if not checkAuth(request):
        return redirect('/')
    if request.POST:
        results = Blog.objects.addBlog(request.POST)
        if results:
            messages.info(request, 'Blog Added')
        else:
            for error in results:
                messages.error(request, error)
            return redirect('mybook:addBlog')
        return redirect('mybook:index')

    user = User.objects.get(id=request.session.get('id'))
    context = {
        'user': user,
    }
    return render(request, 'my_book/addBlog.html', context)

def  newComment(request):
    print "*"*200, request.POST, "*"*200
    blogid = Blog.objects.get(id=request.POST['blog_id'])
    context = {'blogid': blogid}
    return render(request, 'my_book/addComment.html', context)

def addComment(request):
    if not checkAuth(request):
        return redirect('/')
    if request.POST:
        user = request.session['id']
        results = Comment.objects.addComment(request.POST, user)
        if results:
            messages.info(request, 'Comment Added')
        else:
            for error in results:
                messages.error(request, error)
            return redirect('mybook:addComment')
        return redirect('mybook:index')
    return redirect('mybook:index')

def addLike(request):
    if request.POST:
        results = Blog.objects.addLike(request.POST, request.session['id'])
        if not results:
            for error in results:
                messages.error(request, error)
        return redirect('mybook:index')


def checkAuth(request):  # Force non-authorized user back to login/registration page
    try:
        if not request.session.get('id'):
            messages.error(request, 'NO.')
            return False
        return True
    except:
        messages.error(request, 'NO')
        return False