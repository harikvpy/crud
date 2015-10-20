from django.conf.urls import url

from .views import *

urlpatterns = [
        url(r'^questions/$', QuestionCRUDView.as_view(), name='questions')
        ]
