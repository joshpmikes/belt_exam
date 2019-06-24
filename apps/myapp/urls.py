from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^create_user$', views.create_user),
    url(r'^quotes$', views.quotes),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^upload_quote$', views.upload_quote),
    url(r'^like_quote/(?P<quote_id>\d+)$', views.like_quote),
    url(r'^delete_quote/(?P<quote_id>\d+)$', views.delete_quote),  
    url(r'^user/(?P<user_id>\d+)$', views.user_page),
    url(r'^myaccount/(?P<user_id>\d+)$', views.edit_user),
    url(r'^update/(?P<user_id>\d+)', views.update_user),
]





