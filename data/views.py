import json

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render

from car.models import Car
from clarity.models import Clarity
from loudness.models import Loudness
from volatility.models import Volatility
from .models import Data
from pyecharts import options as opts
from pyecharts.charts import Bar

def delete_true_view(request, duty_id):
    print(request.path)
    if not duty_id:
        return HttpResponse('请求异常')

    if request.method == 'GET':
        action = request.path

        try:
            print("delete_true_view")
            print(duty_id)

            obj = Data.objects.get(id=duty_id).__dict__
            print(obj)

        except Exception as e:
            print('delete error is %s' % (e))

        return render(request, 'ManageSystem/delete.html', locals())


    elif request.method == 'POST':

        if request.POST['cancel']:
            print(request.POST['cancel'])
            return HttpResponseRedirect("/admin/data/data")

        try:
            print("delete_true_view")
            print(duty_id)
            Data.objects.get(id=duty_id).delete()

        except Exception as e:
            print('delete error is %s' % (e))
            return HttpResponse('--The note id is error')

    return HttpResponseRedirect("/admin/data/data")

# def res_view(request):
#     return render(request, 'ManageSystem/analyse.html')
#
#
# def analyse(request):
#     analyseParam = request.POST['analyse']
#     forceParam = request.POST['force']
#     print(analyseParam)
#     print(forceParam)
#     request.res = 'res'
#     result_url = "/static/images/交大鸽子.jpg"
#     return render(request, 'ManageSystem/analyse.html', locals())
#

def get_details(request, id):

    if not id:
        return HttpResponse('请求异常')

    try:
        obj = Data.objects.get(id=id)

    except Exception as e:
        print(e)

    return render(request, 'ManageSystem/details.html', locals())


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

        return render(request, 'ManageSystem/analyse.html')

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

        info = []

        datas = Data.objects.filter(id__in=ids)
        print(datas)

        for obj in datas:
            fields = {"id": obj.id}
            for k, v in request.session.get('fields').items():

                fields.update({v: getattr(obj, v)})

            info.append(fields)

    result = {"code": 200, "mes": info}

    # 这里就根据前端给的字段对应的数据返回数据

    return JsonResponse(result)

def compare(request):
    cars = Car.objects.all()
    categories = []
    sound_pressure_list = []
    clarity_left = []
    clarity_right = []
    loudness_left = []
    loudness_right = []
    volatility_left = []
    volatility_right = []

    for car in cars:
        categories.append(str(car.brand))

        if Data.objects.filter(car=car):
            sound_pressure_list.append(Data.objects.filter(car=car).first().result)
        else:
            sound_pressure_list.append(0)

        if Clarity.objects.filter(car=car):
            clarity_left.append(Clarity.objects.filter(car=car).first().left)
            clarity_right.append(Clarity.objects.filter(car=car).first().right)
        else:
            clarity_left.append(0)
            clarity_right.append(0)

        if Loudness.objects.filter(car=car):
            loudness_left.append(Loudness.objects.filter(car=car).first().left)
            loudness_right.append(Loudness.objects.filter(car=car).first().right)
        else:
            loudness_left.append(0)
            loudness_right.append(0)

        if Volatility.objects.filter(car=car):
            volatility_left.append(Volatility.objects.filter(car=car).first().left)
            volatility_right.append(Volatility.objects.filter(car=car).first().right)
        else:
            volatility_left.append(0)
            volatility_right.append(0)

    print(categories)
    print(sound_pressure_list)
    print(clarity_left)
    print(clarity_right)
    print(loudness_left)
    print(loudness_right)
    print(volatility_left)
    print(volatility_right)

    # 提取车型名称和各项数据

    # 创建横向柱状图
    bar = (
        Bar()
        .add_xaxis(categories)
        .add_yaxis("声压", sound_pressure_list, category_gap="50%")  # 设置category_gap以调整柱状图之间的间距
        .add_yaxis("响度左耳", loudness_left, category_gap="50%", stack='stack_1')
        .add_yaxis("响度右耳", loudness_right, category_gap="50%", stack='stack_1')
        .add_yaxis("波动度左耳", volatility_left, category_gap="50%", stack='stack_2')
        .add_yaxis("波动度右耳", volatility_right, category_gap="50%", stack='stack_2')
        .add_yaxis("语言清晰度左耳", clarity_left, category_gap="50%", stack='stack_3')
        .add_yaxis("语言清晰度右耳", clarity_right, category_gap="50%", stack='stack_3')
        .reversal_axis()  # 使用reversal_axis方法将x轴和y轴对调
        .set_global_opts(
            title_opts=opts.TitleOpts(),
            yaxis_opts=opts.AxisOpts(
                name="车型",
            ),
            xaxis_opts=opts.AxisOpts(name="数值"),  # 设置x轴标签为数值
            legend_opts=opts.LegendOpts(
                pos_top="0%",
                pos_left="0%",
            ),
        )
    )

    context = {'bar_chart': bar.render_embed(), 'flag': True}
    return render(request, 'ManageSystem/compare.html', context)
