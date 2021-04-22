#-*- coding:utf-8 -*-
from django.db import models

# Create your models here.
'''
class Book(models.Model):
    name = models.CharField(max_length = 64)
    price = models.IntegerField()
    note = models.TextField()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-id']

class product(models.Model):
    productName = models.CharField(max_length=100)
    url = models.TextField()
'''

class area_repo(models.Model):
    areaName = models.CharField(max_length=20)
    head = models.CharField(max_length=200,default="")
    areaRepoIP = models.CharField(max_length=20)
    codePATH = models.CharField(max_length=200)
    DeliveryPATH = models.CharField(max_length=200)
    docPATH = models.CharField(max_length=200,null=True)
    projectPATH = models.CharField(max_length=200,null=True)

    class Meta:
        db_table="area_repo"
    def __unicode__(self):
        return  self.areaName

class baseline_repo(models.Model):
    component_type_choice = (
        ("special","special"),
        ("public","public"),
        ("general","general"),
        ("universal","universal"),
        ("framework","framework"),
        ("ctm-components","ctm-components"),
        ("tool","tool"),
        ("NetUnit","NetUnit"),
    )
    repoType_choice = (
        ("SVN","SVN"),
        ("GIT","GIT"),
    )
    rule_choice = (
        ("open","open"),
        ("close","close"),
    )

    areaRepoID = models.PositiveIntegerField(default=0)
    componentsID = models.CharField(max_length=100)
    type = models.CharField(max_length=50,choices=component_type_choice)
    GITPath = models.CharField(max_length=255)
    SVNPath = models.CharField(max_length=255)
    head = models.CharField(max_length=200)
    repodescribe = models.TextField(null=True)
    headVersion = models.CharField(max_length=10)
    baserepoType = models.CharField(max_length=3,choices=repoType_choice)
    authority = models.TextField(null=True)
    department = models.CharField(max_length=50,null=True)
    rule = models.CharField(max_length=5,choices=rule_choice)
    errorCode = models.CharField(max_length=50,default="")

    class Meta:
        db_table = "baseline_repo"
    def __unicode__(self):
        return self.componentsID

class baseline_version_repo(models.Model):
    baselinerepoID = models.PositiveIntegerField(default=0)
    version = models.CharField(max_length=10)
    describe = models.TextField(default="",null=True)

    class Meta:
        db_table = "baseline_version_repo"
    def __unicode__(self):
        return "%s_%s"%(self.baselinerepoID,self.version)

class custom_repo(models.Model):
    baselineversionrepoID = models.PositiveIntegerField(default=0)
    arearepoID = models.PositiveIntegerField(default=0)
    repoPath = models.TextField(null=True)
    productManager = models.CharField(max_length=100,default="")
    productName = models.CharField(max_length=100,default="")
    ipmNO = models.CharField(max_length=200)
    describe = models.TextField(default="")

    class Meta:
        db_table = "custom_repo"
    def __unicode__(self):
        return self.ipmNO

class delivery_repo(models.Model):
    DeliveryPath = models.TextField(null=True)
    ipmNO = models.CharField(max_length=200)

    class Meta:
        db_table = "delivery_repo"
    def __unicode__(self):
        return self.ipmNO

class components_type_repo(models.Model):
    ENname = models.CharField(max_length=200)
    CNname = models.CharField(max_length=200)
    typePATH = models.CharField(max_length=200)

    class Meta:
        db_table = "components_type_repo"
    def __unicode__(self):
        return self.CNname

class oldproducts_custom_repo(models.Model):
    department_choice = (
        ("Traffic","Traffic"),
        ("PublicSecurity","PublicSecurity"),
        ("Judicial","Judicial"),
    )
    basicversion = models.CharField(max_length=200)
    repoPath = models.TextField(null=True)
    department = models.CharField(max_length=20,choices=department_choice)
    productName = models.CharField(max_length=100,default="")
    subsystem = models.CharField(max_length=100,default="")
    ipmNO = models.CharField(max_length=200)
    arearepoID = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=100,default="")

    class Meta:
        db_table = "oldproducts_custom_repo"
    def __unicode__(self):
        return "%s_%s"%(self.department,self.ipmNO)

class oldproducts_info_repo(models.Model):
    department_choice = (
        ("Traffic","Traffic"),
        ("PublicSecurity","PublicSecurity"),
        ("Judicial","Judicial"),
    )
    productName = models.CharField(max_length=100,default="")
    department = models.CharField(max_length=20,choices=department_choice)

    class Meta:
        db_table = "oldproducts_info_repo"
    def __unicode__(self):
        return self.productName

class products_info_repo(models.Model):
    pjNO = models.CharField(max_length=50,default="")
    productName = models.TextField(null=True)
    version = models.CharField(max_length=10)
    delivery_path = models.TextField(null=True)
    project_manager = models.CharField(max_length=100,default="")
    qa = models.CharField(max_length=100,default="")
    cm = models.CharField(max_length=100,default="")
    department = models.CharField(max_length=200,default="")

    class Meta:
       db_table = "products_info_repo"
    def __unicode__(self):
        return self.pjNO