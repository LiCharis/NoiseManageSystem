import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


file_path = '通过噪声声压级数据.xlsx'  # 将 'your_excel_file.xlsx' 替换为你的 Excel 文件路径

# 创建 ExcelFile 对象
xls = pd.ExcelFile(file_path)

# 获取所有工作表的名称
sheet_names = xls.sheet_names

# 打印所有工作表的名称
for sheet_name in sheet_names:
    print(sheet_name)
