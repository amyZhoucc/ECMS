"""webPages URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.urls import path
from app_webPages import views

urlpatterns = [
    #url(r'^index/',views.index),
    url(r'^admin/',admin.site.urls),
    #url(r'^$',TemplateView.as_view(template_name="index.html")),
    #ok ok
    url(r'^area/$',views.ajax_area),
    #ok ok
    url(r'^pbg_departs/$', views.ajax_pbg_departments),
    #ok ok
    url(r'^components_types/$', views.ajax_components_types),
    #2ok代码库信息(新) ok
    url(r'^components_info/$', views.ajax_components_info, name='components_info'),
    #3ok定制分支信息(老) ok
    url(r'^oldproducts_custom_info/$', views.ajax_oldproducts_custom_info,name='oldproducts_custom_info'),
    #ok ok
    url(r'^old_departs/$', views.ajax_IPJ_department_info),
    #ok ok
    url(r'^old_products/$', views.ajax_old_products),
    #4ok定制分支信息(新)ok
    url(r'^custom_info/$', views.ajax_custom_info, name='custom_info'),
    #5ok定制项目交付库信息 ok
    url(r'^area_repo_info/$', views.ajax_area_repo_info, name='area_repo_info'),
    #6ok配置库信息 ok
    url(r'^components_version_info/$', views.ajax_components_release_version_info, name='components_version_info'),
    #7ok版本发布信息(新) ok
    url(r'^delivery_info/$', views.ajax_delivery_repo_info, name='delivery_info'),
    #8ok项目信息(新)ok
    url(r'^products_info/$', views.ajax_products_info, name='delivery_info'),

    url(r'^test/$',views.test),
    url(r'^test2/$',views.test2,name='test2'),
    #url(r'^area_repo_info/$', views.ajax_area_repo_info),

    #path(r'^$',views.hello)
    #path(r'admin/', admin.site.urls),
    #path(r'user/',views.hello)
]
