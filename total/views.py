from django.db.models import Max, Min
from django.shortcuts import render

# Create your views here.
import json

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render

from car.models import Car
from data.models import Data
from .models import Total

from ManageSystem.settings import MEDIA_URL
import re
from pyecharts import options as opts
from pyecharts.charts import Bar, Line


def delete_true_view(request, duty_id):
    print(request.path)
    if not duty_id:
        return HttpResponse('请求异常')

    if request.method == 'GET':
        action = request.path

        try:
            print("delete_true_view")
            print(duty_id)

            obj = Total.objects.get(id=duty_id).__dict__
            print(obj)

        except Exception as e:
            print('delete error is %s' % (e))

        return render(request, 'ManageSystem/delete.html', locals())


    elif request.method == 'POST':

        if request.POST.get('cancel'):
            print(request.POST['cancel'])
            return HttpResponseRedirect("/admin/total/total")

        try:
            print("delete_true_view")
            print(duty_id)
            Total.objects.get(id=duty_id).delete()

        except Exception as e:
            print('delete error is %s' % (e))
            return HttpResponse('--The note id is error')

    return HttpResponseRedirect("/admin/total/total")


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

def get_preview(request):
    action = '/admin/total/total'
    output = '/admin/total/total/export/?'
    total_fields = ['data_result', 'clarity_left',
                    'clarity_right', 'clarity_result', 'loudness_left', 'loudness_right',
                    'loudness_result', 'sharpness_left', 'sharpness_right', 'sharpness_result',
                    'volatility_left', 'volatility_right', 'volatility_result', 'index']
    result = {}
    try:
        data_to_preview = Total.objects.all()  # 获取要预览的数据

        for field in total_fields:
            max_value = Total.objects.aggregate(Max(field))
            min_value = Total.objects.aggregate(Min(field))
            result[field] = {
                'max': max_value[f'{field}__max'],
                'min': min_value[f'{field}__min'],
            }
        #
        # # 遍历查询集合并修改记录
        # i = 0
        # for data in data_to_preview:
        #     for field, values in result.items():
        #         temp = getattr(data, field)
        #         if getattr(data, field) == values['max']:
        #             setattr(data, "color", 'blue')
        #
        #         elif getattr(data, field) == values['min']:
        #             setattr(data, "color", 'red')
        #         # else:
        #         #     setattr(data, "color", 'black')
        #         print(data.color)



    except Exception as e:
        print(e)

    return render(request, 'ManageSystem/preview_data.html', locals())


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
    #     return HttpResponseRedirect("/total/get_analyse")


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

        totalDatas = Total.objects.filter(id__in=ids)
        print(totalDatas)

        for obj in totalDatas:
            fields = {"id": obj.id}
            for k, v in request.session.get('fields').items():
                fields.update({v: getattr(obj, v)})

            info.append(fields)

    result = {"code": 200, "mes": info}

    # 这里就根据前端给的字段对应的数据返回数据

    return JsonResponse(result)


def get_image(request, id):
    if not id:
        return HttpResponse('请求异常')

    if request.method == 'GET':
        action = '/admin/total/total'
        try:
            obj = Data.objects.get(id=id).total
            url = MEDIA_URL + str(obj.image)
            totalDataname = '声压级结果'

        except Exception as e:
            print(e)

        return render(request, 'ManageSystem/showImage.html', locals())


def analyse(request, ids):
    print(ids)
    id_list = ids.split(".")

    categories = []
    totalData_left = []
    totalData_right = []
    speed_x_label = []
    y = {'空载': [], '半载': [], '3/4额定载荷（24T）': [], '满载': []}
    for id in id_list:
        totalData = Total.objects.get(id=id)
        categories.append(
            str(str(totalData.speed) + '/' + str(totalData.condition) + '/' + str(totalData.status) + '/' + str(
                totalData.car.brand) + '/' + str(totalData.car.model)))
        y[str(totalData.status)].append(
            str(str(totalData.speed) + '/' + str(totalData.condition) + '/' + str(totalData.status) + '/' + str(
                totalData.car.brand) + '/' + str(totalData.car.model)) + '/' + str(totalData.result))
        flag = True
        temp = re.search(r'\d{2,}', str(totalData.condition), re.M | re.I).group() + 'km'
        for i in speed_x_label:
            if temp == i:
                flag = False
        if flag:
            speed_x_label.append(temp)
        totalData_left.append(totalData.result)

    # print(categories)
    car_type = str(set([''.join(i.split('/')[-2:]) for i in categories]))[2:-2]
    print(car_type)
    speed_type = '/'.join(set([i.split('/')[0] for i in categories]))
    print(speed_type)
    totalData_type = '声压'
    graph_type = '折线对比'
    print(speed_x_label)
    print(categories)

    print(totalData_left)
    print(totalData_right)
    line = (
        Line()
            .add_xaxis(speed_x_label)
            # .add_yaxis("波动度左耳", totalData_left)
            # .add_yaxis("波动度右耳", totalData_right)
            # .reversal_axis()
            .set_global_opts(
            title_opts=opts.TitleOpts(title="{} {} {} {}".format(car_type, speed_type, totalData_type, graph_type),
                                      pos_top="5%",
                                      pos_left="0%", ),
            # yaxis_opts=opts.AxisOpts(
            #     name="",
            #     axislabel_opts=opts.LabelOpts(formatter="{value}"),  # 使用自定义格式化函数
            # ),
            xaxis_opts=opts.AxisOpts(
                name="车速"
            ),
            # legend_opts=opts.LegendOpts(
            #     pos_top="0%",
            #     pos_left="0%",
            # ),
        )
    )
    # for i in ['空载','半载','3/4额定载荷（24T）','满载']:
    #     if len(y[i])==0:
    #         continue
    #     else:
    #         line.add_yaxis("波动度左耳——"+i,[j.split('/')[-2] for j in y[i]])
    #         line.add_yaxis("波动度右耳——"+i,[j.split('/')[-1] for j in y[i]])
    for i in ['空载', '半载', '3/4额定载荷（24T）', '满载']:
        if len(y[i]) == 0:
            continue
        else:
            if len(speed_x_label) == len(y[i]):
                line.add_yaxis("声压——" + i, [j.split('/')[-1] for j in y[i]])
            else:
                right_temp = []
                index4y = 0
                index4x = 0
                while index4y < len(y[i]):
                    temp = y[i][index4y].split('/')
                    while index4x < len(speed_x_label):
                        if temp[1] == speed_x_label[index4x] or speed_x_label[index4x] == re.search(r'\d{2,}', temp[1],
                                                                                                    re.M | re.I).group() + 'km':
                            right_temp.append(temp[-1])
                            index4x += 1
                            break
                        else:
                            right_temp.append(0)
                            index4x += 1
                    index4y += 1

                line.add_yaxis("声压——" + i, right_temp)
    context = {'line_chart': line.render_embed(), 'flag': True}
    return render(request, 'ManageSystem/analyse.html', locals())


def compare(request, ids):
    print(ids)
    id_list = ids.split(".")

    cars = Car.objects.all()
    categories = []
    sound_pressure_list = []
    brand_type = []
    speed_x_label = []
    for id in id_list:
        totalData = Total.objects.get(id=id)
        temp = re.search(r'\d{2,}', str(totalData.condition), re.M | re.I).group() + 'km'
        speed_x_label.append(temp)
        # categories.append(
        #     str(str(total.speed) + '/' + str(total.condition) + '/' + str(total.status) + '/' + str(
        #         total.car.brand) + '/' + str(total.car.model)+'/'+str(total.result)))
        categories.append(
            str(str(totalData.speed) + '/' + temp + '/' + str(totalData.status) + '/' + str(
                totalData.car.brand) + '/' + str(totalData.car.model) + '/' + str(totalData.result)))
        brand_type.append(str(totalData.car.brand) + str(totalData.car.model))

    speed_x_label = list(set(speed_x_label))
    sorted(speed_x_label)
    speed_x_label = speed_x_label[::-1]
    print(categories)
    brand_type = list(set(brand_type))  # 品牌去重
    y = {}
    for i in brand_type:
        y[i] = []
    for i in categories:
        temp = i.split('/')
        brand_temp = temp[-3] + temp[-2]
        y[brand_temp].append([temp[1], temp[-1]])
    print(y)
    print(speed_x_label)
    # 假设categories、sound_pressure_list等变量已定义
    speed_type = '/'.join(set([i.split('/')[0] for i in categories]))
    print(speed_type)
    totalData_type = '声压'
    graph_type = '柱状图对比'
    bar = (
        Bar()
            .add_xaxis(speed_x_label)
            # .add_yaxis("声压", sound_pressure_list, category_gap="50%")
            .reversal_axis()
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                name="速度",
                axislabel_opts=opts.LabelOpts(formatter="{value}"),  # 使用自定义格式化函数
            ),
            xaxis_opts=opts.AxisOpts(
                name="数值",
            ),
            title_opts=opts.TitleOpts(title="{} {} {}".format(speed_type, totalData_type, graph_type),
                                      pos_top="0%",
                                      pos_left="0%")
        )
    )
    for i in y.keys():
        if len(y[i]) == len(speed_x_label):
            bar.add_yaxis(i, [float(j[1]) for j in y[i]], category_gap="50%")
            continue
        else:
            right_temp = []
            for j in speed_x_label:
                temp_flag = True
                for k in y[i]:
                    if k[0] == j:
                        right_temp.append(float(k[1]))
                        temp_flag = False
                        break
                if temp_flag:
                    right_temp.append(0)

            print(right_temp)
            bar.add_yaxis(i, right_temp, category_gap="50%")
    context = {'bar_chart': bar.render_embed(), 'flag': True, 'title': '声压级'}
    return render(request, 'ManageSystem/compare.html', locals())
