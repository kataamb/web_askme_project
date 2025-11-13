
from django import template


register = template.Library() # registrate our tag

TAGS = [
{
       "name" : i,
    } for i in ['bender', 'python', 'django', 'TechnoPark', "MySQL"]
]


@register.simple_tag()
def get_popular_tags_base():
    return TAGS
