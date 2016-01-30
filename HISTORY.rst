History
-------

0.20 - 2016/1/30
++++++++++++++++
- Add support for specifying list column titles through a dictionary specified
  as the class variable - list_display_lables

0.19 - 2016/1/24
++++++++++++++++
- Fix mispelt context variable item_actions (was referred to as itemactions)

0.18 - 2016/1/22
++++++++++++++++
- Fix formatting errors in README.rst.

0.17
++++
- Move changelog to HISTORY.rst and include it in setup long_description
  through embedded script.

0.16
++++
- Fix more errors in setup.py that stopped pip install from working

0.15
++++
- Fix errors in setup.py that stopped pip install from working

0.14
++++
- Fix errors in setup.py.
- Update status to '4 - Beta'.
      
0.13
++++
- Use django-pure-pagination for pagination. This provides margin page
  numbers which provides a nice UX for listing tables with very large
  amounts of data, number of pages for which exceed the available 
  width in the screen.

0.12
++++
- Move delete operation into an independent GET action through the 
  '?o=delete' parameter.

0.11
++++
- Action buttons changed to use buttons grouping them into a btn-group.
- Added colors to the buttons indicating the severity of the action's outcome.

0.10
++++
- Changed table css classes to be specified as view setting provided
  through RequestContext.
      
0.9
+++
- Refactor cryptic flag names to more friendly names. Eg.: can_delete() has
  been changed to item_deletable(). 
- Global flags can_create, can_edit and can_delete has been replaced by 
  enable_create, enable_edit & enable_delete respectively.

0.8
+++
- Add support for view to customize page titles by specifying a class
  variable 'pagetitle'. This title will be used by default and if not
  specified the model's verbose_name_plural will be set as the title
  in the context.

0.7
+++
- Fix media property such that it only returns media fragments necessary
  for the current CRUD operation.

0.6
+++
- Fix incorrect arguments to can_delete() method call.

0.5
+++
- When the derived class specifies a custom form by overriding the
  get_form() method, inline editing/addition of RelatedField objects
  is not available. This version includes a fix for this.

0.4
+++
- Support for per item editing control through the item property
  item.can_edit, which should return a boolean indicating if editing
  is allowed. Defaults to True, if the property is missing.

0.3
+++
- Support for per item deletion control through the item property
  item.can_delete, which should return a boolean indicating if deletion
  is allowed. Defaults to True, if the property is missing.

0.2
+++
- Support for inline editing/addition of RelatedField objects through
  a popup window. Note that base template has to be designed
  to accommodate this feature by removing the embellishments that adorn a 
  regular page.

0.1
+++
- Initial release

