
import matplotlib.pyplot as plt


def trim_list_under(lst, upper):
    first = 0
    last = len(lst)-1
    for i in range(0, len(lst)):
        if lst[i] > upper:
            first = i
            break
    for i in range(len(lst)-1, -1, -1):
        if lst[i] > upper:
            last = i
            break

    return lst[first:last+1]


f = open("house2//wm.dat", "r")
h2_wm_sep_points = [
    76000, 77000, 77900, 78400, 79000, 92000, 175165, 176000, 260000, 274750, 315000, 356000, 360000, 380000, 460000, 468500, 469000, 560000, 580000, 652000, 653000, 654000, 656000, 751700, 752500, 754000, 835206, 836000, 891000, 908000, 948000, 949100, 950000, 963700, 965000, 1019000, 1020000, 1046000, 1062000, 1074225, 1074740, 1075500, 1142500, 1190000, 1239625, 1245000, 1323500, 1324250, 1425000, 1440000, 1520250, 1521000, 1534000, 1536250, 1622000, 1633953, 1634600, 1664000
]
data = []
sups=[]
for x in f:
    data.append(int(x.split(" ")[1]))

for i in range(len(h2_wm_sep_points)-1):
    seg= data[h2_wm_sep_points[i]:h2_wm_sep_points[i+1]]
    sup = trim_list_under(seg,20)
    sups.append(sup)
print(len(sups))
plt.plot(sups[1])
# plt.savefig(f'eps/last.png', format='png')
plt.show()
f.close()
