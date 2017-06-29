# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ..login.models import User


# Create your models here.
class BlogManager(models.Manager):
    def addBlog(self, postData):
        results = {'status': True, 'errors': []}
        if len(postData['title']) < 1 and len(postData['content']) < 1:
            results['errors'].append('All fields must be filled out')
            results['status'] = False

        user = User.objects.get(id=postData['user_id'])
        if results['status']:

            try:
                blog = Blog.objects.create(
                    title=postData['title'],
                    content=postData['content'],
                    user_id=user,
                )
                blog.save()
            except:
                results['errors'].append('Error: Blog not created')

        return results

    def addLike(self, postData, user_id):
        results = {'status': True, 'errors': []}
        user = User.objects.get(id=user_id)
        blog = Blog.objects.get(id=postData['blog_id'])
        if user:
            try:
                like = blog.likes.add(user)
                blog.save()
            except:
                results['errors'].append('Error: Like not created')
        return results

class CommentManager(models.Manager):
    def addComment(self, postData, user):
        results = {'status': True, 'errors': []}
        print "model", "*"*200, postData, "*"*200
        Comment.objects.create(blog_id=postData['blog_id'],
                                user_id=user,
                                comment=postData['content'])
        return results
        
class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=5000)
    user_id = models.ForeignKey('login.User', related_name='blogs')
    likes = models.ManyToManyField('login.User', related_name='likedBlogs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BlogManager()

class Comment(models.Model):
    blog = models.ForeignKey('Blog', related_name='comments')
    user = models.ForeignKey('login.User', related_name='usercomments')
    comment = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = CommentManager()