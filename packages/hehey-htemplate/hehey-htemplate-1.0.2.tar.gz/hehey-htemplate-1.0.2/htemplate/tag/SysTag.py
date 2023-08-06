from ..utils import ViewUtil
from .Tag import Tag
from ..nodes.BaseNode import BaseNode

"""
 * 系统标签库
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class SysTag(Tag):

    def __init__(self,template):

        super().__init__(template)
        self.tags = [
            {'name': "taglib", 'close': False},# 标签库
            {'name': "layout", 'close': False},
            {'name': "block", 'close': True},
            {'name': "call", 'close': False},# 调用模板内部方法
            {'name': "include", 'close': False},
            {'name': "import", 'close': False},# 导入python 模块
            {'name': "css" ,'close': False,'onTag':True},
            {'name': "js", 'close': False, 'onTag': True},
            {'name': "for", 'close': True,'onTag':True},
            {'name': "raw", 'close': False},
            {'name': "list", 'close': True,'onTag':True},
            {'name': "dict", 'close': True,'onTag':True},
            {'name': "if", 'close': True,'onTag':True},
            {'name': "else", 'close': False,'onTag':True},
            {'name': "elif", 'close': False,'onTag':True},
            {'name': "python", 'close': True},# 原始python 源码
            {'name': "comment", 'close': True},  # 注释标签
            {'name': "pass", 'close': True},  # 不解析标签
            {'name': "set", 'close': False},  # 定义变量
            {'name': "empty", 'close': True},  # 判断空
            {'name': "notempty", 'close': True},  # 判断不未空
        ]

        return ;

    # {}
    def _exp(self,node_attrs,mainNode:BaseNode):

        expStr = self.parseVar(node_attrs)
        mainNode.addFormatParams(expStr)
        pass

    # 模板继承
    def _layout(self,node_attrs,mainNode:BaseNode):

        attrs = self.parseAttr(node_attrs)
        fileName =  attrs['file']
        block = attrs.get("block",None)
        blockList = self.parseBlock(block)
        mainNode.writeCode('self.layout("{0}",{1})'.format(fileName, blockList), True, True)

        if block is None:
            tagNode = mainNode.makeNode(mainNode.getNofindBody())
            mainNode.startNode.writeFunc(self.buildBlockFuncName('default'), tagNode)
            mainNode.stopFind()


        return False

    # 加载文件
    def _include(self,node_attrs,mainNode:BaseNode):

        attrs = self.parseAttr(node_attrs)
        fileName = attrs['file']
        mainNode.writeCode('self.include("{0}")'.format(fileName), True, True)
        pass

    # 加载python 模块
    def _import(self,node_attrs,mainNode:BaseNode):

        attrs = self.parseAttr(node_attrs)
        name = attrs['name']
        alias = attrs.get("as")
        pos = name.find(':')
        if pos == -1:
            mainNode.writeCode('import {0}'.format(name), True)
        else:
            packageMeta = name.rsplit(':', 1)
            if alias :
                mainNode.writeCode('from {0} import {1} as {2}'.format(packageMeta[0],packageMeta[1],alias), True)
            else:
                mainNode.writeCode('from {0} import {1}'.format(packageMeta[0], packageMeta[1]), True)

        pass

    # 块模块
    def _block(self, node_attrs, mainNode:BaseNode,subNode:BaseNode):

        attrs = self.parseAttr(node_attrs)
        blockName = attrs['name']
        mainNode.startNode.writeFunc(self.buildBlockFuncName(blockName), subNode)

        pass

    # 页面导入标签库
    def _call(self, node_attrs, mainNode: BaseNode):

        attrs = self.parseAttr(node_attrs)
        if not node_attrs:
            return

        blockName = attrs['name']
        mainNode.writeCode('self.block("{0}")'.format(self.buildBlockFuncName(blockName)), True, True)

        pass

    # 页面导入标签库
    def _taglib(self, node_attrs, mainNode:BaseNode):

        if not node_attrs:
            return

        attrs = self.parseAttr(node_attrs)
        if not isinstance(attrs, dict):
            mainNode.loadTaglib(node_attrs.strip())
        else:
            mainNode.loadTaglib(attrs['name'])

        return False

    def _css(self,node_attrs, mainNode:BaseNode):

        attrs = self.parseAttr(node_attrs)
        href = attrs['href'];
        cssFunc = 'self.call("css","{0}")'.format(href)
        attrs['href'] = '%s';
        attrsHtml = self.buildHtmlAttrs(attrs);
        codeHtml = "'<link {0} />' % ({1})".format(attrsHtml, cssFunc)

        mainNode.writeRawCode(codeHtml, True, True)

    def _js(self,node_attrs, mainNode:BaseNode):

        attrs = self.parseAttr(node_attrs)
        src = attrs['src'];
        jsFunc = 'self.call("js","{0}")'.format(src)
        attrs['src'] = '%s';
        attrsHtml = self.buildHtmlAttrs(attrs);
        codeHtml = "'<script {0} ></script>' % ({1})".format(attrsHtml, jsFunc)

        mainNode.writeRawCode(codeHtml, True, True)

    def _for(self,node_attrs,mainNode:BaseNode,subNode:BaseNode):

        attrs = self.parseAttr(node_attrs)
        if  not isinstance(attrs,dict):
            mainNode.writeCode('for {0}:'.format(node_attrs))
            self.parseNode(mainNode, subNode)
            return

        var_data = attrs['name']
        var_key = attrs.get('key', None)
        var_value = attrs.get('value', None)
        var_index = attrs.get('index', None)

        if var_index is not None:
            mainNode.writeCode('{0} = 0'.format(var_index), True, False)

        if var_key is None:
            mainNode.writeCode('for {0} in self.fordata({1},{2}):'.format(self.parseVar(var_value), self.parseVar(var_data),attrs))
        else:
            mainNode.writeCode(
                'for {0},{1} in self.fordata({2},{3}):'.format(self.parseVar(var_key), self.parseVar(var_value),
                                                        self.parseVar(var_data),attrs))
        # 继续解析node body
        self.parseNode(mainNode,subNode)

        if var_index is not None:
            subNode.writeCode('{0}+=1'.format(var_index),True,False)


    def _list(self,node_attrs,mainNode:BaseNode,subNode:BaseNode):

        attrs = self.parseAttr(node_attrs)
        if not isinstance(attrs, dict):
            mainNode.writeCode('for {0}:'.format(node_attrs))
            self.parseNode(mainNode, subNode)
            return

        varData = attrs['name']
        varKey = attrs.get('key',None)
        varValue = attrs.get('value', None)
        varIndex = attrs.get('index', None)

        if varIndex is not None:
            mainNode.writeCode('{0} = 0'.format(varIndex), True, False)

        if varKey is None:
            mainNode.writeCode('for {0} in {1}:'.format(self.parseVar(varValue), self.parseVar(varData)))
        else:
            if varValue is None:
                mainNode.writeCode('for {0} in range(len({1})):'.format(self.parseVar(varKey), self.parseVar(varData)))
            else:
                mainNode.writeCode('for {0},{1} in enumerate({2}):'.format(self.parseVar(varKey),self.parseVar(varValue), self.parseVar(varData)))

        self.parseNode(mainNode, subNode)

        if varIndex is not None:
            subNode.writeCode('{0}+=1'.format(varIndex),True,False)

    def _dict(self, node_attrs, mainNode: BaseNode, subNode: BaseNode):

        attrs = self.parseAttr(node_attrs)
        if not isinstance(attrs, dict):
            mainNode.writeCode('for {0}:'.format(node_attrs))
            self.parseNode(mainNode, subNode)
            return

        varData = attrs['name']
        varKey = attrs.get('key', None)
        varValue = attrs.get('value', None)
        varIndex = attrs.get('index', None)

        if varIndex is not None:
            mainNode.writeCode('{0} = 0'.format(varIndex), True, False)

        if varValue is None:
            mainNode.writeCode('for {0} in {1}:'.format(self.parseVar(varKey), self.parseVar(varData)))
        else:
            mainNode.writeCode(
                'for {0},{1} in {2}.items():'.format(self.parseVar(varKey), self.parseVar(varValue),
                                                        self.parseVar(varData)))
        self.parseNode(mainNode, subNode)

        if varIndex is not None:
            subNode.writeCode('{0}+=1'.format(varIndex),True,False)


    def _if(self, node_attrs, mainNode: BaseNode, subNode: BaseNode):

        attrs = self.parseAttr(node_attrs)
        if not isinstance(attrs, dict):
            condition = node_attrs
        else:
            condition = attrs['condition']

        mainNode.writeCode('if {0}:'.format(condition))


        # 继续解析node body
        self.parseNode(mainNode, subNode)

    def _elif(self, node_attrs, mainNode: BaseNode):

        attrs = self.parseAttr(node_attrs)
        if not isinstance(attrs, dict):
            condition = node_attrs
        else:
            condition = attrs['condition']

        mainNode.writeCode('elif {0}:'.format(condition),False)



    def _else(self, node_attrs, mainNode: BaseNode):

        mainNode.writeCode('else:',False)


    def _python(self,node_attrs, mainNode: BaseNode, subNode: BaseNode):
        linebody = subNode.getLineBody()

        # 查找空格最少的行
        mincount = 100000;
        for line in linebody:
            lcount = ViewUtil.countlstrip(line)

            if lcount is not False and lcount < mincount:
                mincount = lcount;

        for line in linebody:
            mainNode.writeCode(line[mincount:])

    def _comment(self,node_attrs, mainNode: BaseNode, subNode: BaseNode):

        pass

    def _pass(self,node_attrs, mainNode: BaseNode, subNode: BaseNode):

        mainNode.writeStr(subNode.getBody())

    def _set(self, node_attrs, mainNode: BaseNode):

        attrs = self.parseAttr(node_attrs)
        for name,value in attrs.items():
            mainNode.writeCode('{0} = {1}'.format(name,self.parseVar(value)))

    def _raw(self, node_attrs, mainNode: BaseNode):

        code = str(node_attrs).lstrip()
        mainNode.writeCode(code)


    def _empty(self, node_attrs, mainNode: BaseNode, subNode: BaseNode):

        attrs = self.parseAttr(node_attrs)
        if not isinstance(attrs, dict):
            condition = node_attrs
        else:
            condition = self.parseVar(attrs['name'])

        if_attrs = {
            "condition":'not {0}'.format(condition)
        }

        self._if(if_attrs,mainNode,subNode)

    def _notempty(self, node_attrs, mainNode: BaseNode, subNode: BaseNode):

        attrs = self.parseAttr(node_attrs)
        if not isinstance(attrs, dict):
            condition = node_attrs
        else:
            condition = self.parseVar(attrs['name'])

        if_attrs = {
            "condition": condition
        }

        self._if(if_attrs,mainNode,subNode)