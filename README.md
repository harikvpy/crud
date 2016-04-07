Django CRUD through a single view
=================================

A single view implementation of table CRUD operations for Django. Single view 
means single URL to be registered in URL namespace. All CRUD operations are
invoked with the same URL but with URL arguments to distinguish them. This allows
less crowded and a simpler URL namespace.

# Introduction

Django comes with an excellent admin framework that provides a sophisticated 
interface for table CRUD operations. However, the admin framework is closely 
tied to Django's default user management and its permission management systems.
If your project bypasses either of these, employing the CRUD in the admin 
framework can get a little tricky. 

Secondly, django admin also implicitly adds a number urls to your url 
namespace. These urls list the apps whose models are are registered with it
and for each app, the models in the app that have an admin CRUD interface. While
these can be forcefully removed by overriding the ModelAdmin class and using
it to create your own admin based CRUD classes, managing and getting around
its various dependencies can quickly get tedious to manage. And when Django gets
upgraded, you have the job of reviewing the new admin interface to make sure
that it did not introduce any new 'holes' into your url namespace.

This project is aimed at addressing the above shortcomings by developing a pure 
django view that provides basic table CRUD operations. To use, derive from this 
view class providing it with the appropriate initialization parameters and then 
hook it up to the url namespace yourself explicitly.

# Installation

1. Easiest way to install crud is to get it from PyPi using pip. Do this by:: 

    `pip install singleurlcrud`

2. Add it to INSTALLED_APPS in projects ``settings.py``::
```
INSTALLED_APPS = (
    ...
    'singleurlcrud',
    ...
    )
```
# Dependencies

  * django-bootstrap3
  * django-pure-pagination

# Quickstart

Consider the following model (taken from `polls` app, which is bundled with the 
source code):
```
from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Date published')
    author = models.ForeignKey(Author, null=True, default=None)
```

To get a fully functional CRUD for this table, declare a view like below:
```
from singleurlcrud.views import CRUDView
from .models import Question

QuestionCRUDView(CRUDView):
    model = Question
    list_display = ('question_text', 'pub_date', 'author')
```

Thereafter, hook this view to the desired url through urls.py:
```
from django.conf.urls import url
from .views import *

urlpatterns = [
        url(r'^questions/$', QuestionCRUDView.as_view(), name='questions')
        ]
```

That's it! You get a fully functional CRUD that will allow you to create,
update and delete records from Question table, all rooted at 
`yoursite.com/questions/`.

# Usage examples

## Editing child models using formset

# Reference

## Options
CRUDView provides many options which allows customizing its behavior. These are
documented below:

### `template_name`
Specifies the template that is used to render the list of items. This defaults to
`singleurlcrud/list.html` and is rarely necessary to be customized.

### `form_class`
The form class to be use for create and update operations. This is optional and
if not spefified, CRUD will create a form using `modelform_factory` using the
fields specified in `form_fields` option. If `form_fields` is not spefified,
CRUDView will try to use the fields in `list_display`.

### `allow_create`
A boolean value, this controls whether the create operation is allowed. 
By default it is allowed, that is, this is set to True. 

### `allow_edit`
A boolean value, this controls whether the update operation is allowed. 
By default it is allowed, that is, this is set to True. 

### `allow_delete`
A boolean value, this controls whether the delete operation is allowed. 
By default it is allowed, that is, this is set to True. 

### `context_object_name`
The context variable name that will be set to the object list for the list view.
Defaults to `object_list`. You only need to customize this if you have a custom
template that want to use a different template variable name (for some reason).

### `pagetitle`
Title of the list view page.

### `table_css_classes`
CSS classes applied to the table in list view. Defaults to 
`table table-striped table-condensed table-bordered`.

### `list_display_labels`
A dictionary that contains the labels to be used for each column in the list 
view. If not specified, column names will default to the field name specified
in `list_display`. For callable column entries, attribute value
`<callable>.short_description` is used as the column title.

### `allow_multiple_item_delete`
A boolean value, this controls whether multiple item deletion is allowed. 
Multiple item deletion is implemented using a checkbox against each item row
and then selecting a dropdopwn menu item at the top. Set to `False` by default.

### `related_field_crud_urls`
A dictionary that has the CRUD url for each foreign key field of the model for
which create and update operation through a popup window is to be enabled.

Note that the view urls for the foreign key field models should also be 
implemented using CRUDView for this to work.

## Overridable methods
Like options, CRUDView also provides many methods that can be overridden by the
client class to customize the CRUD behavior. Many of these methods are simple
wrappers around class variables, provided to allow dynamic values to be 
returned for the relevant options.

### `get_form_class()`
Returns the form class that will be instantiated for create and update 
operations. By default returns the value of `form_class` option, if it's 
defined. If `form_class` is not defined, a `ModelForm` class for the model with
fields set to either of the value of `form_fields` or `list_display` will be
returned.

### `get_form(form_class, **kwargs)`
Returns the form object to be used for create and update operations. 
`form_class` will be set to the return value of `get_form_class`. `**kwargs` 
will contain additional arguments, such as form initial data for the update
operation of CRUD, that are to be passed to the form constructor.

### `get_form_fields()`
Return a tuple, that lists the fields of form used in create and update 
operations. Note that this method will only be called if a `form_class` is not
specified and `get_form()` is not overridden.

### `get_formset_class()`
CRUDView supports editing of child models using a formset. To activate this 
feature, override this method and return the formset class to be used for inline
editing of the child model instances. 

Typically one can use one of the django factory methods `inlineformset_factory`
or `modelformset_factory()` to create this class.

By default this method returns `None` which disables child model editing.

### `get_formset(formset_class, **kwargs)`
Return the formset class instance to be used for editing child model instances.

### `get_related_field_crud_urls()`
Wrapper around the class option `related_field_crud_urls`. By default returns
the value assigned to option variable `related_field_curd_urls`.

### `get_add_item_custom_url()`
Return a custom url, presumably with its own view that you write, that you want 
to use for the create operation. By default returns `None`.

### `get_edit_item_custom_url()`
Return a custom url, presumably with its own view that you write, that you want 
to use for the update operation. By default returns `None`.

### `get_delete_item_custom_url()`
Return a custom url, presumably with its own view that you write, that you want 
to use for the delete operation. By default returns `None`.

### `get_item_template(self)`
Returns the template used to render each item in list view. Template returned 
by this method is used to render each row of the model in list view. You can 
override this to customize per item rendering.

For example, by default each row of the table is given on table row. But for 
your model, you might want to render additional rows listing the child model
instances associated with the model row. You can acheive this by overriding this
method to return a custom template.

### `get_pagetitle()`
Wrapper for `pagetitle` class options variable.

### `get_allow_create()`
Wrapper for `allow_create` class option. Method allows for determining this
value during runtime rather than static definition in the code.

### `get_allow_edit()`
Wrapper for `allow_edit` class option.  Method allows for determining this
value during runtime rather than static definition in the code.

### `get_allow_delete()`
Wrapper for `allow_delete` class option. Method allows for determining this
value during runtime rather than static definition in the code.

### `get_allow_multiple_item_delete()`
Wrapper for `allow_multiple_item_delete` class option. Method allows for determining this
value during runtime rather than static definition in the code.

### `get_disallowed_create_message()`
Often times you might want to control the number of rows that a user can
create on a table. Or you might want to limit row creation based on user roles.
When such logic is determined dyanamically and the creation operation is 
disallowed, you can display an alert message when the table CRUD is activated.

This method allows you to specify the custom message that will be displayed on
top of the list view (where the Create New.. button would've been) 
informing the user that row creation is disallowed.

### `get_breadcrumbs()`
If your site supports breadcrumbs, override this method to return a list of
breadcrumbs that depicts the navigation path to the CRUD url. Each item of
this list is a 2-tuple of the form `(text, url)` where `text` is to be added to
the breadcrumbs hyperlinking it to `url`.

Breadcrumbs returned from this method are passed to the context through the 
context variable `breadcrumbs`. Ideally, your project's base template should 
handle this list by rendering each item in the list as an appropriately
styled `<li>` or something similar.

### `get_actions()`
Return a list of tuples where each tuple consists of `(label, handler,)` where
`label` will be displayed in the action dropdown and `handler` is a method
in the derived class that is to be invoked when the user selects the action.

### `get_item_actions()`
Return a list of ItemAction derived objects that represent the additional item 
specific action to be invoked for each item in the itemlist. When the action is
selected, the corresponding ItemAction object's `doAction()` method will be 
invoked. ItemAction has the following prototype:

```
class ItemAction(object):
    title = ''
    key = ''
    css = ''

    def doAction(self, item):
        pass
```

### `item_deletable(object)`
Return a boolean to indicate if the object can be deleted. By default, True is 
returned by the base class.  If False is returned for any object, the delete 
option for that item will be disabled.

This method, alongwith `item_editable` below, allows controlling per item delete
and edit operations based on the row or some other dynamic property.

### `item_editable(object)`
Same as `item_deletable` above, but works for updating an item.

License
-------

Modified BSD

Author
------

`Hari Mahadevan <http://hari.xyz/>`_
