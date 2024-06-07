from django.db import models

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(
        'users.User',
        verbose_name='작성자',
        on_delete=models.CASCADE,
    )
    title = models.TextField('제목')
    content = models.TextField('내용')
    created = models.DateTimeField('생성일시',auto_now_add=True)
    
    def get_comments_count(self):
        return self.comment_set.count()
    
class Comment(models.Model):
    user = models.ForeignKey(
        'users.User',
        verbose_name='작성자',
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(Post, verbose_name='포스트',on_delete=models.CASCADE)
    content = models.TextField('내용')
    created = models.DateTimeField('생성일시',auto_now_add=True)
    
    def __str__(self) :
        return f'Comment by {self.user.username} on {self.post.title}'
