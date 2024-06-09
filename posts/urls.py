# posts/urls.py

from django.urls import path
from posts import views as auth_views
from . import views
from .views import DeletePostView, DeleteUserView


urlpatterns = [
    path('', auth_views.index, name='index'),
    path('register/', auth_views.register, name='register'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('users/', views.user_list, name='user_list'),
    path('delete_user/<int:user_id>/', DeleteUserView.as_view(),
         name='delete_user_view'),
    path('protected/', auth_views.protected_view, name='protected'),
    path('all_posts/', views.all_posts, name='all_posts'),
    path('add/', views.add_post, name='add_post'),
    path('post/<int:post_id>/', views.view_post, name='view_post'),
    path('edit/<int:post_id>', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', DeletePostView.as_view(),
         name='delete_post'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('calculator_view/', views.calculator_view, name='calculator_view'),
    path('two_sum_view/', views.two_sum_view, name='two_sum_view')
]
