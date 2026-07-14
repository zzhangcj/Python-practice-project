# ## 1.给定字符串 s = " Hello Python World "，
# from idlelib.searchengine import search_reverse
#
# s = "  Hello Python World  "
# # 完成以下操作：
# # 去除字符串首尾空格
# s_strip = s.strip()
# print(s_strip)
# # 将所有字母转为小写，统计字母 o 出现的总次数
# s_lower = s.lower()
# print(s_lower)
# count_o = s_lower.count("o")
# print(count_o)
# # 按空格把字符串分割成单词列表，再用 - 拼接成新字符串
# word_list = s_strip.split()
# s_join = "-".join(word_list)
# print(s_join)
# # 把字符串中的 Python 替换为 Java
# s_replace = s_strip.replace("Python","Java")
# print(s_replace)
# # 用切片实现整个字符串反转\
# s_reverse = s_strip[::-1]
# '''
# [::-1] 三个参数全部用了省略写法，对应逻辑：
# start 省略：步长是 - 1（负数），所以默认从字符串最后一个字符开始
# end 省略：步长是 - 1，所以默认到字符串最开头结束（包含第一个字符）
# step = -1：步长为 - 1，也就是从右往左，每次往前走 1 位
# '''
#
# ##2.判断一个字符串是否是回文字符串（正读和反读完全一致，忽略大小写和非字母数字字符）。
# # 示例：输入 "A man, a plan, a canal: Panama"，返回 True；
# # 输入 "race a car"，返回 False
#
# def is_palindrome(s:str) ->bool:
#     valid = [c.lower() for c in s if c.isalnum()]
#     return valid == valid[::-1]
#
# ##3.给定列表，完成以下操作：
# nums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
# # 在列表末尾添加元素 7，在索引为 2 的位置插入元素 0
# nums.append(7)
# nums.insert(2,0)
# # 删除第一个出现的元素 1，再删除索引为 3 的元素
# nums.remove(1)
# nums.pop(3)
# # 分别实现：列表升序排序、降序排序、反转列表
# nums.sort() #升序
# nums.sort(reverse= True) #降序
# nums.reverse()
# # 用列表推导式筛选出列表中所有大于 3 的偶数
# filter_nums = [x for x in nums if x>3 and x%2==0]

#题 4（进阶高频）
# 实现列表去重，要求两种写法：
# 不保留元素原顺序（一行代码完成）
# 保留元素第一次出现的原顺序
# 示例：输入 [3,1,2,3,2,5]，第一种输出 [1,2,3,5]（顺序不定），第二种输出 [3,1,2,5]
def removeDuplicates(nums): #无序数组版本
    write = 0
    se = set()
    for read in range(len(nums)):
        if nums[read] not in se:
            se.add(nums[read])
            nums[write] = nums[read]
            write+=1
    return write

if __name__ == '__main__':
    nums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    res = removeDuplicates(nums)
    print("不重复的元素个数：",res)
    print("去重后的数组：",nums[:res])



