names = []
with open('sanguo.csv', 'r') as f:
    for ed in f.readlines():
        ed = ed.split(",")
        n1 = ed[0].strip()
        n2 = ed[1].strip()
        if n1 not in names:
            names.append(n1)
        if n2 not in names:
            names.append(n2)
with open('names.txt', 'w') as f:
    for name in names:
        f.write(name + "\n")

pairs = {}
with open('sanguo.csv', 'r') as f:
    for ed in f.readlines()[1:]:
        ed = ed.split(",")
        n1 = ed[1].strip() if ed[0].strip() > ed[1].strip() else ed[0].strip()
        n2 = ed[0].strip() if ed[0].strip() > ed[1].strip() else ed[1].strip()
        if (n1,n2) not in pairs:
            pairs[(n1,n2)] = 0.0
        pairs[(n1,n2)] += float(ed[2].strip())
with open('edges.txt', 'w') as f:
    for (e1,e2),weight in pairs.items():
        f.write("{};{};{}\n".format(e1,e2,weight))

