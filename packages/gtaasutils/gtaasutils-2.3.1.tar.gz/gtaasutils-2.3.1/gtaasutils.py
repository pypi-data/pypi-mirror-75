import random
import datetime
import re


# 随机返回请求头
def getHeaders():
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
    ]

    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    return headers


# 解析2天前、2分钟等这种日期格式
def format_datetime(dt):
    try:
        ret = ''
        pattern = re.compile('\\d{2}-\\d{2}')
        pattern2 = re.compile('\\d{4}-\\d{2}-\\d{2}')
        pattern3 = re.compile('\\d{2}:\\d{2}')
        pattern4 = re.compile('\\d{2}月\\d{2}日 \\d{2}:\\d{2}')
        if '分钟前' in dt:
            m = int(dt.split('分钟')[0].strip())
            ret = (datetime.datetime.now() - datetime.timedelta(minutes=m)).strftime("%Y-%m-%d %H:%M:%S")
        elif '小时前' in dt:
            ms = int(dt.split('小时')[0].strip()) * 60
            ret = (datetime.datetime.now() - datetime.timedelta(minutes=ms)).strftime("%Y-%m-%d %H:%M:%S")
        elif '秒前' in dt:
            secs = int(dt.split('秒')[0].strip())
            ret = (datetime.datetime.now() - datetime.timedelta(seconds=secs)).strftime("%Y-%m-%d %H:%M:%S")
        elif '天前' in dt:
            d = int(dt.split('天')[0].strip())
            ret = (datetime.datetime.now() - datetime.timedelta(days=d)).strftime("%Y-%m-%d %H:%M:%S")
        elif '昨天' in dt:
            tt = dt.split('昨天')[-1].strip()
            strdate = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d ") + tt
            df = datetime.datetime.strptime(strdate, '%Y-%m-%d %H:%M')
            ret = datetime.datetime.strftime(df, '%Y-%m-%d %H:%M:%S')
        elif '前天' in dt:
            ret = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")
        elif re.match(pattern, dt):
            strdate = str(datetime.datetime.now().year) + '-' + dt
            dtformat = datetime.datetime.strptime(strdate, '%Y-%m-%d')
            ret = datetime.datetime.strftime(dtformat, '%Y-%m-%d %H:%M:%S')
        elif re.match(pattern2, dt):
            dtformat = datetime.datetime.strptime(dt, '%Y-%m-%d')
            ret = datetime.datetime.strftime(dtformat, '%Y-%m-%d %H:%M:%S')
        elif re.match(pattern3, dt):
            dtformat = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d') + ' '
            ret = dtformat + dt
        elif re.match(pattern4, dt):
            strdate = str(datetime.datetime.now().year) + '-' + dt
            strdate = strdate.replace('月', '-')
            ret = strdate.replace('日', '')
        elif '+0800' in dt:
            dtformat = datetime.datetime.strptime(dt, '%a %b %d %H:%M:%S +0800 %Y')
            ret = datetime.datetime.strftime(dtformat, '%Y-%m-%d %H:%M:%S')
        elif '发布时间：' in dt:
            ret = dt.split('发布时间：')[-1].strip()
        else:
            ret = dt
    except Exception as e:
        print(e.args)
    finally:
        return ret


def format_string(text):
    pattern = re.compile('<[A-Za-z\\/].*?>')
    text = re.sub(pattern, '', text)
    return text
