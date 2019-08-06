from django.contrib import admin

# Register your models here.
from .models import Batting,Export,NFHS


class BattingModelAdmin(admin.ModelAdmin):
  list_display=["name","country","year","average","strikerate"]
  list_filter=["year","country"]
  search_fields=["country","name"]

class ExportModelAdmin(admin.ModelAdmin):
  list_display=["country","commodity","finyear","value"]
  list_filter=["finyear"]
  search_fields=["country","commodity"]

class NFHSModelAdmin(admin.ModelAdmin):
  list_display=["id","state","year"]
admin.site.register(Export,ExportModelAdmin)
admin.site.register(Batting,BattingModelAdmin)
admin.site.register(NFHS,NFHSModelAdmin)
