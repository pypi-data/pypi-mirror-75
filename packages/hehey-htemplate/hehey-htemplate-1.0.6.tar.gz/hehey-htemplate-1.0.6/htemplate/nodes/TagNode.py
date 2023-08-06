from .BaseNode import BaseNode

"""
 * 普通标签节点
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class TagNode(BaseNode):

    def __init__(self,body,attrs = {}):

        super().__init__(body,attrs)

        return ;