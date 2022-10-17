import sys
import os
import tempfile
import codecs
import pytest

if 'lib' not in os.listdir():
    raise Exception('Run pytest from project root...')
sys.path.append(os.getcwd())
from lib import NovelCharacterRelationParser


def test_NovelCharacterRelationParser_parse():
    sanguoParser = NovelCharacterRelationParser('lib/test/sanguo_baihua.txt', 'lib/test/charac_name.txt',
                                                'lib/test/charac_alias.txt')
    tmpf = tempfile.NamedTemporaryFile()
    with codecs.open(tmpf.name, 'w', 'utf8') as testf:
        sanguoParser.parse(outputDevice=testf)
        # Close file to make sure buffer was flushed
    with codecs.open(r'lib/test/sample_sanguo.csv', 'r', 'utf8') as samplef, \
            codecs.open(tmpf.name, 'r', 'utf8') as testf:
        testLines = testf.readlines()
        sampleLines = samplef.readlines()
        try:
            numOfLines = len(sampleLines)
            for i in range(numOfLines):
                if testLines[i] != sampleLines[i]:
                    raise Exception()
        except:
            pytest.fail("NovelCharacterRelationParser.parse() output incorrectly")
    tmpf.close()
