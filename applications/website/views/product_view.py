from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse

from applications.website.models import Customer, Product, Category


def product_page(request):
    customer = request.session.get('customer', None)

    is_phone = True
    page_render = 'pages/phone.html'
    title = 'Điện thoại'

    if 'accessories' in request.path:
        is_phone = False
        page_render = 'pages/accessory.html'
        title = 'Phụ kiện'

    # Query products
    products = Product.objects.filter(is_phone=is_phone)

    # Pagination logic
    # paginator = Paginator(products, 8)  # Show 8 products per page
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    # Get categories
    categories = Category.objects.all()

    # Count total products
    num_product = products.count()

    # Calculate number of pages
    # page_num = paginator.num_pages

    return render(request, page_render, {
        'categories': categories,
        'products': products,
        'title': title,
        'page_num': 1
    })

def product_detail(request, phone_id):
    product = get_object_or_404(Product, id=phone_id)
    return render(request, 'pages/detail.html', {'product': product})