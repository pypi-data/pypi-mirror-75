
# 1. infer type(type assert)
# 2. infer shape(other input's shape, or const)
#       a.shape, [n], 3, [1,2,n]
# 3. infer dtype
#       a.dtype, "int"
# 4. infer output
#       jt.empty(shape, dtype)
# each statement is build or not
#  shape = a.shape not build
#  c[i,j] = a[i,j] + b[i,j]

#  for x in range(y): ---> for (int x=0; x<y; y++)

# 别名分析
# a = 1
# for ...:
#    b = a
# a = ...

# 跳转分析

# for i in range(x):
#     stmta
# for i in range(x):
#     stmtb
# stmta 和 stmtb 是否可交换, 可交换的前提是没有相互依赖关系
# stmta 的输入不影响 stmtb 的输出，反之亦然
# 1. 别名分析（唯一id，id对应符号）
# 2. live in live out 分析（read write）
# 3. inline 分析（外部符号分析）
# 4. ssa计算图（trace var come from）
# 5. 反向链接（跳转，前置代码块）
# 6. jit key, special shape, dtype, shape order(with equal)

'''
每一个stmt都有自己要读的和自己要写的。

每一个stmt：
    读符号，写符号，符号可能有确定的id，不确定的时候，可能是前置代码块不同路径决定的
    读内存，写内存，也可能有确定的id

a = 0
for i in range(10):
    a += i
print(a)


a = 0 # a:%1
i = 0 # i:%2
while i(%2|%4)<10: 
    a += i # a(%3) = a(%1|%3) + i(%2)
    i += 1 # i(%4) = i(%2|%4) + 1

print(a)

'''


import ast, inspect
import jittor as jt
from collections import Sequence

def jiyan(func):
    return print(ast.parse(inspect.getsource(func)))


def func(a, b):
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            a[i,j] += b[j,i]

def __func(a, b):
    out_a, out_b = jt.code([a.shape, b.shape], [a.dtype, b.dtype], [a, b], 
        cpu_src="""
        for (int i=0; i<in0_shape0; i++)
            for (int j=0; j<in1_shape1; j++)
                @in0(i,j) += @in1(j,i);
    """)
    out_a.share_with(a).swap(a)
    out_b.share_with(b).swap(b)

def test1():
    a = 0
    for i in range(100):
        a += i
        # 查找后续使用

def test2():
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            a[i,j] += b[j,i]
            a[i,j] += b[j,i]

def test3():
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            aa = a[i,j]
            bb = b[i,j]
            a[i,j] = aa + bb + bb



'''
some constrain:
    for loop var can not alter
    x = jt.empty must outside
'''

x = ast.parse(inspect.getsource(func))
x = x.body[0]
def dfs(prefix, x):
    print(prefix, '<' + type(x).__name__ + '>')
    for k,v in x.__dict__.items():
        if isinstance(v, str):
            print(prefix+'.'+k+' = '+v)
        elif isinstance(v, Sequence):
            for i,j in enumerate(v):
                if isinstance(j, str):
                    print(prefix+f".{k}[{i}] = {j}")
                    
    for k,v in x.__dict__.items():
        if isinstance(v, ast.AST):
            dfs(prefix+'.'+k, v)
        if isinstance(v, Sequence):
            for i,j in enumerate(v):
                if isinstance(j, ast.AST):
                    dfs(prefix+f".{k}[{i}]", j)
dfs("x", x)

a = jt.array([[1,2],[3,4]])
b = jt.array([[5,6],[7,8]])
__func(a, b)
print(a)
print(b)