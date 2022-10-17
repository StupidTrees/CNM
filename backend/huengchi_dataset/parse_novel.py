import codecs
from lib import NovelCharacterRelationParser

sanguoParser = NovelCharacterRelationParser('data/sanguo/sanguo_baihua.txt', 'data/sanguo/charac_name.txt',
                                            'data/sanguo/charac_alias.txt')
with codecs.open('output/sanguo.csv', 'w', 'utf8') as f:
    sanguoParser.parse(outputDevice=f)
    print('output/sanguo.csv')
    
xiyouParser = NovelCharacterRelationParser('data/xiyou/xiyou.txt', 'data/xiyou/charac_name.txt',
                                            'data/xiyou/charac_alias.txt')
with codecs.open('output/xiyou.csv', 'w', 'utf8') as f:
    xiyouParser.parse(outputDevice=f)
    print('output/xiyou.csv')
    
shuihuParser = NovelCharacterRelationParser('data/shuihu/shuihu.txt', 'data/shuihu/charac_name.txt',
                                            'data/shuihu/charac_alias.txt')
with codecs.open('output/shuihu.csv', 'w', 'utf8') as f:
    shuihuParser.parse(outputDevice=f)
    print('output/shuihu.csv')