from django.urls import path
from .views import PostView, PostListView, PostFileView, PostCommentView, LikeView

urlpatterns = [
    path('posts/', PostView.as_view(), name='post_list'), #POST create
    path('posts/<int:post_pk>/', PostView.as_view(), name='post_detail'), #GET post detail
    path('posts-list/', PostListView.as_view(), name='post_list'), #GET post list
    
    path('posts/<int:post_pk>/files/', PostFileView.as_view(), name='post_file_list'), #GET post file list
    path('posts/<int:post_pk>/files/<int:file_pk>/', PostFileView.as_view(), name='post_file_detail'), #GET post file detail
    
    path('posts/<int:post_pk>/comments/', PostCommentView.as_view(), name='post_comment_list'), #GET, POST post comment list
    
    
    path('posts/<int:post_pk>/likes/', LikeView.as_view(), name='post_like_list'), #GET post like list
]