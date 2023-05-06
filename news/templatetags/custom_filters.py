from django import template

register = template.Library()


@register.filter()
def censor(value):
    count = -1
    badwords = ['damn', 'fuck']

    if isinstance(value, str):
        list_value = value.split()
        for word in list_value:
            count += 1
            if word.casefold() in badwords:
                word = word[0] + '*' * (len(word) - 1)
                list_value[count] = word
            else:
                continue
    else:
        raise ValueError()

    return ' '.join(list_value)
