import drown as dr
import numpy as np
import matplotlib.pyplot as plt

# 生成第三相位红灯时长30-100s，取偶数
l = []
for i in range(101):
    if i >= 30 and i % 2 == 0:
        l = l + [i]

# 计算每个第三相位对应的第一相位红灯时长和阻塞度，求出最小的阻塞度和对应的第一相位红灯时长
TH3 = l
blode = [0] * np.size(l)
TH1time = [0] * np.size(l)
for i in range(np.size(l)):
    print("第三相位红灯时长")
    print(TH3[i])
    blode[i], TH1time[i] = dr.drown(TH3[i], 1, 2, 2, 3, 2, 60)

# 画出第三相位红灯时长和最小阻塞度的关系曲线
plt.figure()
# plt.title("标题")
plt.xlabel("Red light's duration")
plt.ylabel("Blocking degree")
plt.scatter(TH3, blode)  # 画点
plt.plot(TH3, blode)  # 画线

# 画出第三相位红灯时长和最小阻塞度对应的第一相位红灯时长的关系曲线
plt.figure()
# plt.title("标题")
plt.xlabel("Red light's duration")
plt.ylabel("Green light's duration")
plt.scatter(TH3, TH1time)  # 画点
plt.plot(TH3, TH1time)  # 画线

plt.show()
