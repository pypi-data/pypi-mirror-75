
"""
 * 缓存模板基类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class MyTemplate:

    def __init__(self,template = None):

        self.template = template

        self._tempdata = None;

        return ;

    # 模板方法调用统一入口
    # <B> 说明： </B>
    # <pre>
    # 通过此方法间接调用过滤器的方法
    # </pre>
    def call(self,funcName,*params):

        funcMeta = getattr(self.template.__class__.filters, funcName)

        return funcMeta(*params)

    # layout 标签辅助方法
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def layout(self,tplFile,blocks:dict):

        layoutContent = str(self.template.loadTemplate(tplFile))

        for blockName,blockContent in blocks.items():
            blockFunc = getattr(self,blockName)
            layoutContent = layoutContent.replace(blockContent, ''.join(blockFunc()))

        return layoutContent

    # block 标签辅助方法
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def block(self,blockName):

        blockFunc = getattr(self, blockName)

        return ''.join(blockFunc());

    # include 标签辅助方法
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def include(self,tplFile):

        return self.template.loadTemplate(tplFile)

    # for 标签辅助方法
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def fordata(self,data,attrs = {}):

        var_key = attrs.get('key', None)
        var_value = attrs.get('value', None)

        if isinstance(data,list):
            if  var_key is None:
                return data;
            else:
                if var_value is None:
                    return range(len(data))
                else:
                    return enumerate(data)

        elif isinstance(data,dict):
            if var_value is not None and var_key is not None:
                return data.items()
            else:
                return data

        return data

    def getvalue(self,valueDic,keys:str,sale = False):

        if  not valueDic:
            return valueDic;

        keyList = keys.split(".")
        tempVal = valueDic;
        for key in keyList:
            if not tempVal:
                return ;
            tempVal = tempVal.get(key,'')

        if sale :
            tempVal = self.call("safe",tempVal)

        return tempVal;

    # for 标签辅助方法
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def fortag(self, data):

        if isinstance(data, list):
            return data;
        elif isinstance(data, dict):
            data.items()

        return data