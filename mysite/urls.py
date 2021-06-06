
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('downloads', views.downloads, name='downloads'),
    path('contact', views.contact, name='contact'),
    path('login', views.login, name='login'),
    path('scriptrequest', views.scriptrequest, name='scriptrequest'),
    path('login/queries', views.queries, name='queries'),
    path('login/scriptavailable', views.scriptavailable, name='scriptavailable'),
    path('login/addscript', views.addscript, name='addscript'),
    path('login/adddata', views.adddata, name='adddata'),
    path('downloads/<int:id>', views.downloadscript),

]
