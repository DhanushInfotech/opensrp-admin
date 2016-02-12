from django.contrib import admin
from django.contrib import messages
from Masters.models import *
from django.http import HttpResponse
from Masters.forms import *
from django.conf.urls import patterns, url
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.shortcuts import render
from collections import defaultdict
from django.contrib.admin.templatetags.admin_modify import *
from django.contrib.admin.templatetags.admin_modify import submit_row as original_submit_row
from django.http import HttpResponseRedirect
from django.utils.encoding import force_unicode

class DrugInfoAdmin(admin.ModelAdmin):
    list_display= ('drug_name','frequency','dosage','direction','active',)
    search_fields = ('drug_name',)

    def get_actions(self, request):
        actions = super(DrugInfoAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class FrequencyAdmin(admin.ModelAdmin):
    list_display = ('number_of_times','active',)
    search_fields = ('number_of_times',)

    def get_actions(self, request):
        actions = super(FrequencyAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class DosageAdmin(admin.ModelAdmin):
    list_display = ('dosage','active',)
    search_fields = ('dosage',)

    def get_actions(self, request):
        actions = super(DosageAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class DirectionsAdmin(admin.ModelAdmin):
    list_display = ('directions','active',)
    search_fields = ('directions',)

    def get_actions(self, request):
        actions = super(DirectionsAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class ICD10Admin(admin.ModelAdmin): 
    list_display = ('ICD10_Chapter','ICD10_Code','ICD10_Name','can_select','status')
    search_fields = ('ICD10_Chapter','ICD10_Code','ICD10_Name',)

    def get_actions(self, request):
        actions = super(ICD10Admin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class InvestigationAdmin(admin.ModelAdmin):
    list_display = ('service_group_name','investigation_name','is_active',)
    search_fields = ('service_group_name','investigation_name','is_active',)

    def get_actions(self, request):
        actions = super(InvestigationAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class PocInfoAdmin(admin.ModelAdmin):    
    list_display = ('visitentityid','entityidec','anmid','level','clientversion','serverversion','visittype','phc','pending','docid',)
    search_fields = ('visitentityid','entityidec','anmid',)

    def get_actions(self, request):
        actions = super(PocInfoAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class UserMaintenanceAdmin(admin.ModelAdmin):
    form = UserMaintenaceForm

    list_display = ('user_id','user_role','name','phone_number','email','villages','active',)

    search_fields = ('user_id',)

    def get_urls(self):
        urls = super(UserMaintenanceAdmin, self).get_urls()
        my_urls = patterns('',
                url(r'add/$', 'Masters.views.adminadd_usermaintenance',name='user_maintenance'),


                url(r'(?P<batch_id>\d+)/$','Masters.views.edit_usermaintenance',name='editusermaintenance'),
                )

        return my_urls + urls

    def get_actions(self, request):
        actions = super(UserMaintenanceAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class CountryAdmin(admin.ModelAdmin):
    list_display=('country_name','country_code','active',)
    search_fields = ('country_name',)

    def get_actions(self, request):
        actions = super(CountryAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class CountyAdmin(admin.ModelAdmin):
    list_display = ('county_name','country_name','active',)
    search_fields = ('county_name',)

    def get_actions(self, request):
        actions = super(CountyAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class DisttabAdmin(admin.ModelAdmin):
    list_display = ('district_name','county_name','country_name','active')
    search_fields = ('district_name',)

    def get_urls(self):
        urls = super(DisttabAdmin, self).get_urls()
        my_urls = patterns('',
                url(r'add/$', 'Masters.views.adminadd_district',name='add_district'),


                url(r'(?P<district_id>\d+)/$','Masters.views.edit_district',name='editdistrict'),
                )
        return my_urls + urls

    def get_actions(self, request):
        actions = super(DisttabAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class SubdistrictTabAdmin(admin.ModelAdmin):
    list_display = ('subdistrict','district','county','country','active',)
    search_fields = ('subdistrict',)

    def get_urls(self):
        urls = super(SubdistrictTabAdmin, self).get_urls()
        my_urls = patterns('',
                url(r'add/$', 'Masters.views.adminadd_subdistrict',name='add_subdistrict'),


                url(r'(?P<subdistrict_id>\d+)/$','Masters.views.edit_subdistrict',name='editsubdistrict'),
                )
        return my_urls + urls

    def get_actions(self, request):
        actions = super(SubdistrictTabAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class LocationTabAdmin(admin.ModelAdmin):
    list_display = ('location','subdistrict','district','county','country','active',)
    search_fields = ('location',)

    def get_urls(self):
        urls = super(LocationTabAdmin, self).get_urls()
        my_urls = patterns('',
                url(r'add/$', 'Masters.views.adminadd_location',name='add_subdistrict'),


                url(r'(?P<loc_id>\d+)/$','Masters.views.edit_location',name='editlocation'),
                )
        return my_urls + urls
    
    def save_model(self, request, obj, form, change):
        # add an additional message
        messages.info(request, "Extra message here.")
        super(LocationTabAdmin, self).save_model(request, obj, form, change)

    def get_actions(self, request):
        actions = super(LocationTabAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


class HealthCenterAdmin(admin.ModelAdmin):
    list_display = ('hospital_name','hospital_type','hospital_address','country_name','county_name','district_name','subdistrict_name','parent_hospital','villages','active')
    search_fields = ('hospital_name',)

    def get_urls(self):
        urls = super(HealthCenterAdmin, self).get_urls()
        my_urls = patterns('',
                url(r'add/$', 'Masters.views.admin_hospital',name='hospital'),
                #url(r'gettype/$', 'Masters.views.get_hospital',name='hospital'),
                url(r'(?P<hospital_id>\d+)/$', 'Masters.views.edit_hospital',name='edithospital'),
                )
        return my_urls + urls

    def get_actions(self, request):
        actions = super(HealthCenterAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class AppConfigurationAdmin(admin.ModelAdmin):
    list_display = ('wife_age_min','wife_age_max','husband_age_min','husband_age_max','temperature_units','country_name',)
    search_fields = ('wife_age_min',)
    fieldsets = (
      (None, {
          'fields': ('country_name','temperature_units','escalation_schedule','is_highrisk')
      }),
      ('Wife age', {
          'fields': ('wife_age_min','wife_age_max')
      }),
      ('Husband age', {
          'fields': ('husband_age_min','husband_age_max')
      }),

   )

    def get_actions(self, request):
        actions = super(AppConfigurationAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class FormFieldsAdmin(admin.ModelAdmin):
    list_display = ('form_name','field1','field2','field3','field4','field5','country')
    search_fields = ('form_name',)

    def get_actions(self, request):
        actions = super(FormFieldsAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class AnnualTargetAdmin(admin.ModelAdmin):
    list_display = ('anm','indicators','target','year',)
    search_fields = ('anm', )
    list_filter = ('indicators',)

    def get_actions(self, request):
        actions = super(AnnualTargetAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(DrugInfo,DrugInfoAdmin)
admin.site.register(Frequency,FrequencyAdmin)
admin.site.register(Dosage,DosageAdmin)
admin.site.register(Directions,DirectionsAdmin)
admin.site.register(ICD10,ICD10Admin)
admin.site.register(Investigations,InvestigationAdmin)
admin.site.register(PocInfo,PocInfoAdmin)
admin.site.register(UserMasters,UserMaintenanceAdmin)
admin.site.register(CountryTb,CountryAdmin)
admin.site.register(CountyTb,CountyAdmin)
admin.site.register(Disttab,DisttabAdmin)
admin.site.register(SubdistrictTab,SubdistrictTabAdmin)
admin.site.register(LocationTab,LocationTabAdmin)
admin.site.register(HealthCenters,HealthCenterAdmin)
admin.site.register(AppConfiguration,AppConfigurationAdmin)
admin.site.register(FormFields,FormFieldsAdmin)
admin.site.register(AnnualTarget,AnnualTargetAdmin)
