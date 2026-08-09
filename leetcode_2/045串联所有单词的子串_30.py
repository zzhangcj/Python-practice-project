from typing import List
from collections import Counter
from collections import defaultdict
"""
给定一个字符串 s 和一个字符串数组 words。 words 中所有字符串 长度相同。

 s 中的 串联子串 是指一个包含  words 中所有字符串以任意顺序排列连接起来的子串。

例如，如果 words = ["ab","cd","ef"]，
那么 "abcdef"， "abefcd"，"cdabef"， "cdefab"，"efabcd"， 和 "efcdab" 都是串联子串
"acdbef" 不是串联子串，因为他不是任何 words 排列的连接

返回所有串联子串在 s 中的开始索引。你可以以 任意顺序 返回答案

示例 1：

输入：s = "barfoothefoobarman", words = ["foo","bar"]
输出：[0,9]
解释：因为 words.length == 2 同时 words[i].length == 3，连接的子字符串的长度必须为 6。
子串 "barfoo" 开始位置是 0。它是 words 中以 ["bar","foo"] 顺序排列的连接。
子串 "foobar" 开始位置是 9。它是 words 中以 ["foo","bar"] 顺序排列的连接。
输出顺序无关紧要。返回 [9,0] 也是可以的。
"""

'''
我的思路：滑动窗口

'''
#1.这里是自己写得代码，有错的
class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        words_len=len(words)
        words_i_len=len(words[0])
        substr_len=words_i_len*words_len
        left=0
        right=substr_len-1
        s_len=len(s)
        substr=[]
        while right<s_len:
            while left<right:
                if s[left:left+words_i_len] in words and left<right: #或许可以用哈希表（enumerate+字典）
                    left+=words_i_len
                elif left==right:
                    substr.append(left)
                else: #如果这一段不是串联子串,退出循环
                    break
            #复位left，然后窗口移动
            left=right-substr_len+1
            left+=1
            right+=1

        return substr

#2，顺应我的思路修正的解法
class Solution2:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        #判断是否为空
        if not words or not s:
            return []
        words_num=len(words)
        w_len=len(words[0])
        total_len=words_num*w_len
        s_len=len(s)
        res=[]
        words_counter=Counter(words)

        for offset in range(w_len):
            left = offset
            while left+total_len<=s_len:
                window_str=s[left:left+total_len]
                split_words=[]
                for i in range(words_num):
                    start=i*w_len
                    split_words.append(window_str[start:start+w_len])
                if Counter(split_words)==words_counter:
                    res.append(left)
                left+=w_len
        return res
"""
1、为什么要写 for offset in range(w_len)
单词占 3 个字符
就像切甘蔗，每一节固定长 3 厘米
你下刀的位置，可以：
对准刻度 0（offset=0）
错开 1 厘米下刀（offset=1）
错开 2 厘米下刀（offset=2）
只有这 3 种下刀模式，不存在第 4 种
每一种下刀模式独立完整扫描一遍字符串

2、为什么 left += w_len
w_len = 单个单词的字符长度，例如单词foo，w_len=3
外层循环 for offset in range(w_len)，分成w_len 套独立组别：
offset=0：合法起点只能是：0, 3, 6, 9, 12 … → 起点 % 3 == 0
offset=1：合法起点只能是：1, 4, 7, 10 … → 起点 %3 ==1
offset=2：合法起点只能是：2,5,8,11 … → 起点 %3 ==2

组内必须 left += w_len，保证当前 left 永远满足 left % w_len == offset。
❌如果写left +=1：
offset=2 这一组 left 会走到 9，9%3=0，这个起点实际属于 offset=0 组，不属于本组
就会重复收集同一个答案下标，出现输出[0,9,9,9]

3、两者配合
offset 控制：以什么偏移开始切单词
left +=w_len：在当前偏移模式下，跳到下一个候选起点。
两者配合，保证：每个合法起点（即满足left+total_len<=s_len的起点）只会被恰好某一组 offset 处理一次，不会重复、不会漏
"""

#3.最优解法
class Solution3:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if not s or not words:
            return []
        w_num = len(words)
        w_len = len(words[0])
        s_len = len(s)
        word_count = defaultdict(int)
        for w in words:
            word_count[w] += 1
        res = []

        # 遍历全部w_len种起始偏移
        for offset in range(w_len):
            left = offset
            right = offset
            cur_cnt = defaultdict(int)
            match = 0  # 已经匹配成功的不同单词种类

            while right + w_len <= s_len:
                curr_word = s[right:right + w_len]
                right += w_len

                if curr_word in word_count:
                    cur_cnt[curr_word] += 1
                    # 刚好达到目标数量，匹配种类+1
                    if cur_cnt[curr_word] == word_count[curr_word]:
                        match += 1
                    # 当前单词数量超了，移动左边界
                    while cur_cnt[curr_word] > word_count[curr_word]:
                        left_word = s[left:left + w_len]
                        if cur_cnt[left_word] == word_count[left_word]:
                            match -=1
                        cur_cnt[left_word] -= 1
                        left += w_len
                    # 全部单词匹配完成
                    if match == len(word_count):
                        res.append(left)
                else:
                    # 遇到不在words的单词，窗口直接重置
                    cur_cnt.clear()
                    match = 0
                    left = right
        return res

"""
1、defaultdict()函数
普通的字典 {}，如果你访问一个不存在的 key，直接报错 KeyError。
d = {}
print(d["abc"])   # 报错！键不存在

导入：from collections import defaultdict
当你读取不存在的键，不会报错，直接给默认值 0

d = defaultdict(int) 
#生成一个特殊字典，赋值给变量word_count
#内部自带逻辑：当你读取字典里不存在的键，自动返回默认值0，不会抛出KeyError
print(d["foo"])   # 不存在，返回 0，不会报错
d["foo"] +=1
print(d["foo"])   # 1

普通字典写法
d = {}
w = "foo"
if w not in d:    # 手动判断键存不存在
    d[w] = 0
d[w] += 1

等价 defaultdict (int)，省去 if，并自带创建字典的功能，但是计数功能要自己解决
d = defaultdict(int)
d["foo"] +=1

2、为什么要统计原始 words 的单词频次 word_count？
因为题目要求
子串，必须恰好包含 words 里面全部单词，每个单词出现次数完全一样，可以乱序。
例子：words = ["foo","foo"]
✅合法子串：foofoo（foo 出现 2 次）
❌不合法：foobar（foo 只有 1 次）
❌不合法：foofoofoo（foo 出现 3 次，多了）

word_count = defaultdict(int)
for w in words: #计数功能要自己解决
    word_count[w] += 1
    
举例子 words = ["foo","bar"]
循环结束后：word_count = {"foo":1, "bar":1}
"""