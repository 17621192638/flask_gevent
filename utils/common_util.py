import re, json
import urllib.request
import time, datetime,base64
import socket,unicodedata
import numpy as np
import io,html,hashlib
import requests
from PIL import Image
import uuid, threading
import jieba, random
import traceback
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import csv,os


def decorator_none_no_save(fn):
    """
    捕获方法异常,并返回None
    :param fn:被修饰的方法体
    :return:
    """
    def wrapper(*args, **kwargs):
        try:
            res = fn(*args, **kwargs)
            return res
        except Exception as e:
            print(args)
            traceback.print_exc()
            return None
    return wrapper

class common_util(object):
    # --------------------------------------------- 文本处理方法 ------------------------------------------------

    def base64_decode_gbk(self,text):
        """base64解密"""
        return base64.b64decode(str(text)).decode("gbk",'ignore')

    def base64_decode_utf8(self,text):
        """base64解密"""
        return base64.b64decode(str(text)).decode("utf-8")
    def base64_encode_gbk(self,text):
        """base64加密"""
        return base64.b64encode(str(text).encode("gbk"))

    def base64_encode_utf8(self,text):
        """base64加密"""
        return base64.b64encode(str(text).encode("utf-8"))



    def text_gbk_ingore(self,text):
        """将gbk无法识别的字符从文本中丢弃"""
        return text.encode('gbk', 'ignore').decode("gbk")

    def Q2B(self,_char):
        # 全角转半角
        if 65281 <= ord(_char) <= 65374:
            _char = chr(ord(_char) - 65248)
        elif ord(_char) == 12288:
            _char = chr(32)
        return _char

    def clean_content(self,raw,is_black=False):
        """
        is_black: 是否是空格分割
        清除文本中的其它内容,只保留数字、中英文"""
        fil = re.compile(u'[^0-9a-zA-Z\u4e00-\u9fa5]+', re.UNICODE)
        return fil.sub(' ' if is_black else '', raw)

    def punctuation_transfor_zh_to_en(self,text):
        """ 将文本中的中文标点转换为英文标点 """
        t2 = unicodedata.normalize('NFKC', text)
        return t2


    def filter_emoji(self, text):
        """    # 表情字符集过滤"""
        try:
            # python UCS-4 build的处理方式
            highpoints = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            # python UCS-2 build的处理方式
            highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        try:
            return highpoints.sub(u'', text)
        except:
            return text

    # 将str转换为URL语言
    def filter_URLtext(self, text):

        return urllib.parse.quote(text)

    def filter_URLtext_unquote(self, text):
        """解码"""
        return urllib.parse.unquote(text)

    def filter_URLtext_gbk(self, text):
        return urllib.parse.quote(text.encode("gbk"))

    def unicode_escape(self, obj):
        """
        unicode编码解析为中文，并将对象以str的形式返回
        :param obj:
        :return:
        """
        return str(obj).encode('latin-1').decode('unicode_escape')

    def filter_article_text(self, text):
        """
        处理数据库文章文本内容中包含的多个空格和换行符
        :param text:
        :return:
        """

        text = re.sub("\s+", "\n", text)  # \s 空格、回车、换行符等空字符，多个换成一个
        text = re.sub("(\\\\n)+", "\\\\n", text)
        return text

    def filter_spider_title(self,title):
        """过滤爬虫标题"""
        words = re.split("[-_|]", str(title))
        return "-".join(words[0:-1]) if words.__len__()>=2 else title

    def filter_article_title(self, title):
        """
        处理数据库文章标题出现的多种问题
        (1);(一);1、;一、; 第()章; 4）;四);文末含(;空标题;其它;3.2
        :param title:
        :return:
        """
        if not title:
            return "综合概述"
        if title=="其它":
            return "综合概述"
        if str(title).endswith("("):
            title=title[:-2]
        if str(title).endswith("（"):
            title = title[:-2]

        title = re.sub("第(十|一|二|三|四|五|六|七|八|九|\d)*(章|节|篇|编)、?", "", title)
        title = re.sub("(一|二|三|四|五|六|七|八|九|十|\d)*、", "", title)
        title = re.sub("(\(|（)(一|二|三|四|五|六|七|八|九|十|\d)*(\)|）)", "", title)
        title = re.sub("(一|二|三|四|五|六|七|八|九|十|\d)\)", "", title)
        title = re.sub("(\d)+\.(\d)*", "", title)
        if str(title).startswith("、"):
            title = title[1:]
        if str(title).startswith("：") or str(title).startswith(":"):
            title = title[1:]
        if str(title).startswith("."):
            title = title[1:]
        if not str(title).strip():
            return "综合概述"
        else:
            return str(title).strip()

    def filter_punctuation_mark(self,text):
        """
        jieba 文本处理:过滤文章中的标点符号以及特殊字符、空格
        :param text:
        :return:
        """
        return re.sub("[《》;；<>【】,\[\]\.、。，:~!！/、?？@#$%^&*()+_\-：“”\"{}'…\s]", '', str(text))

    def filter_number_and_punctuation_mark(self, text):
        """
        jieba 文本处理:过滤文章中的标点符号以及特殊字符、空格、数字
        :param text:
        :return:
        """
        return re.sub("[,\[\]\.、。，:~!！?？@#$%^&*()+_：“”\"''…\s0-9]", '', str(text))

    # rules = u"([\u4e00-\u9fff]+)"
    # pattern = re.compile(rules)
    def filter_blank(self,text):
        """
        jieba 文本处理:过滤文本空格
        :param text:
        :return:
        """
        return re.sub("\s", '', str(text))


    # ------------------------------------------------------ ID处理 -------------------------------------------
    # 得到UUID
    def get_uuid(self):
        return re.sub('-', "", str(uuid.uuid1()))

    # ------------------------------------------------------文档处理--------------------------------------------------------
    # 写入文档, a 追加写入, w 清空后添加记录, r 阅读
    def write(self, path, text):
        with open(path, 'a', encoding='utf-8') as f:
            f.writelines(text)
            f.write('\n')

    def write_list2txt(self, path, words):
        """将list数组按行存储成txt文件"""
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines([str(word) + "\n" for word in words])


    # 清空文档
    def truncatefile(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            f.truncate()

    # 读取文档
    def read(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            txt = []
            for s in f.readlines():
                txt.append(s.strip())
        return txt


    def read_txtTolist(self, path):
        """ 读取txt文件转换为list,每行的文本用逗号进行了分隔"""
        with open(path, 'r', encoding='utf-8') as f:
            txt = []
            for s in f.readlines():
                txt.append(",".join(s.strip().split(",")))
        return txt

    def read_list_txt(self, path):
        """ 读取txt文件 每行是一个 list对象,但是这个list对象本身是字符串 """
        with open(path, 'r', encoding='utf-8') as f:
            txt = []
            for s in f.readlines():
                txt.append(eval(s))
        return txt

    def write_json_file(self, path, dict_model):
        """
        将dict转换为json dumps 并存储为json文件 dump
        :param path:
        :return:
        """
        with open(path, 'w', encoding='utf-8') as f:
             json.dump(dict_model, f, ensure_ascii=False)


    def read_json_file(self, path):
        """
        读取json文件
        :param path:
        :return:
        """
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def transfor_json_data(self, content):
        """转换为json数据"""
        return json.dumps(content, ensure_ascii=False)


    def read_str_gbk(self, path):
        """
        保存为string类型的文本
        :param path:
        :return:
        """
        with open(path) as f:
            content = f.read()
        return content

    def read_str_utf8(self, path):
        """
        保存为string类型的文本
        :param path:
        :return:
        """
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content

    def txt_filter_set(self, path):
        """对txt文档的每一行进行查重过滤"""
        res = self.read(path=path)
        self.truncatefile(path)
        self.write_list2txt(path=path, words=set(res))

    # ------------------------------------------------------时间控制------------------------------------------

    def time_to_timestamp13(self,format_time):
        """具体时间转换为时间戳13位"""
        # int(time.mktime(time.strptime(str(format_time), '%Y-%m-%d')))-1 (23:59:59)
        return str(int(time.mktime(time.strptime(str(format_time), '%Y-%m-%d %H:%M:%S'))))

    def time_to_timestamp10(self,format_time):
        """具体时间转换为时间戳10位"""
        # int(time.mktime(time.strptime(str(format_time), '%Y-%m-%d')))-1 (23:59:59)
        return str(int(time.mktime(time.strptime(str(format_time), '%Y-%m-%d'))))

    def get_current_time(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def get_current_time_10(self):
        return datetime.datetime.now().strftime('%Y-%m-%d')

    def format_time(self, date):
        """
        时间戳转换为时间
        :param date: string或者int类型的时间戳转换为时间,如  1437487920
        :return:
        """
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(date)))

    # UTC时间转换为本地时间
    def format_UTC_time(self, utc):
        UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
        utcTime = datetime.datetime.strptime(utc, UTC_FORMAT)
        return utcTime + datetime.timedelta(hours=8)

    def get_current_hour(self):
        """
        得到当前时刻
        :return:
        """
        return datetime.datetime.now().hour

    def get_timestamp_now(self):
        """返回10位时间戳"""
        return str(time.time()).split(".")[0]

    def get_timestamp_now_13(self):
        """返回13位当前时间的时间戳"""
        res = str(time.time()).split(".")
        return res[0]+res[1][:3]

    @decorator_none_no_save
    def format_default_time(self,time):
        """强制格式化缺省时间,转换为标准格式"""
        if not time:
            return
        now = datetime.datetime.now()
        year = now.year
        time_text = str(time).strip().replace("T"," ")
        time_text = re.sub("[\.年月/_]","-",time_text)
        time_text = re.sub("[日秒]", "", time_text)
        time_text = re.sub("[时分]", ":", time_text)
        if not time_text:
            return str(now)[0:19]
        time_begin_split = time_text.split(" ")[0].split("-")
        time_end_split = time_text.split(" ")[1].split(":") if time_text.split(" ").__len__()>1 else "00:00:00".split(":")
        source_year = str(time_begin_split[0] if time_begin_split.__len__()==3 else year)
        source_month = time_begin_split[1] if time_begin_split.__len__()==3 else time_begin_split[0]
        source_day = time_begin_split[2] if time_begin_split.__len__()==3 else time_begin_split[1]
        source_hour = time_end_split[0] if time_end_split.__len__()>=1 else "00"
        source_minite =time_end_split[1]  if time_end_split.__len__()>=2  else "00"
        source_second = time_end_split[2]  if time_end_split.__len__()>=3  else "00"

        if  source_year.__len__() == 4:
            curr_year = str(source_year)
        elif source_year.__len__() == 2:
            curr_year = "20" + str(source_year)
        else:
            curr_year = str(year)
        # 月份补全
        curr_month = "0{0}".format(source_month) if source_month.__len__() == 1 else str(source_month)
        # 日数补全
        curr_day = "0{0}".format(source_day) if source_day.__len__() == 1 else str(source_day)
        # 时
        curr_hour = "00" if int(source_hour)> 23 else "0{0}".format(source_hour) if source_hour.__len__() == 1 else str(source_hour)
        # 分
        curr_minite = "00" if int(source_minite) > 59 else "0{0}".format(source_minite) if source_minite.__len__() == 1 else str(
            source_minite)
        # 秒
        curr_second = "00" if int(source_second) > 59 else "0{0}".format(source_second) if source_second.__len__() == 1 else str(
            source_second)
        # 异常数据直接过滤,返回None
        # 年份大于2019 或 小于 1800
        # 月份大于12 或 等于 0
        # 日 大于31或者 等于0
        if int(curr_year)> year or int(curr_year) < 1800 or int(curr_month)>12 or int(curr_month)==0 or int(curr_day)==0  or int(curr_day)>31 :
            return None
        else:
            return "{0}-{1}-{2} {3}:{4}:{5}".format(curr_year,curr_month,curr_day,curr_hour,curr_minite,curr_second)

    def get_delta_timestamp(self,before_num=None,after_num=None,is_timestamp=False,point_time=None):
        """
        获取延迟时间戳,昨日、前天、明日等
        :param before_num: 前面几天
        :param after_num:后面几天
        :param point_time:终止时间,如2019-10-20
        :param is_timestamp: 是否返回10位时间戳,默认返回具体日期,如2019-01-02
        :return:
        """
        today = datetime.date.today() if not point_time else datetime.datetime.strptime(point_time,"%Y-%m-%d %H:%M:%S")
        delta_timestamp = today - datetime.timedelta(days=before_num) if before_num else today + datetime.timedelta(days=after_num)  if after_num else today
        return self.time_to_timestamp10(str(delta_timestamp)[0:10]) if is_timestamp else delta_timestamp

    def get_time_interval_for_today_end(self,):
        """
        获取现在到今天结束时的时间间隔
        """
        current_time = datetime.datetime.now()
        hour= current_time.hour
        minute = current_time.minute
        second = current_time.second
        return (23-hour)*3600+(59-minute)*60+(60-second)

    # ---------------------------------------------- 数组处理 --------------------------------------------------------
    #  取2个数组的交集
    def get_intersection(self, list1, list2):
        return list(set(list1).intersection(set(list2)))

    #  取2个数组的差集
    def get_different(self, list1, list2):
        return list(set(list1).difference(set(list2)))

    #  取2个数组的并集
    def get_union(self, list1, list2):
        return list(set(list1).union(set(list2)))

    def get_ThreadName(self):
        return threading.current_thread().getName()

    # -------------------------------------- 解析html-------------------------------------------------
    def html_to_text(self, content_html):
        """
        将含P标签的html用 \n换行符凭拼接起来
        :param content_html: html内容
        :return:
        """
        data = content_html.find_all("p")
        content_wx = "\\n".join(map(lambda p_text: p_text.get_text(), data))
        return content_wx.replace("\\n\\n", "\\n").replace("\\n\\n", "\\n")

    def  change_html_special_characters(self,text):
        """
        改变 html 页面中的实体代码,参考今日头条返回内容
        【 实体对照表 】 http://www.w3school.com.cn/html/html_entities.asp
        """
        text = str(text)
        text = text.replace("\\&", "&")
        text = html.unescape(text)
        text = text.replace("&nbsp;"," ").replace("&lt;","<").replace("&gt;",">").replace("&amp;","&").replace("&quot;",'"').replace("&apos;","'")\
            .replace("&#x3D;","=").replace("\\u003C","<").replace("\\u003E",">").replace("\\u002F","/")
        return text

    def get_url_site(self,source_url):
        """获取当前url的站点前缀
        如: https://www.baidu.com/dad/sda/das/da/ds
        [out] => https://www.baidu.com
        """
        rule = re.compile("(https?://.*?)/")
        res = rule.findall(source_url)
        return res[0] if res else None

    def filter_img_url(self,head_site,img_url):
        """判断当前图片的路径是否是http开头的，不是的话加上它本身的站点头"""
        if not img_url:
            return
        if img_url.startswith("//"):
            return "https:"+img_url
        elif img_url.startswith("/"):
            return head_site+img_url if head_site else img_url
        else:
            return img_url

    def filter_image(self, img_url, source_url=None, limit_width=80, limit_height=80,print_msg=True):
        """ 对图片进行处理，拦截小于 80*80的图片"""
        if img_url:
            # 对残缺路径的url进行路径拼接
            if source_url:
                url_head = self.get_url_site(source_url)
                img_url = self.filter_img_url(url_head, img_url)
            try:
                res = requests.get(img_url, timeout=10)
                res = io.BytesIO(res.content)
                image = Image.open(res)
                (width, height) = image.size
                return (img_url,image.size) if width > limit_width and height > limit_height else (None,None)
            except:
                if print_msg:
                    traceback.print_exc()
                return (None,None)
        else:
            return (None,None)


    # --------------------------------------- 空内容过滤 ----------------------------------------------------

    def intEmptyFilter(self,val):
        return val if val else 0

    def get_title_cosine_similarity(self, articles):
        """
        获取title之间的余弦相似度矩阵,jieba 全匹配 不过滤
        :param articles:
        :return:
        """
        vectorizer = CountVectorizer()
        jieba_res = [" ".join(jieba.cut(sentence=self.filter_punctuation_mark(article))) for article in articles]
        X = vectorizer.fit_transform(jieba_res)
        return cosine_similarity(X.toarray()).tolist()

    def get_title_cosine_similarity_tfidf(self, titles):
        """
        获取title之间的余弦相似度矩阵,jieba 全匹配 不过滤
        1.分词
        2.生成词袋矩阵
        3.计算余弦相似度的值
        4.文本量大的内容 准确率才会高，文本量少的话差不多
        :param articles:
        :return:
        """
        vectorizer = TfidfVectorizer(stop_words=None)
        jieba_res = [" ".join(jieba.cut(sentence=self.filter_punctuation_mark(title))) for title in titles]
        X = vectorizer.fit_transform(jieba_res)
        return cosine_similarity(X.toarray()).tolist()

    # -------------------------------  数字相关 方法 ------------------------------------
    def random_choice_list(self,res_list):
        """从一个数组中随机取一个值"""
        return random.choice(res_list)

    def nums_normalization_deal(self,nums):
        """对数字进行归一化处理"""
        arr = np.asarray(nums)
        return [float(x - np.min(arr)) / (np.max(arr) - np.min(arr)) for x in arr]


    # -----------------------      CSV文件处理方法       ----------------------------------------
    def read_csv(self, path):
        """tips：pandas的文件处理方法更合适 """
        with open(path, mode='r', encoding='utf-8', newline='') as f:
            # 此处读取到的数据是将每行数据当做列表返回的
            reader = csv.reader(f)
            return [row for row in reader]


    def write_csv(self, head_list, rows, path):
        """
        创建和csv文件
        :param head_list: 标题数组
        :param rows:二维数组 [[],[]]
        :param path:
        :return:
        """
        with open(path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(head_list)
            writer.writerows(rows)

    def csv_add_rows(self, rows, path):
        """
        往csv文件中插入新的行
        :param rows:二维数组 [[],[]]
        :param path:
        :return:
        """
        with open(path, 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)


    # ------------------------------       线程相关处理方式       ------------------------------------
    def page_counter(self, total, page_size, workers):
        """
        分页计数器,获取每个线程应该分配的页数
        1. 获取总爬取页数
        2. 获取页数间隔
        3. 分配页数
        :param total: 总数据大小
        :param page_size:  每页数量
        :param workers:  工作的线程或者进程数
        :return:
        """
        pages = int(total/page_size)+1 if total % page_size else int(total/page_size)
        page_interval = int(pages/workers)
        return [(i*page_interval, (i+1)*page_interval) if i != workers-1 else (i*page_interval, pages+1) for i in range(workers)]

    #  -------------------------    项目路径处理       ---------------------------

    def get_current_service_ip(self):
        # 获取本机计算机名称
        hostname = socket.gethostname()
        # 获取本机ip
        ip = socket.gethostbyname(hostname)
        return ip

    # ---------------------------------     爬虫处理        ---------------------------------------------
    def get_user_agent(self):
        return {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}

    def get_android_user_agent(self):
        return {"User-Agent":"Mozilla/5.0 (Linux; Android 5.1.1; SM-G955F Build/JLS36C) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 MMWEBID/2400 MicroMessenger/7.0.3.1400(0x2700033C) Process/toolsmp NetType/WIFI Language/zh_CN"}

    def get_MD5(self,text):
        """获取MD5编码后的内容"""
        return hashlib.md5(str(text).encode("utf-8")).hexdigest()





if __name__ == '__main__':
    pass
    utils = common_util()
    # titles = ['毛泽东', '毛泽东重孙，与主席同一天生日，高大帅气神似青年毛主席', '看看毛泽东的朋友圈', '这封毛泽东未收到的杨开慧情书，曾沉寂墙缝中60年', '揭秘：毛泽东与邓小平两次不欢而散的谈话', '毛泽东在朝鲜战争中的辉煌之笔', '感人至深，毛泽东9月9日逝世，9月8日仍然在读书', '毛泽东拒穿防弹服，他和警卫员说：“人民是不会搞我的”', '习近平这样缅怀毛泽东', '毛泽东的一张珍贵相片']
    # res1 = utils.get_title_cosine_similarity(titles)[0]
    # res2 = utils.get_title_cosine_similarity_tfidf(titles)[0]
    # print(res1)
    # print(res2)
    #     res = utils.filter_spider_title("你的哈达_234_241")
    # res = utils.page_counter(total=2400000,page_size=200,workers=4)
    # res = utils.format_default_time("1010-10-10 00:00:00")
    # print(res)
    # res = utils.time_to_timestamp13(format_time="2019-01-02 00:00:00")
    # res = utils.get_title_cosine_similarity_tfidf(titles=["四种模式居然还能听收音机夜晚听着电台超级舒服", "收音机最近买的最提升幸福感的小物件既可以听电台收音机"])

    # res = res[0][1]
    # res2 = utils.get_delta_timestamp(text="dadada-da-das-da-sda-ddad.;asdasdanskjdnasdasdas[dad3nj")
    # res = utils.get_delta_timestamp(before_num=0)
    # res = utils.get_uuid()
    # res = utils.format_time("1558924677")
    # res = utils.filter_image(img_url="https://ss2.baidu.com/6ONYsjip0QIZ8tyhnq/it/u=2325543371,1193642690&fm=173&app=25&f=JPEG?w=630&h=354&s=2E121DCFDA366E968DAC84620300F0D1",source_url="https://baijiahao.baidu.com/s?id=1607125434734261224&wfr=spider&for=pc")
    res = utils.base64_decode_gbk(text="")
    print(res)

