# Trial I
# 16 - 21s P = 1
# 40 - 45s B = 2
# 62 - 67s P
# 85 - 90s BT =3
# 107 - 112s BT
# 131 - 136s B
# 153 - 158s P
# 178 - 183s B
# 201 - 206s BT

#Trim head and tail for 2300 data point when training
ts = []
with open('R1_SGR.txt') as f:
    for count, line in enumerate(f):
        pass
    print(count + 1)
    f.seek(0)
    data = [next(f).split(' ') for i in range(count + 1)]
    ts = [int(float(d[0])) for d in data]


start = ts[0]
label = []

for t in ts:
    if start + 16 <= t < start + 21 or start + 62 <= t < start + 67 or start + 153 <= t < start + 158:
        label.append(1)
    elif start + 40 <= t < start + 45 or start + 131 <= t < start + 136 or start + 178 <= t < start + 183:
        label.append(2)
    elif start + 85 <= t < start + 90 or start + 107 <= t < start + 112 or start + 201 <= t < start + 206:
        label.append(3)
    else:
        label.append(0)
        # label.append(0)


with open('MOT1_LYF_LABLE.txt', 'w+') as f:
    for t in label:
        f.write(str(t) + '\n')

