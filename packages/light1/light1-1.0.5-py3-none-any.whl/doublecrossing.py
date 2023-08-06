from scipy import integrate
import linerproblem as lp
import math


# rgdata=[q11,q13,q21,q23,q32,q34,q42,q44,l,v0,tp，Tl=100]
# rgdata2=[q11,q13,q21,q23,q32,q34,q42,q44,l,v0,tp，Tl=100]
# 初始化两个路口的路长l，单位：m，和车辆在路上行驶的平均速度vl，单位：m/s

def doucros(rgdata, rgdata2, l, vl):
    # 将第一个路口的红绿灯时长设置为全局变量，方便后面在其他函数中计算两路口第一相位的时间差函数使用
    global TL1, TL2, TL3, TL4, TH1, TH2, TH3, TH4
    # 计算第一个路口的红绿灯时长
    TL1, TL2, TL3, TL4, TH1, TH2, TH3, TH4 = lp.rgtimeone(rgdata)
    print("第一个路口各个相位红绿灯的时间")
    print("第一相位的红灯时间")
    print(TL1)
    print("第二相位的红灯时间")
    print(TL2)
    print("第三相位的红灯时间")
    print(TL3)
    print("第四相位的红灯时间")
    print(TL4)
    print("第一相位的绿灯时间")
    print(TH1)
    print("第二相位的绿灯时间")
    print(TH2)
    print("第三相位的绿灯时间")
    print(TH3)
    print("第四相位的绿灯时间")
    print(TH4)
    print("\n")

    # 计算通道上的平均流量ql
    ql = (rgdata[1] * TL1 + rgdata[5] * TL3 + rgdata[6] * TL4) / (TL1 + TL2 + TL3 + TL4)
    # 计算第二个路口第一相位左边车流量q211和第二相位左边车流量q223
    q213 = ql * 3 / 5
    q223 = ql * 2 / 5

    # 将得到的流量插入到第二个路口的流量信息中，并计算第二个路口红绿灯时长
    rgdata2.insert(1, q213)
    rgdata2.insert(3, q223)
    # 输出第二个路口的流量信息
    print("第二个路口初始化数据")
    print("[q11,q13,q21,q23,q32,q34,q42,q44,l,v0,tp，Tl=100]")
    print(rgdata2)
    print("\n")
    # 计算第二个路口各个相位的红绿灯时长
    TL21, TL22, TL23, TL24, TH21, TH22, TH23, TH24 = lp.rgtimeone(rgdata2)
    print("第二个路口各个相位红绿灯的时间")
    print("第一相位的红灯时间")
    print(TL21)
    print("第二相位的红灯时间")
    print(TL22)
    print("第三相位的红灯时间")
    print(TL23)
    print("第四相位的红灯时间")
    print(TL24)
    print("第一相位的绿灯时间")
    print(TH21)
    print("第二相位的绿灯时间")
    print(TH22)
    print("第三相位的绿灯时间")
    print(TH23)
    print("第四相位的绿灯时间")
    print(TH24)

    # 计算间隔时间(取两个周期)
    # 定义周期函数
    def f(x):
        T = TL1 + TL2 + TL3 + TL4
        if x >= 0 and x <= TL1:
            return rgdata[1]
        else:
            if x > TL1 and x <= TL1 + TL2:
                return 0
            else:
                if x > TL1 + TL2 and x <= TL1 + TL2 + TL3:
                    return rgdata[5]
                else:
                    if x > TL1 + TL2 + TL3 and x <= T:
                        return rgdata[6]
                    else:
                        if x > T and x <= TL1 + T:
                            return rgdata[1]
                        else:
                            if x > TL1 + T and x <= TL1 + TL2 + T:
                                return 0
                            else:
                                if x > TL1 + TL2 + T and x <= TL1 + TL2 + TL3 + T:
                                    return rgdata[5]
                                else:
                                    if x > TL2 + TL2 + TL3 + T and x <= 2 * T:
                                        return rgdata[6]
                                    else:
                                        return 0

    # 循环找到最大绿灯面积对应的开始时间（不考虑通道长度）
    T = TL1 + TL2 + TL3 + TL4
    # grin记录每个步长的第二个路口第一相位绿灯面积
    grin = [0] * math.ceil(2 * T)
    # grin1记录每个面积对应的绿灯开启时刻
    grin1 = [0] * math.ceil(2 * T)
    i = 0
    while i < 2 * T:
        v, err = integrate.quad(f, i, TL21 + i)
        grin[i] = v
        grin1[i] = i
        i = i + 1

    print("\n")

    # 计算第二个路口变为绿灯的时间（考虑道路长度，以第一路口第一相位为零时刻）
    # 输入路长l和车辆的匀速行驶速度vl
    tg = l / vl + grin1[grin.index(max(grin))]
    print("第二个路口和第一个路口第一相位绿灯的间隔时间")
    print(tg)
