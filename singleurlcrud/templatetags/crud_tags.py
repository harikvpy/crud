from django.template import Library
from django.utils.safestring import mark_safe

register = Library()

@register.simple_tag
def field_value(instance, name):
    """
    Tag to retrieve the value of a field from a model instance
    given its (field's) name.

    Parameters:
        instance - the model's instance
        field_name - name of the field
    """
    value = ""
    try:
        field = instance._meta.get_field_by_name(name)[0]
        value = getattr(instance, name)
    except models.FieldDoesNotExist:
        if hasattr(instance, name):
            value = "to be evaluated"
    return value

@register.filter
def lookup(thelist, index):
    """
    Returns the nth element from a list; element index to return is specified in 'index'.
    """
    return thelist[index]

@register.filter
def verbose_name(model):
    """
    Returns the verbose name of a model.

    This filter is necessary as verbose names are defined in a model's
    meta class, which is accessible through model._meta. However, Django's
    default template system does not allow attribute or variable names to
    begin with an underscore. We get around this limitation by defining
    a filter.
    """
    return model._meta.verbose_name

@register.filter
def verbose_name_plural(model):
    """
    Returns the plural verbose name of a model.

    See comments for verbose_name filter for more details.
    """
    return model._meta.verbose_name_plural

@register.simple_tag
def field_label(view, field):
    """
    Thunk to the view method to retrieve the label for a list_display field.
    """
    return view.get_list_field_label(field)

@register.simple_tag
def eval_field(view, field, obj):
    """
    Thunk to view method to retrieve the value for a list_display field
    for an instance of the model.
    """
    return mark_safe(view.get_list_field_value(field, obj))

@register.inclusion_tag("singleurlcrud/render_item.html", takes_context=True)
def render_item(context, item, rowindex):
    """
    Tag to render an object.
    """
    context['item'] = item
    context['rowindex'] = rowindex
    context['can_delete'] = context['view'].can_delete(item) and \
            getattr(item, 'can_delete', True)
    context['can_edit'] = context['view'].can_edit(item) and \
            getattr(item, 'can_edit', True)
    return context

