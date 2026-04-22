from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Dashboards
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    
    # User Management (Admin)
    path('manage_users/', views.manage_users, name='manage_users'),
    path('create_user/', views.create_user, name='create_user'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('approve_user/<int:user_id>/', views.approve_user, name='approve_user'),
    
    # History
    path('history/users/', views.users_history, name='users_history'),
    path('history/admin/', views.admin_history, name='admin_history'),
    path('history/my/', views.my_history, name='my_history'),
    path('history/delete/<int:history_id>/', views.delete_history, name='delete_history'),
    
    # User Features
    path('user_details/', views.user_details, name='user_details'),
    
    # Prediction
    path('predict/', views.make_prediction, name='make_prediction'),
    
    # API endpoints for Mobile App
    path('api/login/', views.api_login, name='api_login'),
    path('api/predict/', views.api_predict, name='api_predict'),
    path('api/register/', views.api_register, name='api_register'),
    path('api/history/', views.api_history, name='api_history'),
    
    # Default redirect
    path('', views.login_view, name='home'),
]
