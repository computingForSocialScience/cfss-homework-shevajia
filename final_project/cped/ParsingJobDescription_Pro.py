import re
import json
import csv
from io import open


f = open('RegionsDict.json','rb')
RegionsDict = json.load(f)
Regions = RegionsDict.keys()
f.close()

f_md = open("military_dict.json",'rb')
military_dict = json.load(f_md)
f_md.close()

def union(a, b):
    """ return the union of two lists """
    return list(set(a) | set(b))

keyword_regions = u'(石家莊|唐山|秦皇島|邯鄲|邢台|保定|張家口|承德|滄州|廊坊|衡水|太原|長治|大同|晉城|晉中|臨汾|呂梁|朔州|陽泉|運城|忻州|呼和浩特|包頭|赤峰|通遼|烏海|呼倫貝爾|烏蘭察布|鄂爾多斯|巴彥淖爾 |錫林郭勒|興安|阿拉善|瀋陽|大連|鞍山|撫順|本溪|丹東|錦州|營口|阜新|遼陽|盤錦|鐵嶺|朝陽|葫蘆島|長春|吉林|四平|遼源|通化|白山|松原|白城|延邊|哈爾濱|齊齊哈爾|牡丹江|佳木斯|大慶|雞西|雙鴨山|伊春|七台河|鶴崗|黑河|綏化 |大興安嶺|南京|無錫|徐州|常州|蘇州|南通|揚州|鎮江|鹽城|淮安|泰州|連雲港|宿遷|杭州|寧波|溫州|嘉興|湖州|紹興|金華|衢州|舟山|台州|麗水|合肥|蕪湖|蚌埠|淮南|馬鞍山|淮北|銅陵|安慶|黃山|滁州|宣城|阜陽|六安|宿州|亳州|池州|福州|廈門|泉州|漳州|南平|三明|龍岩|莆田|寧德|南昌|景德鎮|萍鄉|九江|新余|鷹潭|贛州|吉安|宜春|撫州|上饒|濟南|青島|淄博|棗莊|東營|煙台|濰坊|濟寧|泰安|威海|日照|濱州|德州|聊城|臨沂|菏澤|萊蕪|鄭州|開封|安陽|許昌|洛陽|新鄉|漯河|商丘|信陽|南陽|焦作|三門峽|鶴壁|平頂山|周口|駐馬店|濮陽|武漢|黃石|十堰|荊州|宜昌|襄陽|鄂州|荊門|孝感|黃岡|咸寧|隨州|恩施|長沙|株洲|湘潭|衡陽|邵陽|岳陽|張家界|益陽|常德|婁底|郴州|永州|懷化|湘西|廣州|深圳|中山|珠海|佛山|茂名|肇慶|惠州|潮州|汕頭|湛江|江門|河源|韶關|東莞|汕尾|陽江|梅州|清遠|揭陽|雲浮|南寧|柳州|桂林|梧州|北海|崇左|來賓|貴港|賀州|玉林|百色|河池|欽州|防城港|成都|自貢|攀枝花|瀘州|德陽|綿陽|廣元|遂寧|樂山|內江|南充|眉山|宜賓|廣安|雅安|達州|資陽|巴中|阿壩|甘孜|涼山|貴陽|六盤水|遵義|安順|畢節|銅仁|黔西南|黔南|黔東南|昆明|曲靖|玉溪|保山|昭通|麗江|普洱|臨滄|西雙版納|大理|楚雄|德宏|紅河|文山|怒江|迪慶|拉薩|昌都|日喀則|阿里|山南|那曲|林芝|西安|咸陽|寶雞|銅川|渭南|漢中|延安|安康|商洛|榆林|蘭州|嘉峪關|天水|金昌|白銀|酒泉|張掖|武威|定西|隴南|平涼|慶陽|臨夏|甘南|西寧|海東|海北|海南|海西|黃南|果洛|玉樹|銀川|石嘴山|吳忠|固原|中衛|烏魯木齊|克拉瑪依|昌吉|博爾塔拉|巴音郭楞|克孜勒蘇|伊犁|阿勒泰|塔城|吐魯番|哈密|阿克蘇|和田|喀什)'
keywords_pro_exact = [u'北京市', u'上海市', u'天津市', u'黑龍江省', u'吉林省', u'遼寧省', u'內蒙古自治區', u'河北省', u'山東省', u'山西省', u'河南省', u'陝西省', u'甘肅省', u'寧夏回族自治區|寧夏自治區', u'青海省', u'新疆維吾爾自治區|新疆自治區', u'西藏自治區', u'四川省', u'貴州省', u'雲南省', u'湖北省', u'湖南省', u'廣西壯族自治區|廣西自治區', u'廣東省', u'海南省', u'福建省', u'江西省', u'安徽省', u'江蘇省', u'浙江省'] 
keywords_pro_short = [u'北京', u'上海', u'天津', u'黑龍江', u'吉林', u'遼寧', u'內蒙古', u'河北', u'山東', u'山西', u'河南', u'陝西', u'甘肅', u'寧夏', u'青海', u'新疆', u'西藏', u'四川', u'貴州', u'雲南', u'湖北', u'湖南', u'廣西', u'廣東', u'海南', u'福建', u'江西', u'安徽', u'江蘇', u'浙江']

pro_dict = {}
pro_dict[u'北京'] = u'北京市'
pro_dict[u'上海'] = u'上海市'
pro_dict[u'天津'] = u'天津市'
pro_dict[u'內蒙古'] = u'內蒙古自治區'
pro_dict[u'新疆'] = u'新疆維吾爾自治區|新疆自治區'
pro_dict[u'西藏'] = u'西藏自治區'
pro_dict[u'寧夏'] = u'寧夏回族自治區|寧夏自治區'
pro_dict[u'廣西'] = u'廣西壯族自治區|廣西自治區'
for keyword_pro in keywords_pro_short:
    if keyword_pro in dict.keys(pro_dict):
        pass
    else:
        pro_dict[keyword_pro] = keyword_pro + u'省'

keywords_pro_indicator = u'(區|縣|地委|市|局|廳|盟|州|委|宣傳部|統戰部|組織部|旗|人大|政協)'
keywords_pro_exclude = u'(市|省|自治區|回族自治區|維吾爾自治區|維族自治區|壯族自治區|州|行政區|特別行政區)'
keywords_region_indicator = u'(市|地區|地委|盟|州|自治州|朝鮮族自治州|土家族苗族自治州|藏族羌族自治州|彝族自治州|布依族苗族自治州|苗族侗族自治州|傣族自治州|白族自治州|傣族景頗族自治州|哈尼族彝族自治州|壯族苗族自治州|傈僳族自治州|藏族自治州|回族自治州|蒙古族藏族自治州|蒙古自治州|柯爾克孜自治州|哈薩克自治州)'

def JobParsing(job_description):
    Pro = []
    for keyword in keywords_pro_exact:
        match = re.search(keyword, job_description)
        if match:
           Pro.append(keyword)
        else:
            pass
        
    match = re.findall(keyword_regions + keywords_region_indicator, job_description)
    if match == [u'']:
        pass
    else:
        for item in match:
            if item == (u'海南', u'自治州'):
                break
            keyword = item[0]
            if RegionsDict[keyword] in Pro:
                pass
            else:
                Pro.append(RegionsDict[keyword])
        
    for keyword in keywords_pro_short:
        match1 = re.search(keyword + u'(?!' + keywords_pro_exclude + u')', job_description)
        match2 = re.search(keyword + u'(.*?' + keywords_pro_indicator + u')', job_description)
        if match2:
            if match2.group(0) == u'海南藏族自治州' or match2.group(0) == u'河南蒙古族自治縣' or match2.group(0) == u'河南縣':
                Pro = union(Pro, [u'青海省'])
                break
            elif match2.group(0) == u'河北區':
                break
            elif match2.group(0) == u'海南自治州':
                Pro = union(Pro, [u'廣東省'])
                break
        if match1 and match2 and pro_dict[keyword] in Pro:
            pass
        elif match1 and match2:
            Pro.append(pro_dict[keyword])
        else:
            pass
    return Pro

def JobParsingChongqing(start_year, end_year, job_description):
    Pro = ''
    match = re.search(u'重慶市', job_description)
    if match and start_year >= 1997:
        Pro = u'重慶市'
    elif match and end_year >= 1998:
        Pro = u'重慶市（檢查）'
    elif match:
        Pro = u'四川省'
    match1 = re.search(u'重慶(?!市)', job_description)
    match2 = re.search(u'重慶(.*?(縣|區|局|廳|委|宣傳部|統戰部|組織部|人大|政協))', job_description)
    if match1 and match2 and start_year >= 1997:
        Pro = u'重慶市'
    elif match1 and match2 and end_year >= 1998:
        Pro = u'重慶市（檢查）'
    elif match1 and match2:
        Pro = u'四川省'
    return Pro

f = open('Exps.json','rb')
exps = json.load(f)
f.close()

Pros = []
for i in range(len(exps)):
    if i % 10000 == 0:
        print i
    job_descriptions = exps[i][-1].split(u'，')
    id = exps[i][0]
    if exps[i][3] == '':
        start_year = 0
    else:
        start_year = int(exps[i][3])
    if exps[i][6] == 'now':
        end_year = 9999
    elif exps[i][6]:
        end_year = int(exps[i][6])
    else:
        end_year = 0
    X = []
    if military_dict[id] == False:
        for job_description in job_descriptions:
            match_military = re.search(u'軍', job_description)
            if match_military:
                continue
            Pro = JobParsing(job_description)
            if Pro == [u'海南省'] and end_year < 1988:
                Pro = [u'廣東省']
            X = union(X, Pro)
            Pro_Chongqing = JobParsingChongqing(start_year, end_year, job_description)
            if Pro_Chongqing in X:
                pass
            elif Pro_Chongqing == '':
                pass
            else:
                X.append(Pro_Chongqing)
        if X == [u'四川省', u'重慶市']:
            X = [u'重慶市'] 
        elif X == [u'廣東省', u'海南省']:
            X = [u'廣東省']
    Pros.append(X)

f_pros = open("pro.csv", 'w', encoding = 'utf8')
for pro in Pros:
    if len(pro) == 0:
        line = u'""\n'
    elif len(pro) == 1:
        line = u'"' + pro[0] + u'"\n'
    elif len(pro) == 2:
        line = u'"' + pro[0] + u'","' + pro[1] + u'"\n'
    elif len(pro) == 3:
        line = u'"' + pro[0] + u'","' + pro[1] + u'","' + pro[2] + u'"\n'
    f_pros.write(line)
f_pros.close()