from rest_framework.routers import DefaultRouter
from .views import (
    CareerViewSet, StepViewSet, MaterialViewSet,
    MyProgressView, MarkStepView, RegisterView,
    CareerProgressView, CareerTestView,
    ChooseCareerView, MyActiveCareerView,
    CategoryWithSubsView, SubcategoryCareersView, StepTopicsView, MarkTopicView, StepTopicsProgressView,
    UserStatsView
)
from django.urls import path

router = DefaultRouter()
router.register('careers', CareerViewSet)
router.register('steps', StepViewSet)
router.register('materials', MaterialViewSet)

urlpatterns = router.urls +[
    path('register/', RegisterView.as_view(), name='register'),
    path('my-progress/', MyProgressView.as_view(), name='my-progress'),
    path('mark-step/<int:step_id>/', MarkStepView.as_view(), name='mark-step'),
    path('career-progress/<int:career_id>/', CareerProgressView.as_view(), name='career-progress'),
    path('career-test/', CareerTestView.as_view(), name='career-test'),
    path('choose-career/<int:career_id>/', ChooseCareerView.as_view(), name='choose-career'),
    path('my-career/', MyActiveCareerView.as_view(), name='my-career'),
    path('categories-subs/', CategoryWithSubsView.as_view(), name='categories-subs'),
    path('subcategory/<int:subcategory_id>/careers/', SubcategoryCareersView.as_view(), name='subcategory-careers'),
    path('step/<int:step_id>/topics/', StepTopicsView.as_view(), name='step-topics'),
    path('mark-topic/<int:topic_id>/', MarkTopicView.as_view(), name='mark-topic'),
    path('step/<int:step_id>/topics-progress/', StepTopicsProgressView.as_view(), name='topics-progress'),
    path('my-stats/', UserStatsView.as_view(), name='my-stats'),
]