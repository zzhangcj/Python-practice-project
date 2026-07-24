
#1.基础版
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        left = 0
        right = 0
        my_set = set()
        max_len = 0
        while right < len(s):
            if s[right] in my_set:
                my_set.remove((s[left]))
                left+=1
            else: #当前元素没记录过
                my_set.add(s[right])
                max_len = max(max_len,len(my_set))
                right+=1

        return max_len

#2.哈希表，联想002的进一步哈希表
class Solution2:
    def lengthOfLongestSubstring(self, s: str) -> int:
        left = 0
        getPos = {}
        longest = 0

        for right,char in enumerate(s):
            # 右指针是谁？怎么移动？
            # enumerate 自动遍历字符串，right就是右指针，从0依次+1，全程自动向右走，不会回头
            if char in getPos:
                left = max[left,getPos[char]+1] # 字符之前出现过，把左边界跳到「上一次该字符位置的下一位」
            getPos[char] = right #不管走没走if，一定会更新字典
            longest = max[longest, right - left + 1]

        return longest


'''
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        left=0
        right=0
        max_len=0
        my_set=set()
        for right in range(len(s)):
            while s[right] in my_set:
                my_set.remove(s[left])
                left+=1
            else:
                my_set.add(s[right])
                max_len=max(max_len,right-left+1)
            
        return max_len
        
#（1）为什么这里得用for+while，而不是for+if else?
如果是if s[right] in my_set 
-->right 往前走一格 → 发现重复 → left 挪一格清理 → 完事，继续下一个 right 
出错案例： 字符串 s = "abcb"
right=0 (a)：加入集合 {a}
right=1 (b)：加入集合 {a,b}
right=2 (c)：加入集合 {a,b,c}
right=3(b)：s[right] = b 在集合内
触发 if：删除 s[left]=a，left 变成 1
👉 现在集合依然是 {b,c}，b 依旧存在！重复字符根本没清掉！
for 循环直接进入下一轮，right 不会停下来再次检查。
窗口内保留重复元素，后续全部逻辑崩坏。

（2）for + while则会锁定当前 right 原地不动，反复移动 left 清理窗口，直到满足条件

关键点：for 只是驱动右指针前进，不会回头重新校验

（3）while +if else结构：
if 分支里不会执行 right +=1！
一旦发现重复，right保持原地不变，下一轮外层循环继续检查同一个 right！
等价实现了 “重复就持续清理” 的效果

（4）总结
模板 A：for(右指针前进) + while(原地反复清理左边界)
模板 B：while(外层循环) + if(重复时不推进右指针，原地清理)
'''
