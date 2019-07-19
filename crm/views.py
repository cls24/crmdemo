from django.shortcuts import render, HttpResponse, redirect
from crm import formvaild
from crm import models
import json


def createorder(req):
    if req.method == "GET":
        form_obj = formvaild.CustomerOrderForm()
        order_list = formvaild.OrderListForm()
        return render(req, "crm/createorder.html", {"formObj": form_obj, "orderList": order_list})
    formObj = formvaild.CustomerOrderForm(req.POST)
    resp = {"msg": "", "status": "ok", "err": formObj.errors}
    if formObj.is_valid():
        print(formObj.cleaned_data)
        orderNum = formObj.cleaned_data["ordernum"]
        orderList = json.loads(req.POST.get("orderList"))
        try:
            models.CustomerOrder.objects.create(**formObj.cleaned_data)
            li = list(map(lambda x: models.OrderList(order_id=orderNum, pm_id=x["pm_id"], productnum=x["productnum"]),
                          orderList))
            models.OrderList.objects.bulk_create(li)
        except Exception as e:
            print(e)
            resp["msg"] = e.__str__()
            resp["status"] = "err"
    else:
        resp["status"] = "err"
    print(resp)
    return HttpResponse(json.dumps(resp))


def orderlist(req):
    if req.method == "GET":
        data = models.CustomerOrder.objects.all()
        return render(req, "crm/orderlist.html", {"data": data})


def stocklist(req):
    if req.method == "GET":
        data = models.Stock.objects.all()
        return render(req, "crm/stocklist.html", {"data": data})


def storage(req):
    if req.method == "GET":
        stock_list = formvaild.StorageForm()
        return render(req, "crm/storage.html", {"stock_list": stock_list})
