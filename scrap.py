import requests
import re
from bs4 import BeautifulSoup


def writeFile(accent, path):
    f.write('-rwxr-xr-x  0 miyatakeyouko staff     ' + accent + ' Aug 29 11:01 ')
    f.write(path + '\n')



f = open('../kanji_datas.txt', mode='w')

f.write('-rwxr-xr-x  0 miyatakeyouko staff     212 Aug 29 11:01 ./._.\n')
f.write('drwxr-xr-x  0 miyatakeyouko staff       0 Aug 29 11:01 ./\n')

all_data = []
initial_list = []
bpmf_list = []
count = 0

for i in range(1, 131):
    # The pages with the list of kanji
    if i == 1:
        page = requests.get('https://bopomofo.kakijun.com/zhuyin/hanzi/index.html')
    else:
        page = requests.get('https://bopomofo.kakijun.com/zhuyin/hanzi/index_' + str(i) + '.html')

    html = BeautifulSoup(page.content, 'html.parser')

    elems = html.find_all('li')
    for elem in elems:
        s = str(elem)
        if 'title' in s:
            kanji = s[32]
            
            # Access to each character's information page
            page2 = requests.get('https://bopomofo.kakijun.com/' + kanji + '.html')
            html2 = BeautifulSoup(page2.content, 'html.parser')

            datatag = html2.find('strong')  # [<strong>蠨（ㄒ丨ㄠ）</strong>]
            if datatag == None:
                break
            data = str(datatag)
            #print(data)
            data = data[8 : data.find('）') + 1] # 蠨（ㄒ丨ㄠ）
            print('p' + str(i) + ' ' + data)
            
            accent = ''
            bpmf = data[data.find('（') + 1 : data.find('）')]
            
            if '˙' in data:
                accent = '0'
                bpmf = bpmf[1:]
            elif 'ˊ' in data:
                accent = '2'
                bpmf = bpmf[:len(bpmf) - 1]
            elif 'ˇ' in data:
                accent = '3'
                bpmf = bpmf[:len(bpmf) - 1]
            elif 'ˋ' in data:
                accent = '4'
                bpmf = bpmf[:len(bpmf) - 1]
            else:
                accent = '1'

            initial = bpmf[0]
            path = initial + '/' + bpmf + '/' + kanji
            dictionary = {
                'kanji': kanji,
                'accent': accent,
                'initial': initial,
                'bopomofo': bpmf
            }
            all_data.append(dictionary)
            count += 1


print('-Read!')

all_data_sorted = sorted(all_data, key=lambda x:x['bopomofo'])
print('-Sorted!')

former_initial = ''
former_bpmf = ''
for data in all_data_sorted:
    path = './' + data['initial'] + '/'
    if not data['initial'] == former_initial:
        writeFile('-1', path)
    path = path + data['bopomofo'] + '/'
    if not data['bopomofo'] == former_bpmf:
        writeFile('-1', path)

    path = path + data['kanji']
    writeFile(data['accent'], path)
    former_bpmf = data['bopomofo']
    former_initial = data['initial']

print('-Finish!')

f.close()
