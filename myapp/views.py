import os
import re
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from reportlab.lib.styles import getSampleStyleSheet
from .models import *
import razorpay
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
import razorpay
from django.conf import settings



# Create your views here.

def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('username')  # Username field contains email
        password = request.POST.get('password')

        # Authenticate admin user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            # Ensure admin session is set
            request.session["is_admin"] = True
            request.session.modified = True  # Ensure session is saved

            print(f"Admin Login - is_admin: {request.session.get('is_admin')}")  # Debugging

            messages.success(request, "Login successful!")
            return redirect('show_user')  # Redirect to dashboard
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('admin_login')

    return render(request, 'admin/page-login.html')

def admin_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('admin_login')

def showmanageuser(request):
    app_logins = User.objects.all()  # Data from your custom Login model

    # Pass both datasets to the template
    context = {
        'logins': app_logins,
    }
    return render(request,'admin/showmanageuser.html', context)
   
def add_area(request):
    if request.method == "POST":
        pincode = request.POST.get('pincode')
        area_name = request.POST.get('area_name')
        areas = Area(pincode=pincode, area_name=area_name)
        areas.save()

        messages.success(request, "Area added successfully!")
        return redirect('showarea')  # Redirect to the list of areas or desired page

    return render(request, 'admin/add_area.html')

def showarea(request):
    areas = Area.objects.all()  # Data from  custom Login model

    # Pass both datasets to the template
    context = {
        'areas': areas,
    }
    return render(request,'admin/showarea.html', context)

def edit_area(request, pincode):
    area = get_object_or_404(Area, pincode=pincode)

    # Check if the request method is POST
    if request.method == "POST":
        # Get POST data
        pincode = request.POST.get('pincode')
        area_name = request.POST.get('area_name')
        
        # Update the area object with new data
        area.pincode = pincode
        area.area_name = area_name
        area.save()  # Save changes to the database

        return redirect('showarea')  # Redirect to the page showing all areas

    context = {
        'area': area,  # Pass the existing area to the template for pre-filling the form
    }
    return render(request, 'admin/edit_area.html', context)

# View to confirm and delete the area
def delete_area(request, pincode):
    # Retrieve the area object by pincode
    area = get_object_or_404(Area, pincode=pincode)

    # If the request method is POST, proceed with deletion
    if request.method == 'POST':
        area.delete()
        # Redirect to the list of areas after deletion
        return redirect('showarea')

    # Render the confirmation page if not POST
    return render(request, 'admin/delete_area.html', {'area': area})

def show_users(request):
    users = Userlogin.objects.all()  # Fetch all users
    return render(request, 'admin/showuser.html', {'users': users})



def add_product_category(request):
    if request.method == "POST":
        cat_name = request.POST.get('cat_name')
        cat_description = request.POST.get('cat_description')
        category = Category(cat_name=cat_name, cat_description=cat_description)
        category.save()

        messages.success(request, "Category added successfully!")
        return redirect('showproductcategory')  # Redirect to the list of categories or desired page

    return render(request, 'admin/add_product_category.html')

def showproductcategory(request):
    productcatdetail = Category.objects.all()
    context = {
        'categories':productcatdetail,
    }
    return render(request,'admin/show_categories.html', context)

def edit_product_category(request, category_id):
    # Fetch the ProductCategory object by ID
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        # Get data from the form
        cate_name = request.POST.get('cat_name')
        cate_description = request.POST.get('cat_description')

        # Update the category name and description
        category.cat_name = cate_name
        category.cat_description = cate_description
        category.save()  # Save the updated object

        # Redirect to the category list view
        return redirect('showproductcategory')

    # Pass the ProductCategory data to the template for editing
    context = {
        'category': category,
    }
    return render(request, 'admin/edit_category.html', context)

def delete_productcategory(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        category.delete()  # Delete the category
        messages.success(request, "Category deleted successfully.")
        return redirect('showproductcategory')  # Redirect to the list of categories

    context = {
        'category': category,
    }
    return render(request, 'admin/delete_product_category.html', context)

def add_employees(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email_id = request.POST.get('email_id')
        password = request.POST.get('password')
        phone_num = request.POST.get('phone_num')
        role = request.POST.get('role')
        work_schedule = request.POST.get('work_schedule')

        # Check if the email already exists
        if Employee.objects.filter(email_id=email_id).exists():
            messages.error(request, "A user with this email already exists.")
        else:
            # Create the AppLogin instance
            user = Employee(
                name=name,
                email_id=email_id,
                password=password,
                phone_num=phone_num,
                role=role,
                work_schedule=work_schedule,
            )
            user.save()

            messages.success(request, "User added successfully!")
            return redirect('manage_employee')  # Redirect to the list of users or a desired page

    return render(request, 'admin/add_employee.html')

def manage_employee(request):
    employee = Employee.objects.all()  # Data from your custom Login model

    # Pass both datasets to the template
    context = {
        'logins': employee,
    }
    return render(request,'admin/showemployee.html', context)

def edit_employee(request, login_id):
    # Fetch the specific login record based on ID
    login = get_object_or_404(Employee, id=login_id)

    if request.method == "POST":
        # Get data from form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_num = request.POST.get('phone_num')
        role = request.POST.get('role')
        work_schedule = request.POST.get('work_schedule')

        # Update the login object
        login.name = name
        login.email = email
        login.password = password
        login.phone_num = phone_num
        login.role = role
        login.work_schedule = work_schedule
        login.save()  # Save the updated object

        # Redirect back to the table view after updating
        return redirect('manage_employee')

    # Pass the login data to the form for editing
    context = {
        'employee': login,
    }
    return render(request, 'admin/edit_employee.html', context)

def delete_employee(request, login_id):
    # Fetch the employee object based on the ID
    employee = get_object_or_404(Employee, id=login_id)

    if request.method == "POST":
        employee.delete()  # Delete the employee record
        messages.success(request, "Employee deleted successfully.")
        return redirect('manage_employee')  # Corrected URL name here

    context = {
        'employee': employee,
    }
    return render(request, 'admin/delete_employee.html', context)


def add_product(request):
    if request.method == "POST":
        cate_id = request.POST.get('Cate')
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        rent_per_day = request.POST.get('rent_per_day')  # Fetching rent per day
        product_details = request.POST.get('product_details')
        product_status = request.POST.get('product_status')
        product_img = request.FILES.get('product_img')

        # Fetch the category
        try:
            category = Category.objects.get(id=cate_id)
        except Category.DoesNotExist:
            messages.error(request, "Invalid category selected.")
            return redirect('add_product')

        # Create and save the Product instance
        product = Product(
            cat_id=category,
            product_name=product_name,
            product_price=product_price,
            rent_per_day=rent_per_day,  # Adding rent per day field
            product_details=product_details,
            product_img=product_img,
            product_status=product_status,
        )
        product.save()

        messages.success(request, "Product added successfully!")
        return redirect('showproductdetail')  # Redirect to the list of products or desired page

    # Fetch all categories for the dropdown
    categories = Category.objects.all()

    return render(request, 'admin/add_product.html', {'categories': categories})


def showproductdetail(request):
    productcatdetail = Product.objects.all()
    context = {
        'products':productcatdetail,
    }
    return render(request,'admin/showproductdetail.html', context)

def edit_product(request, product_id):
    # Fetch the Product object by ID
    product = get_object_or_404(Product, id=product_id)

    # Fetch all available categories for the dropdown
    categories = Category.objects.all()

    if request.method == "POST":
        # Get data from the form
        cate_id = request.POST.get('Cate')
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        rent_per_day = request.POST.get('rent_per_day')  # Fetching rent per day
        product_details = request.POST.get('product_details')
        product_status = request.POST.get('product_status')
        product_img = request.FILES.get('product_img')

        # Update fields
        product.cat_id = get_object_or_404(Category, id=cate_id)
        product.product_name = product_name
        product.product_price = product_price
        product.rent_per_day = rent_per_day  # Updating rent per day field
        product.product_details = product_details
        product.product_status = product_status

        # Update image if provided
        if product_img:
            product.product_img = product_img

        product.save()  # Save the updated object

        # Redirect to the product list view
        return redirect('showproductdetail')

    # Pass the Product data and categories to the template
    context = {
        'product': product,
        'categories': categories,
    }
    return render(request, 'admin/edit_product.html', context)



def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()  # Delete the product
        return redirect('showproductdetail')  # Redirect back to the product list
    # Render the confirmation page if it's a GET request
    return render(request, 'admin/delete_product.html', {'product': product})


def add_custom_product(request):
    if request.method == "POST":
        customize_img = request.FILES.get('customize_img')
        customize_details = request.POST.get('customize_details')
        user_id = request.POST.get('user_id')

        try:
            user = Userlogin.objects.get(id=user_id)
        except Userlogin.DoesNotExist:
            messages.error(request, "Invalid user.")
            return redirect('add_custom_product')

        # Create and save the new CustomizeProduct
        custom_product = CustomizeProduct(
            customize_img=customize_img,
            customize_details=customize_details,
            user_id=user
        )
        custom_product.save()

        messages.success(request, "Customize Product added successfully!")
        return redirect('show_custom_product')

    users = User.objects.all()

    return render(request, 'admin/add_custom_product.html', {
        'user': users
    })

def show_custom_product(request):
    custom_products = CustomizeProduct.objects.all()

    return render(request, 'admin/show_custom_product.html', {
        'custom_products': custom_products
    })

def edit_custom_product(request, product_id):
    # Fetch the existing CustomProduct instance by ID
    custom_product = get_object_or_404(CustomizeProduct, id=product_id)

    if request.method == 'POST':
        # Update the fields from the form
        customize_detail = request.POST.get('rental_status')

        if customize_detail == "Rejected":
            custom_product.status = "Rejected"
        elif customize_detail == "Approved":
            custom_product.status = "Approved"
        elif customize_detail == "Pending":
            custom_product.status = "Pending"
        elif customize_detail == "Completed":
            custom_product.status = "Completed"

        # Save the updated instance
        custom_product.save()

        return redirect('show_custom_product')

    # Render the form with the existing data pre-populated
    return render(request, 'admin/edit_custom_product.html', {'custom_product': custom_product})


def delete_custom_product(request, product_id):
    custom_product = get_object_or_404(CustomizeProduct, id=product_id)

    if request.method == "POST":
        custom_product.delete()
        messages.success(request, "Customize Product deleted successfully!")
        return redirect('show_custom_product')

    return render(request, 'admin/delete_custom_product.html', {
        'custom_product': custom_product
    })

def manage_order(request):
    orders = finalorders.objects.prefetch_related(
        Prefetch('orderitems_set', queryset=OrderItems.objects.select_related('product'))
    )
    return render(request, 'admin/manage_order.html', {'orders': orders})

def manage_rent_orders(request):
    rent_orders = RentOrder.objects.select_related('product_id', 'user_id', 'delivery_person').all()
    context = {
        'rent_orders': rent_orders
    }
    return render(request, 'admin/manage_rent.html', context)

def manage_inventory(request):
    # Fetch all orders
    orders = Inventory.objects.all()
    print("jcvbjdbvjfb",orders)
    return render(request, 'admin/manage_inventory.html', {'orders': orders})

def manage_supplier(request):
    # Fetch all orders
    orders = Supplier.objects.all()
    print("jcvbjdbvjfb",orders)
    return render(request, 'admin/manage_supplier.html', {'orders': orders})

def manage_payment(request):
    context = {
        "razorpay_payments": RazorpayPayment.objects.all(),
        "final_order_payments": FinalOrderPayment.objects.all(),
    }
    return render(request,'admin/managepayment.html',context)

def indexpage(request):
    fetchproducts = Product.objects.all()[:5]
    # print(fetchproducts,fetchcategory)
    context = {
        "products": fetchproducts,
    }
    return render(request,"index.html",context)


def userregister(request):
    return render(request,"register.html")


def fetchregisterdata(request):
    username = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    password = request.POST.get("password", "").strip()
    phone_number = request.POST.get("phone_number", "").strip()
    address = request.POST.get("address", "").strip()
    pincode_id = request.POST.get("pincode", "").strip()  # Fetch pincode ID from the form

    # Validate Required Fields
    if not username or not email or not password or not phone_number or not address or not pincode_id:
        messages.error(request, "All fields are required.")
        return redirect("/register")

    # Validate name (Only alphabets, 3-50 characters)
    if not re.match(r"^[A-Za-z\s]{3,50}$", username):
        messages.error(request, "Name should contain only letters and be 3-50 characters long.")
        return redirect("/register")

    # Validate Email Format
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_regex, email):
        messages.error(request, "Enter a valid email address.")
        return redirect("/register")

    # Validate Password (Min 8 characters, must include letters, numbers, special character)
    password_regex = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    if not re.match(password_regex, password):
        messages.error(request, "Password must be at least 8 characters long, include letters, numbers, and a special character.")
        return redirect("/register")

    # Validate Phone Number (10-15 digits)
    phone_regex = r"^\d{10,15}$"
    if not re.match(phone_regex, phone_number):
        messages.error(request, "Enter a valid phone number (10-15 digits).")
        return redirect("/register")

    # Validate Address Length (10-255 characters)
    if len(address) < 10 or len(address) > 255:
        messages.error(request, "Address must be between 10 and 255 characters.")
        return redirect("/register")

    # Validate if Email already exists
    if Userlogin.objects.filter(email_id=email).exists():
        messages.error(request, "Email already registered. Please login.")
        return redirect("/login")

    # Fetch Pincode Object from `Area` Model
    try:
        pincode_obj = Area.objects.get(pincode=pincode_id)
    except Area.DoesNotExist:
        messages.error(request, "Invalid Pincode selected.")
        return redirect("/register")

    # Hash password before saving
    password_hashed = make_password(password)

    # Save user data with pincode
    insertquery = Userlogin(
        email_id=email,
        password=password_hashed,
        name=username,
        address=address,
        phone_num=phone_number,
        pincode=pincode_obj  # Assigning ForeignKey instance
    )
    insertquery.save()

    print("success")
    return render(request, "login.html")


def userlogin(request):
    return render(request,"login.html")

def fetchlogindata(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        # Debugging prints
        print("Received Email:", email)
        print("Received Password:", password)

        # 1. Check if fields are empty
        if not email or not password:
            messages.error(request, "Both email and password are required.")
            return redirect("/login")

        # 2. Validate email format
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, email):
            messages.error(request, "Enter a valid email address.")
            return redirect("/login")

        # 3. Check if user exists
        userdata = Userlogin.objects.filter(email_id=email).first()
        if not userdata:
            print("User does not exist.")
            messages.error(request, "Invalid email or password.")
            return redirect("/login")

        # 4. Verify password
        print("Stored Hashed Password:", userdata.password)  # Debugging
        if check_password(password, userdata.password):
            # Store user session
            request.session["user_id"] = userdata.id
            request.session["log_username"] = userdata.name
            request.session["log_email"] = userdata.email_id
            request.session.modified = True  # Ensure session updates

            print("Login successful. ID:", request.session["user_id"])
            messages.success(request, "Login successful.")
            return redirect("/")  # Redirect to homepage or dashboard
        else:
            print("Incorrect password.")
            messages.error(request, "Invalid email or password.")
            return redirect("/login")

    return redirect("/login")  # Redirect if accessed via GET request

def logout(request):
    try:
        del request.session["user_id"]
        del request.session["log_username"]
        del request.session["log_email"]
        del request.session["log_password"]

    except:
        pass

    return render(request,"index.html")


def shop(request):
    return render(request,"shop.html")


def showproductpage(request, category_id=None):
    fetchcategory = Category.objects.all()

    if category_id:  # If a category is selected, filter products by category
        selected_category = get_object_or_404(Category, id=category_id)
        fetchproducts = Product.objects.filter(cat_id=selected_category)  # Filter products
    else:  # Show all products if no category is selected
        fetchproducts = Product.objects.all()
        selected_category = None

    context = {
        "products": fetchproducts,  # Only selected category products
        "category": fetchcategory,
        "selected_category": selected_category
    }
    return render(request, "shop.html",context)

def singleproductpage(request):
    # print(user_id)
    # fetchdata = Product.objects.get(id=user_id)
    # context = {
    #     "data":fetchdata
    # }
    return render(request,"single-product.html")

def customizationpage(request):
    return render(request,"customization.html")

from decimal import Decimal, InvalidOperation


def fetchcustomizedata(request):
    print("Session Data:", request.session.items())  # Debugging session data

    userid = request.session.get("user_id")
    if not userid:
        messages.error(request, "User session expired. Please log in again.")
        return redirect("/login")

    if request.method == "POST":
        image = request.FILES.get("customize_img")
        details = request.POST.get("customize_details")
        budget = request.POST.get("budget")
        status = request.POST.get("status")  # Expecting from form, default False if missing

        if not details or not budget:
            messages.error(request, "Customization details and budget are required.")
            return render(request, "customization.html")

        try:
            budget_cleaned = budget.replace(",", ".")  # Convert 1,000.50 to 1000.50 if needed
            budget12 = Decimal(budget_cleaned)         # Now safely convert to Decimal
            print("Budget:", budget12, type(budget12))  # Debug print
        except (ValueError, InvalidOperation):
            messages.error(request, "Invalid budget value.")
            return render(request, "customization.html")

        status_value = "Pending"  # Default when user submits

        # status_value = bool(int(status)) if status else False  # Convert status to boolean

        # Save the customization
        insertquery = CustomizeProduct(
            customize_img=image,
            customize_details=details,
            budget=budget12,
            status=status_value,
            user_id=Userlogin(id=userid)
        )
        insertquery.save()

        print("Customization Saved:", insertquery.id, insertquery.customize_details, insertquery.budget, insertquery.status)
        saved = CustomizeProduct.objects.get(id=insertquery.id)
        print("Saved From DB:", saved.status)  # This must print False

        messages.success(request, "Customization saved successfully!")
        return redirect("/customization")

    return render(request, "customization.html")

def contactuspage(request):
    return render(request,"contact-us.html")

def fetchcontactusdata(request):
    if request.method == "POST":
        name = request.POST.get("contactus_name")
        email = request.POST.get("contactus_email")
        phone = request.POST.get("contactus_phone")
        message = request.POST.get("contactus_message")

        insertquery = contactusmodel(
            contactus_name=name,
            contactus_email=email,
            contactus_phone=phone,
            contactus_message=message
        )
        insertquery.save()
        messages.success(request, "Your message has been sent successfully!")

    return render(request, "contact-us.html")


def showcontactusdata(request):
    all_contacts = contactusmodel.objects.all()
    return render(request, "admin/show_contact_us.html", {"contacts": all_contacts})

def add_inventory(request):
    allproducts = Product.objects.all()
    allsupplier = Supplier.objects.all()
    if request.method == "POST":
        stock_quantity = request.POST.get("stocks")
        product_id = request.POST.get("product_id")
        supplier_id = request.POST.get("supplier_id")
        # Validate inputs
        Inventory.objects.create(stock_quantity=stock_quantity, product_id=Product.objects.get(id=product_id), supplier_id=Supplier.objects.get(id=supplier_id))
        return redirect(manage_inventory)  # Change "task_list" to your actual task list view name

    context = {
        "products": allproducts,
        "supplier": allsupplier
    }
    return render(request, "admin/add_inventory.html", context)


def add_task(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        employee_id = request.POST.get("employee_id")

        order = RazorpayPayment.objects.get(id=order_id)
        employee = Employee.objects.get(id=employee_id)

        Assign_Task.objects.create(order_id=order, employee_id=employee)
        return redirect("show_task")  # Change "show_task" to your actual task list view name

    context = {
        "orders": RazorpayPayment.objects.all(),
        "employees": Employee.objects.all(),
    }
    return render(request, "admin/add_task.html", context)


def add_supplier(request):
    if request.method == "POST":
        name = request.POST.get("name")
        conc = request.POST.get("conc")
        addr = request.POST.get("addr")

        Supplier.objects.create(name=name, contact_info=conc, shop_address=addr)
        return redirect(manage_supplier)  # Change "task_list" to your actual task list view name

    return render(request, "admin/add_supplier.html")


# Define admin users by email ID
ADMIN_EMAILS = ["ritz12@gmail.com","admin@gmail.com"]


def show_task(request):
    # Check if an employee is logged in via session
    employee_id = request.session.get("employee_id")

    # Check if an admin is logged in via Django authentication
    if request.user.is_authenticated:  #  Admins are authenticated via Django's system
        is_admin = request.user.username in ADMIN_EMAILS  # Admins use usernames, not email_id

        if is_admin:
            tasks = Assign_Task.objects.all()
            print("Session Data:", request.session.items())  # Debugging
            return render(request, "admin/show_task.html", {"tasks": tasks, "is_admin": is_admin})

    # If employee is logged in, fetch tasks
    if employee_id:
        try:
            employee = Employee.objects.get(id=employee_id)
            tasks = Assign_Task.objects.filter(employee_id=employee)

            return render(request, "admin/show_task.html", {"tasks": tasks, "is_admin": False})
        except Employee.DoesNotExist:
            messages.error(request, "Invalid session. Please log in again.")
            return redirect("emp_login")

    # Redirect unauthenticated users
    messages.error(request, "You must log in first.")
    return redirect("emp_login")


def edit_inventory(request, inv_id):
    task = get_object_or_404(Inventory, id=inv_id)
    if request.method == "POST":
        stock = request.POST.get("stock")

        task.stock_quantity = stock
        task.save()
        return redirect(manage_inventory)

    return render(request, "admin/edit_inventory.html",
                  {"task": task})


def delete_inventory(request, inv_id):
    task = get_object_or_404(Inventory, id=inv_id)
    task.delete()
    return redirect(manage_inventory)

def edit_supplier(request, sup_id):
    task = get_object_or_404(Supplier, id=sup_id)
    if request.method == "POST":
        name = request.POST.get("name")
        conc = request.POST.get("conc")
        addr = request.POST.get("addr")

        task.name = name
        task.contact_info = conc
        task.shop_address = addr
        task.save()
        return redirect(manage_supplier)

    return render(request, "admin/edit_supplier.html",
                  {"task": task})


def delete_supplier(request, sup_id):
    task = get_object_or_404(Supplier, id=sup_id)
    task.delete()
    return redirect(manage_supplier)


def edit_task(request, task_id):
    task = get_object_or_404(Assign_Task, id=task_id)
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        employee_id = request.POST.get("employee_id")
        rent_id = request.POST.get("rent_id")

        task.order_id = finalorders.objects.get(id=order_id)
        task.employee_id = Employee.objects.get(id=employee_id)
        task.rent_id = RentOrder.objects.get(id=rent_id)
        task.save()
        return redirect("show_task")

    orders = finalorders.objects.all()
    employees = Employee.objects.all()
    rents = RentOrder.objects.all()
    return render(request, "admin/edit_task.html",
                  {"task": task, "orders": orders, "employees": employees, "rents": rents})


def delete_task(request, task_id):
    task = get_object_or_404(Assign_Task, id=task_id)
    task.delete()
    return redirect("show_task")


def update_task_status(request, task_id):
    task = get_object_or_404(Assign_Task, id=task_id)

    if request.method == "POST":
        task_status = request.POST.get("task_status")
        task.task_status = task_status
        task.save()
        return redirect("show_task")  # Redirect to the task list page

    context = {
        "task": task,
        "task_status_choices": Assign_Task.Task_STATUS_CHOICES,
    }
    return render(request, "admin/update_task.html", context)



def update_order_status(request, task_id):
    task = get_object_or_404(Assign_Task, id=task_id)

    if request.method == "POST":
        new_status = request.POST.get("order_status")
        task.order_status = new_status
        task.save()
        messages.success(request, "Order status updated successfully!")
        return redirect("show_task")

    return render(request, "admin/update_order_status.html", {"task": task})


def emp_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = Employee.objects.get(email_id=email)

            # If passwords are hashed, use check_password instead of direct comparison
            if user.password == password:
                request.session["employee_id"] = user.id
                request.session["is_admin"] = user.email_id in ADMIN_EMAILS  # Store admin status in session

                if request.session["is_admin"]:
                    return redirect("show_user")  # Redirect admin to admin panel
                else:
                    return redirect("show_task")  # Redirect employees to their task page

            else:
                messages.error(request, "Invalid email or password")

        except Employee.DoesNotExist:
            messages.error(request, "Invalid email or password")

    return render(request, "admin/emp_login.html")


def emp_logout(request):
    is_admin = request.session.get("is_admin", False)  # Get admin status

    request.session.flush()  # Clear session

    if is_admin:
        return redirect("admin_logout")  # Redirect admins properly
    else:
        return redirect("emp_login")  # Redirect employees

def show_delivery(request):
    deliveries=RentOrder.objects.filter(delivery_person__isnull=False)
    return render(request, 'admin/show_delivery.html', {'deliveries': deliveries})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def update_delivery_status(request, order_id):
    if request.method == "POST":
        try:
            rent_order = RentOrder.objects.get(id=order_id)
            rent_order.status = "Delivered"
            rent_order.save()
            return JsonResponse({"success": True})
        except RentOrder.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order not found"})
    
    return JsonResponse({"success": False, "error": "Invalid request"})

def insertintocart(request):
    if request.method == "POST":
        # Check login first
        userid = request.session.get("user_id")
        if not userid:
            messages.warning(request, "Please login to add items to your cart.")
            return redirect("login")

        quantity = request.POST.get("quantity")
        pid = request.POST.get("id")
        price = request.POST.get("product_price")
        totalamount = float(price) * int(quantity)

        insertquery = cart(
            userid=Userlogin(id=userid),
            productid=Product(id=pid),
            quantity=quantity,
            totalamount=totalamount,
            orderstatus=0,
            orderid=0
        )

        insertquery.save()
        messages.success(request, "Item added to cart.")
        return redirect("showcart")

    # Optional: handle non-POST requests
    return redirect("shop_home")  # or wherever you want to go if someone opens this URL directly


razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))


def yourcustomization(request):
    userid = request.session.get("user_id")

    # Fetch all customized products for the user
    custom_products = CustomizeProduct.objects.filter(user_id=userid).prefetch_related("razorpaypayment_set")

    for product in custom_products:
        # Check if a payment exists and is marked as "Paid"
        product.is_paid = product.razorpaypayment_set.filter(status="Paid").exists()

    for product in custom_products:
        print(f"Debug - ID: {product.id} | Status: '{product.status}'")

    context = {
        "custom_products": custom_products
    }
    return render(request, "myrequests.html", context)


def rent_history(request):
    userid = request.session.get("user_id")  # Get the logged-in user's ID

    # Fetch all rental orders for the user
    rent_orders = RentOrder.objects.filter(user_id=userid).select_related("product_id")

    context = {
        "rent_orders": rent_orders
    }
    return render(request, "myrents.html", context)


def yourorders(request):
    userid = request.session.get("user_id")

    # Get all orders placed by the user
    Allorders = finalorders.objects.filter(u_id_id=userid).order_by("-o_date")  # Latest orders first

    # Prepare order data with associated cart items
    orders_with_items = []
    for order in Allorders:
        order_items = OrderItems.objects.filter(order=order)  # Get items from OrderItems
        payment = FinalOrderPayment.objects.filter(o_id=order).first()

        orders_with_items.append({
            "order": order,
            "items": order_items,
            "payment": payment
        })

    context = {
        "orders_with_items": orders_with_items
    }
    return render(request,"userorders.html",context)

def checkout(request):
    userid =  request.session["user_id"]
    print("Session User ID:", userid)  # Debugging
    if not userid:
        messages.error(request, "Please log in to view your cart.")
        return redirect("login")
    fetchdata = cart.objects.filter(userid=userid, orderstatus=0,orderid=0)
    total_cart_amount = fetchdata.aggregate(Sum("totalamount"))["totalamount__sum"] or 0
    print(fetchdata)
    print("Total Cart Amount:", total_cart_amount)
    total_amount_paise = int((total_cart_amount+50) * 100)

    razorpay_order = razorpay_client.order.create({
        "amount": total_amount_paise,
        "currency": "INR",
        "payment_capture": 1
    })

    context = {
        "cart_items": fetchdata,
        "cart_count": fetchdata.count(),
        "total_cart_amount": total_cart_amount,
        "grand_cart_amount": total_cart_amount+50,
        "razorpay_order_id": razorpay_order["id"],
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
    }
    return render(request,"checkout.html",context)

def update_payment_status(request):
    if request.method == "POST":
        data = json.loads(request.body)
        order_id = data.get("order_id")
        payment_id = data.get("payment_id")

        try:
            payment = RazorpayPayment.objects.get(order_id=order_id)
            payment.payment_id = payment_id
            payment.status = "Paid"
            payment.save()
            return JsonResponse({"message": "Payment status updated successfully."})
        except RazorpayPayment.DoesNotExist:
            return JsonResponse({"error": "Payment record not found."}, status=404)


def payment_success(request):
    if request.method == "POST":
        user_id = request.session.get("user_id")
        razorpay_order_id = request.POST.get("razorpay_order_id")

        try:
            # Calculate total cart amount
            total_amount = cart.objects.filter(userid=user_id, orderstatus=0, orderid=0).aggregate(Sum("totalamount"))["totalamount__sum"] or 0

            # Create a new final order
            new_order = finalorders.objects.create(
                u_id_id=user_id,
                status="Completed",
                total_amount=total_amount
            )

            # Copy cart items to OrderItems table
            cart_items = cart.objects.filter(userid=user_id, orderstatus=0, orderid=0)
            for item in cart_items:
                OrderItems.objects.create(
                    order=new_order,
                    product=item.productid,
                    quantity=item.quantity,
                    price=item.totalamount
                )

            # Update cart items with order ID and mark them as ordered
            cart_items.update(
                orderid=new_order.id,
                orderstatus=1
            )

            # (Optional) Delete cart items
            cart_items.delete()

            # Store Razorpay payment details
            FinalOrderPayment.objects.create(
                u_id_id=user_id,
                o_id=new_order,
                payment_type="online",
                amount=total_amount,
                razorpay_order_id=razorpay_order_id,
                status="Paid"
            )

            messages.success(request, "Payment successful! Your order has been placed.")
            return redirect("/yourorders")

        except Exception as e:
            print("Payment processing error:", e)
            messages.error(request, "There was an error while processing your payment. Please try again.")

    return redirect("/yourorders")


from django.db.models import Sum, Prefetch


def showcart(request):
    userid =  request.session["user_id"]
    print("Session User ID:", userid)  # Debugging
    if not userid:
        messages.error(request, "Please log in to view your cart.")
        return redirect("login")
    fetchdata = cart.objects.filter(userid=userid, orderstatus=0,orderid=0)
    total_cart_amount = fetchdata.aggregate(Sum("totalamount"))["totalamount__sum"] or 0 
    print(fetchdata)
    print("Total Cart Amount:", total_cart_amount) 
    context = {
        "cart_items": fetchdata,
        "cart_count": fetchdata.count(),
        "total_cart_amount": total_cart_amount,
    }
    return render(request, "cart.html",context)


def update_cart_quantity(request, item_id, action):
    cart_item = get_object_or_404(cart, id=item_id)

    if action == "increase":
        cart_item.quantity += 1
    elif action == "decrease":
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete()  # If quantity becomes 0, remove item from cart
            return redirect("showcart")  # Redirect to cart page

    cart_item.totalamount = cart_item.quantity * cart_item.productid.product_price
    cart_item.save()

    return redirect("showcart")  # Refresh cart page after update

def deletefromcart(request, cart_id):
    cart_item = cart.objects.get(id=cart_id)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect("showcart")

def cart_view(request):
    user_id = request.session.get("user_id")  # Ensure session user ID exists
    print("Session User ID:", user_id)

    if not user_id:
        messages.error(request, "Please log in to view your cart.")
        return redirect("login")

    cart_items = cart.objects.filter(userid=user_id, orderstatus=1)
    cart_count = cart_items.count()

    # Debugging: Print data
    print("Cart Items in View:", cart_items)

    context = {
        'cart_items': cart_items,
        'cart_count': cart_count
    }
    return {
        'cart_items': cart_items,
        'cart_count': cart_count
    }

def singleproductpage(request, id):
    fetchdata = get_object_or_404(Product, id=id)  # Handles invalid IDs properly
    context = {"data": fetchdata}
    return render(request, "single-product.html", context)

def rent_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        start_date_str = request.POST.get("start_date")
        end_date_str = request.POST.get("end_date")
        rent_deposit_str = request.POST.get("rent_deposit")

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect("rent_product", product_id=product.id)

        if start_date >= end_date:
            messages.error(request, "End date must be after the start date.")
            return redirect("rent_product", product_id=product.id)

        # Rent Calculation
        rental_days = (end_date - start_date).days
        total_rent = product.rent_per_day * rental_days

        # Backend validation for Rent Deposit (Half of Product Price)
        expected_rent_deposit = product.product_price / 2

        try:
            rent_deposit = float(rent_deposit_str)
            if rent_deposit != expected_rent_deposit:
                messages.error(request, f"Invalid rent deposit amount. It should be ₹{expected_rent_deposit:.2f}")
                return redirect("rent_product", product_id=product.id)
        except ValueError:
            messages.error(request, "Invalid rent deposit value.")
            return redirect("rent_product", product_id=product.id)

        # Create Rent Order
        RentOrder.objects.create(
            product=product,
            user=request.user,
            start_date=start_date,
            end_date=end_date,
            rent_deposit=rent_deposit,
            rent_amount=total_rent,
            return_status="Pending"
        )

        messages.success(request, "Rental confirmed successfully!")
        return redirect("rental_success")

    return render(request, "rent.html", {"product": product})


def fetch_rental_data(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")  # Get product_id from request
        rent_orders = RentOrder.objects.filter(product_id=product_id)

        data = list(rent_orders.values("id", "start_date", "end_date", "rent_amount", "return_status"))
        return JsonResponse({"rental_data": data})

    return JsonResponse({"error": "Invalid request"}, status=400)

import json

def create_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            amount = int(float(data.get("amount")) * 100)
            custom_id = data.get("custom_id")
            user_id = request.session.get("user_id")

            if not all([amount, custom_id, user_id]):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            razorpay_order = razorpay_client.order.create({
                "amount": amount,
                "currency": "INR",
                "payment_capture": "1"
            })

            RazorpayPayment.objects.create(
                user=Userlogin.objects.get(id=user_id),
                custom_product=CustomizeProduct.objects.get(id=custom_id),
                order_id=razorpay_order["id"],
                amount=data["amount"],
                status="Pending"
            )

            return JsonResponse({
                "order_id": razorpay_order["id"],
                "amount": amount,
                "key_id": settings.RAZORPAY_KEY_ID
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from reportlab.lib import colors

def generate_orders_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="orders_report.pdf"'

    # Get start_date and end_date from request
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Validate date inputs
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        return HttpResponse("Invalid date format. Please use YYYY-MM-DD.", status=400)

    # Fetch orders within the given date range
    orders = finalorders.objects.filter(o_date__range=[start_date, end_date])

    # Create PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Add Logo (Adjust path accordingly)
    logo_path = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'img', 'logo.png')
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=120, height=70)
        elements.append(logo)

    # Title
    title = Table([["Crafted Elegance - Order Report"]], colWidths=[500])
    title.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ]))
    elements.append(title)

    # Table Header
    data = [["Order ID", "User ID", "Order Date", "Status", "Total Amount", "Product Name", "Quantity"]]
    span_styles = []  # Store rowspan styles separately
    current_row = 1  # Start from the first data row

    # Construct table with correct rowspan logic
    for order in orders:
        cart_items = OrderItems.objects.filter(order=order)
        row_span = len(cart_items)  # Number of rows to merge for order details

        for index, item in enumerate(cart_items):
            product_name = item.product.product_name if item.product else "N/A"
            quantity = item.quantity

            if index == 0:  # First row for the order (apply rowspan)
                data.append([
                    str(order.id),
                    str(order.u_id.id),
                    str(order.o_date),
                    order.status,
                    f"Rs. {order.total_amount}",
                    product_name,
                    quantity
                ])
                # Store rowspan styles with correct row indexes
                span_styles.extend([
                    ('SPAN', (0, current_row), (0, current_row + row_span - 1)),  # Order ID
                    ('SPAN', (1, current_row), (1, current_row + row_span - 1)),  # User ID
                    ('SPAN', (2, current_row), (2, current_row + row_span - 1)),  # Order Date
                    ('SPAN', (3, current_row), (3, current_row + row_span - 1)),  # Status
                    ('SPAN', (4, current_row), (4, current_row + row_span - 1)),  # Total Amount
                ])
            else:  # Additional product rows for the same order
                data.append(["", "", "", "", "", product_name, quantity])

        current_row += row_span  # Update row index for next order

    # Create table with corrected rowspan styles
    table = Table(data, colWidths=[50, 50, 70, 70, 70, 220, 50])
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ] + span_styles))  # Add the corrected rowspan styles

    elements.append(table)
    doc.build(elements)

    return response

def fetch_rental_data(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        user_id = request.user.id  # Assuming user is authenticated
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        rent_deposit = float(request.POST.get("rent_deposit"))
        rent_amount = float(request.POST.get("rent_amount"))

        # Convert dates
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid date format")
            return redirect("rent_page")

        # Validate rental period
        if start_date >= end_date:
            messages.error(request, "End date must be after start date")
            return redirect("rent_page")

        # Fetch product details
        product = Product.objects.get(id=product_id)

        # Create Rent Order (Without Payment Confirmation Yet)
        rent_order = RentOrder.objects.create(
            product_id=product,
            user_id=Userlogin.objects.get(id=request.session["user_id"]),
            start_date=start_date,
            end_date=end_date,
            rent_deposit=rent_deposit,
            rent_amount=rent_amount,
            return_status="Pending",
        )

        # Create Razorpay Order
        total_payment = rent_deposit + rent_amount
        razorpay_order = razorpay_client.order.create({
            "amount": int(total_payment * 100),  # Amount in paise
            "currency": "INR",
            "payment_capture": "1"
        })

        # Store the Razorpay Order ID
        rent_order.razorpay_order_id = razorpay_order["id"]
        rent_order.save()

        # Redirect to payment page
        return render(request, "payment.html", {
            "order": rent_order,
            "razorpay_order_id": razorpay_order["id"],
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "amount": total_payment
        })

    return redirect("rent_page")

def update_rental_status(request, rent_order_id):
    if request.method == "POST":
        new_status = request.POST.get("status")
        rent_order = RentOrder.objects.get(id=rent_order_id)
        rent_order.status = new_status
        rent_order.save()
        messages.success(request, "Order status updated successfully")
    return redirect("rental_orders")


def rentpayment_success(request):
    order_id = request.GET.get("order_id")
    payment_id = request.GET.get("payment_id")

    rent_order = RentOrder.objects.get(id=order_id)
    rent_order.payment_status = "Paid"
    rent_order.razorpay_payment_id = payment_id
    rent_order.status = "Processing"
    rent_order.save()

    messages.success(request, "Payment successful! Your rental order is confirmed.")
    return redirect(indexpage)

def assign_delivery(request):
    if request.method == "POST":
        order_id = request.POST.get("rent_order_id")
        employee_id = request.POST.get("employee_id")

        rent_order = get_object_or_404(RentOrder, id=order_id)
        employee = get_object_or_404(Employee, id=employee_id)

        # Assign Employee & Update Status
        rent_order.delivery_person = employee  # Use the correct field name
        rent_order.status = "Assigned"  # Use `status` instead of `delivery_status`
        rent_order.save()

        return redirect(show_delivery)  # Redirect to delivery list page

    # Fetch Data
    rent_orders = RentOrder.objects.filter(delivery_person__isnull=True)  # Fetch all rent orders
    employees = Employee.objects.filter(role="Delivery Person")

    return render(request, "admin/assign_delivery.html", {"rent_orders": rent_orders, "employees": employees})


def generate_custom_orders_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="customized_orders_report.pdf"'

    # Get date range from request
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return HttpResponse("Invalid date format. Please use YYYY-MM-DD.", status=400)

    # Fetch customization orders
    custom_orders = CustomizeProduct.objects.filter(submitted_at__range=[start_date, end_date])

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Add Logo (optional)
    logo_path = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'img', 'logo.png')
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=120, height=70)
        elements.append(logo)

    # Title
    title = Table([["Crafted Elegance - Customized Order Report"]], colWidths=[500])
    title.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ]))
    elements.append(title)

    # Table headers
    data = [["User ID", "Details", "Budget", "Status", "Submitted At", "Image"]]

    for order in custom_orders:
        try:
            image_path = os.path.join(settings.MEDIA_ROOT, order.customize_img.name)
            if os.path.exists(image_path):
                img = Image(image_path, width=60, height=60)
            else:
                img = Paragraph("Image not found", styles['Normal'])
        except:
            img = Paragraph("Error loading image", styles['Normal'])

        # Use Paragraph for details to enable wrapping
        details_para = Paragraph(order.customize_details, styles['Normal'])

        data.append([
            str(order.user_id.id),
            details_para,
            f"Rs. {order.budget}",
            order.status or "Pending",
            order.submitted_at.strftime("%Y-%m-%d"),
            img
        ])

    # Adjusted column widths
    table = Table(data, colWidths=[50, 220, 70, 70, 80, 70], repeatRows=1)
    table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('FONTSIZE', (0, 0), (-1, -1), 9),  # Reduce font size if needed
    ]))

    elements.append(table)
    doc.build(elements)

    return response