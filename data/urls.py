from . import views
from django.urls import path

urlpatterns = [
    path('single_delete/<int:duty_id>', views.delete_true_view),
    # path('get_analyse/', views.res_view),
    # path('ret_analyse', views.analyse),
    path('get_ids/', views.get_ids),
    path('get_fields/', views.get_fields),
    path('get_details/<int:id>', views.get_details)
]