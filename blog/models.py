import re
from django.db import models
from django.forms import ValidationError
from django.conf import settings
from django.core.urlresolvers import reverse

from imagekit.models import ImageSpecField
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail

# Create your models here.

class Post(models.Model):
    STATUS_CHOICE = (
        ('d', 'Draft'),
        ('p', 'Published'),
        ('w', 'Withdrawn'),
    )


    def lnglat_validator(value):
        if not re.match(r'^([+-]?\d+\.?\d*),([+-]?\d+\.?\d*)$', value):
            raise ValidationError('Invalid LngLat Type')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blog_post')
    #author = models.CharField(max_length=20)
    title = models.CharField(max_length=100, verbose_name='제목',
                             help_text='포스팅 제목을 입력하세요 최대 100자')
    content = models.TextField(verbose_name='내용')


    '''원본을 유지 한 상태로.'''
    photo = models.ImageField(blank=True, upload_to='blog/post/%Y/%m/%d')
    photo_thumbnail = ImageSpecField(source='photo',
                                     processors=[Thumbnail(300, 300)],
                                     format='JPEG',
                                     options={'quality': 60})
    '''
    원본 없이 섬네일만 저장 할 때
    photo = ProcessedImageField(blank=True, upload_to='blog/post/%Y/%m/%d',
                                processors=[Thumbnail(300, 300)],
                                format='JPEG',
                                options={'quality': 60})
    '''

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tag = models.CharField(max_length=100, blank=True)
    lnglat = models.CharField(max_length=50, blank=True,
                              validators=[lnglat_validator],
                              help_text='경도/위도 포맷으로 입력')
    status = models.CharField(max_length=1, choices=STATUS_CHOICE)
    tag_set =models.ManyToManyField('Tag', blank=True)
    #Tag 모델이 뒤에 정의되어 있기 때문에 문자열로 넣었음.)


    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])

class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True )

    def __str__(self):
        return self.name










