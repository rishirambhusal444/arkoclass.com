import uuid
import hashlib
import base64
import hmac
import json
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Order
from videos.models import Subject, Video
from decouple import config  # For environment variables

# Function to generate HMAC SHA256 signature for eSewa
def generate_signature(total_amount, transaction_uuid, product_code, secret_key):
    string_to_hash = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
    signature = hmac.new(secret_key.encode(), string_to_hash.encode(), hashlib.sha256).digest()
    signature_base64 = base64.b64encode(signature).decode()
    return signature_base64

@login_required(login_url='auth/login')
def vip_form(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    total_videos = Video.objects.filter(subject_id=subject.id).count()
    
    product_code = 'EPAYTEST'
    secret = "8gBm/:&EnhH.1/q"
    transaction_uuid = str(uuid.uuid4())
    price = subject.price
    amount = price - subject.discount
    pdc = 0
    psc = 200
    total_amount = amount + psc + pdc
    tax_amount = 0
    total_amount += tax_amount
    
    # Round to two decimal places
    amount = round(amount, 2)
    total_amount = round(total_amount, 2)

    # Generate signature
    signature = generate_signature(total_amount, transaction_uuid, product_code, secret)     

    context = {
        'subject': subject,
        'total_videos': total_videos,
        'price': price,
        'discount': subject.discount,
        'amount': amount,
        'total_amount': total_amount,
        'pdc': pdc,
        'psc': psc,
        'product_code': product_code,
        'tax_amount': tax_amount,
        'uuid': transaction_uuid,
        'secret_key': secret,
        'signature': signature
    }

    return render(request, 'payment_form.html', context)

import logging

def esewa_success(request):
    encoded_data = request.GET.get('data')
    if not encoded_data:
        return HttpResponseBadRequest("Missing 'data' parameter")
    
    try:
        decoded_bytes = base64.b64decode(encoded_data)
        decoded_str = decoded_bytes.decode('utf-8')
        
        # Log the decoded string for debugging
        logging.debug(f"Decoded eSewa data: {decoded_str}")
        
        transaction_data = json.loads(decoded_str)

        transaction_code = transaction_data.get('transaction_code')
        status = transaction_data.get('status')
        total_amount_str = transaction_data.get('total_amount', '0.0').replace(',', '')
        total_amount = float(total_amount_str)
        transaction_uuid = transaction_data.get('transaction_uuid')
        product_code = transaction_data.get('product_code')

        # Retrieve or create the order
        order, created = Order.objects.get_or_create(
            order_id=transaction_code,
            defaults={
                'user': request.user,
                'transaction_id': transaction_uuid,
                'transaction_code': transaction_code,
                'transaction_status': status,
                'total_amount': total_amount,
                'product_code': product_code,
                'payment_gateway':'Esewa'
            }
        )

        if not created:
            # Update existing order
            order.transaction_id = transaction_uuid
            order.transaction_status = status
            order.total_amount = total_amount
            order.product_code = product_code
            order.payment_gateway = 'Esewa'

            order.save()

    except (TypeError, ValueError, json.JSONDecodeError) as e:
        logging.error(f"Error decoding transaction data: {str(e)}")
        return HttpResponseBadRequest("Error decoding transaction data")

    return redirect('/teacher_profile')

def esewa_failure(request):
    order_id = request.GET.get('oid')
    if order_id:
        try:
            order = Order.objects.get(order_id=order_id)
            order.transaction_status = 'FAILED'
            order.save()
        except Order.DoesNotExist:
            pass

    return render(request, 'fail_payment.html')

def payment_callback(request):
    amount = request.GET.get('amt')
    ref_id = request.GET.get('refId')
    status = request.GET.get('status')

    if status == 'Success':
        return HttpResponse(f"Payment Successful. Reference ID: {ref_id}")
    else:
        return HttpResponse("Payment Failed. Please try again.")

def khalti_payment(request):
    if request.method == 'POST':
        url = "https://a.khalti.com/api/v2/epayment/initiate/"
        return_url = request.POST.get('return_url')
        amount = (request.POST.get('amount'))
        purchase_order_id = request.POST.get('purchase_order_id')

        payload = {
            "return_url": return_url,
            "website_url": return_url,
            "amount": amount,
            "purchase_order_id": purchase_order_id,
            "purchase_order_name": "test",
            "customer_info": {
                "name": "Rishiram Bhusal",
                "email": "test@khalti.com",
                "phone": "9800000001"
            }
        }

        headers = {
            'Authorization': 'key 9e99736e5e3c4ddaa5c4cc1be039f510',
            'Content-Type': 'application/json',
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            new_res = response.json()

            if 'payment_url' in new_res:
                return redirect(new_res['payment_url'])
            else:
                return render(request, 'fail_payment.html', {'error': 'Failed to initiate payment. Please try again.'})
        except requests.exceptions.RequestException as e:
            return render(request, 'fail_payment.html', {'error': f'Request failed: {str(e)}'})
        except json.JSONDecodeError:
            return render(request, 'fail_payment.html', {'error': 'Invalid response from payment gateway.'})

    return redirect('home')

def khalti_success(request):
    if request.method == 'GET':
        pidx = request.GET.get('pidx')
        transaction_id = request.GET.get('transaction_id')
        total_amount = request.GET.get('amount')
        transaction_status = request.GET.get('status')
        purchase_order_id = request.GET.get('purchase_order_id')
        purchase_order_name = request.GET.get('purchase_order_name')

        if transaction_status == 'Completed':
            # Retrieve or create the order
            order, created = Order.objects.get_or_create(
                order_id=purchase_order_id,
                defaults={
                    'user': request.user,
                    'total_amount': total_amount,
                    'transaction_id': transaction_id,
                    'transaction_status': transaction_status,
                    'product_name': purchase_order_name,
                    'payment_gateway': 'Khalti'
                }
            )

            if not created:
                # Update existing order
                order.transaction_id = transaction_id
                order.transaction_status = transaction_status
                order.total_amount = total_amount
                order.product_name = purchase_order_name
                order.payment_gateway = 'khalti'
                order.save()

            return redirect('/profile/teacher_profile')

        else:
            return render(request, 'fail_payment.html', {'error': 'Payment not completed.'})

    return redirect('home')

from django.shortcuts import render, redirect
from .forms import OfflinePaymentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='/auth/login')
def offline_payment(request):
    if request.method == 'POST':
        form = OfflinePaymentForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form but don't commit yet
            payment = form.save(commit=False)
            # Assign the logged-in user to the user_id field
            payment.user = request.user
            # Now save the form
            payment.save()
            messages.success(request, 'Your payment has been submitted successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = OfflinePaymentForm()

    return render(request, 'vip_section/fail_payment.html', {'form': form})
