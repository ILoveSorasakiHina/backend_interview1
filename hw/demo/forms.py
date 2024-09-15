from django import forms

class OrderForm(forms.Form):
    id = forms.CharField(label='訂單編號', max_length=10)
    name = forms.CharField(label='名稱', max_length=255)
    city = forms.CharField(label='城市', max_length=100)
    district = forms.CharField(label='區域', max_length=100)
    street = forms.CharField(label='街道', max_length=255)
    price = forms.IntegerField(label='價格', max_digits=10, decimal_places=2)
    currency = forms.CharField(label='貨幣', max_length=10)
