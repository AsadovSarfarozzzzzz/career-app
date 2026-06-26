from django.contrib import admin
from .models import Career, Material, Progress, Step, Category

# Register your models here.
admin.site.register(Career)
admin.site.register(Step)
admin.site.register(Material)
admin.site.register(Progress)
admin.site.register(Category)