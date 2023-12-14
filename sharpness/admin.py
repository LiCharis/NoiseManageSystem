# Register your models here.
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from import_export.admin import ExportMixin, ExportActionModelAdmin
from import_export.formats import base_formats

from ManageSystem.settings import MEDIA_URL
from total.models import Total
from .models import Sharpness
# Register your models here.

from django.contrib.admin.templatetags.admin_modify import *
from django.contrib.admin.templatetags.admin_modify import submit_row as original_submit_row

from .resource import SharpnessResource


@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def submit_row(context):
    ctx = original_submit_row(context)
    ctx.update({
        'show_save_and_add_another': context.get('show_save_and_add_another', ctx['show_save_and_add_another']),
        'show_save_and_continue': context.get('show_save_and_continue', ctx['show_save_and_continue'])
    })
    return ctx


class SharpnessManger(ExportActionModelAdmin, admin.ModelAdmin):

    # # 限定格式为xlsx
    # def get_export_formats(self):  # 该方法是限制格式
    #     formats = (
    #         base_formats.XLSX,
    #     )
    #     return [f for f in formats if f().can_export()]

    # 对接资源类

    resource_class = SharpnessResource

    list_display = ['car', 'status', 'speed', 'condition', 'left', 'right', 'showFig', 'operate']
    list_display_links = None
    search_fields = []
    list_filter = ('total__car', 'total__speed', 'total__status', 'total__condition')
    list_per_page = 10
    list_max_show_all = 10

    @admin.display(description='汽车', ordering='id')
    def car(self, obj):
        obj = Total.objects.get(id=obj.total_id)
        return "%s%s" % (obj.car.brand, obj.car.model)

    @admin.display(description='荷载状态', ordering='id')
    def status(self, obj):
        obj = Total.objects.get(id=obj.total_id)
        return "%s" % (obj.status)

    @admin.display(description='工况', ordering='id')
    def condition(self, obj):
        obj = Total.objects.get(id=obj.total_id)
        return "%s" % (obj.condition)

    @admin.display(description='速度形式', ordering='id')
    def speed(self, obj):
        obj = Total.objects.get(id=obj.total_id)
        return "%s" % (obj.speed)

    @admin.display(description='尖锐度左耳-acum%', ordering='id')
    def left(self, obj):
        obj = Total.objects.get(id=obj.total_id)
        return "%s" % (obj.sharpness_left)

    @admin.display(description='尖锐度右耳-acum', ordering='id')
    def right(self, obj):
        obj = Total.objects.get(id=obj.total_id)
        return "%s" % (obj.sharpness_right)


    # 重写方法屏蔽按钮
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super(SharpnessManger, self).change_view(request, object_id,
                                                        form_url, extra_context=extra_context)

    # 重写get_action方法，如果不是超级管理员，不能删除（也就是把删除按钮去除）
    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if 'operate' in self.list_display:
                self.list_display.remove('operate')
        else:

            if 'operate' not in self.list_display:
                self.list_display.append('operate')
        return actions

    def has_add_permission(self, request):
        return False

    # 禁用删除
    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description='声品质彩图', ordering='id')
    def showFig(self, obj):
        if not obj.total.sharpness_image == " ":
            page_url = "/sharpness/get_image/%d" % (obj.id)
            image_url = (MEDIA_URL + obj.total.sharpness_image.name)
        else:
            page_url = ""
            image_url = ""
        return format_html(
            '<a title="点击放大" href="{}"><img alt="文件未上传" src="{}" style="width:50px;height:40px;"/></a>'.format(
                page_url,
                image_url))

    # 定义一些操作示例
    @admin.display(description='操作', ordering='id')
    def operate(self, obj):
        # 编辑按钮
        data1 = '{"icon": "fas fa-user-tie","url": "/admin/sharpness/sharpness/%d/change/"}' % (obj.id)
        update_btn = f"""<button onclick='self.parent.app.openTab({data1})'
                                                 class='el-icon-edit el-button el-button--primary el-button--small'>编辑</button>"""

        # 删除按钮
        data2 = '{"icon": "fas fa-user-tie","url": "/sharpness/single_delete/%d"}' % (obj.id)
        delete_btn = f"""<button onclick='self.parent.app.openTab({data2})'
                                            class='el-icon-delete-solid el-button el-button--danger el-button--small'>删除</button>"""

        html_str = f"<div>{update_btn} {delete_btn}</div>"
        return mark_safe(html_str)

    # 添加按钮

    actions = ['analyse', 'compare']

    @admin.display(description='详细信息', ordering='id')
    def detail(self, obj):

        show_link = "<a href='/data/get_details/%d'>查看</a>" % (obj.id)

        return mark_safe(f"{show_link}")

    # 这里应该发送一个get请求给后端返回页面，然后页面快速发送ajax请求给后端同一个view（用get，post区分开）
    # 然后后端

    # detail.action_type = 1
    # detail.action_url = '/data/get_detail/' + str(selected_id)

    # 按钮的点击事件
    def output(self, request):
        return True

    # 按钮的配置
    output.short_description = '导出'
    output.icon = 'el-icon-download'
    output.type = 'primary'
    output.style = 'color:rainbow;'
    output.action_type = 1
    output.action_url = ''

    # 链接按钮，设置之后直接访问该链接
    # 3中打开方式
    # action_type 0=当前页内打开，1=新tab打开，2=浏览器tab打开
    # 设置了action_type，不设置url，页面内将报错
    # 设置成链接类型的按钮后，custom_button方法将不会执行。

    def analyse(self, request, queryset):
        print("hello")
        selected = queryset.values_list('pk', flat=True)
        return HttpResponseRedirect("/sharpness/analyse/{}".format('.'.join(str(pk) for pk in selected)))

    # analyse.layer = {
    #     # 弹出层中的输入框配置
    #     # 这里指定对话框的标题
    #     'title': '数据分析',
    #     # 提示信息
    #     'tips': '数据分析的弹出表单',
    #     # 弹出层对话框的宽度，默认50%
    #     'width': '95%',
    #     # 表单中 label的宽度，对应element-ui的 label-width，默认80px
    #     'labelWidth': "80px",
    #     # 确认按钮显示文本
    #     'confirm_button': '确认提交',
    #     # 取消按钮显示文本
    #     'cancel_button': '取消',
    #
    #     'url': "http://www.baidu.com",
    #     'params': [{
    #         'type': 'select',
    #         'key': 'type',
    #         'label': '选择分析参数',
    #         'width': '200px',
    #         # size对应elementui的size，取值为：medium  small  mini
    #         'size': 'medium',
    #         # value字段可以指定默认值
    #         'value': '0',
    #         'options': [{
    #             'key': '0',
    #             'label': '11'
    #         }, {
    #             'key': '1',
    #             'label': '22'
    #         }]
    #     },
    #         {
    #             'type': 'select',
    #             'key': 'type',
    #             'label': '选择动力形式',
    #             'width': '200px',
    #             # size对应elementui的size，取值为：medium  small  mini
    #             'size': 'small',
    #             # value字段可以指定默认值
    #             'value': '1',
    #             'options': [{
    #                 'key': '0',
    #                 'label': '11'
    #             }, {
    #                 'key': '1',
    #                 'label': '22'
    #             }]
    #         }
    #     ]}
    analyse.short_description = '数据分析（折线图）'
    analyse.icon = 'el-icon-s-data'
    analyse.type = 'warning'
    analyse.style = 'color:rainbow;'

    # analyse.action_type = 1
    # analyse.action_url = '/data/get_analyse'

    def compare(self, request, queryset):
        # 获得被打钩的checkbox对应的对象id的列表
        selected = queryset.values_list('pk', flat=True)
        return HttpResponseRedirect("/sharpness/compare/{}".format('.'.join(str(pk) for pk in selected)))

    # dict = {}
    # url = 'http://127.0.0.1:8000/data/get_ids/'
    #
    # for obj in queryset:
    #     dict.update({"key" + str(obj.id): str(obj.id)})
    #
    # print(queryset)
    #
    # params = json.dumps(dict)
    # requests.post(url, data=params)
    # return True

    compare.short_description = '数据对比（柱状图）'
    compare.icon = 'el-icon-s-opportunity'
    compare.type = 'danger'
    compare.style = 'color:rainbow;'
    # compare.action_type = 1
    # compare.action_url = '/data/get_analyse'


admin.site.register(Sharpness, SharpnessManger)
