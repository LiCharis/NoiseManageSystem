from import_export import resources, fields
from import_export.formats import base_formats
from import_export.widgets import ForeignKeyWidget

from car.models import Car
from .models import Evaluation


class EvaluationResource(resources.ModelResource):
    field_list = []

    def __init__(self):
        super(EvaluationResource, self).__init__()
        # 获取模型的字段列表,
        field_list = Evaluation._meta.fields
        # 做成一个{字段名:中文名}的字典，作为成员变量
        self.vname_dict = {i.name: i.verbose_name for i in field_list}
        # 每一个field中包含有name和verbose_name, 直接提取转化为字典
        # 如果导入和导出的表头都需要为中文，只重写get_fields即可

    def get_fields(self, **kwargs):
        fields = super().get_fields(**kwargs)
        for field in fields:
            field_name = self.get_field_name(field)
            # 自定义导出字段里可能有关联关系，但vname_dict肯定没有双下划线，所以必须处理
            if field_name.find("__") > 0:
                # 如果是关联关系的，只取字段名，不找关联，因为关联内容不在vname_dict里
                field_name = field_name.split("__")[0]
            # 如果此字段有verbose_name，就用
            if field_name in self.vname_dict.keys():
                field.column_name = self.vname_dict[field_name]
        return fields

    # 此处可写方法以添加更多功能
    class Meta:
        model = Evaluation
        # fields内的模型字段会被导入导出, exclude内的会被排除在外，如果都不写，默认为模型中的全部字段都要包含。
        fields = ['id', 'brand', 'speed', 'condition', 'status', 'index']

        # excloud = ()
        # export_order（自定义） 选项设置导出字段的显式顺序，没在这里规定的就按默认顺序排在后面（不能只写一个）(导入不用管顺序)
        export_order = ('id', 'brand', 'speed')
