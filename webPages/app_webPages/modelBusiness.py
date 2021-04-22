from django.db.models import Q
from app_webPages import models
from app_webPages.publicAjax import *

#根据参数，返回数据库basline_repo获取数据以及参数列表
#v_dep：部门,v_ctype：组件类型,v_area：地区,com_id：组件标识,pageNO：页码,pagesize：每页显示的数据条数
def components_info_page(v_dep,v_ctype,v_area,com_id,pageNO,pagesize):
    DepartmentSelection = getInfofromconfByParentnode("Departments","department","value")
    filter_dep = ""
    filter_type = ""
    filter_area = ""
    dofilter = False    #是否有任何过滤的标志
    #com_id为空，但是其他参数有效的时候
    if not com_id:
        #v_dep有参数，并且不是表示全部时：
        if v_dep and v_dep != "None" and v_dep != "all" and v_dep != u"全部":
            filter_dep = DepartmentSelection[v_dep]
            dofilter = True
        if v_ctype and v_ctype != "None" and v_ctype != "all":
            filter_type = v_ctype
            dofilter = True
        if v_area and v_area != "None" and v_area != "all":
            filter_area = v_area
            dofilter = True

        if dofilter and filter_area:
            all_components = models.baseline_repo.objects.filter(department__contains=filter_dep,type__contains=filter_type,areaRepoID=filter_area)
        elif dofilter and not filter_area:
            all_components = models.baseline_repo.objects.filter(department__contains=filter_dep,type__contains=filter_type)
        else:
            all_components = models.baseline_repo.objects.all()
    #com_id不为空时，它的优先级最高，其他参数均无效
    else:
        com_id = com_id.strip()
        all_components = models.baseline_repo.objects.filter(componentsID=com_id)
        filter_dep = "all"
        filter_type = "all"

    if not all_components:
        dict_showdata = {"total":0,"pageNO":pageNO,"pagesize":pagesize,"list":[]}
        return myJsonResponse(1,1,"baseline_repo查询不到信息，请确定是否有误",dict_showdata)

    total = len(all_components)
    components,totalpages = paginatorData(all_components,pageNO,pagesize)
    showdatas = get_baselinerepoinfo(components)
    if showdatas:
        dict_showdata = {"total": total, "pageNO": pageNO, "pagesize": pagesize, "list": showdatas}
        return myJsonResponse(1,1,"SUCCESS",dict_showdata)
    else:
        dict_showdata = {"total": total, "pageNO": pageNO, "pagesize": pagesize, "list": ""}
        return myJsonResponse(0,0,"baseline_repo查找成功，但是函数get_baselinerepoinfo出错",dict_showdata)

#oldproducts_info_repo
#v_area：地区,v_keyword：关键字,v_product：产线,v_ipm：订单号,p：页码,pagesize：每页条数
def oldproducts_custom_info_page(v_area,v_keyword,v_product,v_ipm,pageNO,pagesize):
    filter_area = ""
    filter_keyword = ""
    filter_ipm = ""
    filter_product = ""
    dofilter = False
    if v_area and v_area != "None" and v_area != "all":
        filter_area = v_area
        dofilter = True
    if v_keyword and v_keyword != "None" and v_keyword != "all":
        filter_keyword = v_keyword
        dofilter = True
    if v_ipm and v_ipm != "None" and v_ipm != "all":
        filter_ipm = v_ipm
        dofilter = True
    if v_product and v_product != "None" and v_product != "all":
        filter_product = v_product
        dofilter = True

    #如果没有传递参数
    if not dofilter:
        all_oldcustoms = models.oldproducts_custom_repo.objects.all()
    else:
        if filter_area:
            #ipm有，关键词无
            if filter_ipm and not filter_keyword:
                all_oldcustoms = models.oldproducts_custom_repo.objects.filter((Q(repoPath__contains=filter_ipm)|Q(ipmNO=filter_ipm)),productName__contains=filter_product,arearepoID=filter_area)
            #ipm无，关键词有
            elif not filter_ipm and filter_keyword:
                all_oldcustoms = models.oldproducts_custom_repo.objects.filter(productName__contains=filter_product,repoPath__contains=filter_keyword,arearepoID=filter_area)
            #两者都无，两者都有，就不查了
            else:
                all_oldcustoms = models.oldproducts_custom_repo.objects.filter(productName__contains=filter_product,arearepoID=filter_area)
        else:
            if filter_ipm and not filter_keyword:
                all_oldcustoms = models.oldproducts_custom_repo.objects.filter((Q(repoPath__contains=filter_ipm)|Q(ipmNO=filter_ipm)),productName__contains=filter_product)
            elif not filter_ipm and filter_keyword:
                all_oldcustoms = models.oldproducts_custom_repo.objects.filter(productName__contains=filter_product,repoPath__contains=filter_keyword)
            else:
                all_oldcustoms = models.oldproducts_custom_repo.objects.filter(productName__contains=filter_product)

    if not all_oldcustoms:
        dict_showdata = {"total": 0, "pageNO": pageNO, "pagesize": pagesize, "list": []}
        return myJsonResponse(1,1,"oldproducts_custom_repo查询不到信息，请确定输入是否有误",dict_showdata)

    total = len(all_oldcustoms)
    oldcustoms,totalpages = paginatorData(all_oldcustoms,pageNO,pagesize)
    showdatas = get_oldcustom_showdata(oldcustoms)

    if showdatas:
        dict_showdata = {"total": total, "pageNO": pageNO, "pagesize": pagesize, "list": showdatas}
        return myJsonResponse(1,1,"SUCCESS",dict_showdata)
    else:
        dict_showdata = {"total": total, "pageNO": pageNO, "pagesize": pagesize, "list": ""}
        return myJsonResponse(0,0,"oldproducts_custom_repo查找成功，但是函数get_oldcustom_showdata出错",dict_showdata)

#custom_repo
#com_id：组件标识,v_version：版本,v_ipm：订单号,pageNO：页码,pagesize：每页条数
def custom_info_page(com_id,v_version,v_ipm,pageNO,pagesize):
    is_custom_repo_origin_data = True
    #仅存在ipm
    if v_ipm and v_ipm != "None" and (not com_id or com_id == "None") and (not v_version or v_version == "None"):
        v_ipm = v_ipm.strip().upper()
        all_customs = models.custom_repo.objects.filter(ipmNO=v_ipm)
    #com_id存在，version不存在
    elif com_id and com_id != "None" and (not v_version or v_version == "None"):
        com_id = com_id.strip()
        if v_ipm and v_ipm != "None":
            v_ipm = v_ipm.strip().upper()
        else:
            v_ipm = "None"
        all_customs = get_custom_databycomid(com_id,v_ipm)
        is_custom_repo_origin_data = False
    #com_id不存在，version存在
    elif v_version and v_version != "None" and (not com_id or com_id == "None"):
        v_version = v_version.strip().strip('v').strip('V')
        if v_ipm and v_ipm != "None":
            v_ipm = v_ipm.strip().upper()
        else:
            v_ipm = "None"
        all_customs = get_custom_databyversion(v_version,v_ipm)
        is_custom_repo_origin_data = False
    #version存在，com_id存在
    elif com_id and com_id != "None" and v_version and v_version != "None":
        com_id = com_id.strip()
        v_version = v_version.strip().strip('v').strip('V')
        if v_ipm and v_ipm != "None":
            v_ipm = v_ipm.strip().upper()
        else:
            v_ipm = "None"
        all_customs = get_custom_databycomid_version(com_id,v_version,v_ipm)
        is_custom_repo_origin_data = False
    #都不存在
    else:
        all_customs = models.custom_repo.objects.all()

    if not all_customs:
        dict_showdata = {"total": 0, "pageNO": pageNO, "pagesize": pagesize, "list": []}
        return myJsonResponse(1, 1, "custom_repo查询不到信息，请确定输入是否有误", dict_showdata)

    total = len(all_customs)
    customs,totalpages = paginatorData(all_customs,pageNO,pagesize)

    if is_custom_repo_origin_data:
        showdatas = get_custom_repo(customs)
    else:
        showdatas = get_json_custom_data_fromlist(customs)

    if showdatas:
        dict_showdata = {"total": total, "pageNO": pageNO, "pagesize": pagesize, "list": showdatas}
        return myJsonResponse(1, 1, "SUCCESS", dict_showdata)
    else:
        dict_showdata = {"total": total, "pageNO": pageNO, "pagesize": pagesize, "list": ""}
        return myJsonResponse(0, 0, "custom_repo查找成功，但是函数get_custom_repo或get_json_custom_data_fromlist出错", dict_showdata)

#区域配置信息area_repo
#v_area：地区,v_ip：ip地址,pageNO：页码,pagesize：每页条数
def area_repo_info_page(v_area,v_ip,pageNO,pagesize):
    if v_area and v_area != "None" and v_area != "all":
        v_area = v_area.strip()
        infos = models.area_repo.objects.filter(id=v_area)
    elif v_ip and v_ip != "None":
        v_ip = v_ip.strip()
        infos = models.area_repo.objects.filter(areaRepoIP=v_ip)
    else:
        infos = models.area_repo.objects.all()

    if not infos:
        dict_showdata = {"total": 0, "pageNO": pageNO, "pagesize": pagesize, "list": []}
        return myJsonResponse(1, 1, "area_repo查询不到信息，请确定输入是否有误", dict_showdata)

    total = len(infos)
    p_infos,totalpages = paginatorData(infos,pageNO,pagesize)
    showdatas = get_area_repo_showdata(p_infos)
    if showdatas:
        dict_showdata = {"total": total, "pageNO": pageNO, "pagesize": pagesize, "list": showdatas}
        return myJsonResponse(1, 1, "SUCCESS", dict_showdata)
    else:
        dict_showdata = {"total": total, "pageNO": pageNO, "pagesize": pagesize, "list": ""}
        return myJsonResponse(0, 0, "area_repo查找成功，但是函数get_area_repo_showdata出错", dict_showdata)

#组件版本信息展示页面baseline_version_repo
#com_id：组件标识,v_version：版本,pageNO：页码,pagesize：每页条数
def baseline_version_repo_info_page(com_id,v_version,pageNO,pagesize):
    filter_comid = False
    filter_version = False
    if com_id and com_id != "None":
        filter_comid = True
        component,vers_repos = get_version_repoIDbycomid(com_id)
    elif v_version and v_version != "None":
        filter_version = True
        vers_repos = getComponentsVersion(v_version)
    else:
        vers_repos = models.baseline_version_repo.objects.all()

    if not vers_repos:
        dict_showdata = {"total": 0, "pageNO": pageNO, "pagesize": pagesize, "list": []}
        return myJsonResponse(1, 1, "baseline_version_repo查询不到信息，请确定输入是否有误", dict_showdata)

    total = len(vers_repos)
    p_vers_repos,totalpages = paginatorData(vers_repos,pageNO,pagesize)
    if filter_comid:
        showdatas = get_version_repoJsonDatabycomid(com_id,p_vers_repos)
    elif filter_version:
        showdatas = getJsonComponentsVersion(p_vers_repos)
    else:
        showdatas = get_comp_versionJsonDatas(p_vers_repos)

    if showdatas:
        dict_showdata = {"total": total, "pageNO": pageNO, "pagesize": pagesize, "list": showdatas}
        return myJsonResponse(1, 1, "SUCCESS", dict_showdata)
    else:
        dict_showdata = {"total": 0, "pageNO": pageNO, "pagesize": pagesize, "list": ""}
        return myJsonResponse(0, 0, "baseline_version_repo查找成功，但是函数get_version_repoJsonDatabycomid或getJsonComponentsVersion或get_comp_versionJsonDatas出错", dict_showdata)

#定制项目成果物信息delivery_repo
#ipm：订单号,keyword：关键词,pageNo：页码,pagesize：每页条数
def delivery_repo_info_page(ipm,keyword,pageNO,pagesize):
    if ipm and ipm != "None":
        deliverys = models.delivery_repo.objects.filter(Q(DeliveryPath__contains=ipm)|Q(ipmNO=ipm))
    elif keyword and keyword != "None":
        deliverys = models.delivery_repo.objects.filter(DeliveryPath__contains=keyword)
    else:
        deliverys = models.delivery_repo.objects.all()

    if not deliverys:
        dict_showdata = {"total": 0, "pageNO": pageNO, "pagesize": pagesize, "list": []}
        return myJsonResponse(1, 1, "delivery_repo查询不到信息，请确定输入是否有误", dict_showdata)

    total = len(deliverys)
    p_deliverys,totalpages = paginatorData(deliverys,pageNO,pagesize)
    showdatas = get_delivery_jsonData(p_deliverys)

    if showdatas:
        dict_showdata = {"total": total, "pageNO": pageNO, "pagesize": pagesize, "list": showdatas}
        return myJsonResponse(1, 1, "SUCCESS", dict_showdata)
    else:
        dict_showdata = {"total": total, "pageNO": pageNO, "pagesize": pagesize, "list": ""}
        return myJsonResponse(0, 0, "delivery_repo查找成功，但是函数get_delivery_jsonData出错", dict_showdata)

#products_info_repo
#projectNO,keyword,qa,pageNO,pagesize
def new_products_repo_info_page(projectNO,keyword,qa,pageNO,pagesize):
    filter_qa = False
    filter_pj = False
    if qa and qa != "None":
        filter_qa = True
    if projectNO and projectNO != "None":
        filter_pj = True
    if filter_pj and filter_qa:
        products = models.products_info_repo.objects.filter(Q(pjNO=projectNO),Q(qa=qa))
    elif not filter_qa and filter_pj:
        products = models.products_info_repo.objects.filter(Q(pjNO=projectNO))
    elif not filter_pj and filter_qa:
        products = models.products_info_repo.objects.filter(Q(qa=qa))
    elif keyword and keyword != "None":
        products = models.products_info_repo.objects.filter(productName__contains=keyword)
    else:
        products = models.products_info_repo.objects.all()

    if not products:
        dict_showdata = {"total":0,"pageNO":pageNO,"pagesize":pagesize,"list":[]}
        return  myJsonResponse(1,1,"products_info_repo查询不到信息，请确定驶入是否正确",dict_showdata)

    total = len(products)
    p_products,totalpages = paginatorData(products,pageNO,pagesize)
    showdatas = get_product_jsonData(p_products)

    if showdatas:
        dict_showdata = {"total":total,"pageNO":pageNO,"pagesize":pagesize,"list":showdatas}
        return  myJsonResponse(1,1,"SUCCESS",dict_showdata)
    else:
        dict_showdata = {"total":total,"pageNO":pageNO,"pagesize":pagesize,"list":""}
        return  myJsonResponse(0,0,"products_info_repo查找成功，但是函数get_product_jsonData出错",dict_showdata)


