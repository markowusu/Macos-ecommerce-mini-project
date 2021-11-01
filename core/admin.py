from django.contrib import admin
from .models import Items,OrderItem,Order,Payment, Category

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']
    
# Register your models here.
admin.site.register(Items)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
