from .BaseNode import BaseNode

"""
 * 方法节点
 *<B>说明：</B>
 *<pre>
 * 比如block 的节点,就需要此接口生成对应格式字符
 * block 模块代码 以python 方法的方式呈现
 * 如需方法的方式呈现都可以以此接口表示
 *</pre>
"""
class FuncNode(BaseNode):

    def __init__(self,body,attrs = {}):

        super().__init__(body,attrs)

        return ;