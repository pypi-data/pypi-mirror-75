import re
from ..nodes.MainNode import MainNode
from ..utils import ViewUtil


"""
 * 模板编译类
 *<B>说明：</B>
 *<pre>
 *  负责解析模板
 *</pre>
"""
class TemplateCompiler:

    def __init__(self,template = None):

        # 当前的模板对象
        self.template = template

        # 页面的标签列表
        self.pageTags = {}

        # 表达式对象缓存
        self.expressionsCache = [];

        # 默认表达式对象,比如{}
        self.defaultExp = None;

    # 添加标签库
    # <B> 说明： </B>
    # <pre>
    # 模板动态添加标签库
    # </pre>
    def addTags(self,tag:str):

        tagList = tag.split(',')
        for tag in tagList:
            self.pageTags[tag] = tag

        self.buildPageTagExpression();

        return ;

    # 构建当前页面所有的标签表达式对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def buildPageTagExpression(self):

        self.expressionsCache = self.template.getTaglibExpression()

        for tagName in self.pageTags:
            self.expressionsCache += self.template.buildTaglibExpression(tagName);

        from .Expression import Expression
        if self.defaultExp is None:
            expAttrs = {'name': "exp", 'close': False, 'outbefore': True,'defaultExp':True, 'handle': self.template.defaultSysTag._exp,
                        'start': self.getExpPattern()}
            self.defaultExp = Expression(expAttrs)

        self.expressionsCache.append(self.defaultExp)

        return ;

    # 获取当前页面的所有标签表达式
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getAllExpression(self):

        if not self.expressionsCache:
            self.buildPageTagExpression()

        return self.expressionsCache;


    def buildExpTagPattern(self):

        if hasattr(self, "_expTag"):
            return getattr(self,"_expTag");

        self.getAllExpression();
        expPatternList = [];
        for exp in self.expressionsCache:
            if exp.getName() != 'exp':
                if exp.onTag:
                    expPatternList.append(exp.getStart())
            else:
                expPatternList.append(r"{0}".format(exp.getStart()))

        setattr(self,"_expTag",re.compile(r"{0}".format("|".join(expPatternList))))

        return getattr(self,"_expTag");

    def getExpressionPatternList(self):

        self.buildPageTagExpression();
        expressionsList = ViewUtil.split_list(self.expressionsCache,20)

        newExpList = [];
        for expList in expressionsList :
            expPatternList = [];
            for exp in expList:
                expPatternList.append(r"{0}".format(exp.getStart()))

            if expPatternList:
                newExpList.append(r"{0}".format("|".join(expPatternList)))

        return newExpList

    # 获取当前页面所有表达式对象组合的正则表达式对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getAllExpressionPattern(self):

        self.buildPageTagExpression();
        expList = []

        for exp in self.expressionsCache:
            expList.append(r"{0}".format(exp.getStart()))

        return re.compile(r"{0}".format("|".join(expList)))

    def getTemplatePattern(self,pattern = False):

        if self.template.onTag:
            if pattern:
                return re.compile(r"{0}|{1}".format(self.getExpPattern(), self.getTagPattern()))
            else:
                return "{0}|{1}".format(self.getExpPattern(), self.getTagPattern())
        else:
            if pattern:
                return re.compile(r"{0}".format(self.getExpPattern()))
            else:
                return "{0}".format(self.getExpPattern())

    def getExpStart(self):

        return self.template.expStart

    def getExpEnd(self):

        return self.template.expEnd

    def getTagStart(self):

        return self.template.tagStart

    def getTagEnd(self):

        return self.template.tagEnd

    def getTemplateExpReg(self,pattern):

        expReg = r'{0}[^\s].+?{1}'.format(self.template.expStart, self.template.expEnd)
        tagReg = r'{0}[^{1}]*?{2}'.format(self.template.tagStart, self.template.tagEnd, self.template.tagEnd)

        if self.template.onTag:
            if pattern:
                return re.compile(r"({0}|{1})".format(expReg, tagReg))
            else:
                return r"({0}|{1})".format(expReg, tagReg)
        else:
            if pattern:
                return re.compile(r"({0})".format(expReg))
            else:
                return "({0})".format(expReg)

        return re.compile(r"({0}|{1})".format(expReg, tagReg))

    def getExpPattern(self,pattern = False):

        if pattern:
            return re.compile(r'{0}([^\d\s].+?){1}'.format(self.template.expStart, self.template.expEnd));
        else:
            #exp = r'{0}(?![\\n|\s])(.*?){1}'.format(self.template.expStart,self.template.expEnd)
            exp = r'{0}([^\s].+?){1}'.format(self.template.expStart,self.template.expEnd)
            return exp;

    def getTagPattern(self,pattern = False):

        if pattern:
            return re.compile(r'{0}([^{1}]*?){2}'.format(self.template.tagStart, self.template.tagEnd, self.template.tagEnd));
        else:
            return '{0}([^{1}]*?){2}'.format(self.template.tagStart,self.template.tagEnd,self.template.tagEnd);

    # 编译入口
    # <B> 说明： </B>
    # <pre>
    # 此方法预留吧
    # </pre>
    @classmethod
    def parse(cls, content, attrs = {}):

        template = cls(attrs)

        return template.compiler(content)

    # 解析编译模板内容
    # <B> 说明： </B>
    # <pre>
    # 返回模板解析后的内容
    # </pre>
    def compiler(self,content):

        mainNode = MainNode(content,{
            'template':self.template,
            'compiler':self,
        })

        mainNode.start()
        compileContent = mainNode.formatNode();

        return compileContent
