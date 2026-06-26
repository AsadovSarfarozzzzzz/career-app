from rest_framework.routers import DefaultRouter
from .views import (CareerViewSet, StepViewSet, MaterialViewSet, 
    MyProgressView, MarkStepView, RegisterView, CareerProgressView, CareerTestView)
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
]