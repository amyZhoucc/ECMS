#-*- coding:utf-8 -*-
from django.http import JsonResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.conf import settings
from app_webPages import models
from app_webPages import XMLTool
from django.db.models import Q
import json

#后端对前端的请求的回应
#type_value：类型0/1,code_value：值0/1,msg_value：信息，SUCCESS表成功,dictData：内容
def myJsonResponse(type_value,code_value,msg_value,dictData):
    dictionary = {
        "type":type_value,
        "code":code_value,
        "msg":msg_value,
        "data":dictData,
    }
    #return json.dumps(dictionary)
    return JsonResponse(dictionary)

#根据python的字典数据类型转换为ajax.json数据类型
#是根据前端的需求设计的
def get_jsonDatafromDict(dictData,keyname,valuename):
    #list里面的元素的dict格式
    jsondict = list()
    for k,v in dictData.items():
        d = dict()
        d[keyname] = k
        d[valuename] = v
        jsondict.append(d)
    return jsondict

#根据父节点获取其下所有子节点value以及值
#返回字典数据，key为其属性，value为其nodeText
def getInfofromconfByParentnode(parent,child,attributename):
    conftree = XMLTool.loadXML(settings.CONF_XML)
    selection = XMLTool.getElementByAttribute(conftree,parent,child,attributename)
    return selection

#前端页面显示美化
'''
example: get_pages(10,1) result=[1,2,3,4,5]
example: get_pages(10.9) result=[6,7,8,9,10]
页码个数由WEB_DISPLAY_PAGE设定
'''
def get_pages(totalpage=1,current_page=1):
    WEB_DISPLAY_PAGE = 10
    front_offset = int(WEB_DISPLAY_PAGE / 2)
    if WEB_DISPLAY_PAGE % 2 == 1:
        behind_offset = front_offset
    else:
        behind_offset = front_offset - 1
    if totalpage < WEB_DISPLAY_PAGE:
        return list(range(1, totalpage + 1))
    elif current_page <= front_offset:
        return list(range(1, WEB_DISPLAY_PAGE + 1))
    elif current_page >= totalpage - behind_offset:
        start_page = totalpage - WEB_DISPLAY_PAGE + 1
        return list(range(start_page, totalpage + 1))
    else:
        start_page = current_page - front_offset
        end_page = current_page + behind_offset
        return list(range(start_page, end_page + 1))

#数据分页，datalist：数据列表，必须是一个list类型的数据
#pagesize：每页显示多少
#pageNO：当前页面
#返回当前页面的数据信息和总页数
def paginatorData(datalist,pageNO,pagesize):
    #默认20
    if not pagesize:
        pagesize = 20
    else:
        pagesize = int(pagesize)
    #默认第一页
    if not pageNO:
        p = 1
    else:
        p = int(pageNO)
    paginator = Paginator(datalist,pagesize)
    totalpages = paginator.num_pages
    try:
        showdatas = paginator.page(p)
    except PageNotAnInteger:
        showdatas = paginator.page(1)
    except EmptyPage:
        showdatas = paginator.page(paginator.num_pages)
    return showdatas,totalpages

#basline_repo
def get_baselinerepoinfo(components):
    ctypes = get_componentsTypelist()
    homepage_data = list()
    for c in components:
        print(c.id)
        ctype = c.type
        areaID = c.areaRepoID
        areaName = ""
        if areaID:
            try:
                #area_repo的id就是对应的地域编号，根据编号查，就能在“area_repo”找到对应的地区名字
                areaobj = models.area_repo.objects.get(id=areaID)
                areaName = areaobj.areaName
            except:
                #找不到就返回id号
                areaName = areaID
        chinese_type = ""
        if ctype not in ctypes.keys():
            chinese_type = "其他"
        else:
            chinese_type = ctypes[ctype]
        dict_data = dict()
        dict_data["type"] = chinese_type
        dict_data["componentID"] = c.componentsID
        dict_data["componentName"] = chinese_type
        dict_data["latestVersion"] = c.headVersion
        dict_data["gitPath"] = c.GITPath
        dict_data["svnPath"] = c.SVNPath
        dict_data["areaName"] = areaName
        dict_data["department"] = c.department
        dict_data["head"] = c.head
        dict_data["rule"] = c.rule
        dict_data["errorCode"] = c.errorCode
        homepage_data.append(dict_data)
    return homepage_data

#get_area_jsonData用到的函数
def get_areaNamelist():
    #获取area_repo的数据，只显示id和areaName两个属性值
    areasql = models.area_repo.objects.all().values_list('id','areaName')
    areadic = {}
    areadic["all"] = "全部"
    for a in areasql:
        #字典里面的值  1:地区的中文名
        areadic[str(a[0])] = a[1]
    return areadic

#返回area_json列表
#area_repo
def get_area_jsonData():
    areas = get_areaNamelist()
    return get_jsonDatafromDict(areas,"id","name")

#get_products_jsonData用到的函数
def get_productslist():
    productssql = models.oldproducts_info_repo.objects.all()
    productsdic = {}
    productsdic["all"] = "全部"
    for p in productssql:
        productsdic[p.productName] = p.productName
    return  productsdic

#oldproducts_info_repo
def get_products_jsonData():
    return get_jsonDatafromDict(get_productslist(),"value","name")

#get_componentsType_jsonData用到的函数
def get_componentsTypelist():
    typessql = models.components_type_repo.objects.all().values_list('ENname','CNname')
    typesdic = {}
    typesdic["all"] = "全部"
    for t in typessql:
        typesdic[t[0]] = t[1]
    return typesdic

#components_type_repo
def get_componentsType_jsonData():
    return  get_jsonDatafromDict(get_componentsTypelist(),"value","name")

#根据组件标识，获取baseline_repo表中该组件所在的id
def get_baseline_repoIDbycomponentsID(comid):
    #componentID = ""
    if comid:
        try:
            baselinerepoobj = models.baseline_repo.objects.get(componentsID=comid)
        except:
            baselinerepoobj = ""
    if baselinerepoobj:
        return baselinerepoobj.id,baselinerepoobj.componentsID
    else:
        return "",""

#根据version的值从 baseline_version_repo 获取所有version的baseline_repo表id
#返回一个元组(tuple)
def get_baselinerepoIDfrom_version_repo(ver):
    if ver:
        try:
            baseline_versions = models.baseline_version_repo.objects.filter(version=ver)
        except:
            baseline_versions = ""
    return baseline_versions

def get_componentsnamesbyversionrepoDatas(versionreposdic):
    version_component_list = list()
    for v in versionreposdic:
        try:
            baselinerepoobj = models.baseline_repo.objects.get(id=v.baselinerepoID)
        except:
            print("not found id:%s in table baseline_repo"%v.baselinerepoID)
            baselinerepoobj = ""
        if baselinerepoobj:
            version_component_list.append((v.id,baselinerepoobj.componentsID,v.version))
    return version_component_list

#根据版本号获取组件标识、组件版本
def getComponentsVersion(version):
    baselinerepodatas = get_baselinerepoIDfrom_version_repo(version)
    return get_componentsnamesbyversionrepoDatas(baselinerepodatas)

#根据getComponentsVersion获取的数据，将之转为json格式
def getJsonComponentsVersion(version_component_data):
    versionslist = list()
    for v in version_component_data:
        dv = {}
        dv["version"] = v[2]
        ds = {}
        ds["componentID"] = v[1]
        ds["version"] = [dv]
        versionslist.append(ds)
    return versionslist

#根据组件标识获取该组件的所有版本
def get_version_repoIDbycomid(comid):
    id,componentname = get_baseline_repoIDbycomponentsID(comid)
    try:
        versionrepoids = models.baseline_version_repo.objects.filter(baselinerepoID=id)
    except:
        versionrepoids = ""
    return componentname,versionrepoids

#根据组件标识列表获取其所有版本的json格式数据
def get_version_repoJsonDatabycomid(com_id,vers_repos):
    versionslist = list()
    if vers_repos:
        for vr in vers_repos:
            d = {}
            d["version"] = vr.version
            versionslist.append(d)
    jsond = {}
    jsond["componentID"] = com_id
    jsond["versions"] = versionslist
    return [jsond]

#根据baseline_version_repo，并且将组件清单插入
def get_comp_versionJsonDatas(versionreposdic):
    comslist = list()
    version_comp_datas = get_componentsnamesbyversionrepoDatas(versionreposdic)
    for vc in version_comp_datas:
        compname = vc[1]
        compver = vc[2]
        addnew = True
        for c in comslist:
            if c["componentID"] == compname:
                c["versions"].append({"version":compver})
                addnew = False
        if addnew:
            comslist.append({"componentID":compname,"versions":[{"version":compver}]})
    return comslist

#根据组件标志获取定制信息
def get_custom_databycomid(com_id,ipm):
    customlist = list()
    componentname,versionrepoids = get_version_repoIDbycomid(com_id)
    if not versionrepoids:
        return customlist
    for obj in versionrepoids:
        versionrepoid = obj.id
        version = obj.version
        try:
            customs = models.custom_repo.objects.filter(baselineversionrepoID=versionrepoid)
        except:
            customs = ""
        if customs:
            for c in customs:
                if ipm and ipm != "None":
                    if c.ipmNO == ipm:
                        customlist.append((componentname,version,c.repoPath,c.productName,c.productManager))
                    else:
                        continue
                else:
                    customlist.append((componentname, version, c.repoPath, c.productName, c.productManager))
    return customlist

#根据版本号从custom_repo获取定制数据
def get_custom_databyversion(v_version,ipm):
    customlist = list()
    baseline_versionsobjs = get_baselinerepoIDfrom_version_repo(v_version)
    if baseline_versionsobjs:
        versioncomponentsdata = get_componentsnamesbyversionrepoDatas(baseline_versionsobjs)
        if versioncomponentsdata:
            for v in versioncomponentsdata:
                #version_repoid = v[0]
                componentname = v[1]
                version = v[2]
                try:
                    customs = models.custom_repo.objects.filter(baselineversionrepoID=v[0])
                except:
                    customs = ""
                if customs:
                    for c in customs:
                        if ipm and ipm != "None":
                            if c.ipmNO == ipm:
                                customlist.append((componentname, version, c.repoPath, c.productName, c.productManager))
                            else:
                                continue
                        else:
                            customlist.append((componentname, version, c.repoPath, c.productName, c.productManager))
    return  customlist

def get_custom_databycomid_version(comid,version,ipm):
    customlist = list()
    baseline_versions_objs = get_baselinerepoIDfrom_version_repo(version)
    if baseline_versions_objs:
        versioncomponentsdata = get_componentsnamesbyversionrepoDatas(baseline_versions_objs)
        if versioncomponentsdata:
            for v in versioncomponentsdata:
                componentname = v[1]
                if comid != componentname:
                    continue
                version = v[2]
                try:
                    custom = models.custom_repo.objects.filter(baselineversionrepoID=v[0])
                except:
                    custom = ""
                if custom:
                    for c in custom:
                        if ipm and ipm != "None":
                            if c.ipmNO == ipm:
                                customlist.append((componentname, version, c.repoPath, c.productName, c.productManager))
                            else:
                                continue
                        else:
                            customlist.append((componentname, version, c.repoPath, c.productName, c.productManager))
    return customlist


def get_json_custom_data_fromlist(customsdic):
    customlist = list()
    for c in customsdic:
        d = {}
        d["componentID"] = c[0]
        d["version"] = c[1]
        d["repoPath"] = c[2]
        d["productName"] = c[3]
        d["productManager"] = c[4]
        customlist.append(d)
    return customlist

#根据 custom_repo 中的数据，从 baseline_version_repo 和 baseline_repo 分别获取组件标识和版本
def get_custom_repo(customsdic):
    customlist = list()
    all_custom = customsdic
    for c in all_custom:
        versionrepoid = c.baselineversionrepoID
        if not versionrepoid:
            version = ""
            componentname = ""
        else:
            try:
                #baseline_version_repo的id就是组件版本的id
                versionrepoobj = models.baseline_version_repo.objects.get(id=versionrepoid)
                version = versionrepoobj.version
                try:
                    baselinerepoID = versionrepoobj.baselinerepoID
                    baselinerepoobj = models.baseline_repo.objects.get(id=baselinerepoID)
                    componentname = baselinerepoobj.componentsID
                except:
                    componentname = ""
            except:
                version = ""
        d = {}
        d["componentID"] = componentname
        d["version"] = version
        d["repoPath"] = c.repoPath
        d["productName"] = c.productName
        d["productManager"] = c.productManager
        customlist.append(d)
    return  customlist

def get_oldcustom_showdata(oldproducts_custom_repo_dic):
    showdatas = list()
    areadic = get_areaNamelist()
    for c in oldproducts_custom_repo_dic:
        try:
            areaname = areadic[str(c.arearepoID)]
        except:
            areaname = ""
        d = {}
        d["subsystem"] = c.subsystem
        d["basicVersion"] = c.basicversion
        d["repoPath"] = c.repoPath
        d["productName"] = c.productName
        d["areaName"] = areaname
        showdatas.append(d)
    return showdatas

def get_area_repo_showdata(area_repo_dic):
    showdatas = list()
    areadic = get_areaNamelist()
    for a in area_repo_dic:
        d = {}
        try:
            d["areaName"] = areadic[str(a.id)]
        except:
            d["areaName"] = ""
        d["IP"] = a.areaRepoIP
        d["codePath"] = a.codePATH
        d["deliveryPath"] = a.DeliveryPATH
        d["header"] = a.head
        showdatas.append(d)
    return showdatas

# delivery_repo 获取的数据，整合成ajax的json格式
def get_delivery_jsonData(deliverydic):
    deliverylist = list()
    for d in deliverydic:
        dd = {}
        dd["deliveryPath"] = d.DeliveryPath
        dd["ipm"] = d.ipmNO
        deliverylist.append(dd)
    return deliverylist

# products_info_repo 获取的数据，整合成ajax的json格式
def get_product_jsonData(productdic):
    productlist = list()
    for p in productdic:
        pj = {}
        pj["projectNO"] = p.pjNO
        pj["productName"] = p.productName
        pj["version"] = p.version
        pj["deliveryPath"] = p.delivery_path
        pj["manager"] = p.project_manager
        pj["qa"] = p.qa
        pj["cm"] = p.cm
        pj["department"] = p.department
        productlist.append(pj)
    return productlist

if __name__== "__main__":
    print(get_area_jsonData())
