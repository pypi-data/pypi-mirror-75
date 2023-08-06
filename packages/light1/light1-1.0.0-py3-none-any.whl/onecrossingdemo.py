import linerproblem as lp

# 计算但路口各个红绿灯的最优时间
# 请输入初始化列表,qij见示意图，单位：辆/s，l表示两车头之间的距离，单位：m，tp表示人的反应速度，单位1：s，v0表示平均速度，单位：m/s，Tl为基准值，单位：s
# rgdata=[q11,q13,q21,q23,q32,q34,q42,q44,l,v0,tp，Tl=100]
rgdata = [0.4, 0.3, 0.3, 0.2, 0.3, 0.2, 0.1, 0.3, 2, 2, 2, 100]
# 利用lp.rgtimeone函数计算路口各个红绿灯的时间
TL1, TL2, TL3, TL4, TH1, TH2, TH3, TH4 = lp.rgtimeone(rgdata)
print("一个路口各个相位红绿灯的时间")
print("第一相位的红灯时间")
print(TL1)
print("第二相位的红灯时间")
print(TL2)
print("第三相位的红灯时间")
print(TL3)
print("第四相位的红灯时间")
print(TL4)
print("第一相位的绿l灯时间")
print(TH1)
print("第二相位的绿灯时间")
print(TH2)
print("第三相位的绿灯时间")
print(TH3)
print("第四相位的绿灯时间")
print(TH4)
