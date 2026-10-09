import pandas as pd

'''数据帧的含义
DataFrame（数据帧）是 pandas 最核心的数据结构
可以理解成一张二维表格,就像 Excel 的工作表

✅ Series（序列）：一维，就单独一列
✅ DataFrame（数据帧）：二维，多行 + 多列；
DataFrame 的每一列本质就是一个 Series
'''

data={"name":["Spongebob","zmjjkk","Squidward"],
      "age":[21,22,23],
}

df = pd.DataFrame(data,index=["Employee 1","Employee 2","Employee 3"])

print(df)
print("-"*30)
print(df.loc["Employee 1"])
print("-"*30)
print(df.iloc[1])

#add a new column
df["job"]=["cook","N/A","cashier"]
print(df)
print("-"*30)

#add a new row
new_rows=pd.DataFrame([{"name":"sandy","age":25,"job":"engineer"},
                       {"name":"nobody","age":27,"job":"manager"}],
                     index=["Employee 4","Employee 5"],)
df=pd.concat([df,new_rows])
print(df)
print("-"*30)