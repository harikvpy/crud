from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy

from singleurlcrud.views import CRUDView
from .models import *

# Create your views here.
class AuthorCRUDView(CRUDView):
    model = Author
    list_display = ('name',)

class QuestionCRUDView(CRUDView):
    model = Question
    list_display = ('question_text', 'pub_date', 'author')
    related_field_crud_urls = {
            'author': reverse_lazy("polls:authors")
            }

    def get_actions(self):
        self.related_field_crud_urls = {
            'author': reverse_lazy('polls:authors') +"?o=add",
            }
        return [
            ('Delete', self.delete_multiple_items)
            ]

    def delete_multiple_items(self, request, items):
        pass


    class VoteItemAction(object):
        title = 'Vote'
        key = 'vote1'
        css = 'glyphicon glyphicon-envelope'

        def doAction(self, item):
            pass

    def get_item_actions(self):
        return [self.VoteItemAction()]

