import pysolr
import re

# 需要导入的json文件名
JSON_FILE = (
            'data_utf8.json','yl228_utf8.json',
            #'yl228_utf8.json','data_utf8.json',  
            )

# 在导入前，是否先清空 solr 里面已有的索引数据, True 清空， False， 不清空
CLEAR_INDEX_BEFORE_ADD = True

def json_import():5
    solr = pysolr.Solr('http://localhost:8983/solr/test', timeout=10)
    if CLEAR_INDEX_BEFORE_ADD:
        solr.delete(q='*:*')
        print u'清除索引成功'
    for kkk in JSON_FILE:
        f = open(kkk, 'r')
        cont = f.read()
        # print cont
        # pat = re.compile('^{.+?}', re.DOTALL)
        pat = re.compile('(?<={).+?(?=})', re.DOTALL)
        res = pat.findall(cont)
        print len(res)
        num = 1
        for i in res:
            # print i
            i = i.decode('utf-8')
            a = eval(u'{'.encode('utf-8') + i + u'}'.encode('utf-8'))
            a = eval(u'{' + i + u'}')
            b = {}
            for (key, val) in a.items():
                # print key, val.decode('utf-8') if isinstance(val, str) else val
                b[key] = val.decode('utf-8') if isinstance(val, str) else val


            # a = {'a':u'你好'.encode('utf-8')}
            # solr.add([b])
            try:
                solr.add([b])
            except:
                print u'数据错误，已经跳过第%d条索引数据的插入' % num
                continue
            finally:
                num += 1
            # for (key, val) in a.items():
                # print key, val.decode('utf-8') if isinstance(val, str) else val
            # raw = raw_input()
            print num
            # return
            # num += 1
        f.close()
        #return
    pass

def solr_md5_search(md5):
    solr = pysolr.Solr('http://localhost:8983/solr/test', timeout=10)
    result = solr.search('md5='+md5)
    if len(result) == 0:
        return False

    a  = {}
    for j in result:
        a['title'] = j.get('title')[0]
        a['date'] = j.get('date')[0][0:10]
        a['time'] = j.get('time')[0]
        a['link'] = j.get('link')[0]
        a['md5'] = j.get('md5')[0]
        a['category'] = j.get('category')[0]
        a['fee'] = j.get('fee')[0]
        a['city'] = j.get('city')[0]
        a['image'] = j.get('image')[0]
        a['feeList'] = j.get('feeList')[0]
        a['detailcategory'] = j.get('detailcategory')[0]
        a['place'] = j.get('place')[0]
        a['createdtime'] = j.get('createdtime')[0]
        a['desc'] = j.get('desc')[0]
        return a

    # date:[2015-09-03T00:00:00Z TO *]
# [s_range, s_word, fq]
def solr_search(search_params, start):
    s_range = search_params[0]
    s_word = search_params[1]
    fq = search_params[2]
    solr = pysolr.Solr('http://localhost:8983/solr/test', timeout=10)
    k_word = s_word if s_range == 'all' else u'{}={}'.format(s_range, s_word)
    # print '--------------------in solr-----'
    # print k_word
    results = []
    start_step = int(start)
    while True:
        result = solr.search(k_word, **{
                              'fq': fq,
                              # 'fq': fq[1],
                              'start':str(start_step),
                              'rows':'1',
                              })
        if len(result) == 0:
            return results, start_step

        flag = False
        for i in results:
            if flag:
                break
            for j in result:
                if i['md5'] == j.get('md5')[0]:
                    flag = True
                    break
        
        if flag:
            start_step += 1
            continue

        temp = {}
        for j in result:
            temp['title'] = j.get('title')[0]
            temp['date'] = j.get('date')[0][0:10]
            temp['date'] = temp['date'].replace('-', '.').strip()
            temp['time'] = j.get('time')[0]
            temp['time'] = temp['time'].replace(':', '.').strip()
            temp['link'] = j.get('link')[0]
            temp['md5'] = j.get('md5')[0]
            break

        results.append(temp)
        # results += [temp]
        start_step += 1
        if len(results) == 10:
            # print '------------------------------ss'
            # print results
            return results, str(start_step)

    return results, start_step

    results = solr.search('*')
    for result in results:
        a = result.get('category')
        a = result.get('title')
        if a == None:
            continue

        print a[0]

    print("Saw {0} result(s).".format(len(results)))


    results = solr.search('*', **{
                          # 'fq': 'date:[2015-09-03T00:00:00Z TO *]',
                          'fq': 'date:[* TO *]',
                          'start':'0',
                          # 'rows':'1000',
                          })
    print("Saw {0} result(s).".format(len(results)))
    for result in results:
        a = result.get('category')
        a = result.get('title')
        if a == None:
            continue

        print a[0]
    pass

def solr_search_test(a, b):
    pass
    solr = pysolr.Solr('http://localhost:8983/solr/test', timeout=10)
    results = solr.search('*', **{
                          # 'fq': 'date:[2015-09-03T00:00:00Z TO *]',
                          'fq': ['date:[* TO 2015-09-03T00:00:00Z]', 'time:[* TO *]'],
                          # 'fq': 'time:[* TO *]',
                          'start':'0',
                          # 'rows':'1000',
                          })
    print("Saw {0} result(s).".format(len(results)))
    for result in results:
        a = result.get('category')
        a = result.get('title')
        if a == None:
            continue

        print a[0]
    pass

if __name__ == "__main__":
    json_import()










