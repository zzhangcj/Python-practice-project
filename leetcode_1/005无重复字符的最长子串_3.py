
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

