from django.conf.urls import url
from . import views

app_name = 'info'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    url(r'^search/$', views.search_repo, name='search'),
    url(r'^(?P<repo_id>[0-9]+)/(?P<m>[0-9]+)$', views.commits, name='commits'),

]

