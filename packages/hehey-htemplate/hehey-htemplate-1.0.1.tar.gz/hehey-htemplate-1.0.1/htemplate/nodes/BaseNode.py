import re
from ..utils import ViewUtil

"""
 * 节点基类
 *<B>说明：</B>
 *<pre>
 *  
 *</pre>
"""
class BaseNode:

    NODE_TYPE_STR = 1;# 字符串
    NODE_TYPE_CODE = 2;# py 代码
    NODE_TYPE_NODE = 3;# 子节点
    NODE_TYPE_SAME = 4;  # 同级别

    def __init__(self,body:str,attrs = {}):

        self.body = body
        self.template = None
        self.startNode = None
        self.nodes = [];
        self.compiler = None;
        self.findpos = 0
        self.posend = 0
        # 停止查找
        self.stop = False
        # 表达式匹配的位置
        self.outstartpos = 0
        self.outendpos = 0

        # 格式化参数
        self.formatParams = [];

        if attrs:
            ViewUtil.setAttrs(self,attrs)

        return ;

    def getBody(self):

        return self.body

    def getLineBody(self):

        return self.body.split(r'\n')


    def writeBeforeBody(self,all = False):

        if all is True:
            beforeBody = self.body[self.outstartpos:]
        else:
            beforeBody = self.body[self.outstartpos:self.outendpos]

        beforeBody = re.sub('"', r'\"', beforeBody);

        if self.formatParams:
            #outBeforeBody = re.sub(re.compile(r"{0}".format(self.compiler.getExpPattern())), lambda x: "{" + addnumber() + "}", beforeBody)
            beforeBody = re.sub('%', r'%%', beforeBody);
            outBeforeBody = re.sub(re.compile(r"{0}".format(self.compiler.getExpPattern())),'%s', beforeBody)
        else:
            outBeforeBody = re.sub(re.compile(r"{0}".format(self.compiler.getExpPattern())), "", beforeBody)

        if self.formatParams:
            outBeforeBody = '"{0}" % ({1})'.format(outBeforeBody,','.join(self.formatParams))
        else:
            outBeforeBody = '"{0}" '.format(outBeforeBody)

        self.formatParams = []
        self.writeRawCode(outBeforeBody,True,True)
        self.outstartpos = self.outendpos

        return ;

    def addFormatParams(self,name):

        self.formatParams.append(name);

        return ;

    # 导入标签库
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def loadTaglib(self,taglib):

        self.compiler.addTags(taglib)

        return ;

    def find(self):

        #regexbody = self.compiler.getTemplateExpReg(True)

        self.posend = 0
        expList = self.compiler.getExpressionPatternList();
        regexbody = self.compiler.buildExpTagPattern();

        while True:

            if self.stop:
                break;

            resbody = regexbody.search(self.body, self.findpos)
            if resbody is None:
                self.writeBeforeBody(True)
                self.posend = 0
                break

            ratternResult = False;
            for regexStr in expList:
                regex = re.compile(regexStr);
                res = regex.match(self.body, resbody.span()[0])

                if res is None:
                    continue;

                ratternResult = True;
                expPos = self.findFullExp(res);
                resStartPos = expPos[0]
                resEndPos = expPos[1]
                expRawContent = self.body[resStartPos:resEndPos]

                expContent = expPos[2]
                self.posend = resEndPos

                # 此处,可优化性能
                self.parseExp(expRawContent,expContent,resStartPos,resEndPos);
                self.findpos = self.posend

                break;

            if not ratternResult:
                self.findpos = resbody.span()[1]

        return ;

    def parseExp(self,expRawContent,expContent,resStartPos,resEndPos):

        # 此处,可优化性能
        expressionList = self.compiler.getAllExpression()
        for exp in expressionList:
            if self.stop:
                break;
            startCompile = exp.getStartRule()
            startMatch = startCompile.search(expRawContent)

            if startMatch is not None:
                handleFunc = exp.getHandle();
                self.outendpos = resStartPos;
                # 读取查找之前的内容
                if exp.getOutbefore() is False:
                    self.writeBeforeBody()

                tagAttrs = startMatch.group(1)
                if exp.hasEnd():
                    # 标签类型
                    spanPos = self.findNodeBodyPos(self.posend, exp)
                    if spanPos:
                        self.posend = spanPos[1]
                        tagBody = self.body[resEndPos:spanPos[0]]
                        subTagNode = self.makeNode(tagBody)
                        result = handleFunc(tagAttrs, self, subTagNode)

                        if result is False:
                            break
                else:
                    # {} 类型
                    if exp.hasdefaultExp():
                        result = handleFunc(expContent, self)
                    else:
                        result = handleFunc(tagAttrs, self)

                    if result is False:
                        break

                if exp.getOutbefore() is False:
                    self.outstartpos = self.posend

                break

        return ;


    # 匹配完整的表达式
    # <B> 说明： </B>
    # <pre>
    # 由于{} 存在嵌套的情况,需二次查找
    # </pre>
    def findFullExp(self,pattern):

        # 判断起始符号 是表达式或标签
        expStart = self.compiler.getExpStart();
        tagStart = self.compiler.getTagStart();
        nodeContent = pattern.group()
        nodeStartChar = "";
        nodeEndChar = ""

        if expStart == nodeContent[0:len(expStart)]:
            nodeStartChar = expStart
            nodeEndChar = self.compiler.getExpEnd();
            pass
        elif tagStart == nodeContent[0:len(tagStart)]:
            nodeStartChar = tagStart
            nodeEndChar = self.compiler.getTagEnd();
            pass

        # 计算位置
        startNum = nodeContent.count(nodeStartChar)
        endCharNum = startNum - 1;
        expstartpos = pattern.span()[0]
        find_pos = pattern.span()[1];
        expendpos = pattern.span()[1];
        if endCharNum > 0:
            while (True):
                find_pos = self.body.find(nodeEndChar,find_pos)
                if find_pos == -1:
                    break

                if find_pos != -1:
                    endCharNum -= 1;
                    expendpos = find_pos;

                if endCharNum <= 0:
                    break;
            expendpos += 1

        return (expstartpos,expendpos,self.body[expstartpos + len(nodeStartChar):expendpos - len(nodeEndChar)])

    # 终端当前节点查找
    # <B> 说明： </B>
    # <pre>
    # 即可终止find 的查找匹配操作
    # </pre>
    def stopFind(self):

        self.stop = True

        return ;

    def makeNode(self,tagBody,format = False):

        from .TagNode import TagNode

        if format:
            lines = tagBody.splitlines()
            tagBody = r'\n'.join(lines)

        tagNode = TagNode(tagBody,
                {'template': self.template,
                 'compiler': self.compiler,
                 'startNode':self.startNode
                 });

        return tagNode

    def makeFuncNode(self,tagBody):

        from .FuncNode import FuncNode
        funcNode = FuncNode(tagBody,
                          {'template': self.template,
                           'compiler': self.compiler,
                           'startNode': self.startNode
                           });

        return funcNode

    def getNofindBody(self):

        if self.posend == 0:
            return self.body
        else:
            return  self.body[self.posend:]

    # 通过入栈的方式匹配表达式成对的起始符号与结束符号
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def findNodeBodyPos(self,findpos,exp):

        expNum = 1
        spanPos = ();
        while True:
            if expNum <= 0:
                break;

            startEndCompile = exp.getStartEndRule()
            startEndMatch = startEndCompile.search(self.body, findpos)

            if startEndMatch is not None:
                endCompile = exp.getEndRule()
                findpos = startEndMatch.span()[1]
                if endCompile.search(startEndMatch.group()) is not None:
                    # 找到结束符
                    expNum = expNum - 1
                    spanPos = startEndMatch.span()
                else:
                    expNum = expNum + 1


        return spanPos

    # 输出当前节点
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def formatNode(self,depth = 1):

        nodeList = []
        for (nodeType,node,tab,yld) in self.nodes:
            nodeStr = ''
            if nodeType == self.NODE_TYPE_STR:
                nodeStr = node
                if tab:
                    nodeStr = ('    ' * depth) + nodeStr
                else:
                    nodeStr = ('    ' * (depth - 1)) + nodeStr
            elif nodeType == self.NODE_TYPE_CODE:
                nodeStr = node
                if tab:
                    nodeStr = ('    ' * depth) + nodeStr
                else:
                    nodeStr = ('    ' * (depth - 1)) + nodeStr
            elif nodeType == self.NODE_TYPE_NODE:
                nodeStr = node.formatNode(depth + 1)
            elif nodeType == self.NODE_TYPE_SAME:
                nodeStr = node.formatNode(depth)

            if nodeStr:
                nodeList.append(nodeStr)

        return '\n'.join(nodeList)

    # 写入节点对象
    def writeNode(self, node, tab = True,yld = False):

        self.nodes.append((self.NODE_TYPE_NODE,node,tab,yld))

        return ;

    def writeSameNode(self, node, tab = True,yld = False):

        self.nodes.append((self.NODE_TYPE_SAME,node,tab,yld))

        return ;



    # 写入代码
    def writeCode(self,code,tab = True,yld = False):

        if yld:
            code = 'yield "%s" % ({0})'.format(code)

        self.nodes.append((self.NODE_TYPE_CODE,code,tab,yld))

        return ;

    def writeRawCode(self,code,tab = True,yld = False):

        if yld:
            code = 'yield {0}'.format(code)

        self.nodes.append((self.NODE_TYPE_CODE,code,tab,yld))

        return ;

    # 写入字符
    def writeStr(self,chars,tab = True,yld = True):

        if yld:
            chars = re.sub('"', r'\"', chars);
            chars = 'yield "{0}"'.format(chars)

        self.nodes.append((self.NODE_TYPE_STR, chars,tab,yld))

        return ;

    # 写入方法
    def writeFunc(self,funcName,bodyNode):

        self.writeCode('def {0}(self):'.format(funcName),True,False)
        self.writeNode(bodyNode,False,False)
        bodyNode.find();

        return ;



