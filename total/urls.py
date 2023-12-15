from . import views
from django.urls import path

urlpatterns = [
    path('single_delete/<int:duty_id>', views.delete_true_view),
    path('get_ids/', views.get_ids),
    path('get_fields/', views.get_fields),
    path('get_image/<int:id>', views.get_image),
    path('compare/<str:ids>', views.compare),
    path('analyse/<str:ids>', views.analyse),
    path('get_preview/<str:ids>', views.get_preview)
]
