from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy

from singleurlcrud.views import CRUDView
from .models import *

# Create your views here.
class QuestionCRUDView(CRUDView):
    model = Question
    list_display = ('question_text', 'pub_date')

    def get_actions(self):
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
            import pdb; pdb.set_trace()
            pass

    def get_item_actions(self):
        return [self.VoteItemAction()]

