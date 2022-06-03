import pandas as pd
import numpy as np

# path = r"F:\20211124长寿农村道路\纬地\黄水路-20220321新增\每公里土石方数量表1.xlsx"
# data = pd.read_excel(path, header=[3, 4, 5])
# # pd.set_option("display.max_colwidth", 1000)
# # # 显示所有列
# # pd.set_option('display.max_columns', 8)
# # #显示所有行
# # pd.set_option('display.max_rows',None)
# # data.iloc[:, 2:]
# print(data.head())
# print(data.columns)
# data_new = data.columns.levels[0].str.replace(" ", "")
# print(data_new)
# for i in range(2):
#     data = data.rename(columns=lambda x:str.replace(x, " ", ""), level=i)
# print(data.columns.levels[0])
# print(data.columns)

# colindex = data.columns.levels[0]
# data.set_axis(list(range(27)), axis='columns')
# print(data.columns.levels[0][0])
# for co in colindex:
#     print(co)
# print(data.head())
# print(list(range(27)))
# print(len(data.columns))

# cols = data.columns
# new_cols = []
# for c in cols:
#     new_cols.append(list(c))
# print(new_cols)
# index = pd.MultiIndex.from_product(new_cols)
# data.columns = index
# print(data.columns)

# df = pd.DataFrame([[1, 2], [4, 5], [7, 8]],
#      index=['cobra', 'viper', 'sidewinder'],
#      columns=['max_speed',  'shield'])
# dft = df.loc['viper']
# print(dft)

# tuples = [
#    ('cobra', 'mark i'), ('cobra', 'mark ii'),
#    ('sidewinder', 'mark i'), ('sidewinder', 'mark ii'),
#    ('viper', 'mark ii'), ('viper', 'mark iii')
# ]
# index = pd.MultiIndex.from_tuples(tuples)
# values = [[12, 2], [0, 4], [10, 20],
#         [1, 4], [7, 1], [16, 36]]
# df = pd.DataFrame(values, columns=[(1, 'max_speed'), 'shield'], index=index)
# # df.columns[0]="1"
# # print(df.columns[0])
# print(df)
# print(df.index)
# print(index.levels[0])
# print(index.set_levels(index.levels[0]+"1", level=0))
# # print(df.index.set_levels([1,2,3,4], level = 1))
# # print(df)

# l = [[1, 2, 3], [1, None, 4], [2, 1, 3], [1, 2, 2]]
# df = pd.DataFrame(l, columns=["a", "b", "c"])
# print(df)
# print(df.groupby(by=["b"]).sum())

# var = 'abcd'
# # s = pd.Series(['abcd', 'efg', 'hi'])
# s = pd.Series([{1: 'temp_1', 2: 'temp_2'}, ['a', 'b'], 0.5, 'my_string'])
# # s.str[1]
# print(s)
# print(s.str[1])
# # print(list(range(11)[-1:0:-2]))
#
# print(s.astype('string'))
# print(s.astype('string').str[1])

s1 = pd.Series(['a','b'])
s2 = pd.Series(['cat','dog'])
s1.str.cat(s2,sep='-')
s2.index = [1, 2]
print(s1)
print(s2)
print(s1.str.cat(s2, sep='-', na_rep='?', join='outer'))