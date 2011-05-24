from django.contrib import admin

from models import Employee, PingPongMatch, PingPongGame, PingPongRecords

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["user","date_joined"]
    fieldsets = [
        ("Profile", {
            "fields": ("user", "nick_name", "title","teams","bio","sites","date_joined","birthday"),
        }),
        ("Optional", {
            "fields": ("twitter","facebook","website","skype","aim"),
        })
    ]

class PingPongMatchAdmin(admin.ModelAdmin):
    pass

class PingPongGameAdmin(admin.ModelAdmin):
    pass

class PingPongRecordsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(PingPongMatch, PingPongMatchAdmin)
admin.site.register(PingPongGame, PingPongGameAdmin)
admin.site.register(PingPongRecords, PingPongRecordsAdmin)
