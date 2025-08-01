from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """乘法过滤器"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def sub(value, arg):
    """减法过滤器"""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def add_class(field, css_class):
    """为表单字段添加CSS类"""
    return field.as_widget(attrs={"class": css_class})