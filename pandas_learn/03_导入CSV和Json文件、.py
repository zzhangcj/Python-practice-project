import pandas as pd
# #
# df = pd.read_json("poke.json")
# print(df)

# 读取csv，先全部读入
df = pd.read_csv("data.csv")

"""
`.tolist()`：把 pandas 的 Index/Series 对象，转换成普通 Python 列表 list

`df["Height"]` 是一个 Series 对象

如果直接写 `print(df["Height"])`：pandas 会自动精简输出，数据很多的时候，中间内容会被省略，显示省略号 `...`
`.to_string()`：把 Series / DataFrame 完整转换成字符串文本，全部内容输出，不会省略中间行，打印到控制台看完整内容。
"""

print("===== 当前csv全部列名 =====")
print(df.columns.tolist())
print("="*60)

# ✅ 读完之后再设置索引
df = df.set_index("Name")

# ========== 按列选取 ==========
print("=== 单列 Height ===")
print(df["Height"].to_string())
print("="*60)

print("=== 多列：Height, Weight ===")
print(df[["Height","Weight"]].to_string())
print("="*60)

# ========== loc：按索引名字（宝可梦名称）查询 ==========
print("=== loc 查询 Pikachu ===")
print(df.loc["Pikachu"])
print("="*60)

# loc[行, [列列表]]  注意逗号位置！
print("=== loc 查询 Charizard，只看Height、Weight ===")
print(df.loc["Charizard", ["Height","Weight"]])
print("="*60)

# ========== iloc：数字下标，0开始，start:end:step ==========
print("=== iloc 行0‑10，步长2，全部列 ===")
print(df.iloc[0:11:2])
print("="*60)

print("=== iloc 行0‑10步长2，取前4列 ===")
print(df.iloc[0:11:2, 0:4])
print("="*60)

# ========== 用户输入宝可梦名字查询，捕获不存在异常 ==========
pokemon = input("Enter a Pokemon Name: ")
try:
    print("="*60)
    print(df.loc[pokemon])
except KeyError:
    print(f"{pokemon} is not in the DataFrame")




