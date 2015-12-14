from django.conf.urls import url

from .views import *

urlpatterns = [
        url(r'^authors/$', AuthorCRUDView.as_view(), name='authors'),
        url(r'^questions/$', QuestionCRUDView.as_view(), name='questions')
        ]
