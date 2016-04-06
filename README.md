=================================
Django CRUD through a single view
=================================

A single view implementation of table CRUD operations for Django.

Introduction
------------

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
django view that provides basic table CRUD operations. You derive from this 
view providing it with the appropriate initialization parameters and then hook 
it up to the url namespace yourself explicitly.

Installation
------------

1. Easiest way to install crud is to get it from PyPi using pip. Do this by:: 

    pip install singleurlcrud

2. Add it to INSTALLED_APPS in projects ``settings.py``::

    INSTALLED_APPS = (
        ...
        'singleurlcrud',
        ...
        )

Dependencies
------------

  * django-bootstrap3
  * django-pure-pagination

Quickstart
----------

Consider the following model (taken from 'polls' app, which is bundled with the 
crud source code)::

    from django.db import models

    class Question(models.Model):
        question_text = models.CharField(max_length=200)
        pub_date = models.DateTimeField('Date published')
        author = models.ForeignKey(Author, null=True, default=None)

To get a fully functional CRUD for this table, declare a view like below::

    from singleurlcrud.views import CRUDView
    from .models import Question

    QuestionCRUDView(CRUDView):
        model = Question
        list_display = ('question_text', 'pub_date', 'author')

Thereafter, hook this view to the desired url through urls.py::

    from django.conf.urls import url
    from .views import *

    urlpatterns = [
            url(r'^questions/$', QuestionCRUDView.as_view(), name='questions')
            ]

That's it! You get a fully functional CRUD that will allow you to create,
update and delete records from Question table, all rooted at the url
``yoursite.com/questions/``.

# Overview

TBD

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

TBD

License
-------

Modified BSD

Author
------

`Hari Mahadevan <http://hari.xyz/>`_
