#모델은 데이터베이스의 역할을 한다
#템플릿은 화면 역할
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

#커스텀 관리자를 추가(관리자를 2개 이상 둔다)
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
                      .filter(status=Post.Status.PUBLISHED)

class DraftManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
                      .filter(status=Post.Status.DRAFT)

#함수로만 디비를 만든다
#게시물 모델 만들기 디비에 타이틀, 슬러그, 아이디, 바디에대한 내용이 들어가게 된다

#Post 클래스는 리소스를 생성하고 데이터를 추가할 때 사용되는 클래스, 디비를 관리하는 모델들(title, slug,author등등)을 생성하겠다는 의미
class Post(models.Model):
    # Status클래스는 상태필드, 등록이 완료 됐는지 배포 유부를 확인하는 클래스

    class Status(models.TextChoices):
        DRAFT='DF','Draft'
        PUBLISHED='PB','Published'

    title = models.CharField(max_length=250)# 제목 필드
    slug = models.SlugField(max_length=250, unique_for_date='publish') #부제
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='blog_posts')  # 외래키 설정 어떤 사용자가 어떤 게시물을 작성했는지 관계를 생성한다my

    body = models.TextField()#본문 필드
    publish = models.DateTimeField(default=timezone.now)#게시물이 작성된 날짜
    created = models.DateTimeField(auto_now_add=True)#언제 작성했는지
    updated = models.DateTimeField(auto_now=True)#언제 수정했는지
    status = models.CharField(max_length= 2, choices= Status.choices, default=Status.DRAFT)

    objects=models.Manager()#기본 오브젝트에 적용되는
    published = PublishedManager()#서브 메니저
    drafted = DraftManager()

    class Meta:
        ordering = ['-publish']  # 기본정렬하기 위해 필요한 클래스
        indexes = [models.Index(fields=['-publish']),  # 퍼블리쉬 필드를 기본 값으로 결과를 정렬한다
                   ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day,self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


    class Meta:
        ordering = ['created']#기본정렬하기 위해 필요한 클래스
        indexes=[models.Index(fields=['created']),#퍼블리쉬 필드를 기본 값으로 결과를 정렬한다
                 ]

    def __str__(self):#self는 post class 호출
        return f'Comment by {self.name} on {self.post}'#title 반환
    #url 설정



#다 적용하고 나서 python manage.py makemigrations blog을 실행하여 위에 만들어 놓은 테이블을 실행 시킨다.
# Create your models here.
