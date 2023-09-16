from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from .models import Car

def delete_true_view(request, duty_id):
    if not duty_id:
        return HttpResponse('请求异常')
    try:
        print("delete_true_view")
        print(duty_id)
        car = Car.objects.get(id=duty_id)

    except Exception as e:
        print('delete error is %s'%(e))
        return HttpResponse('--The note id is error')
    car.delete()

    return HttpResponse('删除成功!<a href = "/admin/duty/duty">返回</a>')