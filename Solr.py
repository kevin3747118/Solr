import pypinyin
import datetime
import re
import urllib

from DB_CONNECTION import connection


def parse_page_to_db(data):

    def replace_string(product_name):

        replace_string = ['/', ':', '【', '】', '《', '》', '+', '※', "'", '$',
                          '(', ')', '_', '<', '>', '★', '?', '-', '-', '#', '“',
                          '紅', '橙', '黃', '綠', '藍', '紫', '白', '灰', '黑', '銀',
                          '停', '用', '[', ']']
        for i in product_name:
            if i in replace_string:
                product_name = product_name.replace(i, ' ')
        return product_name.replace('福利網獨享', '').replace('單一規格', '')

    def len_verify(obj_list ,length):

        while len(obj_list) < length:
            obj_list.append('')
        while len(obj_list) > length:
            del obj_list[-1]

        return obj_list

    query_name = replace_string(data[0])
    terms = urllib.parse.quote(query_name)
    result = connection.request.get_page('https://www.google.com.tw/search?&q=' + terms + '&oq=' + terms)

    ### 目前顯示的是以下字詞的搜尋結果
    correct_word = list()
    if result.find_all('a', {'class': 'spell'}):
        for i in result.find_all('a', {'class': 'spell'}):
            correct_word.append(i.text)
    else:
        correct_word.append('')
    correct_word = len_verify(correct_word, 1)

    ### rec_index
    rec_index_idx = dict()
    for i in result.find_all('em'):
        if i.text in rec_index_idx:
            count = rec_index_idx.get(i.text) + 1
            rec_index_idx[i.text] = count
        else:
            rec_index_idx[i.text] = 1
    rec_index_lst = [i[0] for i in sorted(rec_index_idx.items(), key=lambda x: x[1], reverse=True)[:3]]
    rec_index_lst = len_verify(rec_index_lst, 3)

    ### pin_yin
    pin_yin_modify1 = [i.replace(re.sub(r'[^a-zA-Z\d+]', '', i), '') for i in query_name if i.isalpha()]
    pin_yin_modify2 = [i for i in pin_yin_modify1 if i != '']
    pin_yin = [i[0] for i in pypinyin.pinyin(''.join(pin_yin_modify2), style=pypinyin.BOPOMOFO)]
    pin_yin_last = [''.join(pin_yin)]
    pin_yin_last = len_verify(pin_yin_last, 1)

    ### 相關搜尋
    rec_word = list()
    if result.find_all('p', {'class': '_e4b'}):
        for i in result.find_all('p',{'class': '_e4b'}):
            rec_word.append(i.text)
    else:
        rec_word = ['' for _ in range(10)]
    rec_word = len_verify(rec_word, 10)

    ### search_url
    search_url = ['https://www.google.com.tw/search?&q=' + terms + '&oq=' + terms]

    ### date
    date = [datetime.datetime.today().strftime("%Y-%m-%d")]

    to_db = [data[0], data[1]] + correct_word + rec_index_lst + pin_yin_last + rec_word + search_url + date

    sql_stat = ("""insert into [dbo].[BI_GA_USERS_SEARCH_NULL]
                   values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""")
    try:
        connection.db('NP').do_query(sql_stat, tuple(to_db))
    except Exception as e:
        connection.log.WRITE('solr', e, 'solr')


if __name__ == '__main__':

    ### date format = '2016-07-01'
    data = connection.ga.get_search_result('2017-06-01', '2017-06-03')
    k = data[:20]
    print('Parse data inserting...')
    for i in data:
        parse_page_to_db(i)
    print('Finish ' + str(len(data)) +' rows inserting !!')












