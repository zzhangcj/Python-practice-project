import pandas as pd

df = pd.read_csv("data.csv")

# Data cleaning = the process of fixing/removing:
#                 incomplete,incorrect,or irrelevant data.
#                 ~75% of work done with Pandas is data cleaning.

# 1.Drop irrelevant columns

df = df.drop(columns=["Legendary","No"]) #由于删除这一列之后会生成新的表
print(df)
print("="*50)

# 2.Handle missing data

#(1)直接删除dropna
df = df.dropna(subset=["Type2"])
print(df.to_string())
print("="*50)

#(2)替代fillna
df = df.fillna({"Type2": "None"})
print(df.to_string())
print("="*50)
#`fillna` 传入字典参数时，字典需要用大括号 `{}` 包裹

# 3.Fix inconsistent values  修正不一致数据
"""数据不一致
比如 `water` / `Water` / `WATER`（大小写、前后空格、拼写错误）
同一含义但是文本不一样，统计的时候会当成不同类别
"""
df["Type1"] = df["Type1"].replace({"Grass": "GRASS",
                                   "Fire":"FIRE",
                                   "Water":"WATER",}
                                  )
print(df.to_string())
print("="*50)


# 4.Standardize text 标准化
df["Name"]=df["Name"].str.lower()
print(df.to_string())
print("="*50)

# 5.Fix data types 修正数据类型
df["Legendary"]=df["Legendary"].astype(bool)
print(df.to_string())
print("="*50)

# 6.Remove duplicate values 删除重复数据
df = df.drop_duplicates()