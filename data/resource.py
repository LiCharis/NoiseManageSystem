import tablib
from django.db import models
from django.db.models.fields.files import FieldFile, FileField
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.widgets import Widget
from car.models import Car
from data.models import Data
from total.models import Total


class DataResource(resources.ModelResource):

    def export(self, queryset=None, *args, **kwargs):
        """
        Exports a resource.
        """
        if queryset is None:
            queryset = self.get_queryset()

        headers = self.get_export_headers()
        data = tablib.Dataset(headers=headers)

        for obj in queryset:
            # 获取将要导出的源数据，这里export_resource返回的是列表，便于更改。替换到外键的值
            res = self.export_resource(obj)
            """
            这里是关键，因为本模型没有car属性，因此只能手动写入
            同时因为图片类型的数据会报类型不匹配的问题，这里也得手动写入
            """
            res[headers.index('品牌')] = Total.objects.get(id=obj.total.id).car.brand
            res[headers.index('型号')] = Total.objects.get(id=obj.total.id).car.model
            res[headers.index('图片地址')] = Total.objects.get(id=obj.total.id).data_image.path
            data.append(res)
        self.after_export(queryset, data, *args, **kwargs)

        return data

    brand = fields.Field(
        column_name='品牌',
        attribute='brand')

    model = fields.Field(
        column_name='型号',
        attribute='model')

    speed = fields.Field(
        column_name='速度形式',
        attribute='total',
        widget=ForeignKeyWidget(Total, 'speed'))

    condition = fields.Field(
        column_name='工况',
        attribute='total',
        widget=ForeignKeyWidget(Total, 'condition'))

    status = fields.Field(
        column_name='荷载状态',
        attribute='total',
        widget=ForeignKeyWidget(Total, 'status'))

    first_left = fields.Field(
        column_name='测量次数一AA-BB内最大声压级（左侧）-SPL_L',
        attribute='total',
        widget=ForeignKeyWidget(Total, 'first_left'))

    first_right = fields.Field(
        column_name='测量次数一AA-BB内最大声压级（右侧）-SPL_R',
        attribute='total',
        widget=ForeignKeyWidget(Total, 'first_right'))

    second_left = fields.Field(
        column_name='测量次数二AA-BB内最大声压级（左侧）-SPL_L',
        attribute='total',
        widget=ForeignKeyWidget(Total, 'second_left'))

    second_right = fields.Field(
        column_name='测量次数二AA-BB内最大声压级（右侧）-SPL_R',
        attribute='total',
        widget=ForeignKeyWidget(Total, 'second_right'))

    image = fields.Field(
        column_name='图片地址',
        attribute='total',
    )

    result = fields.Field(
        column_name='声压级最终结果',
        attribute='total',
        widget=ForeignKeyWidget(Total, 'data_result'))

    speed = fields.Field(
        column_name='速度形式',
        attribute='total',
        widget=ForeignKeyWidget(Total, 'speed'))

    condition = fields.Field(
        column_name='工况',
        attribute='total',
        widget=ForeignKeyWidget(Total, 'condition'))

    status = fields.Field(
        column_name='荷载状态',
        attribute='total',
        widget=ForeignKeyWidget(Total, 'status'))

    first_left = fields.Field(
        column_name='测量次数一AA-BB内最大声压级（左侧）-SPL_L',
        attribute='total',
        widget=ForeignKeyWidget(Total, 'first_left'))

    first_right = fields.Field(
        column_name='测量次数一AA-BB内最大声压级（右侧）-SPL_R',
        attribute='total',
        widget=ForeignKeyWidget(Total, 'first_right'))

    second_left = fields.Field(
        column_name='测量次数二AA-BB内最大声压级（左侧）-SPL_L',
        attribute='total',
        widget=ForeignKeyWidget(Total, 'second_left'))

    second_right = fields.Field(
        column_name='测量次数二AA-BB内最大声压级（右侧）-SPL_R',
        attribute='total',
        widget=ForeignKeyWidget(Total, 'second_right'))

    image = fields.Field(
        column_name='图片地址',
        attribute='total',
        widget=ForeignKeyWidget(Total, 'data_image'))

    result = fields.Field(
        column_name='声压级最终结果',
        attribute='total',
        widget=ForeignKeyWidget(Total, 'data_result'))



    # 在字段列表里加上这个自定义字段

    # 此处可写方法以添加更多功能

    class Meta:
        model = Data
        # fields内的模型字段会被导入导出, exclude内的会被排除在外，如果都不写，默认为模型中的全部字段都要包含。
        fields = ['id', 'brand', 'model', 'speed', 'condition', 'status', 'first_left', 'first_right', 'second_left',
                  'second_right',
                  'image', 'result']

        # excloud = ()
        # export_order（自定义） 选项设置导出字段的显式顺序，没在这里规定的就按默认顺序排在后面（不能只写一个）(导入不用管顺序)
        export_order = ('id', 'brand', 'model', 'speed')
