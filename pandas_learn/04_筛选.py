import pandas as pd

df = pd.read_csv("data.csv")

#Filtering = keeping the rows that match a condition

tall_pokemon = df[df["Height"] >= 2]

print(tall_pokemon)
print("="*80)

heavy_pokemon = df[df["Weight"] > 100]
print(heavy_pokemon)
print("="*80)

legendary_pokemon = df[df["Legendary"] == 1] #也可以==True
print(legendary_pokemon)
print("="*80)

"""
pandas 的布尔筛选不能用 Python 普通的 `or / and`，要换成：
或：`|`  （竖线）
与：`&`

并且每个条件必须套括号！
>`or`/`and` 是 Python 原生逻辑运算符
pandas 的 Series 布尔数组不识别，直接报`ValueError: The truth value of a Series is ambiguous.`
"""
water_pokemon=df[(df["Type1"]=="Water") | (df["Type2"]=="Water")]
print(water_pokemon)
print("="*80)

flying_fire_pokemon=df[(df["Type1"]=="Fire") &
                    (df["Type2"]=="Flying")]
print(flying_fire_pokemon)
print("="*80)