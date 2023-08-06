
"""
 * 模板上下文
 *<B>说明：</B>
 *<pre>
 *  使用
 *</pre>
"""
class TemplateContext:

    def __init__(self):

        self.template = None

        self.contextList = {} # 上下文定义

        return ;


    def register(self,funcName, funcMeta):

        self.contextList[funcName] = funcMeta

        return ;

    def getContext(self)->'list':

        data = {};
        for funcName,funcMeta in self.contextList.items():
            data.update(funcMeta())

        return data

