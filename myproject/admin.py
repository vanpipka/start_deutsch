from django.contrib import admin
from .models import Category, Article, AdditionalField, Comment, Subscriber, AdditionalFieldAdmin
from .models import CommentAdmin, ArticleAdmin, ArticleLog, ArticleLogAdmin
from quiz.models import Topic, Word
from exam.models import Exam, Question, Section, Result
from exam.models import SectionFieldAdmin, ExamFieldAdmin, QuestionFieldAdmin, ResultFieldAdmin


admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(AdditionalField, AdditionalFieldAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Question, QuestionFieldAdmin)
admin.site.register(Section, SectionFieldAdmin)
admin.site.register(Exam, ExamFieldAdmin)
admin.site.register(Result, ResultFieldAdmin)
admin.site.register(Subscriber)
admin.site.register(Topic)
admin.site.register(Word)
admin.site.register(ArticleLog, ArticleLogAdmin)
