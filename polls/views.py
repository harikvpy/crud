from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.forms.models import inlineformset_factory

from singleurlcrud.views import CRUDView
from .models import *

# Create your views here.
class AuthorCRUDView(CRUDView):
    model = Author
    list_display = ('name', 'email')

    def get_formset_class(self):
        return inlineformset_factory(
                Author,
                Question,
                fields=['question_text', 'pub_date'],
                can_delete=True,
                extra=1)

class QuestionCRUDView(CRUDView):
    model = Question
    list_display = ('question_text', 'pub_date', 'author')
    related_field_crud_urls = {
            'author': reverse_lazy("polls:authors")
            }
    allow_multiple_item_delete = True

    '''
    def get_actions(self):
        self.related_field_crud_urls = {
            'author': reverse_lazy('polls:authors') +"?o=add",
            }
        return [
            ('Delete', self.delete_multiple_items)
            ]
    '''

    def delete_multiple_items(self, request, items):
        Question.objects.filter(pk__in=items).delete()

    class VoteItemAction(object):
        title = 'Vote'
        key = 'vote1'
        css = 'glyphicon glyphicon-envelope'

        def doAction(self, item):
            import logging
            logging.getLogger('general').info("VoteItemAction invoked!")
            return HttpResponseRedirect(reverse('polls:authors'))

    def get_item_actions(self):
        return [self.VoteItemAction()]

