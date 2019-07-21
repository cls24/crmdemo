from django.shortcuts import render, HttpResponse, redirect
from crm import formvaild
from crm import models
import json
from django.views import View
def initdata(req):
    resp = "ok"
    try:
        models.initData()
    except Exception as e:
        resp = e.__str__()
    return HttpResponse(resp)
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

def getSelect(req):
    if req.method == "POST":
        key = req.POST.get("key")
        # ocn_id = models.Customer.objects.all().values("id", "name")
        # print(key)
        if key == "ocn_id":
            data = models.Customer.objects.all().values("id", "name")
            return HttpResponse(json.dumps({"data":list(data)}))


class Orderlist(View):
    def get(self,req):
        data = models.CustomerOrder.objects.all()
        ocn_id = models.Customer.objects.all().values("id", "name")
        selectOptions = {
            "ordernum": "订单号",
            "ordervalue": "订单总金额",
            "arrears": "订单欠款",
            "comment": "备注",
            "ocn_id": "客户",
            "ot": "客户类型",
            "on_id":"订单类型",
            "os_id":"订单状态"
        }
        return render(req,"crm/orderlist.html",{"data": data,"selectOptions": selectOptions})
    def post(self,req):
        obj = req.POST
        return HttpResponse("ok")
def stocklist(req):
    if req.method == "GET":
        data = models.Stock.objects.all()
        return render(req, "crm/stocklist.html", {"data": data})


class Storage(View):
    def get(self,req):
        stock_list = formvaild.StorageForm()
        return render(req, "crm/storage.html", {"stock_list": stock_list})

    def post(self,req):
        return HttpResponse("post")

class Customer(View):
    def get(self,req):
        formObj = formvaild.CustomerForm()
        return render(req, "crm/customer.html", {"formobj": formObj})

    def post(self,req):
        return HttpResponse("post")