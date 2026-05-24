print("这是pytest2会显示的内容")

def test():
    print('哈哈哈')
if __name__ =="__main__": #被当作模块导入时，下面的代码不会显示出来
    print("这是pytest2作为模块不会显示的内容")

