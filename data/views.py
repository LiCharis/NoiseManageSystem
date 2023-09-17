import json

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Data


def delete_true_view(request, duty_id):
    if not duty_id:
        return HttpResponse('请求异常')
    try:
        print("delete_true_view")
        print(duty_id)
        data = Data.objects.get(id=duty_id)

    except Exception as e:
        print('delete error is %s' % (e))
        return HttpResponse('--The note id is error')
    data.delete()

    return HttpResponse('删除成功!<a href = "/admin/duty/duty">返回</a>')


def res_view(request):
    return render(request, 'ManageSystem/analyse.html')


def analyse(request):
    analyseParam = request.POST['analyse']
    forceParam = request.POST['force']
    print(analyseParam)
    print(forceParam)
    request.res = 'res'
    result_url = "/static/images/交大鸽子.jpg"
    return render(request, 'ManageSystem/analyse.html', locals())


def get_ids(request):

    if request.method == 'GET':
        ids = request.GET.get('ids')
        model = request.GET.get('model')
        print(ids)
        print(model)
        id_list = ids.split(",")
        request.session['ids'] = id_list
        # 先获取到所选中的用户id
        print("先获取到所选中的用户id", id_list)

        return HttpResponseRedirect("/data/get_analyse")

    # elif request.method == 'POST':
    #     json_str = request.body
    #     json_dict = json.loads(json_str)
    #
    #     request.session['ids'] = json_dict
    #     # 先获取到所选中的用户id
    #     print("先获取到所选中的用户id", json_dict)
    #
    #     # return render(request, 'ManageSystem/analyse.html')
    #     return HttpResponseRedirect("/data/get_analyse")


def get_fields(request):
    if request.method == 'POST':
        json_str = request.body
        json_dict = json.loads(json_str)
        request.session['fields'] = json_dict
        print(request.session.get('ids'))
        print(request.session.get('fields'))
        ids = []

        for i in request.session['ids']:
            ids.append(int(i))

        info = {}

        datas = Data.objects.filter(id__in=ids)
        print(datas)

        for obj in datas:
            fields = {}
            for k, v in request.session.get('fields').items():

                fields.update({v: getattr(obj, v)})

            info.update({str(obj.id): fields})

    result = {"code": 200, "mes": info}

    # 这里就根据前端给的字段对应的数据返回数据

    return JsonResponse(result)
