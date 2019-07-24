
from django.urls import path,re_path
from crm import views
urlpatterns = [
    path('createorder', views.createorder),
    path('createpurchaseorder', views.CreatePurchaseOrder.as_view()),
    path('getpms', views.CreatePurchaseOrder.addProduct),
    path('orderlistdetail', views.orderListDetail),
    path('getselect', views.getSelect),
    path('orderlist', views.Orderlist.as_view()),
    path('stocklist', views.stocklist),
    path('initdata', views.initdata),
    path('storage', views.Storage.as_view()),
    path('customer', views.Customer.as_view()),
    path('home',views.home)
]
