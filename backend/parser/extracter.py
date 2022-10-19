from tqdm import tqdm

from utils.config import raw_path


def extract_names(raw_file, label):
    import jieba.posseg as psg
    with open(raw_file, encoding='utf-8') as f:
        text = f.readlines()
    # for t in text:
    #     res = psg.cut(t)
    # print([(item.word, item.flag) for item in res])
    dict = {}
    for t in tqdm(text):
        res = psg.cut(t)
        for item in res:
            if item.flag == 'nr' and item.word in dict:
                dict[item.word] += 1
            elif item.flag == 'nr' and item.word not in dict:
                dict[item.word] = 1

    # 合并同类
    name_merged = {}
    for n, f in dict.items():
        if n[0] == '和' or n[0] == '但' or n[0] == '与':
            coll = False
            for ot in [k for k in dict.keys() if k != n]:
                if ot == n[1:] or (ot[0] != '和' and ot[0] != '与' and ot[0] != '但' and ot[1:] == n[1:]):
                    coll = True
                    break
            if not coll:
                name_merged.setdefault(n, 0)
                name_merged[n] += f
        else:
            prefx = False
            prefx_ot = None
            for ot in [k for k in dict.keys() if k != n]:
                if ot[1:] == n:
                    prefx = True
                    prefx_ot = ot
                    break
            if prefx:
                name_merged.setdefault(prefx_ot, 0)
                name_merged[prefx_ot] += f
            else:
                name_merged.setdefault(n, 0)
                name_merged[n] += f
    name_count = sorted(name_merged.items(), key=lambda x: x[1], reverse=True)
    name_count = name_count[:min(len(name_count), 200)]
    with open(raw_path + '{}/charac_name.txt'.format(label), 'w') as f:
        for name, freq in name_count:
            if len(name) > 1:
                f.write(name + '\n')
    with open(raw_path + '{}/charac_alias.txt'.format(label), 'w') as f:
        for name, freq in name_count:
            if len(name) == 3:
                f.write("{}:{}\n".format(name, name[1:]))
