from django.conf.urls import url
from.import views

app_name = 'mybook'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^addBlog$', views.addBlog, name='addBlog'),
    url(r'^addLike$', views.addLike, name='addLike'),
    url(r'^showAll$', views.showAll, name='showAll'),
    url(r'^newComment$', views.newComment, name='newComment'),
    url(r'^addComment$', views.addComment, name='addComment'),
    url(r'^showBlog/(?P<id>\d+)$', views.showBlog, name='showBlog'),
]
