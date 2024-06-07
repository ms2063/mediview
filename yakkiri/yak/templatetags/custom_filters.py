from django import template
import re

register = template.Library()

@register.filter
def strip_whitespace(value):
    value = value.strip()
    if value.endswith('..'):
        value = value[:-1]  # Remove the trailing period if there are two
    return value

@register.filter
def split_sentences(value):
    # Split the text into sentences
    sentence_endings = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')
    return sentence_endings.split(value)
