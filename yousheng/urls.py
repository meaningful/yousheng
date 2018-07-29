"""yousheng URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import view

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^$',view.index),
    url(r'^homePage.html$',view.homePage),
    url(r'^carfixManage.html$',view.carfixManage),
    url(r'^customManage.html$',view.customManage),
    url(r'^materialPurchase.html$',view.materialPurchase),
    url(r'^monthWastage.html$',view.monthWastage),
    url(r'^saleform.html$',view.saleform),
    url(r'^404.html$',view.unfound),
    url(r'^editCustomManage$',view.editCustomManage),
    url(r'^staffManage', view.staffManage),
    url(r'^editStaffManage', view.editStaffManage),
    url(r'^gasManage', view.gasManage),
    url(r'^editGasManage', view.editGasManage),
    url(r'^trailerManage', view.trailerManage),
    url(r'^tractorManage', view.tractorManage),
    url(r'^editTrailerManage', view.editTrailerManage),
]

urlpatterns += static(settings.STATIC_URL , document_root=settings.STATIC_ROOTS)