"""PaymentsRequests URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView
from projects import views
from django.conf import settings
from django.views.static import serve


urlpatterns = [
    url(r'^$', views.index, name='home'),

    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^accounts/', include('django.contrib.auth.urls')),


    url(r'^paymentrequest/', views.paymentrequest, name='paymentrequest' ),
    url(r'^projects/', views.projects, name='projects' ),
    url(r'^succes/', views.succes, name='succes' ),
    url(r'^$', views.index, name='index'),
    url(r'^project/(?P<pid>[0-9]+)/$', views.single_project, name='single_project'),
    url(r'^project/(?P<pid>[0-9]+)/invoice/(?P<iid>[0-9]+)/confirm/$', views.confirmProjectInvoice, name='confirmInvoice' ),
    url(r'^project/(?P<pid>[0-9]+)/invoice/(?P<iid>[0-9]+)/disconfirm/$', views.disconfirmProjectInvoice, name='disconfirmInvoice'),
    url(r'^invoice/(?P<iid>[0-9]+)/$', views.single_invoice, name='single_invoice')
#TODO make confirm, disconfirm and single invoice links, EVT. overzicht van gemaakte invoices
]
if settings.DEBUG:
     urlpatterns += [
         url(r'^media/(?P<path>.*)$',
             serve, { 'document_root':
                      settings.MEDIA_ROOT,}),
     ]