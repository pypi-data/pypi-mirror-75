"""
① 函数 mxmul：矩阵乘法
② 函数 mxsum：矩阵求和
③ 模块的名称属性 if __name__ = "__main__"： 包含对上述函数的测试代码   ❤使用import导入该模块时，不会被执行
"""
""" 矩阵乘法：
有5个输入参数： mx1、mx2 “第1、2个矩阵“   nrow、nk ”第1个矩阵的行、列“     ncol ”第2个矩阵的列“
由于要对两个矩阵进行操作，生成 “第3个矩阵”，需要生成一个矩阵 rst，即生成1个二维列表，在运算之后将二维列表的引用返回
"""
def mxmul(mx1, mx2, nrow, nk, ncol):   #矩阵乘法
    rst = [[0 for y in range(ncol)] for x in range(nrow)]
    for i in range(nrow):
        for j in range(ncol):
            for k in range(nk):
                rst[i][j] += mx1[i][k] * mx2[k][j]
    return rst

def mxsum(mx, nrow, ncol):     #矩阵求和：矩阵累加和，返回了一个求和对象 s
    s = 0
    for i in range(nrow):
        for j in range(ncol):
            s += mx[i][j]
    return s

if __name__ == "__main__":  #如何测试这段代码？？对算法“两个矩阵的乘” 进行计时，在调用 mxmul() 函数前后各调用了一次perf_counter()
    import time
    nrow, nk, ncol = 500, 300, 500
    mx1 = [[y for y in range(nk)] for x in range(nrow)]
    mx2 = [[y for y in range(ncol)] for x in range(nk)]
    start = time.perf_counter()
    rst = mxmul(mx1, mx2, nrow, nk, ncol)
    end = time.perf_counter()
    print("运算时间为{:.4f}s".format(end - start))


