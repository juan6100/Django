from django.contrib import admin
from .models import Post, Comment

#목록 생성
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status','created', 'publish', 'author']
    search_fields = ['title', 'body']#검색
    prepopulated_fields = {'slug': ('title',)}#포스트를 추가할 때 자동적으로 타이틀을 입력하면 slug에 값이 입력되는 기능
    raw_id_fields = ['author']#게시물 작성할 때 작성자를 검색해서 선택하는 기능 조회위젯과 함께 표시된다
    date_hierarchy = 'publish'
    ordering = ['status','publish']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']