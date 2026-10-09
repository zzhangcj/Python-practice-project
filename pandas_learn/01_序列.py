import pandas as pd

## 1.以列表为例
data=[100.23,200.3,399.99,278,125]

# 使用列表创建Series，同时自定义索引标签 a‑e
series=pd.Series(data,index=['a','b','c','d','e'])
print(series)

# 通过标签索引loc，获取索引'a'对应的元素值
print(series.loc['a'])

series.loc['b']=999 ## 通过loc标签索引，修改索引'b'位置的元素值为999
print(series)

# 通过数字位置iloc，获取下标为1（第二个）的元素
print(series.iloc[1])

# 索引筛选，取出数值大于等于200的元素
print(series[series >= 200])

print("-" * 50)

## 2.以字典为例子
calories = {"day 1":1234,"day 2":2345,"day 3":1700}
series=pd.Series(calories)
print(series)
print(series.loc["day 1"])
series.loc["day 3"]+=200
print(series.loc["day 3"])

print(series[series >= 2000])