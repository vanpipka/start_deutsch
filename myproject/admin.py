from django.contrib import admin
from .models import Category, Article, AdditionalField, Comment, Subscriber, AdditionalFieldAdmin
from .models import CommentAdmin
from quiz.models import Question, Answer, Topic, Word, Result, ResultAdmin

admin.site.register(Category)
admin.site.register(Article)
admin.site.register(AdditionalField, AdditionalFieldAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Subscriber)
admin.site.register(Topic)
admin.site.register(Word)
admin.site.register(Result, ResultAdmin)
