# Register your models here.
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.http import HttpResponseRedirect

from django.utils.safestring import mark_safe

# Register your models here.

from django.contrib.admin.templatetags.admin_modify import *
from django.contrib.admin.templatetags.admin_modify import submit_row as original_submit_row
from import_export.admin import ExportMixin, ExportActionModelAdmin
from import_export.formats import base_formats

from clarity.models import Clarity
from data.models import Data
from evaluation.models import Evaluation
from loudness.models import Loudness
from sharpness.models import Sharpness
from total.models import Total
from total.resource import TotalResource
from volatility.models import Volatility


@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def submit_row(context):
    ctx = original_submit_row(context)
    ctx.update({
        'show_save_and_add_another': context.get('show_save_and_add_another', ctx['show_save_and_add_another']),
        'show_save_and_continue': context.get('show_save_and_continue', ctx['show_save_and_continue'])
    })
    return ctx


class TotalManger(ExportActionModelAdmin, admin.ModelAdmin):

    # # 限定格式为xlsx
    # def get_export_formats(self):  # 该方法是限制格式
    #     formats = (
    #         base_formats.XLSX,
    #     )
    #     return [f for f in formats if f().can_export()]

    # 对接资源类
    resource_class = TotalResource

    list_display = ['car', 'status', 'speed', 'condition', 'data_result', 'clarity_left',
                    'clarity_right', 'clarity_result', 'loudness_left', 'loudness_right',
                    'loudness_result', 'sharpness_left', 'sharpness_right', 'sharpness_result',
                    'volatility_left', 'volatility_right', 'volatility_result', 'index']
    list_display_links = None
    search_fields = []
    list_filter = ('car', 'speed', 'status', 'condition')
    list_per_page = 10
    list_max_show_all = 10

    selected_id = []

    # 重写方法屏蔽按钮
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super(TotalManger, self).change_view(request, object_id,
                                                    form_url, extra_context=extra_context)

    # # 重写编辑方法，将作为外键的用户选项自动填为当前登录用户
    # def save_model(self, request, obj, form, change):
    #     # If creating new article, associate request.user with author.
    #     if not change:
    #         loudness_obj = Loudness.objects.get()
    #     super().save_model(request, obj, form, change)

    # # 重写查看返回方法，超级管理员可以查看所有数据，否则只可以看到自己创建的数据
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(user=request.user)

    # 重写get_action方法，如果不是超级管理员，不能操作
    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if not request.user.is_superuser:
    #         if 'operate' in self.list_display:
    #             self.list_display.remove('operate')
    #     else:
    #
    #         if 'operate' not in self.list_display:
    #             self.list_display.append('operate')
    #     return actions

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    # 禁用删除
    def has_delete_permission(self, request, obj=None):
        return False

    # @admin.display(description='声品质彩图', ordering='id')
    # def showFig(self, obj):
    #     picture = '{"icon": "fas fa-user-tie","url": "/static/images/头像.jpg"}'
    #     show_btn = f"""<button onclick='self.parent.app.openTab({picture})'
    #                                          class='el-icon-picture el-button el-button--warning el-button--small'>查看</button>"""
    #     return mark_safe(f"<div>{show_btn}</div>")

    # 定义一些操作示例
    @admin.display(description='操作', ordering='id')
    def operate(self, obj):
        # 编辑按钮
        data1 = '{"icon": "fas fa-user-tie","url": "/admin/total/total/%d/change/"}' % (obj.id)
        update_btn = f"""<button onclick='self.parent.app.openTab({data1})'
                                     class='el-icon-edit el-button el-button--primary el-button--small'>编辑</button>"""

        # data1 = "/admin/data/data/%d/change/" % (obj.id)

        # update_btn = '<a class="el-icon-edit el-link--primary"   href="{}">编辑</a>'.format(data1)
        # update_btn = "<button onclick='window.location.href=%s' class='el-icon-edit el-button el-button--primary el-button--small'>编辑</button>" %(data1)

        # 删除按钮
        data2 = '{"icon": "fas fa-user-tie","url": "/total/single_delete/%d"}' % (obj.id)
        # data2 = "/data/single_delete/%d" % (obj.id)
        delete_btn = f"""<button onclick='self.parent.app.openTab({data2})'
                                class='el-icon-delete-solid el-button el-button--danger el-button--small'>删除</button>"""
        # delete_btn = '<a class="el-icon-delete-solid el-link--danger"  href="{}">删除</a>'.format(data2)

        html_str = f"<div>{update_btn} {delete_btn}</div>"
        return mark_safe(html_str)

    # 添加按钮
    actions = ['preview']

    @admin.display(description='声压级结果', ordering='id')
    def data(self, obj):
        data_obj = Data.objects.get(id=obj.loudness)
        return "%s  |  %s|  %s|  %s" % (data_obj.speed, data_obj.condition, data_obj.status, data_obj.result)

    @admin.display(description='响度', ordering='id')
    def loudness(self, obj):
        loudness_obj = Loudness.objects.get(id=obj.loudness)

        return "%s  |  %s|  %s" % (loudness_obj.left, loudness_obj.right, loudness_obj.result)

    @admin.display(description='尖锐度', ordering='id')
    def sharpness(self, obj):
        sharpness_obj = Sharpness.objects.get(id=obj.sharpness)

        return "%s  |  %s|  %s" % (sharpness_obj.left, sharpness_obj.right, sharpness_obj.result)

    @admin.display(description='波动度', ordering='id')
    def volatility(self, obj):
        volatility_obj = Volatility.objects.get(id=obj.volatility)

        return "%s  |  %s|  %s" % (volatility_obj.left, volatility_obj.right, volatility_obj.result)

    @admin.display(description='语音清晰度', ordering='id')
    def clarity(self, obj):
        clarity_obj = Clarity.objects.get(id=obj.clarity)

        return "%s  |  %s|  %s" % (clarity_obj.left, clarity_obj.right, clarity_obj.result)

    @admin.display(description='声品质综合评价指数', ordering='id')
    def evaluation(self, obj):
        evaluation_obj = Evaluation.objects.get(id=obj.evaluation)

        return "%s" % (evaluation_obj.index)

    @admin.display(description='声压级结果', ordering='id')
    def data(self, obj):
        data_obj = Data.objects.get(id=obj.loudness)
        return "%s  |  %s|  %s|  %s" % (data_obj.speed, data_obj.condition, data_obj.status, data_obj.result)

    @admin.display(description='响度', ordering='id')
    def loudness(self, obj):
        loudness_obj = Loudness.objects.get(id=obj.loudness)

        return "%s  |  %s|  %s" % (loudness_obj.left, loudness_obj.right, loudness_obj.result)

    @admin.display(description='尖锐度', ordering='id')
    def sharpness(self, obj):
        sharpness_obj = Sharpness.objects.get(id=obj.sharpness)

        return "%s  |  %s|  %s" % (sharpness_obj.left, sharpness_obj.right, sharpness_obj.result)

    @admin.display(description='波动度', ordering='id')
    def volatility(self, obj):
        volatility_obj = Volatility.objects.get(id=obj.volatility)

        return "%s  |  %s|  %s" % (volatility_obj.left, volatility_obj.right, volatility_obj.result)

    @admin.display(description='语音清晰度', ordering='id')
    def clarity(self, obj):
        clarity_obj = Clarity.objects.get(id=obj.clarity)

        return "%s  |  %s|  %s" % (clarity_obj.left, clarity_obj.right, clarity_obj.result)

    @admin.display(description='声品质综合评价指数', ordering='id')
    def evaluation(self, obj):
        evaluation_obj = Evaluation.objects.get(id=obj.evaluation)

        return "%s" % (evaluation_obj.index)

    # 这里应该发送一个get请求给后端返回页面，然后页面快速发送ajax请求给后端同一个view（用get，post区分开）
    # 然后后端

    # detail.action_type = 1
    # detail.action_url = '/data/get_detail/' + str(selected_id)

    # 按钮的点击事件
    def preview(self, request):
        print("=====hello====")
        return HttpResponseRedirect('/total/get_preview')

    # 按钮的配置
    preview.short_description = '预览'
    preview.icon = 'el-icon-download'
    preview.type = 'primary'
    preview.style = 'color:rainbow;'
    preview.action_type = 1
    preview.action_url = ''
    preview.action_url = '/total/get_preview'

    # 链接按钮，设置之后直接访问该链接
    # 3中打开方式
    # action_type 0=当前页内打开，1=新tab打开，2=浏览器tab打开
    # 设置了action_type，不设置url，页面内将报错
    # 设置成链接类型的按钮后，custom_button方法将不会执行。

    def analyse(self, request):
        print("hello")
        return True

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
    analyse.short_description = '数据分析'
    analyse.icon = 'el-icon-s-data'
    analyse.type = 'warning'
    analyse.style = 'color:rainbow;'

    # analyse.action_type = 1
    # analyse.action_url = '/data/get_analyse'

    def compare(self, request, queryset):
        # 获得被打钩的checkbox对应的对象id的列表

        selected = queryset.values_list('pk', flat=True)

        # 获取对应的模型

        ct = ContentType.objects.get_for_model(queryset.model)
        print(selected)  # 选择的数据
        print(ct.pk)  # id号

        # 构造访问的url，使用GET方法，跳转到相应的页面
        return HttpResponseRedirect('/data/get_ids?model=%s&ids=%s' % (

            ct,

            ','.join(str(pk) for pk in selected),

        ))

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

    compare.short_description = '数据对比'
    compare.icon = 'el-icon-s-opportunity'
    compare.type = 'danger'
    compare.style = 'color:rainbow;'
    # compare.action_type = 1
    # compare.action_url = '/data/get_analyse'


admin.site.register(Total, TotalManger)
