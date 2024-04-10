rlist =['PBR', 'PER', 'PSR', 'EE', 'PCR','DIV']
x = [64.77,59.81,74.53, 94.46,66.14,31.47]
y = 61.59
z = []
for xx in x:
    z.append((xx**2)/y**2)

print(z)