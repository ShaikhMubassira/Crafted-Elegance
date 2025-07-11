from django.utils import timezone
from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User


class Area(models.Model):
    pincode = models.IntegerField(primary_key=True)
    area_name = models.CharField(max_length=30, null=False)

class Userlogin(models.Model):
    name = models.CharField(max_length=50, null=False)
    email_id = models.EmailField(max_length=50, unique=True, null=False)
    password = models.CharField(max_length=30, null=False)
    phone_num = models.BigIntegerField(null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.ForeignKey(Area, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
class Employee(models.Model):
    name = models.CharField(max_length=50, null=False)
    email_id = models.EmailField(max_length=50, unique=True, null=False)
    password = models.CharField(max_length=30, null=False)
    phone_num = models.BigIntegerField(null=False)
    role = models.CharField(max_length=30, null=False)
    work_schedule = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=50, null=False)
    contact_info = models.BigIntegerField(null=False)
    shop_address = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name

class Category(models.Model):
    cat_name = models.CharField(max_length=50, null=False)
    cat_description = models.CharField(max_length=255, null=True, blank=True )

    def __str__(self):
        return self.cat_name

class Product(models.Model):
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_img = models.ImageField(upload_to='product_images/', blank=True, default='')
    product_name = models.CharField(max_length=50, null=False)
    product_price = models.IntegerField(null=False)
    rent_per_day = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    product_details = models.CharField(max_length=200, null=False)
    product_status = models.CharField(max_length=50, null=False)

    def pic(self):
        return mark_safe('<img src = "{}" width = "100">'.format(self.product_img.url))

    pic.allow_tags = True

    def __str__(self):
        return self.product_name

class Inventory(models.Model):
    stock_quantity = models.IntegerField(null=False)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

class CustomizeProduct(models.Model):
    customize_img = models.ImageField(upload_to='customized_products/', null=False)
    customize_details = models.CharField(max_length=300, null=False)
    budget = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=30,null=True)
    submitted_at = models.DateTimeField(default=timezone.now)
    user_id = models.ForeignKey(Userlogin, on_delete=models.CASCADE)

    def custom_pic(self):
        return mark_safe('<img src = "{}" width = "100">'.format(self.customize_img.url))

    custom_pic.allow_tags = True

    def __str__(self):
        return self.customize_details

from django.core.exceptions import ValidationError

class RazorpayPayment(models.Model):
    user = models.ForeignKey(Userlogin, on_delete=models.CASCADE)
    custom_product = models.ForeignKey(CustomizeProduct, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Paid", "Paid")])

    def __str__(self):
        return f"{self.custom_product} - {self.amount}"


class RentOrder(models.Model):
    product_id = models.ForeignKey("Product", on_delete=models.CASCADE)
    user_id = models.ForeignKey(Userlogin, on_delete=models.CASCADE, related_name="rental_orders")  # Customer's orders
    start_date = models.DateField()
    end_date = models.DateField()
    rent_deposit = models.IntegerField()
    rent_amount = models.FloatField()
    return_status = models.CharField(max_length=50, default="Pending")

    # Assign delivery person with a unique related_name
    delivery_person = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'Delivery Person'},
        related_name="delivery_assignments"  # Unique related_name to avoid conflicts
    )

    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Processing", "Processing"),("Assigned", "Assigned") ,("Delivered", "Delivered"), ("Returned", "Returned")],
        default="Pending",
    )

    # Razorpay Payment Fields
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Paid", "Paid")], default="Pending")

    def __str__(self):
        return f"Order {self.id} - {self.status}"


class contactusmodel(models.Model):
    contactus_name= models.CharField(max_length=80)
    contactus_email = models.EmailField()
    contactus_phone = models.BigIntegerField()
    contactus_message = models.TextField()

class Assign_Task(models.Model):
    order_id = models.ForeignKey(RazorpayPayment, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    Task_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Ready', 'Ready'),
    ]
    task_status = models.CharField(max_length=30, choices=Task_STATUS_CHOICES, default='Pending')


class cart(models.Model):
    userid = models.ForeignKey(Userlogin,on_delete=models.CASCADE)
    productid = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    totalamount = models.FloatField()
    orderstatus = models.IntegerField(default=0)
    orderid = models.IntegerField(default=0)
    timeStamp = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.userid} - {self.productid.product_name} ({self.quantity})"



class finalorders(models.Model):
    u_id = models.ForeignKey(Userlogin, on_delete=models.CASCADE)
    status = models.CharField(max_length=15)
    total_amount = models.FloatField()
    o_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.u_id.name}"

    class Meta:
        verbose_name_plural="order"


from django.utils import timezone

class FinalOrderPayment(models.Model):
    PAYMENT_MODE_CHOICES = [
        ('online', 'Online Payment'),
        ('offline', 'Offline Payment'),
    ]

    PAYMENT_STATUS = (
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Failed", "Failed"),
        ("Not Paid", "Not Paid"),

    )

    u_id = models.ForeignKey(Userlogin, on_delete=models.CASCADE)
    o_id = models.ForeignKey(finalorders, on_delete=models.CASCADE)
    pay_datetime = models.DateTimeField(default=timezone.now)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_MODE_CHOICES)  # Payment mode
    amount = models.FloatField()  # Store the total order amount
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    offline_reference = models.CharField(max_length=255, blank=True, null=True)  # Reference number for offline payment
    offline_remarks = models.TextField(blank=True, null=True)  # Optional remarks for offline payments
    address = models.TextField(blank=True, null=True)  # Optional remarks for offline payments
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="Pending")

    def get_total_amount(self):
        return self.amount
    
    def __str__(self):
        return f"Order Payment {self.id} for Order {self.o_id.id}"

    class Meta:
        verbose_name_plural="payment"

class OrderItems(models.Model):
    order = models.ForeignKey(finalorders, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField()

    def __str__(self):
        return f"{self.order.id} - {self.product.product_name} ({self.quantity})"

class Delivery(models.Model):
    order_id = models.ForeignKey(finalorders, on_delete=models.CASCADE, null=True, blank=True)
    rent_id = models.ForeignKey(RentOrder, on_delete=models.CASCADE, null=True, blank=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    delivery_date = models.DateField(null=False)

    def get_status(self):
        """ Fetch order status from Assign_Task """
        task = Assign_Task.objects.filter(employee_id=self.employee_id).last()
        return task.order_id.order_status if task and task.order_id else "N/A"

    def __str__(self):
        if self.order_id:
            return f"Order {self.order_id.id} by {self.employee_id.name}"
        elif self.rent_id:
            return f"Rent Order {self.rent_id.id} by {self.employee_id.name}"
        return "Unassigned Delivery"