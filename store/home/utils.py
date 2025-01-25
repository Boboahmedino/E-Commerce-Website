import json
from .models import *


'''
1) This function here is to reduce the large amount of code in the cart, checkout and shop page 
for an unauthenticated user

2) I will be doing it for only check out and shop but so i can rememeber and refer back to the
cart to understand how to do it and remember the root of the movement
'''
def cookieCart(request):
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
    return{'cartItems': cartItems, 'order': order , 'items' : items}



'''
i want to clear the data in views more since i already know how to link it up more
this time i will do it for the same checkout and shop so i can know how to do it in the future
'''

"""
everything here can be used in the both the shop function and the checkout function in the view
"""

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        #to display all child selected objects
        items = order.orderitem_set.all() 
        cartItems = order.get_cart_items
    else:
        # this uses the cookies in the utils.py to create the cart for an unauthenticated user
        # instead if copying the entire code in ther utils here
        cookieData =  cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

        # this creates an empty cart for non-logged in users withpout using cookies in utils.py
        # order = {'get_cart_total': 0,
        #          'get_cart_items': 0,
        #          'shipping': False,
        #         }
        # items = []
        # cartItems = order['get_cart_items']
    return{'cartItems': cartItems, 'order': order , 'items' : items}
