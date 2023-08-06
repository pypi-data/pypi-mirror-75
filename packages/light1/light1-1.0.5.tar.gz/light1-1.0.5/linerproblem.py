import pulp as pl
import adelaytime as ad


# 计算一个路口各个相位的红绿灯时长
# 请输入初始化列表,qij见示意图，l表示两车头之间的距离，tp表示人的反应速度,v0表示平均速度,Tl为基准值
# rgdata=[q11,q13,q21,q23,q32,q34,q42,q44,l,v0,tp，Tl=100]
# 返回四个相位的红绿灯时长
def rgtimeone(list):
    # 设置绿灯时长为变量
    TL1 = pl.LpVariable("TL1", 20, 40)
    TL2 = pl.LpVariable("TL2", 20, 40)
    TL3 = pl.LpVariable("TL3", 20, 40)
    TL4 = pl.LpVariable("TL4", 20, 40)
    # 设置红灯时长
    TH1 = TL2 + TL3 + TL4
    TH2 = TL1 + TL3 + TL4
    TH3 = TL1 + TL2 + TL4
    TH4 = TL1 + TL2 + TL3
    prob = pl.LpProblem("myProblem", pl.const.LpMinimize)
    # 计算基准灯长
    THl = int(3 * list[11] / 4)

    # 计算平均延误车辆
    stcar = 1 / 8 * (TH1 * sum(list[0:1]) + TH2 * sum(list[2:3]) + TH3 * sum(list[4:5]) + TH4 * sum(list[6:7]))
    # 计算平均延误车辆基准值
    stcarl = 1 / 8 * (THl * sum(list[0:1]) + THl * sum(list[2:3]) + THl * sum(list[4:5]) + THl * sum(list[6:7]))
    # 平均延误车辆无量纲化
    stcars = (stcar - stcarl) / stcarl

    # 周期范围：80-120
    T = 100

    # 计算延误率d
    d_ = [0] * 8
    d_[0] = ad.delayt(list[0], TH1, list, (sum(list[0:7]) - list[0]) / sum(list[0:7]), T) / (3 * T * list[0])
    d_[1] = ad.delayt(list[1], TH1, list, (sum(list[0:7]) - list[1]) / sum(list[0:7]), T) / (3 * T * list[1])
    d_[2] = ad.delayt(list[2], TH2, list, (sum(list[0:7]) - list[2]) / sum(list[0:7]), T) / (3 * T * list[2])
    d_[3] = ad.delayt(list[3], TH2, list, (sum(list[0:7]) - list[3]) / sum(list[0:7]), T) / (3 * T * list[3])
    d_[4] = ad.delayt(list[4], TH3, list, (sum(list[0:7]) - list[4]) / sum(list[0:7]), T) / (3 * T * list[4])
    d_[5] = ad.delayt(list[5], TH3, list, (sum(list[0:7]) - list[5]) / sum(list[0:7]), T) / (3 * T * list[5])
    d_[6] = ad.delayt(list[6], TH4, list, (sum(list[0:7]) - list[6]) / sum(list[0:7]), T) / (3 * T * list[6])
    d_[7] = ad.delayt(list[7], TH4, list, (sum(list[0:7]) - list[7]) / sum(list[0:7]), T) / (3 * T * list[7])
    d = 1 / 8 * sum(d_) / (3 * T)

    # 计算基准延误率
    d_l = [0] * 8
    d_l[0] = ad.delayt1(list[0], THl, list) / (3 * T * list[0])
    d_l[1] = ad.delayt1(list[1], THl, list) / (3 * T * list[1])
    d_l[2] = ad.delayt1(list[2], THl, list) / (3 * T * list[2])
    d_l[3] = ad.delayt1(list[3], THl, list) / (3 * T * list[3])
    d_l[4] = ad.delayt1(list[4], THl, list) / (3 * T * list[4])
    d_l[5] = ad.delayt1(list[5], THl, list) / (3 * T * list[5])
    d_l[6] = ad.delayt1(list[6], THl, list) / (3 * T * list[6])
    d_l[7] = ad.delayt1(list[7], THl, list) / (3 * T * list[7])
    dl = 1 / 8 * sum(d_l) / (3 * T)

    # 延误率无量纲化
    ds = (d - dl) / dl

    # 目标函数
    targ = 1 / 2 * 1 / 35 * stcars + 1 / 2 * ds
    prob += targ
    # 约束条件
    prob += max(list[0:7]) * TH1 <= TL1 * list[9] / list[8]
    prob += max(list[0:7]) * TH2 <= TL2 * list[9] / list[8]
    prob += max(list[0:7]) * TH3 <= TL3 * list[9] / list[8]
    prob += max(list[0:7]) * TH4 <= TL4 * list[9] / list[8]
    prob += TL1 + TL2 + TL3 + TL4 == T
    status = prob.solve(pl.PULP_CBC_CMD(msg=0))
    # 返回四个相位的红绿灯时长
    return pl.value(TL1), pl.value(TL2), pl.value(TL3), pl.value(TL4), pl.value(TH1), pl.value(TH2), pl.value(
        TH3), pl.value(TH4)
