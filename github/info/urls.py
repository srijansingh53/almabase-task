from django.conf.urls import url
from . import views

app_name = 'info'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    url(r'^search/$', views.search_repo, name='search'),

]

