
# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from ManageSystem.settings import MEDIA_URL

from .models import Loudness
# Register your models here.
from django.contrib.admin.templatetags.admin_modify import *
from django.contrib.admin.templatetags.admin_modify import submit_row as original_submit_row

@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def submit_row(context):
    ctx = original_submit_row(context)
    ctx.update({
        'show_save_and_add_another': context.get('show_save_and_add_another', ctx['show_save_and_add_another']),
        'show_save_and_continue': context.get('show_save_and_continue', ctx['show_save_and_continue'])
        })
    return ctx




class LoudnessManger(admin.ModelAdmin):
    list_display = ['car', 'status', 'speed', 'condition',  'left', 'right', 'showFig', 'operate']
    list_display_links = None
    search_fields = []
    list_filter = ('car', 'speed', 'status', 'left', 'right')
    list_per_page = 7
    list_max_show_all = 7

    # # 重写编辑方法，将作为外键的用户选项自动填为当前登录用户
    # def save_model(self, request, obj, form, change):
    #     # If creating new article, associate request.user with author.
    #     if not change:
    #         loudness_obj = Loudness.objects.get()
    #     super().save_model(request, obj, form, change)



    @admin.display(description='声品质彩图', ordering='id')
    def showFig(self, obj):
        if not obj.image == " ":
            url = (MEDIA_URL + obj.image.name)
        else:
            url = ""
        return format_html(
            '<a title="点击放大" href="{}"><img alt="文件未上传" src="{}" style="width:50px;height:40px;"/></a>'.format(url,
                                                                                                               url))

    # image_tag.action_type = 1
    # image_tag.action_url =

    # @admin.display(description='声品质彩图', ordering='id')
    # def image_tag(self, obj):
    #     #picture = '{"icon": "fas fa-user-tie","url": %s}' % (MEDIA_URL + '/' + obj.image.name)
    #     url = (MEDIA_URL + '/' + obj.image.name)
    #     show_btn = """<button onclick='window.location.href="{}"'
    #             class='el-icon-picture el-button el-button--warning el-button--small'>查看</button>""".format(url)
    #     return mark_safe(f"<div>{show_btn}</div>")


    # 重写方法屏蔽按钮
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super(LoudnessManger, self).change_view(request, object_id,
                                                      form_url, extra_context=extra_context)



    # 重写get_action方法，如果不是超级管理员，不能删除（也就是把删除按钮去除）
    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if not request.user.is_superuser:
                actions.clear()
                if 'operate' in self.list_display:
                    self.list_display.remove('operate')
            else:

                if 'operate' not in self.list_display:
                    self.list_display.append('operate')
        return actions

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    # 禁用删除
    def has_delete_permission(self, request, obj=None):
        return False

    # 定义一些操作示例
    @admin.display(description='操作', ordering='id')
    def operate(self, obj):
        # 编辑按钮
        data1 = '{"icon": "fas fa-user-tie","url": "/admin/loudness/loudness/%d/change/"}' % (obj.id)
        update_btn = f"""<button onclick='self.parent.app.openTab({data1})'
                                             class='el-icon-edit el-button el-button--primary el-button--small'>编辑</button>"""

        # 删除按钮
        data2 = '{"icon": "fas fa-user-tie","url": "/loudness/single_delete/%d"}' % (obj.id)
        delete_btn = f"""<button onclick='self.parent.app.openTab({data2})' 
                                        class='el-icon-delete-solid el-button el-button--danger el-button--small'>删除</button>"""

        html_str = f"<div>{update_btn} {delete_btn}</div>"
        return mark_safe(html_str)


admin.site.register(Loudness, LoudnessManger)