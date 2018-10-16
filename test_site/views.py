from django.shortcuts import render, redirect
from .models import Client
from pythonAPI.dwapi import datawiz 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

# Create your views here.


def client_info(sale):
    #sales = []
    #for key, s in sale.iterrows():
    #    sales.append(s.turnover)
    #return sales
    sales = {}
    for key, s in sale.items():
        sales[key] = s
    return sales


def sale_list(request):
    try: 
        dw = datawiz.DW(request.user.username, request.user.password)
        client = dw.get_client_info()
        sales = {}
        for sh in ('turnover', "qty", "receipts_qty"):
            sales[sh] = dw.get_categories_sale(categories = ["sum"],by = sh,
						    date_from = "2015-11-17", date_to = "2015-11-18",
						    interval = 'days', show = sh, view_type = 'raw').to_dict('split')
        return render(request, 'test_site/sale_list.html', {'client': client, 'sales': sales})
        
    except Exception:        
        return render(request, 'test_site/index.html',{})

