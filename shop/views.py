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
        for product in original.getlist('product'):
            post = original
            post['product'] = product
            print(Product.objects.get(id=product).price)
            price += Product.objects.get(id=product).price
            if len(Product.objects.filter(buying=True)) > 1:
                post['discount'] = 0.1
                discount = 0.1
            else:
                post['discount'] = 0
                discount = 0
            request.POST = post
            form = PurchaseForm(request.POST)
            if form.is_valid():
                saved_form = form.save()
                show_response = True
        if show_response:
            return HttpResponse(f'Спасибо за покупку, {saved_form.person}!'
                                    f'\n Скидка за одновременную покупку экземпляров товаров разного вида: {discount}%'
                                    f'\n Общая сумма покупки: {int(price * (1 - (discount)))}')
    purchase_products = Product.objects.filter(buying=True)
    form = PurchaseForm()
    context = {
        'form': form,
        'purchase_products': purchase_products,
    }
    return render(request, 'shop/purchase_form.html', context)