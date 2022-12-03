from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Product, Purchase
from .forms import PurchaseForm

# Create your views here.
def index(request):
    products = Product.objects.all()
    print(request.method)
    if request.method == 'POST':
        print("INDEX POST")
        print(request.POST)
        id_list = request.POST.getlist('buyCheckbox')

        products.update(buying=False)
        for x in id_list:
            Product.objects.filter(pk=int(x)).update(buying=True)
        if len(Product.objects.filter(buying=True)) > 0:
            return redirect('buy')

    context = {'products': products}
    return render(request, 'shop/index.html', context)

def purchase(request):
    error = ''
    discount = 0
    price = 0
    if request.method == 'POST':
        show_response = False
        original = request.POST.copy()
        print("Testssss ", Product.objects.filter(buying=True))
        cortege = calculate_general_price_and_discount(Product.objects.filter(buying=True), original, request.POST)
        if len(cortege[0]) > 0:
            for element in cortege[0]:
                saved_form = element.save()
                show_response = True
        print("cortege result: ", cortege)
        if show_response:
            Product.objects.filter(buying=True).update(buying=False)
            return HttpResponse(f'Спасибо за покупку, {saved_form.person}!'
                                    f'\n Скидка за одновременную покупку экземпляров товаров разного вида: {cortege[2]}%'
                                    f'\n Общая сумма покупки: {cortege[1]}')
    purchase_products = Product.objects.filter(buying=True)
    form = PurchaseForm()
    context = {
        'form': form,
        'purchase_products': purchase_products,
    }
    return render(request, 'shop/purchase_form.html', context)

def calculate_general_price_and_discount(products_list, post, request):
    finalForm = []
    price = 0
    discount = 0
    for product in products_list:
        if post is not None:
            post['product'] = product
        price += product.price
        discount = calculate_discount(products_list)
        if post is not None:
            post['discount'] = discount
            request.POST = post
            form = PurchaseForm(request.POST)
            if form.is_valid():
                finalForm.append(form)
    return finalForm, int(price * (1 - discount)), discount * 100

def calculate_discount(Products):
    resultValue = 0
    if len(Products) > 1:
        resultValue = 0.1
    return resultValue