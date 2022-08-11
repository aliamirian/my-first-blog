from django.urls import path
from . import views

urlpatterns = [
   # path('', views.post_list, name='post_list'),
    path('', views.PostsListView.as_view(),
         name='post_list'),   # در حالت استفاده از کلاس
   # path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/', views.PostDetailsView.as_view(),
         name='post_detail'),  # در حالت کلاس به جای خط بالا
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    path('post/<int:pk>/comment/', views.add_comment_to_post,
         name='add_comment_to_post'),
    path('comment/<int:pk>/approve/',
         views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('login/', views.LoginInterfaceView.as_view(), name='login'),
    path('logout/', views.LogoutInterfaceView.as_view(), name='logout'),


]
