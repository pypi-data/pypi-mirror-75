from ..utils import ViewUtil
import re

"""
 * 表达式类
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
"""
class Expression:

    def __init__(self,attrs = []):

        # 起始符号
        self.start = None;
        # 结束符号
        self.end = None;
        # 表达式名称,比如for,if list
        self.name = None
        # 表达式对应的处理方法,表达式匹配成功后,交由此方法处理
        self.handle = None
        # 是否输出之前的字符
        self.outbefore = False
        # 是否默认表达式({})
        self.defaultExp = False;
        # 是否使用标签
        self.onTag = False;

        if attrs:
            ViewUtil.setAttrs(self,attrs)

    def getName(self):

        return self.name

    def getOutbefore(self):

        return self.outbefore

    def hasdefaultExp(self):

        return self.defaultExp

    def getHandle(self):

        return self.handle

    def hasEnd(self):

        if self.end:
            return True
        else:
            return False

    def getStart(self):

        return self.start

    def getEnd(self):

        return self.end

    def getEndRule(self):

        return re.compile(r'{0}'.format(self.end));

    def getStartRule(self):
        return re.compile(r'{0}'.format(self.start));

    def getStartEndRule(self):

        return  re.compile(r'{0}|{1}'.format(self.start,self.end))



