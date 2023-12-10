import json

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from ManageSystem.settings import MEDIA_URL
from .models import Sharpness
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

            obj = Sharpness.objects.get(id=duty_id).__dict__
            print(obj)

        except Exception as e:
            print('delete error is %s' % (e))

        return render(request, 'ManageSystem/delete.html', locals())


    elif request.method == 'POST':

        if request.POST.get('cancel'):
            print(request.POST['cancel'])
            return HttpResponseRedirect("/admin/sharpness/sharpness")

        try:
            print("delete_true_view")
            print(duty_id)
            Sharpness.objects.get(id=duty_id).delete()

        except Exception as e:
            print('delete error is %s' % (e))
            return HttpResponse('--The note id is error')

    return HttpResponseRedirect("/admin/sharpness/sharpness")


def get_ids(request):
    if request.method == 'GET':
        ids = request.GET.get('ids')
        model = request.GET.get('model')
        print(ids)
        print(model)
        id_list = ids.split(",")
        request.session['sharpness_ids'] = id_list
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
        request.session['sharpness_fields'] = json_dict
        print(request.session.get('sharpness_ids'))
        print(request.session.get('sharpness_fields'))
        ids = []

        for i in request.session['sharpness_ids']:
            ids.append(int(i))

        info = []

        datas = Sharpness.objects.filter(id__in=ids)
        print(datas)

        for obj in datas:
            fields = {"id": obj.id}
            for k, v in request.session.get('sharpness_fields').items():
                fields.update({v: getattr(obj, v)})

            info.append(fields)

    result = {"code": 200, "mes": info}

    # 这里就根据前端给的字段对应的数据返回数据

    return JsonResponse(result)


def get_image(request, id):
    if not id:
        return HttpResponse('请求异常')

    if request.method == 'GET':
        action = '/admin/sharpness/sharpness'
        try:
            obj = Sharpness.objects.get(id=id)
            url = MEDIA_URL + str(obj.image)
            dataname = '尖锐度'


        except Exception as e:
            print(e)

        return render(request, 'ManageSystem/showImage.html', locals())

def analyse(request, ids):
    print(ids)
    id_list = ids.split(".")

    categories = []
    sharpness_left = []
    sharpness_right = []
    speed_x_label = []
    y = {'空载':[],'半载':[],'3/4额定载荷（24T）':[],'满载':[]}
    for id in id_list:
        sharpness = Sharpness.objects.get(id=id)
        categories.append(
            str(str(sharpness.speed) + '/' + str(sharpness.condition) + '/' + str(sharpness.status) + '/' + str(
                sharpness.car.brand) + '/' + str(sharpness.car.model)))
        y[str(sharpness.status)].append(str(str(sharpness.speed) + '/' + str(sharpness.condition) + '/' + str(sharpness.status) + '/' + str(
                sharpness.car.brand) + '/' + str(sharpness.car.model))+'/'+str(sharpness.left)+'/'+str(sharpness.right))
        flag = True
        temp = re.search( r'\d{2,}', str(sharpness.condition), re.M|re.I).group()+'km'
        for i in speed_x_label:
            if temp == i:
                flag = False
        if flag:        
            speed_x_label.append(temp)
        sharpness_left.append(sharpness.left)
        sharpness_right.append(sharpness.right)

    # print(categories)
    car_type = str(set([''.join(i.split('/')[-2:]) for i in categories]))[2:-2]
    print(car_type)
    speed_type = '/'.join(set([i.split('/')[0] for i in categories]))
    print(speed_type)
    data_type = '尖锐度'
    graph_type = '折线对比'
    print(speed_x_label)
    print(categories)

    print(sharpness_left)
    print(sharpness_right)
    line = (
        Line()
        .add_xaxis(speed_x_label)
        # .add_yaxis("尖锐度左耳", sharpness_left)
        # .add_yaxis("尖锐度右耳", sharpness_right)
        # .reversal_axis()
        .set_global_opts(
            title_opts=opts.TitleOpts(title="{} {} {} {}".format(car_type,speed_type,data_type,graph_type),
                pos_top="5%",
                pos_left="0%",),
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
    #         line.add_yaxis("尖锐度左耳——"+i,[j.split('/')[-2] for j in y[i]])
    #         line.add_yaxis("尖锐度右耳——"+i,[j.split('/')[-1] for j in y[i]])
    for i in ['空载','半载','3/4额定载荷（24T）','满载']:
        if len(y[i])==0:
            continue
        else:
            if len(speed_x_label) == len(y[i]):
                line.add_yaxis("尖锐度左耳——"+i,[j.split('/')[-2] for j in y[i]])
                line.add_yaxis("尖锐度右耳——"+i,[j.split('/')[-1] for j in y[i]])
            else:      
                left_temp = []
                right_temp = []         
                index4y = 0
                index4x = 0
                while index4y<len(y[i]):
                    temp = y[i][index4y].split('/')
                    while index4x<len(speed_x_label):
                        if temp[1] == speed_x_label[index4x] or speed_x_label[index4x] == re.search(r'\d{2,}', temp[1], re.M|re.I).group()+'km':
                            left_temp.append(temp[-2])
                            right_temp.append(temp[-1])
                            index4x += 1
                            break
                        else:
                            left_temp.append(0)
                            right_temp.append(0)
                            index4x += 1
                    index4y += 1
                
                line.add_yaxis("尖锐度左耳——"+i,left_temp)
                line.add_yaxis("尖锐度右耳——"+i,right_temp)
    context = {'line_chart': line.render_embed(), 'flag': True}
    action = '/admin/sharpness/sharpness'
    return render(request, 'ManageSystem/analyse.html', locals())


def compare(request, ids):
    id_list = ids.split(".")
    categories = []
    sharpness_left = []
    sharpness_right = []

    brand_type = []
    speed_x_label = []
    for id in id_list:
        sharpness = Sharpness.objects.get(id=id)
        temp = re.search( r'\d{2,}', str(sharpness.condition), re.M|re.I).group()+'km'
        speed_x_label.append(temp)
        categories.append(
            str(str(sharpness.speed) + '/' + temp + '/' + str(sharpness.status) + '/' + str(
                sharpness.car.brand) + '/' + str(sharpness.car.model)+'/'+str(sharpness.left)+'/'+str(sharpness.right)))
        brand_type.append(str(sharpness.car.brand) + str(sharpness.car.model))
        
        # sharpness_left.append(sharpness.left)
        # sharpness_right.append(sharpness.right)
    speed_x_label = list(set(speed_x_label))
    sorted(speed_x_label)
    speed_x_label = speed_x_label[::-1]
    print(categories)
    brand_type = list(set(brand_type)) # 品牌去重
    y = {}
    for i in brand_type:
        y[i] = []
    for i in categories:
        temp = i.split('/')
        brand_temp = temp[-4]+temp[-3]
        y[brand_temp].append([temp[1],temp[-2],temp[-1]])
    print(y)
    print(speed_x_label)
    # 假设categories、sound_pressure_list等变量已定义
    speed_type = '/'.join(set([i.split('/')[0] for i in categories]))
    print(speed_type)
    data_type = '尖锐度'
    graph_type = '柱状图对比'
    bar = (
        Bar()
        .add_xaxis(speed_x_label)
        # .add_yaxis("尖锐度左耳", sharpness_left)
        # .add_yaxis("尖锐度右耳", sharpness_right)
        .reversal_axis()
        .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                name="速度",
                axislabel_opts=opts.LabelOpts(formatter="{value}", interval=0),  # 使用自定义格式化函数
            ),
            xaxis_opts=opts.AxisOpts(
                name="数值",
            ),
            title_opts=opts.TitleOpts(title="{} {} {}".format(speed_type,data_type,graph_type),
            pos_top="0%",
            pos_left="0%")
        )
    )
    for i in y.keys():
        if len(y[i])==len(speed_x_label):
            bar.add_yaxis(i+'——尖锐度左耳', [float(j[1]) for j in y[i]], category_gap="50%")
            bar.add_yaxis(i+'——尖锐度右耳', [float(j[2]) for j in y[i]], category_gap="50%")
            continue
        else:
            left_temp = []
            right_temp = []
            for j in speed_x_label:
                temp_flag = True
                for k in y[i]:
                    if k[0] == j:
                        left_temp.append(float(k[1]))
                        right_temp.append(float(k[2]))
                        temp_flag=False
                        break
                if temp_flag:
                    right_temp.append(0)
            print(left_temp)            
            print(right_temp)
            bar.add_yaxis(i+'——尖锐度左耳', left_temp, category_gap="50%")
            bar.add_yaxis(i+'——尖锐度右耳', right_temp, category_gap="50%")
    context = {'bar_chart': bar.render_embed(), 'flag': True, 'title': '尖锐度'}
    action = '/admin/sharpness/sharpness'
    return render(request, 'ManageSystem/compare.html', locals())
