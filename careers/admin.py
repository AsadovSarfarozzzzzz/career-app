from django.contrib import admin
from .models import Career, Step, Material, Progress, Category, Question, Answer

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'question', 'career']

admin.site.register(Career)
admin.site.register(Step)
admin.site.register(Material)
admin.site.register(Progress)
admin.site.register(Category)
admin.site.register(Question)