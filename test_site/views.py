from django.shortcuts import render, redirect
from .models import Client
from pythonAPI.dwapi import datawiz 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

# Create your views here.

def sale_list(request):    
    dw = datawiz.DW(request.user.username, request.user.password)
    shop = dw.get_products_sale(by="receipts_qty", date_from="2015-11-17", date_to="2015-11-18", show= "name") 
    return render(request, 'test_site/sale_list.html', {'shop': shop})