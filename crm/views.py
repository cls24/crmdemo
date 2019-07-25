from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q,F
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from crm import formvaild
from crm import models
import json
from django.views import View
import datetime,time

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self,obj)
def home(request):
    return render(request,'crm/index.html',{'title':'index'})


class Conditions:
    @staticmethod
    def orderListQ(lst):
        con = Q()
        # lst = [{"key1":[]},{"key2":[]},{"key3":[]}]
        for i in lst:
            q = Q()
            if i[0] == "addtime" or i[0] == "ordervalue" or i[0] == "arrears":
                q.connector = "AND"
                q.children.append((i[0] + "__gte", i[1][0]))
                q.children.append((i[0] + "__lte", i[1][1]))
            else:
                q.connector = "OR"
                for j in i[1]:
                    q.children.append((i[0], j))
            con.add(q, "AND")
        return con
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
        factory_select = formvaild.FactorySelectForm()
        # time.strftime("%Y%m%d%H%M%S", time.localtime())
        return render(req, "crm/createorder.html", {"formObj": form_obj, "orderList": order_list,"factory_select":factory_select})
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
            updateStock(orderList,"minus")
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
        if key == "ocn__name":
            data = models.Customer.objects.all().values("id", "name")
            return HttpResponse(json.dumps({"data":list(data)}))
        elif key == "on__name":
            data = models.CustomerOrderType.objects.all().values("id", "name")
            return HttpResponse(json.dumps({"data":list(data)}))
        elif key == "os__name":
            data = models.OrderStatus.objects.all().values("id", "name")
            return HttpResponse(json.dumps({"data":list(data)}))
        elif key == "ocn__ct__name":
            data = models.CustomerType.objects.all().values("id", "name")
            return HttpResponse(json.dumps({"data":list(data)}))

def orderListDetail(req):
    colsMap = {
        "pm__model": "产品型号",
        "pm__value": "产品单价",
        "productnum": "产品数量",
    }
    orderNum = req.POST.get("orderNum")
    print(req.POST)
    ret = models.OrderList.objects.filter(order_id=orderNum).select_related("pm_id").values("pm__model","pm__value","productnum")
    print(ret.query)
    print(list(ret))
    return HttpResponse(json.dumps({"data":list(ret),"tablehead":colsMap}))

class Orderlist(View):
    colsMap = {
        "ordernum": "订单号",
        "ordervalue": "订单总金额",
        "arrears": "订单欠款",
        "addtime":"下单时间",
        "ocn__name": "客户",
        "ocn__ct__name": "客户类型",
        "on__name": "订单类型",
        "os__name": "订单状态",
        "comment": "备注",
    }

    def get(self,req):
        return render(req,"crm/orderlist.html",{"selectOptions": self.colsMap})

    def paser(self,x):
        tmp = x[0]
        if "__name" in x[0]:
            tmp = x[0].replace("_name", "id")
        elif "comment" == x[0]:
            tmp = x[0]+"__contains"
        return (tmp,x[1])

    def post(self,req):
        obj = req.POST.get("data")
        pn = req.POST.get("pn")
        page_number = req.POST.get("page_number")
        obj = json.loads(obj)
        obj = list(map(lambda x:self.paser(x),obj.items()))
        ret = models.CustomerOrder.objects.filter(Conditions.orderListQ(obj)).select_related("on_id","os_id","ocn_id").values(
            *self.colsMap.keys())
        p = Paginator(list(ret), page_number)
        # print(ret.query)
        return HttpResponse(json.dumps({
            "data":p.page(pn).object_list,
            "page_range":[p.page_range.start,p.page_range.stop],
            "total_page":p.num_pages,
            "tablehead":self.colsMap},cls=DateEncoder))

def stocklist(req):
    if req.method == "GET":
        data = models.Stock.objects.all()
        return render(req, "crm/stocklist.html", {"data": data})

class Storage(View):
    def get(self,req):
        stock_list = formvaild.StorageForm()
        all = models.Stock.objects.select_related("pm_id","pm__fn_id").all().values("pm__model","number","pm__fn__name")
        print(list(all))
        return render(req, "crm/storage.html", {"stock_list": list(all)})

    def post(self,req):
        return HttpResponse("post")

class Customer(View):
    def get(self,req):
        formObj = formvaild.CustomerForm()
        return render(req, "crm/customer.html", {"formobj": formObj})

    def post(self,req):
        return HttpResponse("post")

class CreatePurchaseOrder(View):
    @staticmethod
    def addProduct(req):
        fn_id = req.POST.get("fn_id")
        ret=  models.ProductModel.objects.filter(fn_id=fn_id).values()
        return HttpResponse(json.dumps({"pms":list(ret)}))

    def get(self,req):
        form_obj = formvaild.PurchaseOrderForm()
        order_list = formvaild.OrderListForm()
        # return render(req, "crm/createpurchaseorder.html", {"formObj": form_obj, "orderList": order_list})        order_list = formvaild.OrderListForm()
        return render(req, "crm/createpurchaseorder.html", {"formObj": form_obj})

    def post(self,req):
        formObj = formvaild.PurchaseOrderForm(req.POST)
        resp = {"msg": "", "status": "ok", "err": formObj.errors}
        if formObj.is_valid():
            print(formObj.cleaned_data)
            orderNum = formObj.cleaned_data["ordernum"]
            orderList = json.loads(req.POST.get("orderList"))
            try:
                models.PurchaseOrder.objects.create(**formObj.cleaned_data)
                li = list(
                    map(lambda x: models.PurchaseOrderList(order_id=orderNum, pm_id=x["pm_id"], productnum=x["productnum"]),
                        orderList))
                models.PurchaseOrderList.objects.bulk_create(li)
                updateStock(orderList,"add")
            except Exception as e:
                print(e)
                resp["msg"] = e.__str__()
                resp["status"] = "err"
        else:
            resp["status"] = "err"
        print(resp)
        return HttpResponse(json.dumps(resp))

def updateStock(pmlist,opt):
    for one in pmlist:
        pm_id = one["pm_id"]
        number = one["productnum"]
        o = models.Stock.objects.filter(pm_id=pm_id)
        if o.exists():
            if opt == "add":
                o.update(number=F("number") + number)
            else:
                o.update(number=F("number") - number)
        else:
            models.Stock.objects.create(pm_id=pm_id, number=number)

class Ajax:
    @staticmethod
    def checkStock(req):
        data = req.POST.get("data")
        li = json.loads(data)["list"]
        dic = {}
        for i in li:
            pm_id = i["pm_id"]
            number = int(i["productnum"])
            if dic.get(pm_id):
                dic[pm_id] = dic[pm_id] + number
            else:
                dic[pm_id] = number
        ret = {"msg": "","status":"ok"}
        for i,n in dic.items():
            o = models.Stock.objects.filter(pm_id=i).values("number","pm__model").first()
            if o["number"] < n:
                ret["status"] = "err"
                ret["msg"]+="%s 库存数量%d 少于订单数量%s"%(o["pm__model"],o["number"],dic[i])
        print(ret)
        return HttpResponse(json.dumps(ret))