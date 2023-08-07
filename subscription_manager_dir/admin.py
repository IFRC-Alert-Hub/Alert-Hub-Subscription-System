from django.contrib import admin
from .models import SubscriptionAlerts
from .external_alert_models import CapFeedAdmin1, CapFeedAlert, CapFeedAlertadmin1, \
    CapFeedAlertinfo, CapFeedCountry

class PrototypeInline(admin.StackedInline):
    using = 'AlertDB'
    extra = 0

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(PrototypeInline, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(PrototypeInline, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(PrototypeInline, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)



class AlertAdmin1Inline(PrototypeInline):
    model = CapFeedAlertadmin1
    extra = 0

class AlertInfoInline(PrototypeInline):
    model = CapFeedAlertinfo
    extra = 0


class MultiDBModelAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = 'AlertDB'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(MultiDBModelAdmin, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)

class AlertAdmin(MultiDBModelAdmin):
    using = 'AlertDB'
    list_display = ["id", "sent"]
    search_fields = ["id"]

    inlines = [AlertInfoInline, AlertAdmin1Inline]

admin.site.register(CapFeedAdmin1, MultiDBModelAdmin)
admin.site.register(CapFeedAlert, AlertAdmin)
admin.site.register(CapFeedAlertadmin1, MultiDBModelAdmin)
admin.site.register(CapFeedAlertinfo, MultiDBModelAdmin)
admin.site.register(CapFeedCountry, MultiDBModelAdmin)
admin.site.register(SubscriptionAlerts)