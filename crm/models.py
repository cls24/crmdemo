from django.db import models
from django.db.models import Model

class Role(Model):
    name = models.CharField(max_length=32)

class User(Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    r = models.ForeignKey("Role",on_delete=models.CASCADE)

class Customer(Model):
    name = models.CharField(max_length=32)
    address = models.CharField(max_length=128)
    phone = models.CharField(max_length=11)
    addtime = models.DateField()
    ct = models.ForeignKey("CustomerType",on_delete=models.CASCADE)
    cl = models.ForeignKey("CustomerLevel",on_delete=models.CASCADE)

class CustomerType(Model):
    """
    客户类型 1.个人 2.经销商
    """
    name = models.CharField(max_length=32)

class CustomerLevel(Model):
    """
    客户评级
    """
    name = models.CharField(max_length=32)

class CustomerOrder(Model):
    ordernum = models.BigIntegerField(primary_key=True,null=False,default=0)
    addtime = models.DateTimeField(auto_now_add=True)
    ordervalue = models.FloatField()
    arrears = models.FloatField()
    comment = models.CharField(max_length=256)
    ocn = models.ForeignKey("Customer",related_name = 'ocn',on_delete=models.CASCADE)
    on = models.ForeignKey("CustomerOrderType",on_delete=models.CASCADE)
    os = models.ForeignKey("OrderStatus",on_delete=models.CASCADE)

class OrderStatus(Model):
    """
    订单状态 1。完成，2。未完成
    """
    name = models.CharField(max_length=32)

class CustomerOrderType(Model):
    """
    订单类型 1。零售 2。批发 3。租赁 4.维修
    """
    name = models.CharField(max_length=32)

class OrderList(Model):
    order = models.ForeignKey("CustomerOrder",to_field="ordernum",on_delete=models.CASCADE)
    pm = models.ForeignKey("ProductModel",on_delete=models.CASCADE)
    productnum = models.IntegerField(null=False,default=1)
    ctime = models.DateTimeField(auto_now_add=True)
class ProductModel(Model):
    model = models.CharField(max_length=128)
    value = models.FloatField()
    fn = models.ForeignKey("Factory",on_delete=models.CASCADE)

class Factory(Model):
    name = models.CharField(max_length=64)

class Stock(Model):
    number = models.IntegerField()
    addtime = models.DateTimeField(auto_now_add=True)
    pm = models.ForeignKey("ProductModel",on_delete=models.CASCADE)

class PurchaseOrder(Model):
    addtime = models.DateTimeField()
    ordervalue = models.FloatField()
    status = models.BooleanField(default=False)
    comment = models.CharField(max_length=256)
    fn = models.ForeignKey("Factory",on_delete=models.CASCADE)
    
class PurchaseOrderList(Model):
    order = models.ForeignKey("PurchaseOrder",on_delete=models.CASCADE)
    pm = models.ForeignKey("ProductModel",on_delete=models.CASCADE)