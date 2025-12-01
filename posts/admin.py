from django.contrib import admin
from posts.models import Post, PostFile, PostComment, Like

# Register your models here.


class PostFileInline(admin.TabularInline):
    model = PostFile
    extra = 0
    fields = ['file']
    max_num = 10
    min_num = 1
    verbose_name = 'Post File'
    verbose_name_plural = 'Post Files'
    
class PostCommentInline(admin.TabularInline):
    model = PostComment
    extra = 0
    fields = ['user', 'text', 'is_approved']
    readonly_fields = ['user']
    max_num = 10
    min_num = 1
    verbose_name = 'Post Comment'
    verbose_name_plural = 'Post Comments'
    
class LikeInline(admin.TabularInline):
    model = Like
    extra = 0
    fields = ['is_liked']
    max_num = 10
    min_num = 1
    verbose_name = 'Like'
    verbose_name_plural = 'Likes'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'is_active', 'is_public', 'created_at', 'updated_at']
    list_filter = ['is_active', 'is_public']
    search_fields = ['title', 'caption']
    list_editable = ['is_active', 'is_public']
    list_per_page = 10
    list_max_show_all = 100
    list_display_links = ['title']
    inlines = [PostFileInline, PostCommentInline, LikeInline]
    
    def save_formset(self, request, form, formset, change):
        """Automatically set user for new comments when saving through inline"""
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, PostComment) and not instance.user_id:
                instance.user = request.user
            instance.save()
        formset.save_m2m()


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'user', 'text', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['text', 'user__username', 'post__title']
    list_editable = ['is_approved']
    readonly_fields = ['created_at', 'updated_at']
    
    def save_model(self, request, obj, form, change):
        """Automatically set user to current admin user if not set"""
        if not change:  # Only for new comments
            obj.user = request.user
        super().save_model(request, obj, form, change)
    
