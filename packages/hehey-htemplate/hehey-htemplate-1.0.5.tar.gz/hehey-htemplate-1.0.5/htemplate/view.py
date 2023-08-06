from .base.BaseTemplate import BaseTemplate
from .utils import ViewUtil

"""
 * 模板视图
 *<B>说明：</B>
 *<pre>
 *  主要用于对外提供模板操作接口
 *</pre>
"""
class BaseView:

    def __init__(self,attrs = {}):

        self.data = {}

        # 视图路径
        self.tplPath = '';

        # 是否开启模板缓存
        self.onCache = True;

        # 模板缓存文件目录
        self.cachePath = '';

        # 资源地址,比如js,css,img
        self.urls = {}

        # 模板缓存有效期,单位秒,0 表示无有效期
        self.timeout = 30 * 60;

        self.expStart = '{{';

        self.expEnd = '}}'

        # 表达式结束符号
        self.expEndSign = '/'

        self.onTag = True

        self.tagStart = '<'

        self.tagEnd = '>'
        # 标签结束符号
        self.tagEndSign = '/'

        self.sysTags = [];

        self.customTags = [];

        if attrs:
            ViewUtil.setAttrs(self, attrs)


    def assign(self,name,value):

        self.data[name] = value


    def fetch(self,tplFile,data = {}):

        tpldata = {};
        if data:
            tpldata = data.copy();

        tpldata = dict(tpldata, **self.data);

        self.data = {};
        template = self.getTemplate();

        return template.fetch(tplFile,tpldata)

    def getTemplate(self)->'Template':

        tpl_conf = self.__getTemplateConf()

        return Template(tpl_conf)


    def __getTemplateConf(self):

        return {
            'tplPath':self.tplPath,
            'onCache':self.onCache,
            'cachePath':self.cachePath,
            'urls': self.urls,
            'timeout': self.timeout,
            'expStart': self.expStart,
            'expEnd': self.expEnd,
            'expEndSign': self.expEndSign,
            'onTag': self.onTag,
            'tagStart': self.tagStart,
            'tagEnd': self.tagEnd,
            'tagEndSign': self.tagEndSign,
            'sysTags': self.sysTags,
            'customTags': self.customTags,
        }

class Template(BaseTemplate):

    pass

class View(BaseView):

    pass

# 注册模板过滤器
def reg_temp_filter(funcName = ''):

    def decorator(func):

        name = funcName;
        if not name:
            name = func.__name__

        Template.registerFilter(name,func)

        return func

    return decorator

# 注册模板上下文数据
def reg_temp_context():

    def decorator(func):

        name = func.__name__
        Template.registerContext(name, func)

        return func

    return decorator






