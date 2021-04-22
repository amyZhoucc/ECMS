#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse,Http404,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from  django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q
from django.conf import settings
from  app_webPages import models
from  app_webPages import  XMLTool
from  app_webPages.publicAjax import *
from  app_webPages.modelBusiness import *
import json


# Create your views here.
#def hello(request):
#    return HttpResponse("hello world")
'''
def index(request):
    template = get_template('index.html')
    #showdatas = get_baselinerepo()
    html = template.render(locals())
    return HttpResponse(html)
'''

def test(request):
    dic = {'test':'test'}
    return render(request,'test.html',dic)
def test2(request):
    list=[
        {"id":"all","areaName":"全部"},
        {"id":"shanghai","areaName":"上海"},
        {"id":"hangzhou","areaName":"杭州"},
        {"id":"beijing","areaName":"北京"}
    ]
    dict_arealist = dict()
    dict_arealist["list"] = list
    dictionary = {
        "type":1,
        "code":1,
        "msg":"SUCCESS",
        "data":dict_arealist,
    }
    dic = json.dumps(dictionary)
    #dictionary = myJsonResponse(1, 1, "SUCCESS", dict_arealist)
    return render(request,'test2.html',{"Dic":dic})
#前端获取的内容均是string类型的

def homepage(request):
    template = get_template('index.html')
    welcome = "welcome to PBG management center"
    html = template.render(locals())
    return HttpResponse(html)

def ajax_area(request):
    arealist = get_area_jsonData()
    if arealist:
        dict_arealist = dict()
        dict_arealist["list"] = arealist
        return myJsonResponse(1,1,"SUCCESS",dict_arealist)
    else:
        return myJsonResponse(0,0,"area_repo objects get failed",None)

def ajax_pbg_departments(request):
    pbg_departs = getInfofromconfByParentnode("Departments","department","value")
    if pbg_departs:
        dict_pbg_department = dict()
        dict_pbg_department["list"] = get_jsonDatafromDict(pbg_departs,"value","name")
        return myJsonResponse(1,1,"SUCCESS",dict_pbg_department)
    else:
        return myJsonResponse(0,0,"conf.xml Departments read failed",None)

def ajax_components_types(request):
    typeslist = get_componentsType_jsonData()
    if typeslist:
        dict_typelist = dict()
        dict_typelist["list"] = typeslist
        return myJsonResponse(1,1,"SUCCESS",dict_typelist)
    else:
        return myJsonResponse(0,0,"components_type_repo objects get failed",None)

@csrf_exempt
def ajax_components_info(request):
    #DepartmentSelection = getInfofromconfByParentnode("Departments","department","value")
    if request.method == "GET":
        com_id = request.GET.get('comp_id')
        v_dep = request.GET.get('department')
        v_ctype = request.GET.get('comp_type')
        v_area = request.GET.get('area')
        p = request.GET.get('pageNO')
        pagesize = request.GET.get('pageSize')
    else:
        com_id = request.POST.get('comp_id')
        v_dep = request.POST.get('department')
        v_ctype = request.POST.get('comp_type')
        v_area = request.POST.get('area')
        p = request.POST.get('pageNO')
        pagesize = request.POST.get('pageSize')

    if not p:
        p = 1
    if not pagesize:
        pagesize = 20
    return components_info_page(v_dep,v_ctype,v_area,com_id,p,pagesize)


@csrf_exempt
def ajax_oldproducts_custom_info(request):
    if request.method == "GET":
        v_area = request.GET.get('area')
        v_keyword = request.GET.get('project_keyword')
        v_product = request.GET.get('product')
        v_ipm = request.GET.get('ipm')
        p = request.GET.get('pageNO')
        pagesize = request.GET.get('pageSize')
    else:
        v_area = request.POST.get('area')
        v_keyword = request.POST.get('project_keyword')
        v_product = request.POST.get('product')
        v_ipm = request.POST.get('ipm')
        p = request.POST.get('pageNO')
        pagesize = request.POST.get('pageSize')
    if not p:
        p = 1
    if not pagesize:
        pagesize = 20
    return oldproducts_custom_info_page(v_area,v_keyword,v_product,v_ipm,p,pagesize)

def ajax_IPJ_department_info(request):
    old_departs = getInfofromconfByParentnode("oldDepartments","olddepart","value")
    if old_departs:
        dict_tpj_department = dict()
        dict_tpj_department["list"] = get_jsonDatafromDict(old_departs,"value","name")
        return myJsonResponse(1,1,"SUCCESS",dict_tpj_department)
    else:
        return myJsonResponse(0,0,"conf.xml Old Departments read failed",None)

def ajax_old_products(request):
    old_products_list = get_products_jsonData()
    if old_products_list:
        dict_productslist = dict()
        dict_productslist["list"] = old_products_list
        return myJsonResponse(1,1,"SUCCESS",dict_productslist)
    else:
        return myJsonResponse(0,0,"oldproducts_info_repo selct data failed, please check the correct of input",{"list":[]})

@csrf_exempt
def ajax_custom_info(request):
    if request.method == "GET":
        com_id = request.GET.get('comp_id')
        v_version = request.GET.get('version')
        v_ipm = request.GET.get('ipm')
        p = request.GET.get('pageNO')
        pagesize = request.GET.get('pageSize')
    else:
        com_id = request.POST.get('comp_id')
        v_version = request.POST.get('version')
        v_ipm = request.POST.get('ipm')
        p = request.POST.get('pageNO')
        pagesize = request.POST.get('pageSize')

    if not p:
        p = 1
    if not pagesize:
        pagesize = 20
    return custom_info_page(com_id,v_version,v_ipm,p,pagesize)

@csrf_exempt
def ajax_area_repo_info(request):
    if request.method == "GET":
        v_area = request.GET.get('area')
        v_ip = request.GET.get('svn_ip')
        p = request.GET.get('pageNO')
        pagesize = request.GET.get('pageSize')
    else:
        v_area = request.POST.get('area')
        v_ip = request.POST.get('svn_ip')
        p = request.POST.get('pageNO')
        pagesize = request.POST.get('pageSize')

    if not p:
        p = 1
    if not pagesize:
        pagesize = 20
    return area_repo_info_page(v_area,v_ip,p,pagesize)

@csrf_exempt
def ajax_components_release_version_info(request):
    if request.method == "GET":
        com_id = request.GET.get('comp_id')
        v_version = request.GET.get('version')
        p = request.GET.get('pageNO')
        pagesize = request.GET.get('pageSize')
    else:
        com_id = request.POST.get('comp_id')
        v_version = request.POST.get('version')
        p = request.POST.get('pageNO')
        pagesize = request.POST.get('pageSize')

    if not p:
        p = 1
    if not pagesize:
        pagesize = 20
    return baseline_version_repo_info_page(com_id,v_version,p,pagesize)

@csrf_exempt
def ajax_delivery_repo_info(request):
    if request.method == "GET":
        ipm = request.GET.get('ipm')
        keyword = request.GET.get('project_keyword')
        p = request.GET.get('pageNO')
        pagesize = request.GET.get('pageSize')
    else:
        ipm = request.POST.get('ipm')
        keyword = request.POST.get('project_keyword')
        p = request.POST.get('pageNO')
        pagesize = request.POST.get('pageSize')

    if not p:
        p = 1
    if not pagesize:
        pagesize = 20
    return delivery_repo_info_page(ipm,keyword,p,pagesize)

@csrf_exempt
def ajax_products_info(request):
    if request.method == "GET":
        projectNO = request.GET.get('pjNO')
        keyword = request.GET.get('product_keyword')
        qa = request.GET.get('qa')
        p = request.GET.get('pageNO')
        pagesize = request.GET.get('pageSize')
    else:
        projectNO = request.POST.get('pjNO')
        keyword = request.POST.get('product_keyword')
        qa = request.POST.get('qa')
        p = request.POST.get('pageNO')
        pagesize = request.POST.get('pageSize')

    if not p:
        p = 1
    if not pagesize:
        pagesize = 20
    return new_products_repo_info_page(projectNO,keyword,qa,p,pagesize)
