from django.contrib import admin

from .models import Project, Invoices, UserProjectRights

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'budget', 'spend')


@admin.register(Invoices)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'project', 'invoice', 'submission_date', 'Confirmed' )

@admin.register(UserProjectRights)
class UserProjectRightsAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'rights')