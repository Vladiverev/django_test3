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
        sales = dw.get_categories_sale(categories = ["sum"],by = ['turnover', 'qty', 'receipts_qty'],
						date_from = "2015-11-17", date_to = "2015-11-18",
						interval = 'days', view_type = 'raw').drop(['name', 'category', 'date'], axis='columns')
      #  sales['turnover'] = dw.get_categories_sale(categories = ["sum"],by = 'qty',
						#date_from = "2015-11-17", date_to = "2015-11-18",
						#interval = 'days', view_type = 'raw')['qty']        
      #  sales['qty'] = dw.get_categories_sale(categories = ["sum"],by = "receipts_qty",
						#date_from = "2015-11-17", date_to = "2015-11-18",
						#interval = 'days', view_type = 'raw')['receipts_qty']
        sales['average_qty'] = sales['turnover'] / sales['qty']
        sales1  = sales.T

                
        
        return render(request, 'test_site/sale_list.html', {'client': client, 'sales': sales1})
        
    except Exception:        
        return render(request, 'test_site/index.html',{})

