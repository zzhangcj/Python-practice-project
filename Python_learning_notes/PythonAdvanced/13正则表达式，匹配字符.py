###一.正则表达式（字符串处理工具）
import re #需要导入re模块
# #1.特点
# #   （1）语法比较复杂，可读性较差
# #   （2）通用性很强，适用多种编程语言
# #2.match方法
# #（1）核心本质
# #   只从字符串【最开头第 0 位】开始匹配，不会向后搜寻,只要开头不满足正则，直接返回 None，不再往后找
# #   区别：search 是全字符串任意位置找，match 固定从头
# #（2）返回两种结果
# #   匹配成功：返回 Match 对象，可用 .group() 取出匹配到的字符串
# #   匹配失败：返回 None，不能调用.group ()，调用直接报错
#
# #（3）格式：re.match(pattern,string,flags)
# #   pattern匹配正则表达式
# #   string 要匹配的字符
#
# res = re.match("冰","冰冰永远18")
# print(res)
# #<re.Match object; span=(0, 1), match='冰'>
# print(res.group()) #冰
#
# re1 = re.match("冰","小冰永远18")
# print(re1) #None
# # print(re1.group()) #AttributeError: 'NoneType' object has no attribute 'group'
# #第一个字不是 冰 会报错
# #注意：match是从开始位置匹配，匹配不到就没有，而且匹配的是pattern整体（比如“冰冰”）
#
# ###二.匹配单个字符
# #1. 符号 .  匹配任意一个字符，除了\n以外        -常用
# re2 = re.match('.e',"hello")
# print(re2.group()) #he
#
# #2.[]匹配[]中例举的字符                      -常用
# re3 = re.match('[he].','ello')
# print(re3.group()) #el
# re4 = re.match('[1-5]','24351')
# print(re4.group()) #2
# re5 = re.match('[a-zA-Z][1-57-9]','m8out')
# print(re5.group()) #m8
#
# """
# 总结
# 正则 pattern 规则（match 按正则规则匹配开头）
# ① 普通字符：精准原样匹配
# re.match("ab","abc123")：开头必须依次 a→b，匹配 ab
# re.match("ab","acb123")：第二位是 c≠b → None
#
# ② . ：任意单个字符（除换行 \n）
# re.match('.e','hello')
# 第 0 位任意字符 h、第 1 位 e → 匹配 he
#
# ③ [abc] ：匹配括号内任意单个字符
# [0-9]数字、[a-z]小写、[A-Z]大写
# re.match('[he]l','hello')：首字符只能是 h 或 e，后面跟 l
# """
#
# #3. \d 匹配数字0-9
# re6 = re.match(r'.\d\d','s243s')
# print(re6.group()) #s24
# #注意：\d里的\在普通字符串里是转义符，Python 把\d当成非法转义，警告invalid escape sequence '\d'
# #可以使用 原生字符串 r"" 或者 双反斜杠 \\d 解决
#
# #4. \D匹配非数字
# re7 = re.match(r'\D','/12')
# print(re7.group()) # /
#
# #5. \s 匹配空白，即 空格和tab键
# re8 = re.match(r'\s\s..','  hello')
# print(re8.group()) #  he ==> 可以看出一个tab等于两个空白
#
# #6. \S 匹配非空白
# re9 = re.match(r'\S','zcj')
# print(re9.group()) #z
#
# #7. \w 匹配单词字符，即a-z,A-Z,0-9,下划线_,汉字   --常用
# re10 = re.match(r'\w..','我是Leo')
# print(re10.group()) #我是L
#
# #8. \W 匹配非单词字符
# re11 = re.match(r'\W.','。我是Leo')
# print(re11.group()) #我是L
#
# ###三.匹配多个字符
# #1. * 匹配前一个字符出现0次或者无限次，即可有可无   --常用
# re12 = re.match(r'\w*','bing。2x')
# print(re12.group()) #bing
# r"""
# 1.为什么没有匹配到2x？
# (1)re.match()：只从字符串最开头开始匹配，不会向后跳过字符
# (2)\w 匹配：字母、数字、下划线； 这里的。不属于\w，匹配终止
#
# 2.为什么这里注释前面要加r？
# 不加r会出现报错：SyntaxWarning: invalid escape sequence '\w' 警告原因
# 报错来源：代码注释里直接写\w，普通字符串\是转义符，Python 把\w当成非法转义字符
# """
# re13 = re.match(r'\d*','bing。2x')
# print(re13.group()) #啥也没有，即没有匹配到
#
# #2. + 匹配前一个字符出现1次或者无限次，即至少一次,连续匹配   --常用
# re14 = re.match(r'\w+','康神开播了')
# print(re14.group()) #康神开播了
#
# #3. ？ 匹配前一个字符出现一次或者0次              --常用
# re15 = re.match(r'\w?','kskbl,真的假的')
# print(re15.group()) #k   因为？最多只能匹配一个
#
# #4. {m} 匹配前一个字符出现m次
# re16 = re.match(r'\w{3}','kskbl,真的假的')
# print(re16.group()) #ksk
# #不能超出位数，会报错
#
# #5. {m,n} 匹配前一个字符出现从m次到n次（m<n，即最少匹配m个，最多n个）
# re17 = re.match(r'\w{2,4}','kskbl,真的假的')
# print(re17.group()) #kskb
#
# ###四.匹配开头和结尾
# #1. ^ ：匹配字符串开头，表示以...开头；表示对...取反
# re18 = re.match('^ks','kskbl,真的假的')
# print(re18.group()) #ks
# #注意： ^在[]中表示不匹配
# re19 = re.match('[^ks]','bl,真的假的')
# print(re19.group()) #b  因为[^ks]表示匹配除了p、y之外的字符
#
# #2. $ ：匹配以...结尾
# '''
# re20 = re.match('.{3}的$','kskbl,真的假的')
# print(re20.group())
#
# 为什么报错：AttributeError: 'NoneType' object has no attribute 'group'
# .{3}：任意3个字符
# 的$：这3个字符串后面，紧接着末尾必须是「的」，即字符串总共只能有4个字符组成
#
# 如果要修改{}里面必须包含9（因为一共10个字符）
# '''
# re20 = re.match('.{7,9}的$','kskbl,真的假的')
# print(re20.group())

###五.匹配分组
##1. | 匹配任意一个表达式   --常用
re21 = re.match('abc|deg','deg')
print(re21.group()) #deg 如果左右两边都匹配不到则报错

re22 = re.match(r'\d|\S','s234')
print(re22.group())

##2. (ab) 将括号中字符作为一个分组   --常用
re23 = re.match(r'\w*@(163|qq|4499).com','123@4499.com')
print(re23.group()) #123@4499.com
print(re23.group(1)) #4499

re24 = re.match(r'(\w+)@((qq|163).com)','root@qq.com')
print(re24.group(1)) # root 第一个左括号所包含内容，匹配到了root
print(re24.group(2)) # qq.com 第二个左括号所包含内容，匹配到了qq.com
print(re24.group(3)) # qq 第二个左括号所包含内容，匹配到了qq
r'''
1.'\w*@(163|qq|4499).com'理解
\w* :字母/数字/下划线，0个或多个 → 123
(163|qq|4499) :是或，只能三选一
@和.com :原样匹配

2.补充group(序号)
group(0) = 整串全部匹配内容（固定自带，不算自定义分组）
group(1) = 第 1 个(内容
group(2) = 第 2 个(内容

(1)数左小括号 ( 个数 = 最大分组号
(2)序号不能超过括号总数，超了报错
(3)group () /group (0) 永远是完整匹配字符串
'''

##3. \num 匹配num匹配到的字符串  ————常在匹配标签时被使用
re25 = re.match(r'<(\w*)>\w*</\1>','<html>login</html>')
print(re25.group()) #<html>login</html>
r'''
1. (\w*)什么意思
    分组 1：捕获标签名，字母数字任意个
2. \1什么意思
    \1 = 复用第 1 个括号抓到的内容 (html)
3. 为什么要加()
    加 () 才有分组、才能被 \1 反向引用，不加括号存不住数据
'''
re26 = re.match(r'<(\w*)><(\w*)>.*</\2></\1>','<html><body>login</body></html>')
print(re26.group()) #<html><body>login</body></html>
#注意：从外到内排序，编号从1开始

##4. (?P<name>) 分组起别名
##5. (?P=name) 引用别名为name分组匹配到的字符串
re26 = re.match(r'<(?P<L1>\w*)><(?P<L2>\w*)>.*</(?P=L2)></(?P=L1)>','<html><body>login</body></html>')
print(re26.group()) #<html><body>login</body></html>

#一句话总结：对，就是给\1、\2这类数字分组起名字
#日常简单正则：用的少，普通反向引用\1 \2够用

##6.匹配网址 前缀一般是www 后缀为.com/.cn/.org
li = ['www.baidu.com','www.python.org','http.jd.cn','www.py.en','www.abc.cn']
re27 = re.match(r'www\.\w*\.(com|cn|org)','www.baidu.com')
print(re27.group()) #www.baidu.com
#注意这里的\.是因为只写一个 . 表示这里匹配任意字符

for i in li:
    re27 = re.match(r'www\.\w*\.(com|cn|org)', i)
    if re27: #等同于re27 != None
        print(re27.group())
    else:
        print(f"The website {i} is wrong")
