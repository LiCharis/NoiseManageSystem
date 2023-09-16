
# # Register your models here.
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User
# Register your models here.

from django.contrib.admin.templatetags.admin_modify import *
from django.contrib.admin.templatetags.admin_modify import submit_row as original_submit_row






class UserManger(admin.ModelAdmin):
    list_display = ['username', 'name', 'agency', 'department', 'operate']
    list_display_links = None
    search_fields = []
    list_filter = ('username', 'name', 'agency', 'department')
    list_per_page = 5
    list_max_show_all = 5

    @register.inclusion_tag('admin/submit_line.html', takes_context=True)
    def submit_row(context):
        ctx = original_submit_row(context)
        ctx.update({
            'show_save_and_add_another': context.get('show_save_and_add_another', ctx['show_save_and_add_another']),
            'show_save_and_continue': context.get('show_save_and_continue', ctx['show_save_and_continue'])
        })
        return ctx

    # 重写方法屏蔽按钮
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super(UserManger, self).change_view(request, object_id,
                                                       form_url, extra_context=extra_context)


    # 重写查看用户信息返回方法，超级管理员可以查看所有数据，否则只可以看到自己的帐号
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(username=request.user.username)

    # 重写get_action方法，如果不是超级管理员，不能删除（也就是把删除按钮去除）
    def get_actions(self, request):
        actions = super().get_actions(request)
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
        data1 = '{"icon": "fas fa-user-tie","url": "/admin/user/user/%d/change/"}' % (obj.id)
        update_btn = f"""<button onclick='self.parent.app.openTab({data1})'
                                                 class='el-icon-edit el-button el-button--primary el-button--small'>编辑</button>"""

        # 删除按钮
        data2 = '{"icon": "fas fa-user-tie","url": "/user/single_delete/%d"}' % (obj.id)
        delete_btn = f"""<button onclick='self.parent.app.openTab({data2})' 
                                            class='el-icon-delete-solid el-button el-button--danger el-button--small'>删除</button>"""

        html_str = f"<div>{update_btn} {delete_btn}</div>"
        return mark_safe(html_str)


admin.site.register(User, UserManger)