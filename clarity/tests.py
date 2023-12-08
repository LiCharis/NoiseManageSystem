def compare(request, ids):
    print(ids)
    id_list = ids.split(".")

    cars = Car.objects.all()
    categories = []
    sound_pressure_list = []
    clarity_left = []
    clarity_right = []
    loudness_left = []
    loudness_right = []
    volatility_left = []
    volatility_right = []

    for id in id_list:
        data = Data.objects.get(id=id)
        categories.append(
            str(str(data.speed) + '/' + str(data.condition) + '/' + str(data.status) + '/' + str(
                data.car.brand) + '/' + str(data.car.model)))

        sound_pressure_list.append(data.result)
        clarity_left.append(data.clarity_left)
        clarity_right.append(data.clarity_right)
        loudness_left.append(data.loudness_left)
        loudness_right.append(data.loudness_right)
        volatility_left.append(data.volatility_left)
        volatility_right.append(data.volatility_right)

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
        from pyecharts import options as opts
        from pyecharts.charts import Bar

        # 假设categories、sound_pressure_list等变量已定义

        bar = (
            Bar()
            .add_xaxis(categories)
            .add_yaxis("声压", sound_pressure_list, category_gap="50%")
            .add_yaxis("响度左耳", loudness_left, category_gap="50%", stack='stack_1')
            .add_yaxis("响度右耳", loudness_right, category_gap="50%", stack='stack_1')
            .add_yaxis("波动度左耳", volatility_left, category_gap="50%", stack='stack_2')
            .add_yaxis("波动度右耳", volatility_right, category_gap="50%", stack='stack_2')
            .add_yaxis("语言清晰度左耳", clarity_left, category_gap="50%", stack='stack_3')
            .add_yaxis("语言清晰度右耳", clarity_right, category_gap="50%", stack='stack_3')
            .reversal_axis()
            .set_global_opts(
                title_opts=opts.TitleOpts(),
                yaxis_opts=opts.AxisOpts(
                    name="车型",
                    axislabel_opts=opts.LabelOpts(formatter="{value}"),  # 使用自定义格式化函数
                ),
                xaxis_opts=opts.AxisOpts(
                    name="数值",
                ),
                legend_opts=opts.LegendOpts(
                    pos_top="0%",
                    pos_left="0%",
                ),
            )
        )

        context = {'bar_chart': bar.render_embed(), 'flag': True}
    return render(request, 'ManageSystem/compare.html', context)
