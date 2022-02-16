import imp
import numpy as np
from mip import Model, xsum, minimize, BINARY, INTEGER
import time

# ビンの容量
B = 8
# アイテムの集合
# I = [1, 2, 3, 4]
I = [i+1 for i in range(10)]
# 各アイテムの大きさ
# S = [1, 3, 6, 7]
S = [(I[i] + 1234) % B for i in range(10)]

m = Model('binpacking')

# 変数を定義
# アイテムiをビンjに詰めるとき1、そうでないとき0となる変数x
# ビンの数はアイテム数にする（各アイテムを1ビンに入れたときが最大のビンの数)
x = [[m.add_var('x({},{})'.format(i, j), var_type=BINARY)
      for j in range(len(I))] for i in range(len(I))]

# ビンjが使われるとき1,そうでないとき0となる変数y
y = [m.add_var(var_type=BINARY) for j in range(len(I))]

# 目的関数を定義
m.objective = minimize(xsum(y[j] for j in range(len(I))))

# 制約条件を定義
# アイテムはどこかのビンに入るはず
for i in range(len(I)):
    m += xsum(x[i][j] for j in range(len(I))) == 1

# 各ビンで入っているアイテムはビンの容量以下になる
for j in range(len(I)):
    m += xsum(S[i] * x[i][j] for i in range(len(I))) <= B * y[j]

start = time.perf_counter()
m.optimize()
end = time.perf_counter()

# 問題設定の表示
# 瓶の容量
print('# 問題設定')
print('瓶の容量:{}'.format(B))
# 各アイテムの大きさ
print('各アイテムの大きさ' + ','.join(map(str, S)))

print('----')
print('# 解')

# 解の表示
for i in range(len(I)):
    for j in range(len(I)):
        if x[i][j].x == 1:
            print('アイテム{}はビン{}に詰める'.format(i+1, j+1))

print('実行時間(秒)：' + str(end-start))

print('----')
print('# 値の検証')

# 値の検証
# 瓶に入ってるアイテムの数
num1 = 0
for j in range(len(I)):
    for i in range(len(I)):
        if x[i][j].x == 1:
            num1 += 1
print('瓶に入ってるアイテムの数:{}'.format(num1))

# 各瓶に入っているアイテムの容量
for j in range(len(I)):
    num2 = 0
    for i in range(len(I)):
        if x[i][j].x == 1:
            num2 += S[i] * x[i][j].x
    print('ビン{}に入っている合計の容量:{}'.format(j+1, num2))

print('----')
