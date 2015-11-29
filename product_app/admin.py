from django.contrib import admin

from .models import PurchaseHistory

class PurchaseHistoryAdmin(admin.ModelAdmin):
    list_display = ('confirmation_code', 'fullName', 'name', 'totalPrice')
    fieldsets = (
        ('Buyer Information', {
            'fields': ('fullName', 'email', 'phone'),
            'classes': ('wide', 'extrapretty'),
        }),
        ('Product Information', {
            'fields': ('confirmation_code', 'name', 'price', 'quantityTickets'),
            'classes': ('wide', 'extrapretty'),
        }),
    )
    search_fields = ['confirmation_code', 'fullName', 'name']

    def totalPrice(self, obj):
        return "$%.2f" % float(float(obj.price)*obj.quantityTickets)


admin.site.register(PurchaseHistory, PurchaseHistoryAdmin)
