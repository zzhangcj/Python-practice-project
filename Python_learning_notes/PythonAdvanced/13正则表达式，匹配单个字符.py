###一.正则表达式（字符串处理工具）
import re #需要导入re模块
#1.特点
#   （1）语法比较复杂，可读性较差
#   （2）通用性很强，适用多种编程语言
#2.match方法
#（1）核心本质
#   只从字符串【最开头第 0 位】开始匹配，不会向后搜寻,只要开头不满足正则，直接返回 None，不再往后找
#   区别：search 是全字符串任意位置找，match 固定从头
#（2）返回两种结果
#   匹配成功：返回 Match 对象，可用 .group() 取出匹配到的字符串
#   匹配失败：返回 None，不能调用.group ()，调用直接报错

#（3）格式：re.match(pattern,string,flags)
#   pattern匹配正则表达式
#   string 要匹配的字符

res = re.match("冰","冰冰永远18")
print(res)
#<re.Match object; span=(0, 1), match='冰'>
print(res.group()) #冰

re1 = re.match("冰","小冰永远18")
print(re1) #None
# print(re1.group()) #AttributeError: 'NoneType' object has no attribute 'group'
#第一个字不是 冰 会报错
#注意：match是从开始位置匹配，匹配不到就没有，而且匹配的是pattern整体（比如“冰冰”）

###二.匹配单个字符
#1. 符号 .  匹配任意一个字符，除了\n以外        -常用
re2 = re.match('.e',"hello")
print(re2.group()) #he

#2.[]匹配[]中例举的字符                      -常用
re3 = re.match('[he].','ello')
print(re3.group()) #el
re4 = re.match('[1-5]','24351')
print(re4.group()) #2
re5 = re.match('[a-zA-Z][1-57-9]','m8out')
print(re5.group()) #m8

"""
总结
正则 pattern 规则（match 按正则规则匹配开头）
① 普通字符：精准原样匹配
re.match("ab","abc123")：开头必须依次 a→b，匹配 ab
re.match("ab","acb123")：第二位是 c≠b → None

② . ：任意单个字符（除换行 \n）
re.match('.e','hello')
第 0 位任意字符 h、第 1 位 e → 匹配 he

③ [abc] ：匹配括号内任意单个字符
[0-9]数字、[a-z]小写、[A-Z]大写
re.match('[he]l','hello')：首字符只能是 h 或 e，后面跟 l
"""

#3. \d 匹配数字0-9
re6 = re.match(r'.\d\d','s243s')
print(re6.group()) #s24
#注意：\d里的\在普通字符串里是转义符，Python 把\d当成非法转义，警告invalid escape sequence '\d'
#可以使用 原生字符串 r"" 或者 双反斜杠 \\d 解决

#4. \D匹配非数字
re7 = re.match(r'\D','/12')
print(re7.group()) # /

#5. \s 匹配空白，即 空格和tab键
re8 = re.match(r'\s\s..','  hello')
print(re8.group()) #  he ==> 可以看出一个tab等于两个空白

#6. \S 匹配非空白
re9 = re.match(r'\S','zcj')
print(re9.group()) #z

#7. \w 匹配单词字符，即a-z,A-Z,0-9,下划线_,汉字
re10 = re.match(r'\w..','我是Leo')
print(re10.group()) #我是L

#8. \W 匹配非单词字符
re11 = re.match(r'\W.','。我是Leo')
print(re11.group()) #我是L


