from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^signup/$', views.signup_view, name='signup'),
    url(r'^selectchannel/$', views.selectchannel_view, name='selectchannel'),
    url(r'^home/$', views.home_view, name='home'),
    url(r'^logout/$', views.logout_view, name='logout')
]