from ..view import reg_temp_context

# 注入默认上下文

# django 过滤器
@reg_temp_context()
def django():

    return {"reqeust":{"mok":88}}

