from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    Area, Userlogin, Employee, Supplier, Category, Product,
    Inventory, CustomizeProduct,
    RentOrder, contactusmodel, Assign_Task, Delivery, cart
)

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('pincode', 'area_name')

@admin.register(Userlogin)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email_id', 'phone_num', 'address', 'pincode')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email_id', 'phone_num', 'role', 'work_schedule')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info', 'shop_address')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('cat_name', 'cat_description')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_price', 'product_status', 'cat_id')

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'stock_quantity', 'supplier_id')

@admin.register(CustomizeProduct)
class CustomizeProductAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'custom_pic', 'customize_details', 'budget', 'status', 'submitted_at')

    def custom_pic(self, obj):
        if obj.customize_img and hasattr(obj.customize_img, 'url'):
            return mark_safe(f'<img src="{obj.customize_img.url}" width="100">')
        return "No Image Available"

@admin.register(RentOrder)
class RentOrderAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'product_id', 'start_date', 'end_date',
                    'rent_deposit', 'rent_amount', 'return_status')

@admin.register(contactusmodel)
class showcontactusdata(admin.ModelAdmin):
    list_display = ["contactus_name","contactus_email","contactus_phone","contactus_message"]

@admin.register(Assign_Task)
class showassigtask(admin.ModelAdmin):
    list_display = ["order_id", "employee_id", "task_status"]

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id', 'rent_id', 'employee_id', 'delivery_date')
    search_fields = ('order_id__id', 'rent_id__id', 'employee_id__name')
    list_filter = ('delivery_date',)

@admin.register(cart)
class cart(admin.ModelAdmin):
    list_display = ('id','userid','productid','quantity','totalamount','orderstatus','orderid')

