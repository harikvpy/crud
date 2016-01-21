=================================
Django CRUD through a single view
=================================

A single view implementation of table CRUD operations for `Django <http://www.djangoproject.com>`_.

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
these can be forcefully removed by overriding the ``ModelAdmin`` class and using
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

1. Easiest way to install crud is to get it from PyPi using pip. Do this by:: 

    pip install singleurlcrud

2. Add it to INSTALLED_APPS in projects ``settings.py``::

    INSTALLED_APPS = (
        ...
        'singleurlcrud',
        ...
        )

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
'yoursite.com/questions/'.

License
-------

Distributed under Modified BSD License (3-clause license). See `LICENSE
<LICENSE>`_ file for details.

Author
-----

Developed by `Hari Mahadevan <http://www.hari.xyz>`_.

