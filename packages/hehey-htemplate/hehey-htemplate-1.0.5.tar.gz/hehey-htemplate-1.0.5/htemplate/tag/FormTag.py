from .Tag import Tag
from ..nodes.BaseNode import BaseNode

"""
 * html标签库
 *<B>说明：</B>
 *<pre>
 *  使用
 *</pre>
"""
class FormTag(Tag):

    def __init__(self,template):

        super().__init__(template)
        self.tags = [
            {'name': "select", 'close': False,'onTag':True},
            {'name': "text", 'close': False, 'onTag': True},
            {'name': "radio", 'close': False, 'onTag': True},
            {'name': "checkbox", 'close': False, 'onTag': True},
        ]

        return ;


    # select 标签
    def _select(self,node_attrs,mainNode:BaseNode):

        attrs = self.parseAttr(node_attrs)
        htmlAttrs,heAttrs = self.spiltAttr(attrs);
        hename = heAttrs.get("he-name")
        hetext = heAttrs.get("he-text","")
        hevalue = heAttrs.get("he-value", None)

        if not hevalue:
            hevalue = "_request.{0}".format(attrs['name'])

        attrsHtml = self.buildHtmlAttrs(htmlAttrs);
        html = '''<select {0}>
               <option value="">{1}</option>
               <for name="{2}" key="_key" value="_value">
                   <if condition="str(_key) == str({3})">
                        <option selected="selected" value="{4}">{5}</option>
                   <else/>
                        <option value="{4}">{5}</option>
                   </if>
               </for>
               </select>'''

        html = html.format(attrsHtml,hetext,hename,hevalue,self.buildVar("_key"),self.buildVar("_value"));
        tagNode = mainNode.makeNode(html,True)
        tagNode.find();

        mainNode.writeSameNode(tagNode,False,False)

        pass

    # input text 标签
    def _text(self, node_attrs, mainNode: BaseNode):

        attrs = self.parseAttr(node_attrs)
        htmlAttrs, heAttrs = self.spiltAttr(attrs);
        hevalue = heAttrs.get("he-value",None)

        if not hevalue:
            hevalue = self.buildVar("_request.{0}".format(attrs['name']))
        else:
            hevalue = self.buildVar(hevalue)

        attrsHtml = self.buildHtmlAttrs(htmlAttrs);
        html = '''<input type="text" {0} value="{1}" />'''

        html = html.format(attrsHtml, hevalue);
        tagNode = mainNode.makeNode(html, True)
        tagNode.find();

        mainNode.writeSameNode(tagNode, False, False)

        pass

    # input text 标签
    def _radio(self, node_attrs, mainNode: BaseNode):

        attrs = self.parseAttr(node_attrs)
        htmlAttrs, heAttrs = self.spiltAttr(attrs);
        hevalue = heAttrs.get("he-value", None)
        radiovalue = htmlAttrs.get("value", '')

        if not hevalue:
            hevalue = "_request.{0}".format(attrs['name'])

        attrsHtml = self.buildHtmlAttrs(htmlAttrs);
        html = '''<input type="radio" {0} <if condition="str({1}) == str({2})">checked="checked"</if> />'''
        html = html.format(attrsHtml, hevalue,radiovalue);
        tagNode = mainNode.makeNode(html, True)
        tagNode.find();

        mainNode.writeSameNode(tagNode, False, False)

        pass

    # input text 标签
    def _checkbox(self, node_attrs, mainNode: BaseNode):

        attrs = self.parseAttr(node_attrs)
        htmlAttrs, heAttrs = self.spiltAttr(attrs);
        hevalue = heAttrs.get("he-value", None)
        radiovalue = htmlAttrs.get("value", '')

        if not hevalue:
            hevalue = "_request.{0}".format(attrs['name'])

        attrsHtml = self.buildHtmlAttrs(htmlAttrs);
        html = '''<input type="checkbox" {0} <if condition="str({1}) == str({2})">checked="checked"</if> />'''
        html = html.format(attrsHtml, hevalue, radiovalue);
        tagNode = mainNode.makeNode(html, True)
        tagNode.find();

        mainNode.writeSameNode(tagNode, False, False)

        pass













