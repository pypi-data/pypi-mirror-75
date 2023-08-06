import numpy as np
import math


# 返回每个路口全部车辆的延误时间
# TH1,TH2,TH3,TH4为pulp包中的变量，listan为列表中的一个流量，TH在TH1，TH2，TH3,TH4中选择，list为传入linerproblem的初始化列表，flowra为流量比率，T为周期

def delayt(listan, TH, list, flowra, T):
    # 计算每个路口红灯等待的车辆
    list1 = [0] * math.ceil(flowra * 3 * T * listan)
    # 计算每辆车的延误时间
    for k in range(np.size(list1)):
        list1[k] = TH - k * (1 / listan - list[8] / list[9]) + list[10]
    # 计算每个路口全部车辆的延误时间
    sumlist1 = sum(list1)
    return sumlist1


# 返回基准延误时间，用来无量纲化
def delayt1(listan, TH, list):
    # 计算每辆车的延误时间
    list1 = [0] * (TH * math.ceil(listan))
    # 计算每辆车的延误时间
    for k in range(np.size(list1)):
        list1[k] = TH - k * (1 / listan - list[8] / list[9]) + list[10]
    # 计算每个路口全部车辆的延误时间
    sumlist1 = sum(list1)
    return sumlist1
