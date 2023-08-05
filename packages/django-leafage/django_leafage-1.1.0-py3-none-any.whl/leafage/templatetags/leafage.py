from django import template
from distutils.sysconfig import get_python_lib
from django.template import Library, loader, Context


register = template.Library()

@register.filter(name='paginator')
def paginator(object_list, style=None):
    path = 'paginator.html'
    html = loader.render_to_string(
        path,
        {
            'obj_list': object_list,
            'style': style
        }
    )

    return html


@register.simple_tag(takes_context=True)
def paginate(context, object_list, **kwargs):
    template_name = 'paginator.html'
    style = ''
    if kwargs:
        style = kwargs.get('style', '')
    t = loader.get_template(template_name)
    return t.render({
        'obj_list': object_list,
        'style': style
    })

