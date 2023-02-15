from django.contrib import admin
from .models import Category, Article, AdditionalField, Comment, Subscriber, AdditionalFieldAdmin
from .models import CommentAdmin
from quiz.models import Topic, Word, Result, ResultAdmin
from exam.models import Exam, Question, Section
from exam.models import SectionFieldAdmin, ExamFieldAdmin, QuestionFieldAdmin

admin.site.register(Category)
admin.site.register(Article)
admin.site.register(AdditionalField, AdditionalFieldAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Question, QuestionFieldAdmin)
admin.site.register(Section, SectionFieldAdmin)
admin.site.register(Exam, ExamFieldAdmin)
admin.site.register(Subscriber)
admin.site.register(Topic)
admin.site.register(Word)
admin.site.register(Result, ResultAdmin)
