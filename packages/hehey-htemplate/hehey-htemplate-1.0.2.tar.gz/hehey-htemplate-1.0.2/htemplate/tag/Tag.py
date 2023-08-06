from ..base.Expression import Expression
from ..utils import ViewUtil
import re

"""
 * 标签库基类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class Tag:

    def __init__(self,template):

        self.alias = ''
        self.tags = []
        self.template = template

        return ;

    def buildVar(self,name):

        var = '{0}{1}{2}'.format(self.template.expStart,name,self.template.expEnd)

        return var;

    @classmethod
    def make(cls,tagName,template)->'Tag':
        if not tagName:
            raise RuntimeError('tagName is empty')

        if tagName.find('.') == -1:
            tagClazzName = ViewUtil.ucfirst(tagName) + 'Tag'
            tagClazz = __package__ + "." + tagClazzName + '.' + tagClazzName
        else:
            tagClazz = tagName

        tagMeta = ViewUtil.getModuleMeta(tagClazz)

        return tagMeta(template)

    def getAlias(self):

        return self.alias

    def getTagExpression(self,alias = ''):
        expList = [];

        for tag in self.tags:
            attrs = tag.copy()

            tagName = attrs['name']
            if alias:
                attrs['name'] = '{0}:{1}'.format(alias,tagName)

            # 处理函数
            handle = tag.get('handle', None)
            if handle is None:
                handle = '_{0}'.format(tagName)

            attrs['handle'] = getattr(self,handle)

            # 起始符号
            startTag = tag.get('start', None)
            if startTag is None:
                attrs['start'] = r'{0}{1}(.*?){2}'.format(self.template.expStart, attrs['name'], self.template.expEnd)
            else:
                attrs['start'] = tag['start']

            # 结束符号符号
            closeTag = tag.get('close',None)
            if closeTag:
                eofName = tag.get('eof', self.template.expEndSign)
                attrs['end'] = '{0}{1}{2}{3}'.format(self.template.expStart,eofName,attrs['name'],self.template.expEnd)

            expList.append(Expression(attrs))

            # 启用标签
            onTag = tag.get('onTag', None)
            if onTag:
                tagAttrs = attrs.copy()
                # 起始符号
                tagStart = '{0}{1}([^a-zA-Z0-9].*?){2}'.format(self.template.tagStart, tagAttrs['name'], self.template.tagEnd)
                tagAttrs['start'] = r'{0}'.format(tagStart)

                # 结束符号符号
                closeTag = tag.get('close', None)
                if closeTag:
                    eofName = tag.get('eof', self.template.tagEndSign)
                    tagEnd = '{0}{1}{2}{3}'.format(self.template.tagStart, eofName, tagAttrs['name'],self.template.tagEnd)
                    tagAttrs['end'] = r'{0}'.format(tagEnd)

                expList.append(Expression(tagAttrs))

        return expList

    # 构建标签表达式
    def buildTagExp(self,exp:str):

        return exp.format(self.template.expStart,self.template.expStart)

    def buildCommonExp(self,exp:str):

        return exp.format(self.template.expStart,self.template.expEnd)

    # 解析变量{name} {:U('xxx')}
    def parseVar(self,varBody):
        if not varBody:
            return ''

        # 读取首字母
        firstChar =  varBody[0]
        result = '';
        if  firstChar == '$':
            # 变量
            result = self.parseName(varBody[1:],True)
        elif firstChar == ':':
            #方法
            func = varBody[1:];
            funcFirstChar = func[0];
            funcList = func.split('|')
            findpos = funcList[0].find('(')
            if findpos == -1:
                if funcFirstChar == '$':
                    funcList[0] = self.parseName(funcList[0][1:],True);
                else:
                    funcList[0] = self.parseName(funcList[0],False);

            func = "|".join(funcList)
            result = self.parseFunc(func)
        else:
            # 不处理,直接返回
            result = self.parseName(varBody);

        return result

    def parseName(self,varname,sale = False):

        #regex = re.compile("\['(\\w+)'\]|" + '\["(\\w+)"\]')
        regex1 = re.compile("\['(\\w+)'\]")
        regex2 = re.compile('\["(\\w+)"\]')
        matches1 = regex1.findall(varname);
        matches2 = regex2.findall(varname);
        if matches1 or matches2:

            keys = [];
            for key in matches1:
                keys.append(key);

            for key in matches2:
                keys.append(key);

            varnamekey = varname[0:varname.find('[')];
            if sale :
                newName = 'self.getvalue({0},"{1}",True)'.format(varnamekey,".".join(keys));
            else:
                newName = 'self.getvalue({0},"{1}")'.format(varnamekey, ".".join(keys));
            return newName
        else:
            return varname;

    # 解析属性 name="admin" file="yonghu"
    def parseAttr(self,attrBody):

        if not attrBody:
            return attrBody

        if isinstance(attrBody,dict):
            return attrBody
        reg = r'\s+([\-a-zA-Z]+)\s*=\s*"([^"]+)"'
        pattern = re.compile(reg);

        matchs = re.findall(pattern, attrBody)
        if not matchs:
            return attrBody

        attrs = {}
        for match in matchs:  # i 本身也是可迭代对象，所以下面要使用 i.group()
            attrs[match[0]] = match[1]

        return attrs


    def parseNode(self,mainNode,subNode):

        subNode.find()
        mainNode.writeNode(subNode)

        return ;


    # 解析方法
    def parseFunc(self,func:str):

        funcList = func.split('|')
        findpos = funcList[0].find('(')
        if findpos == -1:
            value = funcList.pop(0)
        else:
            value = '';

        for funcstr in funcList:
            funcName,funcParams = self.formatFunc(funcstr);
            value = self.buildFuncCall(funcName,funcParams,value);

        return value

    def buildFuncCall(self,funcName,funcParams:str,value):

        # 验证过滤器存在
        if self.template.hasfilters(funcName):
            if value:
                return 'self.call("{0}",{1})'.format(funcName, funcParams.format(value))
            else:
                return 'self.call("{0}",{1})'.format(funcName, funcParams)
        else:
            if value:
                return '{0}({1})'.format(funcName, funcParams.format(value))
            else:
                return '{0}({1})'.format(funcName, funcParams)



    # 分析字符串方法
    def formatFunc(self,func:str):

        startPos = func.find('(')
        if startPos == -1:
            # 未找到(
            paramsPos = func.find('=')
            if paramsPos == -1:
                funcName = func
                funcParams = '###';
            else:
                funcName = func[0:paramsPos]
                funcParams = func[paramsPos + 1:]
                if funcParams.find("###") == -1:
                    funcParams = '###,{0}'.format(funcParams)

        else:
            endPos = func.rfind(')')
            funcName = func[0:startPos]
            funcParams = func[startPos + 1:endPos]

        funcParams = funcParams.replace('###', "{0}")

        return funcName,funcParams

    def buildBlockFuncName(self,funcName):

        return 'layout_block_{0}'.format(funcName)

    def buildBlockFuncList(self,funcs:dict):

        blockList = {}
        for funcName,funcContent in funcs.items():
            blockList[self.buildBlockFuncName(funcName)] = funcContent

        return blockList

    def parseBlock(self,block):

        blockList = {}

        if block is None:
            blockList["default"] = "__CONTENT__"
        else:
            blocks = str(block).split(',')
            for block in blocks:
                blockValue = block.split(":")
                blockList[blockValue[0]] = blockValue[1]

        blockList = self.buildBlockFuncList(blockList)

        return blockList

    def buildHtmlAttrs(self,attrs = {}):

        html = []

        for name,value in attrs.items():
            html.append('{0}="{1}"'.format(name,value))

        return " ".join(html)


    def spiltAttr(self,attrs:dict):

        htmlAttrs = {};
        heAttrs = {};
        for attrname,attrvalue in attrs.items():
            if attrname[0:3] == 'he-':
                heAttrs[attrname] = attrvalue
            else:
                htmlAttrs[attrname] = attrvalue

        return [htmlAttrs,heAttrs];

