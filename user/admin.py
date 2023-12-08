
# # Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation.trans_null import gettext_lazy

from .models import User
# Register your models here.
from django.db.models import Q
from django.contrib.admin.templatetags.admin_modify import *
from django.contrib.admin.templatetags.admin_modify import submit_row as original_submit_row






class UserManger(UserAdmin):
    list_display = ['username', 'name', 'agency', 'department', 'operate']
    list_display_links = None
    search_fields = []
    list_filter = ('username', 'name', 'agency', 'department')
    list_per_page = 10
    list_max_show_all = 10

    fieldsets = (
        (None, {'fields': ('username', 'password', 'email')}),

        (gettext_lazy('个人信息'), {'fields': ('name', 'agency', 'department')}),  # 添加模型里的字段openid

        (gettext_lazy('权限信息'), {'fields': ('is_superuser', 'is_staff', 'is_active',
                                                  'groups',)}),

        (gettext_lazy('日期信息'), {'fields': ('last_login', 'date_joined')}),
    )




    @register.inclusion_tag('admin/submit_line.html', takes_context=True)
    def submit_row(context):
        ctx = original_submit_row(context)
        ctx.update({
            'show_save_and_add_another': context.get('show_save_and_add_another', ctx['show_save_and_add_another']),
            'show_save_and_continue': context.get('show_save_and_continue', ctx['show_save_and_continue'])
        })
        return ctx

    # 重写编辑方法，添加的每个用户都admin上的staff，因为只有这样才能登陆到这个管理站点
    def save_model(self, request, obj, form, change):
        # If creating new article, associate request.user with author.
        if not change:
            obj.is_staff = 1
        super().save_model(request, obj, form, change)


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
             return qs.filter(~Q(username=request.user.username)) #自己看不到自己的数据，避免误操作
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
        #原始方法，但是会打开新页面，修改数据后原页面不刷新不可重复读
        #编辑按钮
        #data1 = "/admin/user/user/%d/change/" %(obj.id)
        data1 = '{"icon": "fas fa-user-tie","url": "/admin/user/user/%d/change/"}' % (obj.id)
        update_btn = f"""<button onclick='self.parent.app.openTab({data1})'
                                                 class='el-icon-edit el-button el-button--primary el-button--small'>编辑</button>"""
        #用js不可行欸
        # data1 = "'{}'".format('/admin/user/user/%d/change/' %(obj.id))
        # update_btn = f"""<button onclick="javascript:jump({data1})" class="el-icon-edit el-button el-button--primary el-button--small">编辑</button>"""

        # data1 = "/admin/user/user/%d/change/" %(obj.id)
        # update_btn = '<a class="btn btn-xs btn-primary" href="{}" rel="external nofollow" >' \
        #              '<input name="通过审核"' \
        #              'type="button" id="passButton" ' \
        #              'title="passButton" value="通过审核">' \
        #              '</a>'.format(data1)

        # 删除按钮
        data2 = '{"icon": "fas fa-user-tie","url": "/user/single_delete/%d"}' % (obj.id)
        delete_btn = f"""<button onclick='self.parent.app.openTab({data2})'
                                            class='el-icon-delete-solid el-button el-button--danger el-button--small'>删除</button>"""
        # delete_btn = '<a  href="{}" rel="external nofollow" >' \
        #           '<input class="el-button el-button--danger el-button--small" name="通过审核"' \
        #           'type="button" id="passButton" ' \
        #           'title="passButton" value="通过审核">' \
        #           '</a>'.format(data1)


        html_str = f"<div>{update_btn}{delete_btn}</div>"
        return mark_safe(html_str)

    class Media:
        js = ('js/jump_get.js',)


admin.site.register(User, UserManger)


