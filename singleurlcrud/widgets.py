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

    def __init__(self, widget, related_url, permission=True):
        self.widget = widget
        self.needs_multipart_form = getattr(widget, "needs_multipart_form", False)
        self.attrs = getattr(widget, 'attrs', None)
        # This custom data attribute allows us to easily identify and locate
        # CRFWW select fields from Javascript.
        self.attrs['data-crfww'] = 'true'
        self.choices = widget.choices
        self.related_url = related_url
        self.permission = permission

    def render(self, name, value, *args, **kwargs):
        self.widget.choices = self.choices
        output = [self.widget.render(name, value, *args, **kwargs)]
        if self.permission:
            prefix = '&' if '?' in self.related_url else '?'

            # form the edit url template
            edit_url_templ = self.related_url
            edit_url_templ += prefix
            edit_url_templ += "o=edit&_popup=1&item=__fk__"
            output.insert(0, '&nbsp;<a data-hreftempl=%s class="change-existing" id="change_id_%s"> ' % \
                    (edit_url_templ, name))
            output.insert(1, '<span class="glyphicon glyphicon-edit" title="%s"/></a>' % (_('Edit current')))

            # for add url
            add_url = self.related_url
            add_url += prefix
            add_url += "o=add&_popup=1"
            output.insert(2, '&nbsp;<a href="%s" class="add-another" id="add_id_%s" onclick="return showRelatedObjectPopup(this);"> ' % \
                    (add_url, name))
            output.insert(3, '<span class="glyphicon glyphicon-plus" title="%s"/></a>' % (_('Add new')))
        return mark_safe(u''.join(output))
