import numpy as np
import math


# 返回每个路口车辆的总延误时间
# listan为流量，TH为红灯时长，v0为汽车在红绿灯处匀加速运动的平均速度，l为两车车头间的距离，tp为人的反应时间

def delayt(listan, TH, v0, l, tp):
    list1 = [0] * math.ceil((TH * listan))
    for k in range(np.size(list1)):
        list1[k] = TH - k * (1 / listan - l / v0) + tp
    sumlist1 = sum(list1)
    return sumlist1
