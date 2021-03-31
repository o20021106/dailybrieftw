from datetime import datetime
import sys
import os
sys.path.append(os.getcwd())
from web.app.models import Article

def test_new_article():
    id_ = '123'
    article = Article(id_, 'appledaily',
                      'https://tw.appledaily.com/life/20210331/PVY7PBM6YFAUZAC3GUAQGPHPEY/',
                      '高雄外送員竟遇女大生「帶槍」領餐　幾秒後立懂！網友直呼專業', 
                      ('外送員網友在《爆廢公社》PO文，他送餐到中山大學女生宿舍，結果來領餐的女學生竟然拿著槍'
                       '，原來是這裡猴子猖狂，果不其然，幾秒後就有2隻猴子竄出，突襲其他手中有東西的女學生，其'
                       '中一名女學生嚇到投降立刻把東西丟到地上，猴子看到後將東西撿走。過程中，帶槍的女學生朝'
                       '地開了幾槍，嚇阻猴子來搶她要領的餐。'), datetime.now(), datetime.now())
    assert article.id == id_

