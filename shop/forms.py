from .models import Purchase
from django.forms import ModelForm

class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = ['product', 'person', 'address', 'discount']