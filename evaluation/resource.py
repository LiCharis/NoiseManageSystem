import tablib
from import_export import resources, fields
from import_export.formats import base_formats
from import_export.widgets import ForeignKeyWidget

from car.models import Car
from total.models import Total
from .models import Evaluation


class EvaluationResource(resources.ModelResource):

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
            """
            res[headers.index('品牌')] = Total.objects.get(id=obj.total.id).car.brand
            res[headers.index('型号')] = Total.objects.get(id=obj.total.id).car.model
            res[headers.index('声品质综合评价指数')] = Total.objects.get(id=obj.total.id).index
            data.append(res)
        self.after_export(queryset, data, *args, **kwargs)

        return data

    brand = fields.Field(
        column_name='品牌',
        attribute='car',
        )

    model = fields.Field(
        column_name='型号',
        attribute='car',
       )

    # 在字段列表里加上这个自定义字段
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

    index = fields.Field(
        column_name='声品质综合评价指数',
        attribute='total',
        widget=ForeignKeyWidget(Total, 'evaluation_result'))

    brand = fields.Field(
        column_name='品牌',
        attribute='car',
        widget=ForeignKeyWidget(Car, 'brand'))

    model = fields.Field(
        column_name='型号',
        attribute='car',
        widget=ForeignKeyWidget(Car, 'model'))

    # 在字段列表里加上这个自定义字段
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

    index = fields.Field(
        column_name='声品质综合评价指数',
        attribute='total',
        widget=ForeignKeyWidget(Total, 'evaluation_result'))

    # 此处可写方法以添加更多功能
    class Meta:
        model = Evaluation
        # fields内的模型字段会被导入导出, exclude内的会被排除在外，如果都不写，默认为模型中的全部字段都要包含。
        fields = ['id', 'brand', 'model', 'speed', 'condition', 'status', 'index']
        # excloud = ()
        # export_order（自定义） 选项设置导出字段的显式顺序，没在这里规定的就按默认顺序排在后面（不能只写一个）(导入不用管顺序)
        export_order = ('id', 'brand', 'speed')
