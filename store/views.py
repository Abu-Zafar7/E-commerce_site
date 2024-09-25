from django.shortcuts import render
from .models import *
from django.http import HttpResponseBadRequest, JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder
import razorpay
from django.views.decorators.csrf import csrf_exempt
from secret_key import API_KEY, API_SECRET

def homepage(request):

    context = {}
    return render(request,'homepage.html', context)


def store(request):

   
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems, 'shipping': False}
    return render(request,'store.html', context)


def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems,'shipping': False}
    return render(request,'cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    # Set up Razorpay client with your API key and secret
    client = razorpay.Client(auth=(API_KEY, API_SECRET))

    # Convert the total amount to paisa (since Razorpay uses the smallest currency unit)
    amount = int(order.get_cart_total * 100)  # Convert INR to paisa

    # Create Razorpay order
    razorpay_order = client.order.create({
        'amount': amount,
        'currency': 'INR',
        'payment_capture': '1'  # Auto capture payment after successful transaction
    })

    # Pass the Razorpay order and key to the template context
    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'razorpay_key': API_KEY,  # Ensure this is your actual Razorpay API key
        'razorpay_order': razorpay_order  # The Razorpay order object
    }

    return render(request, 'checkout.html', context)

def updateItem(request):

    data = json.loads(request.body)
    productId = data['productID']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer = customer, status = 'Pending')
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)

    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()    

    if orderItem.quantity < 0:
        orderItem.delete()

    return JsonResponse('Item added...', safe=False)
    


@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = request.POST
        client = razorpay.Client(auth=(API_KEY,API_SECRET))
        

        # Verify payment signature
        params_dict = {
            'razorpay_order_id': data['razorpay_order_id'],
            'razorpay_payment_id': data['razorpay_payment_id'],
            'razorpay_signature': data['razorpay_signature']
        }

        try:
            client.utility.verify_payment_signature(params_dict)

            # Retrieve the order using the Razorpay order ID
            order = Order.objects.get(razorpay_order_id=data['razorpay_order_id'])
            order.status = 'Completed'
            order.save()

            return render(request, 'order_complete.html')

        except razorpay.errors.SignatureVerificationError:
            return HttpResponseBadRequest("Payment verification failed")

    return HttpResponseBadRequest("Invalid request method")


@csrf_exempt
def processOrder(request):
    data = json.loads(request.body)
    
    # Get customer and order info
    customer, created = Customer.objects.get_or_create(email=data['email'])
    customer.name = data['name']
    customer.phone_number = data['phone_number']
    customer.save()

    # Create order
    order = Order.objects.create(
        customer=customer,
        status='Pending',
        razorpay_order_id=data['razorpay_order_id']
    )

    # If shipping info exists, add it to the order
    Shipping.objects.create(
        customer=customer,
        order=order,
        address=data['address'],
        state=data['state'],
        city=data['city'],
        zip_code=data['zip_code']
    )

    # Verify Razorpay Payment
    client = razorpay.Client(auth=(API_KEY, API_SECRET))
    params_dict = {
        'razorpay_order_id': data['razorpay_order_id'],
        'razorpay_payment_id': data['razorpay_payment_id'],
        'razorpay_signature': data['razorpay_signature']
    }

    try:
        client.utility.verify_payment_signature(params_dict)
        order.status = 'Completed'
        order.save()

        return JsonResponse({'status': 'Order completed'})
    except razorpay.errors.SignatureVerificationError:
        return JsonResponse({'error': 'Payment verification failed'}, status=400)

def order_complete(request):
    return render(request,'order_complete.html')