from django.db import models
from django.contrib.auth.models import User
from .resources import POST_TYPE_CHOICES
from django.db.models.functions import Coalesce
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def generate(self):
        post_rating = Post.objects.filter(post_author_id=self.pk).aggregate(post_rating_sum=Coalesce(
            Sum('rating_post') * 3, 0))
        comment_rating = Comment.objects.filter(user_id=self.user).aggregate(comment_rating_sum=Coalesce(
            Sum('rating_comments'), 0))
        post_comment_rating = Comment.objects.filter(pos__author__name=self.user).aggregate(comment_rating_sum=Coalesce(
            Sum('rating_comments'), 0))
        self.rating_author = (post_rating['post_rating_sum']+comment_rating['comment_rating_sum']
                              + post_comment_rating['comment_rating_sum'])
        self.save()


def __str__(self):
    return self.user.username


'''Суммарный рейтинг каждой статьи автора умножается на 3
    # post_rating = sum(post.rating for post in self.post_set.all()) * 3
    # # Суммарный рейтинг всех комментариев автора
    # comment_rating = sum(comment.rating for comment in Comment.objects.filter(user=self.user))
    # # Суммарный рейтинг всех комментариев к статьям автора
    # post_comment_rating = sum(comment.rating for comment in Comment.objects.filter(post__author=self))
    # # Обновление рейтинга автора
    # self.rating = post_rating + comment_rating + post_comment_rating
    # self.save()
'''


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category_name


class Post(models.Model):
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=1, choices=POST_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.content[:124]}...'

    def __str__(self):
        return self.title


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
