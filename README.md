# crud
A single view implementation of basic table CRUD operations for Django.

# Introduction
Django comes with an excellent admin framework that provides a sophisticated interface for table CRUD operations. However, the admin framework is closely tied to Django's default user management and its permission management systems. If your project bypasses either of these, employing the CRUD in the admin framework can get a little tricky. Besides using the admin CRUD also implicitly adds a number urls to your url namespace.

This project is aimed at addressing the above shortcomings by developing a pure django view that provides basic table CRUD operations. You derive from this view providing it with the appropriate initialization parameters and then hook it up to the url namespace yourself explicitly.

# Quickstart
TBD

