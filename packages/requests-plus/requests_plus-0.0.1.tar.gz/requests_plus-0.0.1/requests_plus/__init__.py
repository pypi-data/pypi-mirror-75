import requests, bs4

def help():
    print('''这是一个在requests库和bs4库的基础上的简洁库，
可以缩小爬虫代码，当然，你要先用import命令导入requests_plus库。
这个库有三个功能:
1. [data] = requests_plus.get(网址,请求头,解析名称,解析类名,解析类型('find','find_all'),编码
作用:获取网页源码并解析。
注意:只有网址参数必填。
2. [data] = requests_plus.getcode(网址):
作用:获取请求状态码
3. [data] = requests_plus.quick_read(文件名,读取类型)
作用:快速读取文件''')

def help_en():
    print('''This is a concise library based on the requests library and the bs4 library.
You can reduce the crawler code, of course, you have to use the import command to import the requests_ plus library.
This library has three functions:
1. [data] = requests_plus.get (url,headers,resolution name,resolution class name, resolution type ('find','find_all'), encoding)
Function: get the source code of the web page and parse it.
Note: only url parameters are required.
2. [data] = requests_plus.getcode (url):
Function: get the request status code
3. [data] = requests_plus.quick_read (file name, read type).
Function: read files quickly''')
    print()
    print('Translation is not 100% accurate')
    

def get(url,headers='',name='',class_='',type_='find',encoding='utf-8'):
    if headers != '':
        plus_1 = requests.get(url=url,headers=headers)
        plus_1.encoding = encoding
    elif headers == '':
        plus_1 = requests.get(url=url)
        plus_1.encoding = encoding
    plus_2 = bs4.BeautifulSoup(plus_1.text,'html.parser')
    if name != '' and class_ != '':
        if type == 'find_all':
            plus_3 = soup.find_all(name=name,class_=class_)
            return plus_3
        elif type == 'find':
            plus_3 = soup.find(name=name,class_=class_)
            return plus_3
    elif name != '' and class_ == '':
        if type == 'find_all':
            plus_3 = soup.find_all(name=name)
            return plus_3
        elif type == 'find':
            plus_3 = soup.find(name=name)
            return plus_3
    else:
        return plus_2

def getcode(url):
    codingtext = requests.get(url)
    return codingtext.status_code

def quick_read(name,type_):
    with open (name,type_) as file:
        data = file.read()
    return data

