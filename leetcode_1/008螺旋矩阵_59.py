from typing import List

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





'''
for _ in range(n)
range(n) 生成 0,1,2,...,n-1 一共 n 个数字
_ 是占位变量，代表循环 n 次，我们不需要用到这个数字，只用循环次数
每次循环都会执行一次 [0]*n，生成一行全 0 列表
'''