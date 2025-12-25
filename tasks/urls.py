from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs (NEW)
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
    path('user/', views.user_detail_view, name='user_detail'),
    path('user/edit/', views.user_edit_view, name='user_edit'),
    path('user/change-password/', views.change_password_view, name='change_password'),
    path('user/delete/', views.delete_account_view, name='delete_account'),
    
    # Existing Task URLs
    path('', views.TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('task/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('task/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_edit'),
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
]