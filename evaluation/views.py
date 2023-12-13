from django.shortcuts import render

# Create your views here.
import json

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from total.models import Total
from .models import Evaluation

def delete_true_view(request, duty_id):
    print(request.path)
    if not duty_id:
        return HttpResponse('请求异常')

    if request.method == 'GET':
        action = request.path

        try:
            print("delete_true_view")
            print(duty_id)

            obj = Evaluation.objects.get(id=duty_id).__dict__
            print(obj)

        except Exception as e:
            print('delete error is %s' % (e))

        return render(request, 'ManageSystem/delete.html', locals())


    elif request.method == 'POST':

        if request.POST.get('cancel'):
            print(request.POST['cancel'])
            return HttpResponseRedirect("/admin/evaluation/evaluation")

        try:
            print("delete_true_view")
            print(duty_id)
            obj = Evaluation.objects.get(id=duty_id)
            Total.objects.get(id=obj.total.id).delete()
            obj.delete()

        except Exception as e:
            print('delete error is %s' % (e))
            return HttpResponse('--The note id is error')


    return HttpResponseRedirect("/admin/evaluation/evaluation")