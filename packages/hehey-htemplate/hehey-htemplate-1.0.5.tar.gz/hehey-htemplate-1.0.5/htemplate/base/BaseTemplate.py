from ..utils import ViewUtil
import hashlib,os,time,types,inspect
from .TemplateCompiler import TemplateCompiler
from .Filters import Filters

"""
 * 模板基类
 *<B>说明：</B>
 *<pre>
 *  使用
 *</pre>
"""
class BaseTemplate:

    # 函数过滤器对象
    filters = None;

    # 上下文对象
    context = None;

    # 模板代码缓存字典
    caches = {}


    def __init__(self, attrs={}):

        # 模板文件扩展名
        self.suffix = 'html'

        # 模板文件根路径
        self.tplPath = '';

        # 是否开启模板缓存,开启后,会自动缓存代码,加快模板解析的速度
        self.onCache = True;

        # 模板缓存文件目录,模板编译的python代码缓存在文件中,缓存文件存储此目录中
        self.cachePath = '';

        # 资源地址,比如js,css,img,默认提供static(静态资源路径),res(外部资源,比如上传的文件) 字典key
        self.urls = {}

        # 模板缓存有效期,单位秒,0 表示无有效期
        self.timeout = 3;

        # 表达式起始符
        self.expStart = '{{';
        # 表达式结束符
        self.expEnd = '}}'

        # 结束表达式的结束符比如/ 则完整表达式为{/for} 或end,{endfor}
        self.expEndSign = '/'

        # 是否启用标签规则,开启后,匹配表达式 <import name="eduhome.name.yong" />
        self.onTag = True

        # 标签起始符
        self.tagStart = '<'
        # 标签结束符
        self.tagEnd = '>'

        # 结束标签结束符号
        self.tagEndSign = '/'

        # 系统标签,默认自动加载sys 表达式,默认标签,书写时无需写入前缀,比如<css href="xxx" />
        self.sysTags = [];

        # 自定义标签,书写时必须写入前缀,比如 标签名称html,则css 标签的书写规则为: <html:css href="xxx" />
        self.customTags = [];

        # 当前模板数据
        self.data = {};

        # 默认表达式标签对象列表
        self.defaultExpressions = []

        # 系统标签对象
        self.defaultSysTag = None;

        self.contextData = {}; # 当前模板上下文数据

        if attrs:
            ViewUtil.setAttrs(self, attrs)

        self.__initView()

    def __initView(self):

        if self.__class__.filters.template is None:
            self.__class__.filters.setTemplate(self)

        staticUrl = self.urls.get('static', None)
        if staticUrl is None:
            self.urls['static'] = '';

        resUrl = self.urls.get('res', None)
        if resUrl is None:
            self.urls['res'] = '';

        return ;

    # 验证过滤器是否存在
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def hasfilters(self, func):

        return hasattr(self.__class__.filters, func)

    # 获取模板预加载的标签库表达式对象
    # <B> 说明： </B>
    # <pre>
    # 不包括模板文件导入的标签
    # </pre>
    def getTaglibExpression(self)->'list':

        if self.defaultExpressions:
            return self.defaultExpressions;

        expList = [];
        from ..tag.Tag import Tag

        defaultSysTag = Tag.make('sys', self)
        self.defaultSysTag = defaultSysTag;

        expList = defaultSysTag.getTagExpression();

        # 系统标签
        for tagName in self.sysTags:
            expList = expList + self.buildTaglibExpression(tagName,True)

        # 自定义标签
        for tagName in  self.customTags:
            expList = expList + self.buildTaglibExpression(tagName)


        self.defaultExpressions = expList

        return self.defaultExpressions

    # 获取指定标签库的所有表达式对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def buildTaglibExpression(self,tagName,sysTag = False)->'list':

        from ..tag.Tag import Tag
        tagObj = Tag.make(tagName, self)

        tagAlias = ''
        if sysTag is False:
            tagAlias = tagObj.getAlias();
            if not tagAlias:
                tagAlias = tagName

        return tagObj.getTagExpression(tagAlias)

    # 注册模板过滤器
    # <B> 说明： </B>
    # <pre>
    # 对外唯一入口
    # </pre>
    @classmethod
    def registerFilter(cls,funcName,funcMeta):

        if cls.filters is None:
            cls.filters = Filters()

        signature = inspect.signature(funcMeta)
        firstArg = list(signature.parameters.keys())[0];
        if firstArg == 'self':
            setattr(cls.filters, funcName,  types.MethodType(funcMeta, cls.filters))
        else:
            setattr(cls.filters, funcName,funcMeta)

    # 注册模板上下文
    # <B> 说明： </B>
    # <pre>
    # 对外唯一入口
    # </pre>
    @classmethod
    def registerContext(cls, funcName, funcMeta):

        if cls.context is None:
            from .TemplateContext import TemplateContext
            cls.context = TemplateContext()

        cls.context.register(funcName,funcMeta)


    # 注入模板参数
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def assign(self, name, value):

        self.data[name] = value

        return ;

    # 加载模板并返回执行模板结果
    # <B> 说明： </B>
    # <pre>
    # 对外唯一入口
    # </pre>
    def fetch(self, tpl, data = {}):

        self.data.update(data)

        return self.loadTemplate(tpl)

    # 加载模板
    # <B> 说明： </B>
    # <pre>
    # 内部调用,目前用于小物件
    # </pre>
    def render(self,tpl,data = {}):

        # 扩展名处理
        tpl = self._buildTempExt(tpl)
        viewTplCode = self.compile(tpl)
        result = ''
        mydata = self._mergeContext(data);
        from .MyTemplate import MyTemplate
        mydata['_result'] = result
        mydata['_this'] = self
        mydata['_MyTemplate'] = MyTemplate
        mydata['FI'] = self.__class__.filters

        exec(viewTplCode, mydata)

        return mydata['_result']

    # 加载,执行模板模板
    # <B> 说明： </B>
    # <pre>
    # 内部调动,目前用于include,layout 标签,
    # </pre>
    def loadTemplate(self, tpl):
        # 扩展名处理
        tpl = self._buildTempExt(tpl)
        viewTplCode = self.compile(tpl)
        result = ''

        mydata = self._mergeContext(self.data);
        from .MyTemplate import MyTemplate
        mydata['_result'] = result
        mydata['_this'] = self
        mydata['_MyTemplate'] = MyTemplate
        mydata['FI'] = self.__class__.filters
        exec(viewTplCode,mydata)

        return mydata['_result']

    # 检测模板缓存文件有效
    # <B> 说明： </B>
    # <pre>
    # True: 表示模板缓存有效
    # False:表示模板缓存失效
    # </pre>
    def checkTemplateCacheFile(self, templateFile = ''):

        if self.onCache is not True:
            return False

        tplFilePath = self._buildTemplateFilePath(templateFile)
        tplCacheFilePath = self._buildTemplateCacheFilePath(templateFile)

        if not os.path.exists(tplFilePath):
            raise RuntimeError('template {0} file is not exist'.format(templateFile))

        if not os.path.exists(tplCacheFilePath):
            return False

        tplFilePathStat = os.stat(tplFilePath)
        tplCacheFilePathStat = os.stat(tplCacheFilePath)
        tplFilePathUptime = tplFilePathStat.st_mtime

        # 校验修改事件
        if tplFilePathUptime > tplCacheFilePathStat.st_mtime:
            return False
        # 校验有效期
        nowTime = int(time.time())

        if self.timeout > 0 and nowTime > (int(tplCacheFilePathStat.st_mtime) + self.timeout):
            return False

        return True

    # 检测代码缓存是否过期
    # <B> 说明： </B>
    # <pre>
    # True: 表示模板缓存有效
    # False:表示模板缓存失效
    # </pre>
    def checkTemplateCacheCode(self, templateFile):

        tplFilePath = self._buildTemplateFilePath(templateFile)
        if not os.path.exists(tplFilePath):
            raise RuntimeError('template {0} file is not exist'.format(templateFile))

        tplFilePathUptime = os.stat(tplFilePath).st_mtime
        cacheCode = self._getTemplateContentFromCache(templateFile);

        if not cacheCode:
            return False

        cacheCodeTime = cacheCode['time']

        if tplFilePathUptime > cacheCodeTime:
            return False

        nowTime = int(time.time())

        if self.timeout > 0 and nowTime > (cacheCodeTime + self.timeout):
            return False

        return True;

    # 合并上下文数据
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def _mergeContext(self,data):

        if self.__class__.context and not self.contextData:
            self.contextData = self.__class__.context.getContext()

        mydata = {}
        mydata.update(self.contextData);
        mydata.update(data);

        return mydata;

    # 构建模板扩展名
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def _buildTempExt(self,tpl):

        tplExt = ViewUtil.getFileExt(tpl);
        if not tplExt:
            tpl = '{0}.{1}'.format(tpl,self.suffix)

        return tpl

    # 编译模板
    # <B> 说明： </B>
    # <pre>
    # 单纯的编译模板文件,不执行python 代码
    # </pre>
    def compile(self, templateFile):

        if self.onCache and (self.cachePath and self.checkTemplateCacheFile(templateFile)) or (not self.cachePath and self.checkTemplateCacheCode(templateFile)):
            cacheCode = self._getTemplateContentFromCache(templateFile)
            if not cacheCode:
                # 缓存有效
                tplCacheFilePath = self._buildTemplateCacheFilePath(templateFile)
                with open(tplCacheFilePath, 'r') as f:
                    viewTplCode = f.read()

                self._writeTemplateContentToCache(templateFile,viewTplCode)

            else:
                viewTplCode = cacheCode['code']

        else:
            templateContent = self.__compileTemplate(templateFile);
            viewTplCode = self._buildFullTemplateCode(templateContent, templateFile)

            # 编译代码写入内存缓存
            if self.cachePath:
                tplCacheFilePath = self._buildTemplateCacheFilePath(templateFile)
                with open(tplCacheFilePath, 'w') as f:
                    f.write(viewTplCode)

            # 编译代码写入内存缓存
            self._writeTemplateContentToCache(templateFile,viewTplCode)

        return viewTplCode

    def __compileTemplate(self,templateFile)->'str':

        tplCompilerContent = self._readTemplateContent(templateFile);
        templateCompiler = self.makeTemplateCompiler()
        templateContent = templateCompiler.compiler(tplCompilerContent)

        return templateContent

    # 读取模板内容
    def _readTemplateContent(self,templateFile)->'str':

        tplFilePath = self._buildTemplateFilePath(templateFile)
        tplCompilerContent = ''
        with open(tplFilePath, 'r') as f:
            tplCompilerContent = f.read()

        lines = tplCompilerContent.splitlines()
        tplCompilerContent = r'\n'.join(lines)

        return tplCompilerContent

    # 创建模板编译对象
    # <B> 说明： </B>
    # <pre>
    # 用于编译模板
    # </pre>
    def makeTemplateCompiler(self) -> 'TemplateCompiler':

        return TemplateCompiler(self)

    # 从缓存获取模板内容
    # <B> 说明： </B>
    # <pre>
    #
    # </pre>
    def _getTemplateContentFromCache(self,templateFile):

        cacheKey = self._buildCacheKey(templateFile)

        return self.__class__.caches.get(cacheKey,None)

    def _writeTemplateContentToCache(self,templateFile,tplCompilerContent):

        cacheKey = self._buildCacheKey(templateFile)
        self.__class__.caches[cacheKey] = {"time":int(time.time()),"code":tplCompilerContent}

        return ;

    def _buildCacheKey(self,templateFile):

        tplFilePath = self._buildTemplateFilePath(templateFile).encode("utf8");
        tplFileHash = hashlib.md5(tplFilePath)

        return tplFileHash.hexdigest()



    # 构建模板文件绝对路径
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def _buildTemplateFilePath(self, templateFile):

        tplFilePath = self.tplPath + templateFile

        return tplFilePath

    # 构建模板缓存文件绝对路径
    # <B> 说明： </B>
    # <pre>
    # True: 表示模板缓存有效
    # False:表示模板缓存失效
    # </pre>
    def _buildTemplateCacheFilePath(self, templateFile):

        tempFileList = templateFile.split('.')[0].split('/');
        tempFile = '_'.join(tempFileList);
        tplFile = self._buildTemplateFilePath(templateFile).encode("utf8");
        tplFileHash = hashlib.md5(tplFile)

        return '{0}{1}_{2}.py'.format(self.cachePath, tplFileHash.hexdigest(),tempFile)

    def _buildTemplateClazz(self, templateFile):

        tplFile = self._buildTemplateFilePath(templateFile).encode("utf8");
        tplFileHash = hashlib.md5(tplFile)
        templateClazz = 'view{0}'.format(tplFileHash.hexdigest());

        return templateClazz

    def _buildFullTemplateCode(self, compileContent, templateFile):

        templateClazz = self._buildTemplateClazz(templateFile)
        with open(os.path.dirname(os.path.realpath(__file__)) + '/view.html', 'r') as f:
            viewTplCode = f.read()
            viewTplCode = viewTplCode.format(clazz=templateClazz, body=compileContent)

        return viewTplCode