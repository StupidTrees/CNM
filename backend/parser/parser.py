import os
import sys
import codecs

from utils.config import raw_path
from .LineParser import parse_line
from .extracter import extract_names


class RelationAdjacentMatrix:
    def __init__(self, nameList: list[str]):
        self.nameToSerialDict: dict[str:int] = {}
        self.serialToNameDict: dict[int:str] = {}
        for t in range(len(nameList)):
            self.nameToSerialDict[nameList[t]] = t
            self.serialToNameDict[t] = nameList[t]
        self.adjMatrix: list[list[int]] = [[0] * len(nameList) for _ in range(len(nameList))]

    def add_relation(self, relationTuple: tuple[str, str, int]):
        name1, name2, weight = relationTuple
        name1_idx = self.nameToSerialDict[name1]
        name2_idx = self.nameToSerialDict[name2]
        self.adjMatrix[name1_idx][name2_idx] += weight

    def print_relations_to_device(self, device=sys.stdout, delimiter=' '):
        for i in range(len(self.adjMatrix)):
            for j in range(i + 1, len(self.adjMatrix)):
                w = self.adjMatrix[i][j]
                if w > 0:
                    print(self.serialToNameDict[i], self.serialToNameDict[j], w, file=device, sep=delimiter)


class NovelCharacterRelationParser:
    def __init__(self, novelFilepath, charaNameFilepath, charaAliasFilepath):
        self.nameList = self.__create_name_list(charaNameFilepath)
        self.aliasDict = self.__create_alias_dict(charaAliasFilepath)
        self.novelFilepath = novelFilepath
        self.adjMatrix = RelationAdjacentMatrix(self.nameList)

    @staticmethod
    def __create_name_list(nameFilename) -> list[str]:
        nameList: list[str] = []
        with codecs.open(nameFilename, 'r', 'utf8') as f:
            for line in f.readlines():
                nameList.append(line.split('\r')[0].strip())
        return nameList

    @staticmethod
    def __create_alias_dict(aliasFilename) -> dict[str, list[str]]:
        aliasDict: dict[str, list[str]] = {}
        with codecs.open(aliasFilename, 'r', 'utf8') as f:
            for line in f.readlines():
                l = line.split(':')
                aliasDict[l[0]] = l[1].split('\n')[0].split(',')
        return aliasDict

    def parse(self, outputDevice=sys.stdout):
        with codecs.open(self.novelFilepath, 'r', 'utf8') as f:
            for line in f.readlines():
                relationPair = parse_line(line, self.nameList, self.aliasDict)
                for tuple_ in relationPair:
                    self.adjMatrix.add_relation(tuple_)
            print('CharacterA,CharacterB,Frequencies', file=outputDevice)
            self.adjMatrix.print_relations_to_device(delimiter=',', device=outputDevice)


def parse_novel_text(label):
    if not os.path.exists(raw_path+'{}/charac_name.txt'.format(label, label)):
        extract_names(raw_path+'{}/{}.txt'.format(label, label), label)
    parser = NovelCharacterRelationParser(raw_path+'{}/{}.txt'.format(label, label),
                                          raw_path+'{}/charac_name.txt'.format(label),
                                          raw_path+'{}/charac_alias.txt'.format(label))
    if not os.path.exists('backend/data/parsed/{}/'.format(label)):
        os.makedirs('backend/data/parsed/{}/'.format(label))
    with codecs.open('backend/data/parsed/{}/{}.csv'.format(label, label), 'w+', 'utf8') as f:
        parser.parse(outputDevice=f)
