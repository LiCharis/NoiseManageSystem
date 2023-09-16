from . import views
from django.urls import path

urlpatterns = [
    path('single_delete/<int:duty_id>', views.delete_true_view)
]