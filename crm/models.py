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
    addtime = models.DateField(auto_now_add=True)
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
    ordernum = models.BigIntegerField(primary_key=True)
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
    productnum = models.IntegerField()

class ProductModel(Model):
    model = models.CharField(max_length=128)
    value = models.FloatField()
    fn = models.ForeignKey("Factory",on_delete=models.CASCADE)

class Factory(Model):
    name = models.CharField(max_length=64)

class Stock(Model):
    number = models.IntegerField()
    pm = models.ForeignKey("ProductModel",on_delete=models.CASCADE)

class PurchaseOrder(Model):
    ordernum = models.BigIntegerField(primary_key=True)
    addtime = models.DateTimeField(auto_now_add=True)
    ordervalue = models.FloatField()
    payment = models.FloatField()
    comment = models.CharField(max_length=256)
    fn = models.ForeignKey("Factory",on_delete=models.CASCADE)
    os = models.ForeignKey("OrderStatus",on_delete=models.CASCADE)

class PurchaseOrderList(Model):
    productnum = models.IntegerField(null=False)
    order = models.ForeignKey("PurchaseOrder",on_delete=models.CASCADE)
    pm = models.ForeignKey("ProductModel",on_delete=models.CASCADE)

def initData():
    role_data = {"name":"admin"}
    Role().objects.create(**role_data)

    user_data = {"name":"admin","password":"admin","r_id":1}
    User().objects.create(**user_data)

    li = [{"name":"经销商"},{"name":"个人"}]
    li = list(map(lambda x:CustomerType(**x),li))
    CustomerType.objects.bulk_create(li)

    li = [{"name":"优质"},{"name":"普通"},{"name":"失信"},{"name":"黑名单"}]
    li = list(map(lambda x:CustomerLevel(**x),li))
    CustomerLevel.objects.bulk_create(li)

    li = [{"name":"完成"},{"name":"未完成"}]
    li = list(map(lambda x:OrderStatus(**x),li))
    OrderStatus.objects.bulk_create(li)

    li = [{"name":"零售"},{"name":"批发"},{"name":"租赁"},{"name":"维修"}]
    li = list(map(lambda x:CustomerOrderType(**x),li))
    CustomerOrderType.objects.bulk_create(li)

