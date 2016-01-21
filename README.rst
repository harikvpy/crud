============================================
Django CRUD operations through a single view
============================================

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
these can be forcefully removed but overriding the ModelAdmin class and using
it to create your own admin based CRUD classes, managing and getting around
its various dependencies can quickly get tedious to manage. And when Django gets
upgraded, you have the job of reviewing the new admin interface to make sure
that it did not introduce any new 'holes' into your url namespace.

This project is aimed at addressing the above shortcomings by developing a pure 
django view that provides basic table CRUD operations. You derive from this 
view providing it with the appropriate initialization parameters and then hook 
it up to the url namespace yourself explicitly.

Dependencies
------------

  * django-bootstrap3
  * django-pure-pagination

Installation
------------

1. Easiest way to install crud is to get it from PyPi using pip. Do this by: 

    ``pip install singleurlcrud``

2. Add it to INSTALLED_APPS in projects ``settings.py``:

    .. code:: Django

    INSTALLED_APPS = (
        ...
        'singleurlcrud',
        ...
        )

Quickstart
----------

Consider the following model (taken from 'polls' app, which is bundled with the 
crud source code), 

    .. code:: Django

    from django.db import models

    class Question(models.Model):
        question_text = models.CharField(max_length=200)
        pub_date = models.DateTimeField('Date published')
        author = models.ForeignKey(Author, null=True, default=None)

To get a fully functional CRUD for this table, declare a view like below:

    .. code:: Django

    from singleurlcrud.views import CRUDView
    from .models import Question

    QuestionCRUDView(CRUDView):
        model = Question
        list_display = ('question_text', 'pub_date', 'author')

Thereafter, hook this view to the desired url through urls.py:

    .. code:: Django

    from django.conf.urls import url
    from .views import *

    urlpatterns = [
            url(r'^questions/$', QuestionCRUDView.as_view(), name='questions')
            ]

That's it! You get a fully functional CRUD that will allow you to create,
update and delete records from Question table, all rooted at the url
'yoursite.com/questions/'.

License
-------

Distributed under Modified BSD License (3-clause license). See `LICENSE
<LICENSE>`_ file for details.

Author
------

Developed by `Hari Mahadevan <http://www.hari.xyz>`_.

History
-------

0.1 - Initial release

0.2 - Support for inline editing/addition of RelatedField objects through
      a popup window. Note that base template has to be designed
      to accommodate this feature by removing the embellishments that adorn a 
      regular page.

0.3 - Support for per item deletion control through the item property
      item.can_delete, which should return a boolean indicating if deletion
      is allowed. Defaults to True, if the property is missing.

0.4 - Support for per item editing control through the item property
      item.can_edit, which should return a boolean indicating if editing
      is allowed. Defaults to True, if the property is missing.

0.5 - When the derived class specifies a custom form by overriding the
      get_form() method, inline editing/addition of RelatedField objects
      is not available. This version includes a fix for this.

0.6 - Fix incorrect arguments to can_delete() method call.

0.7 - Fix media property such that it only returns media fragments necessary
      for the current CRUD operation.

0.8 - Add support for view to customize page titles by specifying a class
      variable 'pagetitle'. This title will be used by default and if not
      specified the model's verbose_name_plural will be set as the title
      in the context.

0.9 - Refactor cryptic flag names to more friendly names. Eg.: can_delete() has
      been changed to item_deletable(). Also, global flags can_create, can_edit
      and can_delete has been replaced by enable_create, enable_edit & 
      enable_delete respectively.

0.10  Changed table css classes to be specified as view setting provided
      through RequestContext.
      
0.11  Action buttons changed to use buttons grouping them into a btn-group.
      Added colors to them indicating the severity of the action's outcome.

0.12  Move delete operation into an independent GET action through the 
      '?o=delete' parameter.

0.13  Use django-pure-pagination for pagination. This provides margin page
      numbers which provides a nice UX for listing tables with very large
      amounts of data, number of pages for which exceed the available 
      width in the screen.

0.14  Fix errors in setup.py.
      Update status to '4 - Beta'.

      
