from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User 
from django.contrib import messages,auth
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from .models import *

def index(r):
    return render(r,'index.html')
def user(r):
    orders = Order.objects.filter(user=r.user).prefetch_related('items__product')  

    return render(r,'user.html', {'orders': orders})





def order_details_view(request, order_id):
    try:
        order = Order.objects.prefetch_related('items__product').get(pk=order_id, user=request.user)
        shipping_address = order.address  

        order_items_with_totals = []
        for item in order.items.all():  
            item_total = item.quantity * item.price  
            order_items_with_totals.append({
                'product': item.product,
                'quantity': item.quantity,
                'price': item.price,
                'total': item_total  
            })

        context = {
            'order': order,
            'order_items_with_totals': order_items_with_totals, 
            'shipping_address': shipping_address 
        }
        return render(request, 'userorderdetail.html', context)

    except Order.DoesNotExist:
        return redirect('user')

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')  
def cart(request):
    if request.user.is_authenticated:
        return render(request, 'cart.html')
    else:
        return redirect('login')  


from django.contrib import messages
from django.shortcuts import render

def login_view(request):
    messages.info(request, "Please log in to view your cart.")
    
    return render(request, 'login.html')

def checkout(r):
     return render(r,'checkout.html') 

def contact(r):
     return render(r,'contact.html') 
def shop_detail(r):
     return render(r,'shop_detail.html')
def shop(r):
     return render(r,'shop.html') 
def login(r):
     return render(r,'login.html')
def register(r):
     return render(r,'register.html')
def admin(r):
     return render(r,'admin.html', {'active_nav': 'admin'})
def add_product(r):
    return render(r,'add_product.html')
def product_list(request):
    user = request.user
    products = Product.objects.all()
    return render(request, 'admin.html', {'products': products, 'active_nav': 'products'})



from django.shortcuts import render
from .models import Product
from django.shortcuts import render
from .models import Product

def category_products_view(request, category):
    print("CATEGORY",category)
    if category == 'all':
        products = Product.objects.filter(is_active=True, is_deleted=False)
        print("Product in if",products)
    else:
        products = Product.objects.filter(category=category, is_active=True, is_deleted=False)
        print("Product",products)

    print("Product",products)
    return render(request, 'shop.html', {'products': products, 'category': category})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('firstName')
        password = request.POST.get('password')
        email = request.POST.get('email')
        role = request.POST.get('role')  

        if not username or not password or not email:
            messages.error(request, 'Please fill in all required fields')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'register.html')

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        if role == 'delivery_boy':
            license_photo = request.FILES.get('license_photo')
            rc_book_photo = request.FILES.get('rc_book_photo')

            if not license_photo or not rc_book_photo:
                messages.error(request, 'Please upload both license and RC book photos')
                return render(request, 'register.html')

            DeliveryBoy.objects.create(
                user=user,
                license_photo=license_photo,
                rc_book_photo=rc_book_photo,
                status='offline'
            )
            messages.success(request, 'Delivery Boy registration successful. Awaiting admin approval.')

        else:
            messages.success(request, 'User registration successful')

        return redirect('login')
    else:
        return render(request, 'register.html')


from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import DeliveryBoy  
from django.contrib import auth, messages

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if hasattr(user, 'deliveryboy'):
                if user.deliveryboy.status == 'offline':
                    messages.error(request, 'Your account is awaiting admin approval.')
                    return render(request, 'login.html')

            auth.login(request, user)
            if user.is_superuser:
                return redirect('blank')
            else:
                return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')



def logout(request):
    request.session.flush()
    return redirect('login')
def user_management(request):
    obj = User.objects.filter(is_staff=False, is_superuser=False)
    return render(request, 'admin.html', {'values': obj, 'active_nav': 'users'})
def product_management(request):
    products = Product.objects.all()  
    return render(request, 'admin.html', {'products': products, 'active_nav': 'products'})
from django.shortcuts import render, get_object_or_404, redirect
from .models import Order

def order_management(request):
    orders = Order.objects.prefetch_related('items__product', 'address').all()  
    return render(request, 'admin.html', {'orders': orders, 'active_nav': 'orders'})

from .models import DeliveryAssignment

def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    delivery_boys = DeliveryBoy.objects.filter(status='available')  
    assignment = DeliveryAssignment.objects.filter(order=order).first() 
    if request.method == 'POST':
        new_status = request.POST.get('status')
        delivery_boy_id = request.POST.get('delivery_boy') 
        if new_status in ['pending', 'shipped', 'delivered', 'canceled']:
            order.status = new_status
        
        if delivery_boy_id:
            delivery_boy = DeliveryBoy.objects.get(id=delivery_boy_id)
            if assignment:  
                assignment.delivery_boy = delivery_boy
                assignment.save()
            else:  
                DeliveryAssignment.objects.create(order=order, delivery_boy=delivery_boy)
        
        order.save()
        return redirect('order_details', order_id=order_id) 

    return render(request, 'order_details.html', {
        'order': order,
        'delivery_boys': delivery_boys,  
        'assignment': assignment  
    })



def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        order.delete()
        return redirect('order_management') 
    return render(request, 'order_confirm_delete.html', {'order': order})

from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DeliveryBoy, Order  

@login_required
def delivery_boy_management(request):
    """View to display all delivery boys."""
    delivery_boys = DeliveryBoy.objects.all()
    return render(request, 'admin.html', {
        'delivery_boys': delivery_boys,
        'active_nav': 'delivery_boys',  
    })

@login_required
def update_delivery_boy(request, delivery_boy_id):
    """View to update the status of a delivery boy."""
    delivery_boy = get_object_or_404(DeliveryBoy, id=delivery_boy_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['offline', 'available', 'on_route']:
            delivery_boy.status = new_status
            delivery_boy.save()
            return redirect('delivery_boy_management')  
    return render(request, 'admin.html', {
        'active_nav': 'delivery_boys',
        'delivery_boy': delivery_boy,
    })

@login_required
def delete_delivery_boy(request, delivery_boy_id):
    """View to delete a delivery boy."""
    delivery_boy = get_object_or_404(DeliveryBoy, id=delivery_boy_id)
    if request.method == 'POST':
        delivery_boy.delete()
        return redirect('delivery_boy_management')  

    return render(request, 'admin.html', {
        'delivery_boy': delivery_boy,
        'active_nav': 'delivery_boys',
        'deletion_confirmation': True 
    })
from django.shortcuts import render, get_object_or_404, redirect
from .models import DeliveryAssignment, Order
from django.contrib.auth.decorators import login_required

@login_required
def delivery_boy_dashboard(request):
    delivery_boy = get_object_or_404(DeliveryBoy, user=request.user)

    assigned_orders = DeliveryAssignment.objects.filter(delivery_boy=delivery_boy).select_related('order')

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        
        order = get_object_or_404(Order, id=order_id)
        assignment = get_object_or_404(DeliveryAssignment, order=order, delivery_boy=delivery_boy)
        
        if new_status in ['shipped', 'on_route', 'delivered']:
            order.status = new_status
            order.save()

        return redirect('delivery_boy_dashboard') 

    return render(request, 'delivery.html', {'assigned_orders': assigned_orders})

@login_required
def update_order_status(request, order_id):
    delivery_boy = get_object_or_404(DeliveryBoy, user=request.user)
    order = get_object_or_404(Order, id=order_id)

    assignment = get_object_or_404(DeliveryAssignment, order=order, delivery_boy=delivery_boy)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['shipped', 'on_route', 'delivered']:
            order.status = new_status
            order.save()

            messages.success(request, f"The status of order {order.id} has been updated to '{new_status}' by {delivery_boy.user.username}.")
            

            return redirect('delivery_boy_dashboard')  

    return render(request, 'order_status_update.html', {'order': order})





@login_required
def view_delivery_boy_orders(request, delivery_boy_id):
    """View to display all orders assigned to a specific delivery boy."""
    delivery_boy = get_object_or_404(DeliveryBoy, id=delivery_boy_id)
    orders = Order.objects.filter(delivery_boy=delivery_boy)  
    return render(request, 'admin.html', {
        'delivery_boy': delivery_boy,
        'orders': orders,
        'active_nav': 'delivery_boys',
    })
from django.shortcuts import render, get_object_or_404

@login_required
def view_delivery_boy_details(request, delivery_boy_id):
    """View to display details of a specific delivery boy."""
    delivery_boy = get_object_or_404(DeliveryBoy, id=delivery_boy_id)
    
    return render(request, 'viewdetails.html', {
        'delivery_boy': delivery_boy,
    })


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            print('fst ex1',e)
            messages.info(request,"Email id not registered")
            return redirect(forgot_password)
        
        token = get_random_string(length=4)
        PasswordReset.objects.create(user=user, token=token)

        
        reset_link = f'http://127.0.0.1:8000/reset/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}','settings.EMAIL_HOST_USER', [email],fail_silently=False)
            
            messages.success(request, "Password reset  email sent successfully. Please check your inbox.")
        except Exception as e:
            print(e)
            messages.info(request,"Failed to send password reset email. Please try again later.")
            return redirect(forgot_password)

    return render(request, 'forgot_password.html')
def reset_password(request, token):
    print(token)
    password_reset = PasswordReset.objects.get(token=token)
    usr = User.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            password_reset.user.set_password(new_password)
            password_reset.user.save()
            
            return redirect(login)
    return render(request, 'reset_password.html',{'token':token})

def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category=request.POST.get('category')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')
        product = Product.objects.create(
            name=name,
            description=description,
            category=category,
            price=price,
            stock=stock,
            image=image,
        )

        return redirect('product_list')  
    else:
        categories = Product.CATEGORY_CHOICES
        return render(request, 'add_product.html', {'categories': categories})

def detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if not product.is_active or product.is_deleted:
        return render(request, 'product_not_found.html')

    
    return render(request, 'shop_detail.html', {'product': product})

def add_to_cart(request, product_id):
    if request.user.is_authenticated:  
        if Product.objects.filter(id=product_id).exists():
            product = Product.objects.get(id=product_id)

            if CartItem.objects.filter(product=product, user=request.user).exists():
                cart_item = CartItem.objects.get(product=product, user=request.user)
                cart_item.quantity += 1
                cart_item.save()
                messages.success(request, f'Updated quantity of {product.name} in your cart.')
            else:
                CartItem(product=product, quantity=1, user=request.user).save()
                messages.success(request, f'Added {product.name} to your cart.')

            return redirect(request.META.get('HTTP_REFERER', 'shop'))  
        else:
            messages.error(request, 'Product not found.')
            return redirect(request.META.get('HTTP_REFERER', 'shop'))  
    else:
        messages.warning(request, 'Please log in to add items to your cart.')
        return redirect('login')  

def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    try:
        cart_item = CartItem.objects.get(user=request.user, product__id=product_id)
        cart_item.delete()
        messages.success(request, f'Removed {product.name} from your cart')
    except CartItem.DoesNotExist:
        messages.error(request, 'Product not in cart.')

    return redirect('cart')  

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CartItem

def cart_detail(request):
    if not request.user.is_authenticated:
        messages.info(request, "Please log in to view your cart.")
        return redirect('login')   
    
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')

    if not cart_items:
        return render(request, 'cart.html', {'empty_cart': True})  

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        if quantity < 1:
            quantity = 1

        try:
            cart_item = CartItem.objects.get(user=request.user, product_id=product_id)
            product = cart_item.product  

            if quantity > product.stock:
                messages.error(request, f"Cannot add {quantity}. Only {product.stock} available.")
                return redirect('cart')  

            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully.')
        except CartItem.DoesNotExist:
            messages.error(request, 'Product not found in cart.')
            
        return redirect('cart')  

    item_totals = []
    total_amount = 0
    for item in cart_items:
        total_price = item.product.price * item.quantity
        item_totals.append({'item': item, 'total_price': total_price})
        total_amount += total_price

    return render(request, 'cart.html', {'item_totals': item_totals, 'total_amount': total_amount})


def update_cart(request):
    if request.method == "POST":
        error_occurred = False  

        for item_id, quantity in request.POST.items():
            if item_id != 'csrfmiddlewaretoken':  
                try:
                    item_id = int(item_id)

                    cart_item = CartItem.objects.get(id=item_id, user=request.user)

                    product = cart_item.product

                    requested_quantity = int(quantity)

                    if requested_quantity < 1:
                        raise ValueError("Quantity must be at least 1.")

                    if requested_quantity > product.stock:  
                        messages.error(request, f"Cannot add {requested_quantity} of {product.name}. Only {product.stock} available.")
                        error_occurred = True
                    else:
                        cart_item.quantity = requested_quantity
                        cart_item.save()

                except CartItem.DoesNotExist:
                    messages.error(request, "Cart item not found.")
                    error_occurred = True  
                except ValueError as e:
                    messages.error(request, str(e))
                    error_occurred = True  

        if not error_occurred:
            messages.success(request, "Cart updated successfully.")

    return redirect('cart')  
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .models import CartItem, Order, OrderItem, Address  
import razorpay

def checkout(request):
    user = request.user

    try:
        address = Address.objects.get(user=user)
    except Address.DoesNotExist:
        address = None  

    cart_items = CartItem.objects.filter(user=user).select_related('product')

    total_price = 0
    for item in cart_items:
        item.total_price = item.product.price * item.quantity  
        total_price += item.total_price  

    if request.method == 'POST':
        billing_name = request.POST.get('billing_name')
        billing_street = request.POST.get('billing_street')
        billing_city = request.POST.get('billing_city')
        billing_postcode = request.POST.get('billing_postcode')
        billing_phone = request.POST.get('billing_phone')

        if address:
            address.name = billing_name
            address.street = billing_street
            address.city = billing_city
            address.postcode = billing_postcode
            address.phone = billing_phone
            address.save()
        else:
            address = Address.objects.create(
                user=user,
                name=billing_name,
                street=billing_street,
                city=billing_city,
                postcode=billing_postcode,
                phone=billing_phone,
            )

        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                address=address,
                total_amount=total_price
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

                product = item.product
                product.stock -= item.quantity  
                product.save()  

                if product.stock <= 2:
                    subject = f"Low Stock Alert: {product.name}"
                    message = f"The stock for {product.name} is running low. Only {product.stock} left!"
                    admin_email = settings.ADMIN_EMAIL  

                    send_mail(
                        subject,
                        message,
                        settings.EMAIL_HOST_USER,  
                        [admin_email],  
                        fail_silently=False,
                    )

            return redirect('payment', order_id=order.id)  

    context = {
        'address': address,
        'cart_items': cart_items,  
        'total_price': total_price,  
    }
    return render(request, 'checkout.html', context)

from django.shortcuts import render, redirect
from django.conf import settings
from .models import Order
import razorpay

def payment(request, order_id):
    order = Order.objects.get(id=order_id)
    client = razorpay.Client(auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))

    razorpay_order = client.order.create({
        'amount': int(order.total_amount * 100),  
        'currency': 'INR',
        'payment_capture': '1'
    })

    order.razorpay_order_id = razorpay_order['id']
    order.save()

    context = {
        'order': order,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_merchant_key': 'rzp_test_SROSnyInFv81S4',
        'amount': order.total_amount,  
        'currency': 'INR'
    }

    return render(request, 'payment.html', context)

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order, CartItem

def razorpay_success(request):
    if request.method == "POST":
        razorpay_order_id = request.POST.get('razorpay_order_id')
        payment_id = request.POST.get('razorpay_payment_id')

        try:
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
        except Order.DoesNotExist:
            messages.error(request, "Order not found")
            return redirect('checkout')

        order.status = 'paid'
        order.save()

        CartItem.objects.filter(user=order.user).delete()

        return render(request, 'payment_success.html', {
            'order': order,
            'payment_id': payment_id
        })

    return redirect('checkout')

    
from django.core.mail import send_mail
from django.conf import settings

def send_low_stock_email(product):
    subject = f"Low Stock Alert: {product.name}"
    message = f"The stock for {product.name} is running low. Only {product.stock} left!"
    
    admin_email = settings.ADMIN_EMAIL 

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,  
        [admin_email],  
        fail_silently=False,
    )





def display(request):
    products = Product.objects.filter(is_active=True, is_deleted=False)

    cart_items = []
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user).values_list('product_id', flat=True)

    return render(request, 'shop.html', {
        'products': products,
        'cart_items': cart_items,
        'active_nav': 'products'
    })




 




        
from django.shortcuts import render, redirect, get_object_or_404


def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')
        if name and description and price and stock:
            try:
                product.name = name
                product.description = description
                product.price = float(price)
                product.stock = int(stock)
                if image:
                    product.image = image
                product.save() 
                return redirect('product_management')  
            except ValueError:
                return HttpResponse('Invalid price or stock value.', status=400)
        else:
            return HttpResponse('All fields are required.', status=400)

    return render(request, 'edit_product.html', {'product': product})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_management')  
    return render(request, 'confirm_delete.html', {'product': product})



def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
        return redirect('user_management')
    else:
        return render(request, 'user_edit.html', {'user': user})

def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_management')
    return render(request, 'confirm_delete_user.html', {'user': user})


