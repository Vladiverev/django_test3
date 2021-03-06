from django.shortcuts import render, redirect
from .models import Client
from dwapi import datawiz
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate


# Create your views here.


def sale_list(request):

    dw = datawiz.DW(request.user.username, Client.objects.get(user_name=request.user).pass_user)
    client = dw.get_client_info()

    sales = dw.get_categories_sale(categories=["sum"], by=['turnover', 'qty', 'receipts_qty'],
                                   date_from="2018-03-01", date_to="2018-03-18",
                                   interval='days', view_type='raw').drop(['name', 'category', 'date'],
                                                                          axis='columns')
    sales['average_qty'] = sales['turnover'] / sales['qty']
    sales1 = sales.T.reset_index().rename(columns={0: "2018-03-01", 1: "2018-03-18"})
    sales1['dif_per'] = sales1["2018-03-18"] / sales1["2018-03-01"]
    sales1['dif_min'] = sales1["2018-03-18"] - sales1["2018-03-01"]

    product1 = dw.get_products_sale(by=['turnover', 'qty'], date_from="2018-03-01", date_to="2018-03-18",
                                    interval='days', show="name", view_type='raw').drop(['date', 'product'],
                                                                                        axis='columns')
    product2 = dw.get_products_sale(by=['turnover', 'qty'], date_from="2018-03-01", date_to="2018-03-18",
                                    interval='days', show='name', view_type='raw').drop(['date', 'product'],
                                                                                        axis='columns')
    product1['differ_qty'] = product2['qty'] - product1['qty']
    product1['differ_turnover'] = product2['turnover'] - product1['turnover']
    product = product1.drop(['turnover', 'qty'], axis='columns')
    return render(request, 'test_site/sale_list.html',
                  {'client': client, 'sales': sales1.to_html(index=False, classes="table"),
                   'products1': product.sort_values(by='differ_qty', ascending=False).to_html(index=False,
                                                                                              classes="table table-striped table-bordered",
                                                                                              table_id='differ_max'),
                   'products2': product.sort_values(by='differ_qty').to_html(index=False,
                                                                             classes="table table-striped table-bordered",
                                                                             table_id='differ_min')})