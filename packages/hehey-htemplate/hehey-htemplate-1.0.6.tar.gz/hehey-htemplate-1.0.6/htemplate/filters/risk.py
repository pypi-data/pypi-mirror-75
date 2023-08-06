from ..view import reg_temp_filter
"""
 * 安全过滤器
 *<B>说明：</B>
 *<pre>
 * 略
 *</pre>
"""

html_xss = {
    '&':'&amp;',
    '>':'&gt;',
    '<':'&lt;',
    "'":'&#39;',
    '"':'&#34;',
}

# xss 过滤器
@reg_temp_filter('xss')
def xss_filter(value):
    text = '{0}'.format(value)
    for find,replace in html_xss.items():
        text = text.replace(find,replace)

    return text

# 过滤所有有风险的字符
@reg_temp_filter('safe')
def safe_filter(self,value):

    value = xss_filter(value)

    return value
