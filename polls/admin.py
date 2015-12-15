from django.contrib import admin

from polls.models import *

# Register your models here.
admin.site.register(Author)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'author',)
