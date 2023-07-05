from django import template

register = template.Library()

@register.filter(name='censor')
def censor(value):
    bad_words = ['плохое_слово1', 'плохое_слово2', 'плохое_слово3', 'плохое_слово4']
    for w in bad_words:
        if w in value:
            value = value.replace(w, '***')
    return value
