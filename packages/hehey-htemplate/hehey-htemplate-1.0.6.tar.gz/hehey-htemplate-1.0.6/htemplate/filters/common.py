from ..view import reg_temp_filter
import time, datetime,re
from decimal import Decimal

# 注入默认过滤器

# 静态资源-地址
@reg_temp_filter('sta')
def sta_filter(self,imgUrl):

    return  '{0}{1}'.format(self.template.urls['static'],imgUrl)

# 静态资源-js
@reg_temp_filter('js')
def js_filter(self,jsUrl):

    return '{0}{1}'.format(self.template.urls['static'],jsUrl)

# 静态资源-css
@reg_temp_filter('css')
def css_filter(self,cssUrl):

    return  '{0}{1}'.format(self.template.urls['static'],cssUrl)

# 静态资源-图片
@reg_temp_filter('img')
def img_filter(self,imgUrl):

    return  '{0}{1}'.format(self.template.urls['static'],imgUrl)

# 外部资源
@reg_temp_filter('res')
def res_filter(self,resUrl):

    return  '{0}{1}'.format(self.template.urls['res'],resUrl)

# 小物件
@reg_temp_filter('widget')
def widget_filter(self,func:str,data = {},options = {}):

    from ..utils import ViewUtil
    pos = func.find(':')
    if pos == -1:
        # 函数
        funcMeta = ViewUtil.getFuncMeta(func)
        return funcMeta(data)
    else:
        # 类方法
        clazz = func[0:pos]
        clazzMeta = ViewUtil.getModuleMeta(clazz)
        funcName = func[pos + 1:]
        funcMeta = getattr(clazzMeta(data),funcName)

        return funcMeta()

# 计算字符长度
@reg_temp_filter('len')
def len_filter(value):

    text = "{0}".format(value)

    return len(text)

# 去掉两边空格
@reg_temp_filter('trim')
def trim_filter(value):

    text = "{0}".format(value)

    return text.strip()

# 去掉左边空格
@reg_temp_filter('ltrim')
def ltrim_filter(value):

    text = "{0}".format(value)

    return text.lstrip()

# 去掉右边空格
@reg_temp_filter('rtrim')
def rtrim_filter(value):

    text = "{0}".format(value)

    return text.rstrip()

# 日期格式化
@reg_temp_filter('date')
def date_filter(datestr,format):
    if datestr is None:
        now = datetime.datetime.now()
        return  now.strftime(format)
    else:

        if datestr:
            if isinstance(datestr,int):
                #时间戳
                timeItems = time.localtime(datestr)
            else:
                timeItems = time.strptime(datestr, "%Y-%m-%d %H:%M:%S")
            return time.strftime(format, timeItems)
        else:
            return ''
    pass


# 截取字符串
@reg_temp_filter('substr')
def substr_filter(value:str,start_pos = 0,sublen = 0):

    if sublen:
        return value[start_pos:sublen]
    else:
        return value[start_pos:]

# 浮点型,保留小数点
@reg_temp_filter('float')
def float_filter(value:float,point = None):
    decimal = Decimal(value)
    if  point is None:
        return round(decimal)

    if isinstance(point,int):
        return round(decimal,point)

    return value

# 去除html 标签
@reg_temp_filter('striptags')
def striptags_filter(html:str):

    regex = re.compile(r'<[^>]+>', re.S)
    html = regex.sub('', html)

    return html
