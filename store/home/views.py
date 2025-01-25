from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import JsonResponse
import json
import datetime
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponse



from .utils import cookieCart, cartData
# this is to reduce the try repition of code in the shop, cart and checkout page
# doing this will not allow the code on this page to be too bulky




def home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        # For unauthenticated users, check if cart cookie exists
        try:
            cart = json.loads(request.COOKIES.get('cart', '{}'))
        except json.JSONDecodeError:
            cart = {}

        cartItems = sum(item['quantity'] for item in cart.values()) if cart else 0

    context = {
        'cartItems': cartItems
    }
    return render(request, 'home/home.html', context)


def shop(request):
    data = cartData(request)
    cartItems= data['cartItems']
   
    # products = Product.objects.all() 
    products = Product.objects.all().order_by('id')  # Order by 'id' or any other field(i did this for pagination)
    
    # for pagination
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'products': products,
        'cartItems' : cartItems,
        'page_obj': page_obj,

    }
    return render(request, 'home/shop.html', context)


def shop_detail(request, product_id):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        # For unauthenticated users, check if cart cookie exists
        try:
            cart = json.loads(request.COOKIES.get('cart', '{}'))
        except json.JSONDecodeError:
            cart = {}

        cartItems = sum(item['quantity'] for item in cart.values()) if cart else 0

        # Retrieve the product with the given ID or return a 404 error if not found
    product = get_object_or_404(Product, id=product_id)

    context = {
        'product' :product,
        'cartItems': cartItems

    }
    return render(request, 'home/shop_detail.html', context)

 
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
    #to display all child selected objects
        items = order.orderitem_set.all() 
        cartItems = order.get_cart_items

        # for unauthenticated user
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}

        print('Cart:', cart)
        # this creates an empty cart for non-logged in users
        items = []
        order = {'get_cart_total': 0,
                 'get_cart_items': 0,
                 'shipping': False,
                }
        cartItems = order['get_cart_items']

        for i in cart:
            # try here was used to prevent items in the cart that may have been removed from causing error
            try:
                cartItems += cart[i]['quantity']

                product = Product.objects.get(id=i)
                total = (product.price * cart[i]['quantity'])

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']

                item = {
                    'product':{
                        'id' : product.id,
                        'name' : product.name,
                        'price' : product.price,
                        'imageURL' : product.imageURL,
                    },
                    'quantity': cart[i]['quantity'],
                    'get_total': total,
                }
                items.append(item)

                if product.digital == False:
                    order['shipping'] = True
            except:
                pass 

    context = {'items' : items,
               'order' : order,
               'cartItems' : cartItems
                }  

    return render(request, 'home/cart.html', context)
   

def updateitem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('ProductId:', productId)

    customer =request.user.customer
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer = customer, complete = False)

    # if the ordered item exist we don't want to create a new one, we just want to add or subtract from it 
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    
    # if the ordered item is 0 remove it entirely
    if orderItem.quantity == 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
def processorder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        
        # this is to make sure authenticated users carted item is saved and the total is generated
        # total = float(data['form']['total'])
        # order.transaction_id = transaction_id

        # # this is to make sure the total of the user tallies with what is n the 
        # if total == order.get_cart_total:
        #     order.complete = True
        # order.save()

        # shipping info front end to the back end
        # if order.shipping == True:
        #     ShippingAddress.objects.create(
        #         customer = customer,
        #         order = order,
        #         address = data['shipping']['address'],
        #         city = data['shipping']['city'],
        #         state = data['shipping']['state'],
        #         zipcode = data['shipping']['zipcode'],
        #         country = data['shipping']['country'],
        #     )

    else:
        print("User is not logged in")
        messages.error(request, 'User not logged in')

        print('COOKIES:', request.COOKIES)
        name = data['form']['name']
        email = data['form']['email']
        phone_number = data['form']['phone_number']


        cookieData = cookieCart(request)
        items = cookieData['items']

        customer, created = Customer.objects.get_or_create(
            email = email,
        )

        customer.name = name
        customer.phone_number = phone_number
        customer.save()

        order = Order.objects.create(
            customer = customer,
            complete = False
        )

        for item in items:
            product = Product.objects.get(id = item['product']['id'])
            orderItem = OrderItem.objects.create(
                product = product,
                order = order,
                quantity = item['quantity']
            )
    
    # since i have created another statement to allow the unauthenticated users to use the cart 
    # the statemenmt below should be used for both unauth and auth users
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

        # this is to make sure the total of the user tallies with what is n the 
    if total == order.get_cart_total:
            order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
            country = data['shipping']['country'],
        )

    return JsonResponse('Payment complete!', safe = False)


def checkout(request):
    data = cartData(request)
    cartItems= data['cartItems']
    order= data['order']
    items= data['items']

    context = {'items' : items,
               'order' : order,
                'cartItems' : cartItems   
            }
    return render(request, 'home/checkout.html', context)


def error(request):
    return render(request, 'home/error.html')

from django.contrib.auth.decorators import login_required

@login_required(login_url='authentication/admin_user')
def dashboard(request):
    # Fetch all orders from the database
    orders = Order.objects.all().order_by('-id')

    # Fetch all customers (users) from the database
    customers = Customer.objects.all()

      # Add ShippingAddress to each order
    for order in orders:
        order.shipping_address = ShippingAddress.objects.filter(order=order).first()  # Add shipping address to the order

    # Prepare context data to send to the template
    context = {
        'orders': orders,
        'customers': customers,
        'is_superuser': request.user.is_superuser  # Check if the logged-in user is a superuser
    }

    # Render the custom HTML template with the context
    return render(request, 'home/dashboard.html', context)


def update_order_status(request, order_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        order = Order.objects.get(id=order_id)
        order.status = status
        order.save()
        return redirect('dashboard')  # Redirect back to the dashboard
    return HttpResponse("Invalid request", status=400)

def contact(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        # For unauthenticated users, check if cart cookie exists
        try:
            cart = json.loads(request.COOKIES.get('cart', '{}'))
        except json.JSONDecodeError:
            cart = {}

        cartItems = sum(item['quantity'] for item in cart.values()) if cart else 0

    context = {
        'cartItems': cartItems
    }

    return render(request, 'home/contact.html', context)