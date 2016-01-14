"""
Defines CRUDView, which is a ListView derived view that forms the primary
user interface for table CRUD operations.

CRUD operations start by displaying the user the list of existing items
in the table. Against each item, we provide two buttons -- one for the edit
(update) op and another for the delete op. In other words, for the two per
item operations. At the top of the list, we also provide a button for adding
new items to the table.

With these two widgets in place, we the go on to provide hooks to extend them
whereby the user can specify additional buttons to be added to the per item
op list (besides the 'edit' and 'delete' op buttons). Also, we provide hooks
for the user to specify multiple-item actions which, if specified, will appear
as a drop down menu to the right of the add item button on the top of the list.

This interface completes a barebone reusable CRUD operations interface that
can be easily extended.

Modification history:

I have not been disciplined enough to maintain all the changes and tweaks that
has gone into this code over the period of last 6 months of existing of this
code. But after seeing how much this code has evolved from its initial simple
rudimentary version, and how difficult it has proven to myself to change
something, from henceforth I'm going to make an effort to keep a decent
change history. Hopefully I'll be disciplined enough to maintain this
practice at least for the foreseeable future.

    2015/05/14  Changed the column label for ForeignKey fields in listview
                to the related models verbose_name.

    2015/05/15  Added interface for the client class to specify custom urls
                for item add/edit/delete operations. These are provided as
                overridable methods, which if omitted will default to the
                built in mechanisms.

    2015/12/11  Added support for django admin like related object add through
                a popup window. Capability only works for ForeignKey field.
                ManyToManyField field implementation is pending.
"""

from django.db import models
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import ListView
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.forms import ModelForm, forms
from django.conf import settings
from django.db.models.fields.related import RelatedField
from django.utils import six
from django.utils.html import escape, escapejs
from django.utils.encoding import force_str, force_text, smart_text
try:
    from django.contrib.admin.util import display_for_field, display_for_value
except ImportError:
    from django.contrib.admin.utils import display_for_field, display_for_value
from django.core.exceptions import ObjectDoesNotExist, ValidationError, ImproperlyConfigured

from singleurlcrud.widgets import CustomRelatedFieldWidgetWrapper

class CRUDView(ListView):
    """
    Base view class for a single page CRUD interface.

    Uses the ListView as the base which lists the records of the
    table in tabular form. CRUD operations are driven from that.
    """
    paginate_by = 10
    template_name = "singleurlcrud/list.html"
    js = [ 'singleurlcrud/js/crud-controller.js',
            'admin/js/admin/RelatedObjectLookups.js' ]
    version = 1
    form_class = None
    enable_create = True
    enable_edit = True
    enable_delete = True
    context_object_name = 'object_list'
    pagetitle = None

    # set this to a dictionary where each item is the CRUD url of
    # the related field, indexed by the field's name
    related_field_crud_urls = {}

    class ItemAction(object):
        title = ''
        key = ''
        css = ''

        def doAction(self, item):
            pass

    def media(self):
        extra = '' if settings.DEBUG else '.min'
        css = { 'all': ('singleurlcrud/css/crud.css',) }
        js = self.js
        from django.forms.widgets import Media
        media = Media(js=['%s' % url for url in js], css=css)
        op = self.get_op()
        if op == "add" or op == "edit":
            form = self.get_form(self.get_form_class())
            if hasattr(form, 'media'):
                media += form.media
        return media

    def get_form_class(self):
        '''
        Returns the form class to be used for CRUD Add/Edit operations.
        '''
        if self.form_class:
            return self.form_class
        from django.forms.models import modelform_factory
        return modelform_factory(self.get_model(), fields=self.get_form_fields())

    def get_related_field_crud_urls(self):
        """
        Return the related field CRUD urls for inline related field add/edit
        popups.
        """
        return {}

    def get_form(self, form_class, **kwargs):
        """
        Returns the form instance contructed from the supplied form_class.
        """
        return form_class(**kwargs)

    def get_form_fields(self):
        """
        Return a tuple of field names that are to be displayed for the CRUD form.
        """
        if hasattr(self, 'form_fields'):
            return self.form_fields
        return self.list_display

    def get_add_item_custom_url(self):
        return ''

    def get_edit_item_custom_url(self):
        return ''

    def get_delete_item_custom_url(self):
        return ''

    def get_opless_path(self):
        """
        Returns the URL path without the 'o' and 'item' arguments.
        """
        path = self.request.path
        isFirst = True
        for item in self.request.GET:
            if not item in ('o', 'item'):
                path += '?' if isFirst else '&'
                isFirst = False
                path += "%s=%s" % (item, self.request.GET.get(item))
        return path

    def check_permission(self, op, item, request):
        '''
        Override to control per item edit permissions
        '''
        return True

    def get_list_field_label(self, name):
        """
        Returns the label for a list_display field which can be used
        in column headings.

        'field_label' template tag uses this method to get label for each
        column specified in list_display.
        """
        assert(name in self.list_display)
        return self.label_for_field(name)

    def get_list_field_value(self, name, obj):
        """
        Returns the displayable value for a field specified in
        list_display.
        """
        value = ""
        assert(name in self.list_display)
        try:
            field = obj._meta.get_field(name)
            try:
                if len(field.get_choices()) > 0 and hasattr(obj, 'get_'+name+'_display'):
                    value = getattr(obj, 'get_'+name+'_display')()
                else:
                    value = getattr(obj, name)
            except AttributeError:
                value = getattr(obj, name)
        except models.FieldDoesNotExist:
            from django.utils.safestring import mark_safe
            if hasattr(self.get_model(), name):
                value = getattr(self.get_model(), name)(obj)
            elif hasattr(self, name):
                value = getattr(self, name)(obj)
            else:
                raise models.FieldDoesNotExist("Could not evaluate column '"+name+"'")
            if type(value) != type(True):
                value = mark_safe(value)
        return value

    def label_for_field(self, name):
        """
        Returns a label for a field. Based on label_for_field function in
        django.contrib.admin.util.
        """
        model = self.get_model()
        label = ""
        try:
            field = model._meta.get_field_by_name(name)[0]
            label = field.verbose_name.capitalize()
        except models.FieldDoesNotExist:
            '''
            Not a db field. Treat as one of:
                1. model object's attribute
                2. view subclass's attribute
            '''
            if hasattr(self.get_model(), name):
                method = getattr(self.get_model(), name)
                if hasattr(method, "short_description"):
                    label = getattr(method, "short_description")
                else:
                    label = name.capitalize()
            elif hasattr(self, name):
                method = getattr(self, name)
                label = getattr(method, "short_description")
            else:
                message = "Unable to locate '%s' on %s" % (name, self)
                raise AttributeError(message)
        return label

    def get_actions_as_str(self):
        """
        Returns the actions tuples, with the handler part of the
        tuple converted to a string. This handler string is used
        as the signature for the action and used to uniquely identify
        the handler during invocation.
        """
        actions = self.get_actions()
        new_actions = []
        if len(actions):
            for label, handler in actions:
                new_actions.append((label, handler.__name__,))
        return new_actions

    def get_op(self, request=None):
        # return current operation mode which is one if add|edit|delete
        if not request:
            request = self.request
        return request.GET.get('o', None)

    def get_template_names(self):
        op = self.get_op()
        if op == u'add':
            return ['singleurlcrud/edit.html']
        elif op == u'edit':
            return ['singleurlcrud/edit.html']
        return ['singleurlcrud/list.html']

    def get_context_data(self, **kwargs):
        """
        Context data for the template to render the CRUD view.
        """
        context = {
            'view': self,
            'base_template': settings.SIMPLECRUD_BASE_TEMPLATE,
            'breadcrumbs': self.get_breadcrumbs(),
            'media': self.media(),
            'item_name': self.get_model()._meta.verbose_name.title(),
            'enable_create': self.enable_create,
            'enable_edit': self.enable_edit,
            'enable_delete': self.enable_delete,
            }

        context_handler = {
            'add': self.get_add_context_data,
            'edit': self.get_edit_context_data,
            'delete': self.get_delete_context_data,
        }

        if self.get_op() in context_handler:
            if '_popup' in self.request.GET:
                context['popup'] = self.request.GET['_popup']
            context.update(context_handler[self.get_op()](**kwargs))
            return context

        # list-view context data
        context.update(super(CRUDView, self).get_context_data(**kwargs))
        extra_context = {
            'pagetitle': self.get_pagetitle(),
            'list_display': self.list_display,
            'delete_msg': _("Are you sure you want to delete the %s: {1}") % self.get_model()._meta.verbose_name.title(),
            'create_button_text': _('Create new %s') % self.get_model()._meta.verbose_name.title(),
            'actions': self.get_actions_as_str(),
            'itemactions': self.get_item_actions(),
            'add_item_custom_url': self.get_add_item_custom_url(),
            'edit_item_custom_url': self.get_edit_item_custom_url(),
            'delete_item_custom_url': self.get_delete_item_custom_url(),
        }
        context.update(extra_context)
        return context

    def _get_form_helper(self, form_class, **kwargs):
        '''
        Helper function to return a form class instance where the
        widgets for RelatedField instances are replaced with the
        CustomRelatedFieldWidgetWrapper so that inline edit/add
        operations can be supported like in admin CRUD.

        Note that this method is only necessary to be invoked for
        those cases where the form is returned in the context to be
        rendered by the template. For POST request data validation, the
        original self.get_form() method is used.
        '''
        form = self.get_form(form_class, **kwargs)
        # If related_field_crud_urls was specified, iterate through all the
        # form's fields and if any of the fields is an instance of
        # ForeignKey and the user has requested the related model to be
        # editable inline, replace its widget with our
        # CustomRelatedFieldWidgetWrapper that allows this.
        for field in self.model._meta.fields:
            if isinstance(field, models.ForeignKey) and \
                    field.name in self.related_field_crud_urls:
                # replace the form field's widget with CRFWW
                form_field_ = form.fields[field.name]
                from django.forms import Select
                form_field_.widget = CustomRelatedFieldWidgetWrapper(
                        Select(choices=form_field_.choices),
                        self.related_field_crud_urls[field.name],
                        True)
        # replace the widget for those fields
        for field in self.model._meta.fields:
            if isinstance(field, models.ForeignKey) and \
                    field.name in self.related_field_crud_urls:
                # replace the form field's widget with CRFWW
                form_field_ = form.fields[field.name]
                from django.forms import Select
                form_field_.widget = CustomRelatedFieldWidgetWrapper(
                        Select(choices=form_field_.choices),
                        self.related_field_crud_urls[field.name],
                        True)
        return form

    def get_add_context_data(self, **kwargs):
        '''Return context data for add opereation'''
        context = kwargs
        context['add'] = True
        context['pagetitle'] = _("Create new %s") % (self.get_model()._meta.verbose_name.title())
        if 'form' not in context:
            context['form'] = self._get_form_helper(self.get_form_class())
        return context

    def get_edit_context_data(self, **kwargs):
        '''Return context data for edit opereation'''
        context = kwargs
        _object = self.get_model().objects.get(pk=self.request.GET.get('item'))
        object_title = _object._meta.verbose_name.title()
        item = self.get_model().objects.get(pk=self.request.GET.get('item'))
        context['object'] = _object
        context['edit'] = True
        context['pagetitle'] = _("Edit %s") % object_title
        if 'form' not in context:
            context['form'] = self._get_form_helper(self.get_form_class(), instance=_object)
        return context

    def get_delete_context_data(self, **kwargs):
        '''Return context data for delete operation'''
        context = kwargs
        _object = self.get_model().objects.get(pk=self.request.GET.get('item'))
        object_title = _object._meta.verbose_name.title()
        context['object'] = _object
        context['pagetitle'] = _("Delete %s") % object_title
        context['delete_msg'] = _("Are you sure you want to delete the %s: {1}") % object_title,
        return context

    def get_paginate_by(self, queryset):
        """
        Overridden to support special page value of 'all' that would disable
        pagination.
        """
        page = self.kwargs.get(self.page_kwarg) or self.request.GET.get(self.page_kwarg) or 1
        if page == 'all':
            return None
        return super(CRUDView, self).get_paginate_by(queryset)

    def get(self, request, *args, **kwargs):
        try:
            if request.GET.get('o', '') == u'add':
                if not self.check_permission('add', None, request):
                    raise Http404
            elif request.GET.get('o', '') == u'edit' and request.GET.get('item'):
                item = get_object_or_404(self.get_model(), pk=self.request.GET.get('item'))
                if not self.check_permission('edit', item, request):
                    raise Http404
            elif request.GET.get('o', '') == u'delete' and request.GET.get('item'):
                item = get_object_or_404(self.get_model(), pk=self.request.GET.get('item'))
                if not self.check_permission('delete', item, request):
                    raise Http404
            else:
                # invalid request arguments, raise 404
                pass
            return super(CRUDView, self).get(request, *args, **kwargs)
        except ObjectDoesNotExist:
            raise Http404

    def post(self, request, *args, **kwargs):
        # do one of ADD, EDIT or DELETE operations
        form = None
        op_handler = {
            'add': self.post_add,
            'edit': self.post_edit,
            'delete': self.post_delete,
            'action': self.post_action,
            }
        op = self.get_op(request)
        if op in op_handler.keys():
            return op_handler[op](request, *args, **kwargs)
        return HttpResponseRedirect(self.get_opless_path())

    def post_add(self, request, *args, **kwargs):
        # add a new item
        try:
            form = self.get_form(self.get_form_class(), data=self.request.POST)
            if form.is_valid():
                item = self.save_form(request, form, False, True)
                if "_popup" in request.POST:
                    return HttpResponse('<script type="text/javascript">opener.dismissAddRelatedObjectPopup(window, "%s", "%s");</script>' % \
                            (escape(item.pk), escapejs(item)))
                return HttpResponseRedirect(self.get_opless_path())
        except ValidationError as ve:
            form._errors[forms.NON_FIELD_ERRORS] = form.error_class(ve.messages)

        # re-render the view with the form together with the
        # erroneous data and error messages
        context = self.get_context_data(form=form)
        if form._errors and len(form._errors) > 0:
            context['form_haserrors'] = True
        return self.render_to_response(context)

    def post_edit(self, request, *args, **kwargs):
        # edit
        try:
            item = get_object_or_404(self.get_model(), pk=self.request.GET.get('item'))
            form = self.get_form(self.get_form_class(), instance=item, data=self.request.POST,
                        files=request.FILES)
            if form.is_valid():
                item = self.save_form(request, form, True, True)
                if "_popup" in request.POST:
                    return HttpResponse('<script type="text/javascript">opener.dismissAddRelatedObjectPopup(window, "%s", "%s");</script>' % \
                            (escape(item.pk), escapejs(item)))
                msg = _('%s details updated') % self.get_model()._meta.verbose_name.title()
                messages.info(self.request, msg)
                self.object_list = self.get_queryset()
                return HttpResponseRedirect(self.get_opless_path())
        except ValidationError as ve:
            form._errors[forms.NON_FIELD_ERRORS] = form.error_class(ve.messages)
        except ObjectDoesNotExist as ode:
            pass
        # form has validation errors; re-render the view with the
        # form together with the erroneous data and error messages
        context = self.get_context_data(form=form)
        if form._errors and len(form._errors) > 0:
            context['form_haserrors'] = True
        return self.render_to_response(context)

    def post_delete(self, request, *args, **kwargs):
        # delete
        item = get_object_or_404(self.get_model(), pk=self.request.GET.get('item'))
        # verify global delete view flag and individual item deletable flag
        # (if it was specified) before doing the actual deletion.
        if not getattr(item, 'is_readonly', False) and self.item_deletable(item):
            item.delete()
            msg = _('%s %s deleted') % (self.get_model()._meta.verbose_name.title(), item)
            messages.info(self.request, msg)
        return HttpResponseRedirect(self.get_opless_path())

    def post_action(self, request, *args, **kwargs):
        # custom action
        response = self.invoke_action(request);
        if isinstance(response, HttpResponse):
            return response
        return HttpResponseRedirect(self.get_opless_path())

    def get_list_display_field(self, field, obj):
        return ""

    def invoke_action(self, request):
        """
        Invoke a custom action corresponding to the one requested
        by the client.

        The requested action is specified in the POST argument 'handler'
        which is the name of the handler method to be invoked.
        """
        # if 'id' is specified in the request argument list,
        # this is a single item action.
        item_id = request.GET.get('item', None)
        if item_id:
            # per item action key
            handler = request.POST.get('handler')
            for ia in self.get_item_actions():
                # find matching ItemAction object
                if ia.key == handler:
                    ia.doAction(self.get_model().objects.get(pk=item_id))
                    break
            return

        # action to be performed on multiple items
        selected = request.POST.getlist('ids')
        if selected:
            handler = request.POST.get('handler')
            actions = self.get_actions()
            for label, action in actions:
                if action.__name__ == handler:
                    return action(request, self.get_queryset().filter(pk__in=selected[0].split(',')))

    def save_form(self, request, form, change=True, commit=True):
        """
        Saves the add/change form and returns the created object.

            :: request  - the request
            :: form     - the form being saved
            :: change   - a boolean indicating if this is a save owing
                          to editing an item. Set to False for 'add's

            :: returns the created object (python object)
        """
        return form.save(True)

    # ###############################################################
    # METHODS THAT WILL TYPICALLY BE OVERRIDDEN BY THE DERIVED CLASS
    # ###############################################################

    def get_pagetitle(self):
        if self.pagetitle:
            return self.pagetitle
        title = self.get_model()._meta.verbose_name_plural
        return title.capitalize()

    # OPTIONAL OVERRIDE
    def get_breadcrumbs(self):
        """
        Return a list of breadcrumb items, where each item in the list is
        a tuple of the form (text, url).
        """
        return [
            (self.get_model()._meta.verbose_name_plural.capitalize(), None,)
            ]

    def get_model(self):
        return self.model

    def get_actions(self):
        """
        Return a list of tuples where each tuple consists of
            (label, handler,)
                label -- will be displayed in the action dropdown
                handler - method to be invoked for the action
        """
        return []

    def get_item_actions(self):
        """
        Return a list of ItemAction derived objects that represent
        the additional item specific action to be invoked for each
        item in the itemlist.
        """
        return []

    def item_deletable(self, obj):
        """
        Return a boolean to indicate if the item can be deleted (defaults to True).
        """
        return True

    def item_editable(self, obj):
        """
        Return a boolean to indicate if the item can be edited (defaults to True).
        """
        return True

