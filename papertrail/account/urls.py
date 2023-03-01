from django.urls import path

from .views import ActivateUserTemplateView

urlpatterns = [
    path('activate/<str:uid>/<str:token>/', ActivateUserTemplateView.as_view(), name='activate-user'),
]
