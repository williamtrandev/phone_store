import json

from django.db import transaction
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from applications.website.models import Customer, Product, CartItem, Order, OrderItem


@require_http_methods(['POST'])
def add_product_to_cart(request):
    if 'customer' not in request.session:
        redirect('login')

    try:
        body = json.loads(request.body)
        product_id = body.get('product_id')
        quantity = int(body.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        customer_id = request.session['customer']['id']
        customer = get_object_or_404(Customer, id=customer_id)
        cart_item = CartItem.objects.filter(customer=customer, product=product).first()

        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
            status_code = 200
        else:
            cart_item = CartItem.objects.create(
                customer=customer,
                product=product,
                quantity=quantity,
            )
            status_code = 201

        return JsonResponse({
            'id': cart_item.id,
            'customer_id': cart_item.customer_id,
            'product_id': cart_item.product_id,
            'quantity': cart_item.quantity,
        }, status=status_code)

    except KeyError as e:
        return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["PUT", "DELETE"])
def action_product_in_cart(request, cart_id):
    customer_id = request.session['customer']['id']
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'PUT':
        try:
            body = json.loads(request.body)
            quantity = int(body.get('quantity', 1))

            cart_item = get_object_or_404(CartItem, id=cart_id, customer=customer)

            cart_item.quantity = quantity
            cart_item.save()

            return JsonResponse({
                'id': cart_item.id,
                'customer_id': cart_item.customer_id,
                'product_id': cart_item.product_id,
                'quantity': cart_item.quantity,
            }, status=200)

        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'DELETE':
        try:
            cart_item = get_object_or_404(CartItem, id=cart_id, customer=customer)

            cart_item.delete()

            return JsonResponse({'message': 'Item removed from cart'}, status=204)

        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


def cart_page(request):
    if 'customer' not in request.session:
        return redirect('login')
    customer_id = request.session['customer']['id']
    customer = get_object_or_404(Customer, id=customer_id)
    carts = CartItem.objects.filter(customer=customer).select_related('product')
    return render(request, 'pages/cart.html', {'carts': carts})


@require_http_methods(["POST"])
def checkout(request):
    if 'customer' not in request.session:
        return redirect('login')

    try:
        customer_id = request.session['customer']['id']
        customer = get_object_or_404(Customer, id=customer_id)

        cart_items = CartItem.objects.filter(customer=customer).select_related('product')

        if not cart_items:
            return JsonResponse({'error': 'Giỏ hàng trống!'}, status=400)

        total_price = sum(item.total_price for item in cart_items)

        with transaction.atomic():

            order = Order.objects.create(
                customer=customer,
                total_price=total_price,
                order_status='pending'
            )

            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.retail_price
                )
                for item in cart_items
            ]

            OrderItem.objects.bulk_create(order_items)

            cart_items.delete()

        return JsonResponse({
            'order_id': order.id,
            'total_price': order.total_price,
            'status': order.order_status,
            'message': 'Đặt hàng thành công!'
        }, status=200)

    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e)}, status=500)