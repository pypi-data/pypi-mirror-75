import math
import numpy as np
import drownade as dr


# 实现双路口坐标图的绘制，输入参数为第三相位向下单行红灯时长TH2，单位：s，流量q32和第一相位向左单行流量q11，单位：辆/s,l为两车头的距离，单位：m，v0为汽车匀加速运动的平均速度,单位：m/s
# tp为司机反应时间，单位：s，tl为基准时间，单位：s
# 返回第一相位红灯时长对应最小的延误率和对应的第三相位红灯时长
def drown(TH3, q11, q32, l, v0, tp, tl):
    # TH1下限
    t1 = q32 * TH3 * l / v0
    # TH1上限
    t2 = TH3 * v0 / (l * q11)
    # 计算第一相位红灯TH1时间范围
    t = int(t2) - math.ceil(t1)
    # x为红灯时长的取值范围
    x = [0] * (t + 1)
    for i in range(t + 1):
        x[i] = math.ceil(t1) + i
    # 第一相位红灯取值范围
    print("第一相位红灯时长取值范围")
    print(x)

    # 计算基准时间t下的红灯时长集x1
    t1_ = q32 * tl * l / v0
    t2_ = tl * v0 / (l * q11)
    t_ = int(t2_) - math.ceil(t1_)
    x_ = [0] * (t_ + 1)
    for i in range(t_ + 1):
        x_[i] = math.ceil(t1_) + i

    # 计算每个第一相位红灯时长的延误车辆
    stcar = [0] * (t + 1)
    for i in range(np.size(x)):
        stcar[i] = 1 / 2 * (x[i] * q11 + TH3 * q32)

    # 计算基准滞留车辆
    stcarl = 1 / 2 * (x_[0] * q11 + tl * q32)

    # 无量纲化
    stcars = [0] * (t + 1)
    for i in range(np.size(x)):
        stcars[i] = 1 / 35 * (stcar[i] - stcarl) / stcarl
    print("每个第一相位红灯时长对应的去量纲化延误车辆数")
    print(stcars)

    # 计算每个第一相位的红灯时长对应的延误率
    d = [0] * (t + 1)
    for j in range(np.size(x)):
        d_ = [0] * 2
        d_[0] = dr.delayt(q11, x[j], v0, l, tp) / ((x[j] + TH3) * q11)
        d_[1] = dr.delayt(q32, TH3, v0, l, tp) / ((x[j] + TH3) * q32)
        d[j] = 1 / 2 * sum(d_) / (x[j] + TH3)
    # print(d)

    # 计算基准延误率
    d_l = [0] * 2
    d_l[0] = dr.delayt(q11, x_[0], v0, l, tp) / ((x_[0] + tl) * q11)
    d_l[1] = dr.delayt(q32, tl, v0, l, tp) / ((x_[0] + tl) * q32)
    dl = 1 / 2 * sum(d_l) / (x_[0] + tl)

    # 无量纲化
    ds = [0] * (t + 1)
    for i in range(np.size(x)):
        ds[i] = (d[i] - dl) / dl
    print("每个第一相位红灯时长对应的去量纲化延误率")
    print(ds)

    # 计算每个第一相位的红灯时长对应的优化目标
    targ = [0] * (t + 1)
    for i in range(np.size(targ)):
        targ[i] = 1 / 2 * stcars[i] + 1 / 2 * ds[i]
    print("每个第一相位红灯时长对应的优化目标：阻塞度")
    print(targ)
    print("\n")
    # 返回最小目标
    # 返回最小目标对应的第一相位的红灯时长
    return min(targ), x[targ.index(min(targ))]
