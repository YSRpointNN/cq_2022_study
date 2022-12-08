Numb = 123456
def mystr(innumb):
    lenumb = 0
    lenbuff = innumb
    while lenbuff:
        lenbuff = lenbuff // 10
        lenumb += 1
    print('size:' + str(lenumb))

    numblist = []
    for i in range(lenumb, 0, -1):
        quwei = 1
        for j in range(0, i):
            quwei = quwei * 10
        numblist.append((innumb % quwei) // (quwei // 10) + 0x30)
    rechar = ''
    for i in numblist:
        rechar += chr(i)
    return rechar

def hanshu(numb):
    if numb == 1:
        return numb
    else:
        out = 10 * hanshu(numb - 1)
    return out

print(hanshu(4))
print(mystr(Numb))
