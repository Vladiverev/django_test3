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
        sales['average_qty'] = sales['turnover'] / sales['qty']
        sales1  = sales.T.reset_index().rename(columns={0: "2015-11-17", 1: "2015-11-18"})
        sales1['dif_per'] = sales1["2015-11-18"] / sales1["2015-11-17"]
        sales1['dif_min'] = sales1["2015-11-18"] - sales1["2015-11-17"]

        product1 =  dw.get_products_sale(by=['turnover', 'qty'], date_from = "2015-11-17", date_to = "2015-11-17",
						interval = 'days',show="name", view_type = 'raw').drop(['date', 'product'], axis='columns')
        product2 =  dw.get_products_sale(by=['turnover', 'qty'], date_from = "2015-11-18", date_to = "2015-11-18",
						interval = 'days',show='name', view_type = 'raw').drop(['date', 'product'], axis='columns')        
        product1['differ_qty'] = product1['qty'] - product2['qty']
        product1['differ_turnover'] = product1['turnover'] - product2['turnover']
        product = product1.drop(['turnover', 'qty'], axis='columns')
        
        return render(request, 'test_site/sale_list.html', {'client': client, 'sales': sales1.to_html, 
                                                            'products1': product.sort_values(by='differ_qty').to_html,
                                                           'products2': product.sort_values(by='differ_qty', ascending=False).to_html})
        
    except Exception:        
        return render(request, 'test_site/index.html',{})

