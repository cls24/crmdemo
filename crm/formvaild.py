from django import forms
from crm import models
import time

class CustomerForm(forms.Form):
    name = forms.CharField(max_length=32)
    address = forms.CharField(max_length=128)
    phone = forms.CharField(max_length=11)
    ct_id = forms.fields.TypedChoiceField(
        coerce=lambda x: int(x),
        label="客户类型",
        required=True,
        choices=models.CustomerType.objects.values_list("id","name")
    )
    cl_id = forms.fields.TypedChoiceField(
        coerce=lambda x: int(x),
        label="客户级别",
        required=True,
        choices=models.CustomerLevel.objects.values_list("id","name")
    )

class CustomerOrderForm(forms.Form):
    ordernum = forms.IntegerField(
        label="订单号",
        required=True,
        min_value=0,
        initial=int(time.strftime("%Y%m%d%H%M", time.localtime())),
        error_messages={
            "required": "不能为空",
            "min_value": "不能为负数",
        }
    )
    # addtime = forms.fields.DateTimeField(
    #     label="时间",
    #     required=True,
    # )
    ordervalue = forms.fields.FloatField(
        label="订单金额",
        required=True,
        max_value=9999999,
        min_value=0,
        error_messages={
            "required":"不能为空",
            "max_value":"超过9999999",
            "min_value":"不能为负数",
        }
    )
    arrears = forms.fields.FloatField(
        label="欠款金额",
        required=True,
        max_value=9999999,
        min_value=0,
        error_messages={
            "required":"不能为空",
            "max_value":"超过9999999",
            "min_value":"不能为负数",
        }
    )
    os_id = forms.fields.ChoiceField(
        label="状态",
        required=True,
        choices=models.OrderStatus.objects.values_list("id", "name")
    )
    comment = forms.fields.CharField(
        label="备注",
        required=False,
        widget=forms.Textarea,
    )
    ocn_id = forms.fields.TypedChoiceField(
        coerce=lambda x: int(x),
        label="客户",
        required=True,
        choices=models.Customer.objects.values_list("id","name")
    )
    on_id = forms.fields.TypedChoiceField(
        coerce=lambda x: int(x),
        label="订单类型",
        required=True,
        choices=models.CustomerOrderType.objects.values_list("id","name")
    )

class OrderListForm(forms.Form):
    pm_id = forms.fields.TypedChoiceField(
        coerce=lambda x: int(x),
        label="产品型号",
        required=True,
        choices=models.ProductModel.objects.values_list("id","model")
    )
    productnum = forms.IntegerField(
        label="产品数量",
        required=True,
        max_value=9999999,
        min_value=0,
        initial=1,
        error_messages={
            "required": "不能为空",
            "max_value": "超过9999999",
            "min_value": "不能为负数",
        }
    )
class StorageForm(forms.Form):
    # fn_id = forms.TypedChoiceField(
    #     coerce=lambda x: int(x),
    #     label="厂家名",
    #     required=True,
    #     choices=models.Factory.objects.values_list("id", "name")
    # )
    pm_id = forms.fields.TypedChoiceField(
        coerce=lambda x: int(x),
        label="产品型号",
        required=True,
        choices=models.ProductModel.objects.values_list("id","model")
    )
    number = forms.IntegerField(
        label="产品数量",
        required=True,
        max_value=9999999,
        min_value=0,
        initial=1,
        error_messages={
            "required": "不能为空",
            "max_value": "超过9999999",
            "min_value": "不能为负数",
        }
    )
