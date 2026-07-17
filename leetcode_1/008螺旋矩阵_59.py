from typing import List
#1.常规解法
class Solution:
    def generateMatrix(self, n: int) -> List[List[int]]:
        mat = [[0] * n for _ in range(n)]
        count = 1
        start_index = 0  # (0,0)
        while not count >= n ** 2:
            for j in range(start_index, n - 1 - start_index):
                mat[start_index][j] = count
                count += 1
            for i in range(start_index, n - 1 - start_index):
                mat[i][n - 1 - start_index] = count
                count += 1
            for j in range(n - 1 - start_index, start_index, -1):
                mat[n - 1 - start_index][j] = count
                count += 1
            for i in range(n - 1 - start_index, start_index, -1):
                mat[i][start_index] = count
                count += 1

            start_index += 1

        if n % 2 == 1:
            mat[n // 2][n // 2] = count

        return mat

if __name__ == '__main__':
    s = Solution()
    res = s.generateMatrix(4)
    print(res)


#2.边界收缩法（解特定的题，有奇效，即没那么泛用，就像005的有序数组的读写指针）
'''
当看到对矩阵进行某些奇怪操作比如螺旋，对角线等，就要想到边界收缩
类似于你看到关于数组字符串要进行有记忆的操作，就得想到哈希表
'''
class Solution2:
    def generateMatrix(self, n: int) -> List[List[int]]:
        mat = [[0]*n for _ in range(n)]
        top,bottom = 0,n-1
        left,right = 0,n-1
        count=1
        while count<=n**2:
            for j in range(left,right+1):
                mat[top][j]=count
                count+=1
            top+=1
            for i in range(top,bottom+1):
                mat[i][right]=count
                count+=1
            right-=1
            for j in range(right,left-1,-1):
                mat[bottom][j]=count
                count+=1
            bottom-=1
            for i in range(bottom,top+1,-1):
                mat[i][left]=count
                count+=1
            left+=1
        return mat



'''
for _ in range(n)
range(n) 生成 0,1,2,...,n-1 一共 n 个数字
_ 是占位变量，代表循环 n 次，我们不需要用到这个数字，只用循环次数
每次循环都会执行一次 [0]*n，生成一行全 0 列表
'''
