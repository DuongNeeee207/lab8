from django import template
from decimal import Decimal

register = template.Library()

@register.filter(name='vnd')
def vnd(value):
    """
    Format số thành định dạng tiền Việt Nam chuẩn: 189000 -> 189.000₫
    Hỗ trợ int, float, Decimal, str
    """
    if value is None or value == '':
        return '0₫'
    try:
        val = int(round(float(value)))
        formatted = f"{val:,}".replace(",", ".")
        return f"{formatted}₫"
    except (ValueError, TypeError):
        return f"{value}₫"

@register.filter(name='vnd_symbol')
def vnd_symbol(value):
    """Alias cho vnd"""
    return vnd(value)

@register.filter(name='vnd_text')
def vnd_text(value):
    """
    Format số thành dạng text: 189000 -> 189.000 VNĐ
    """
    if value is None or value == '':
        return '0 VNĐ'
    try:
        val = int(round(float(value)))
        formatted = f"{val:,}".replace(",", ".")
        return f"{formatted} VNĐ"
    except (ValueError, TypeError):
        return f"{value} VNĐ"

@register.filter(name='vnd_no_symbol')
def vnd_no_symbol(value):
    """
    Format số chỉ có dấu chấm phân cách: 189000 -> 189.000
    """
    if value is None or value == '':
        return '0'
    try:
        val = int(round(float(value)))
        return f"{val:,}".replace(",", ".")
    except (ValueError, TypeError):
        return str(value)
