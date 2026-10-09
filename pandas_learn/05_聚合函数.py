import pandas as pd

df = pd.read_csv("data.csv")


##1. Whole dataframe
#平均
print(df.mean(numeric_only=True))
print("-"*50)
"""对整个表格中所有数值列计算平均值
numeric_only=True只计算数字列，跳过字符串列(Name、Type1、Type2)
"""

#求和
print(df.sum(numeric_only=True))
print("-"*50)

#最小值
print(df.min(numeric_only=True))
print("-"*50)

#计数：统计每一列的非空有效数据的数量；NaN空值不会计数
print(df.count())
print("-"*50)

#Type2         67
#这是因为不是所有的宝可梦都有第二属性

##2. Single dataframe 单独选取某一列做统计

#
print(df["Height"].mean())
print("-"*50)

#
print(df["Height"].sum())
print("-"*50)

#
print(df["Height"].max())
print("-"*50)

#
print(df["Height"].count()) #150
print(df["Type2"].count()) #67
print("-"*50)

##3. groupby 分组聚合统计
group=df.groupby("Type1")

print(group["Height"].mean())
print("-"*50)
print(group["Height"].sum())
print("-"*50)
print(group["Height"].count())
print("-"*50)