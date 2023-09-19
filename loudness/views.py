from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Loudness

def delete_true_view(request, duty_id):
    print(request.path)
    if not duty_id:
        return HttpResponse('请求异常')

    if request.method == 'GET':
        action = request.path

        try:
            print("delete_true_view")
            print(duty_id)

            obj = Loudness.objects.get(id=duty_id).__dict__
            print(obj)

        except Exception as e:
            print('delete error is %s' % (e))

        return render(request, 'ManageSystem/delete.html', locals())


    elif request.method == 'POST':

        if request.POST['cancel']:
            print(request.POST['cancel'])
            return HttpResponseRedirect("/admin/loudness/loudness")

        try:
            print("delete_true_view")
            print(duty_id)
            Loudness.objects.get(id=duty_id).delete()

        except Exception as e:
            print('delete error is %s' % (e))
            return HttpResponse('--The note id is error')

    return HttpResponseRedirect("/admin/loudness/loudness")