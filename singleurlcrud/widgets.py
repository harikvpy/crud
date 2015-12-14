"""
Defines replacement widgets that CRUDView uses.
"""
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper

class CustomRelatedFieldWidgetWrapper(RelatedFieldWidgetWrapper):
    """
    Based on the admin RelatedFieldWidgetWrapper, this does the same
    thing but outside of the admin interface

    Rhe parameters for a relation and the admin site are replaced
    by a url for the add operation
    """
    class Media:
        js = ('admin/js/admin/RelatedObjectLookups.js', )

    def __init__(self, widget, add_url, permission=True):
        self.widget = widget
        #self.is_hidden = getattr(widget, "is_hidden", False)
        self.needs_multipart_form = getattr(widget, "needs_multipart_form", False)
        self.attrs = getattr(widget, 'attrs', None)
        self.choices = widget.choices
        self.add_url = add_url
        self.permission = permission

    def render(self, name, value, *args, **kwargs):
        self.widget.choices = self.choices
        output = [self.widget.render(name, value, *args, **kwargs)]
        if self.permission:
            add_url = self.add_url
            prefix = '?'
            if '?' in add_url:
                prefix = '&'
            add_url += prefix
            add_url += "o=add&_popup=1"
            output.insert(0, '&nbsp;<a href="%s" class="add-another" id="add_id_%s" onclick="return showRelatedObjectPopup(this);"> ' % \
                    (add_url, name))
            output.insert(1, '<span class="glyphicon glyphicon-plus" title="%s"/></a>' % (_('Add Another')))
        return mark_safe(u''.join(output))
