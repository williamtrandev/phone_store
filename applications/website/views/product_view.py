from django.conf import settings
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404

from applications.website.models import Customer, Product, Category


def product_page(request):

    is_phone = True
    page_render = 'pages/phone.html'
    title = 'Điện thoại'

    if 'accessories' in request.path:
        is_phone = False
        page_render = 'pages/accessory.html'
        title = 'Phụ kiện'

    # Query products
    products = Product.objects.filter(is_phone=is_phone).order_by('id')

    limit = settings.LIMIT_PAGING
    # Get categories
    categories = Category.objects.all().order_by('id')
    page_total = (products.count() + limit - 1) // limit
    products = products[0: limit]
    return render(request, page_render, {
        'categories': categories,
        'products': products,
        'title': title,
        'page_num': 1,
        'page_total': page_total
    })

def product_detail(request, phone_id):
    product = get_object_or_404(Product, id=phone_id)
    return render(request, 'pages/detail.html', {'product': product})

def accessory_detail(request, accessory_id):
    product = get_object_or_404(Product, id=accessory_id)
    return render(request, 'pages/detail.html', {'product': product})


def api_list_product_paging(request, page):
    category = request.GET.get('category')
    limit = settings.LIMIT_PAGING
    offset = (page - 1) * limit
    is_phone = request.GET.get('is_phone', 'true').lower() == 'true'
    products = Product.objects.filter(is_phone=is_phone).order_by('id')
    if category:
        products = products.filter(category_id=category)
    page_total = (products.count() + limit - 1) // limit
    products = products[offset: offset + limit]

    products_data = []
    for product in products:
        product_dict = model_to_dict(product)
        product_dict['image'] = product.image.url if product.image else None
        products_data.append(product_dict)

    return JsonResponse({
        'products': products_data,
        'current_page': page,
        'page_total': page_total
    }, status=200)
