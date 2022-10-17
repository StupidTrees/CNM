def get_line_name_freq(line: str, nameList: list[str], aliasDict: dict[str, list[str]]) -> dict[str, int]:
    nameFreq: dict[str, int] = {}
    for name in nameList:
        if cnt := line.count(name):
            nameFreq[name] = nameFreq[name] + cnt if nameFreq.__contains__(name) else cnt
        try:
            for alias in aliasDict[name]:
                if cnt := line.count(alias):
                    nameFreq[name] = nameFreq[name] + cnt if nameFreq.__contains__(name) else cnt
        except KeyError:
            continue
    return nameFreq


def create_relation_pairs(nameFreq: dict[str, int]) -> list[tuple[str, str, int]]:
    relationPair = []
    keysList = list(nameFreq.keys())
    for i in range(len(keysList)):
        for j in range(i + 1, len(keysList)):
            name1 = keysList[i]
            name2 = keysList[j]
            tuple_ = (name1, name2, min(nameFreq[name1], nameFreq[name2]))
            relationPair.append(tuple_)
    return relationPair


def parse_line(line: str, nameList: list[str], aliasDict: dict[str, list[str]]):
    nameFreq: dict[str, int] = get_line_name_freq(line, nameList, aliasDict)
    relationPair: tuple[str, str, int] = create_relation_pairs(nameFreq)
    return relationPair
