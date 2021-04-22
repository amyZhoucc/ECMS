from django.contrib import admin
from app_webPages import models
# Register your models here.
admin.site.register(models.area_repo)
admin.site.register(models.baseline_repo)
admin.site.register(models.baseline_version_repo)
admin.site.register(models.custom_repo)
admin.site.register(models.delivery_repo)
admin.site.register(models.components_type_repo)
admin.site.register(models.oldproducts_custom_repo)
admin.site.register(models.oldproducts_info_repo)
admin.site.register(models.products_info_repo)