from django.db import models
from django.contrib.auth.models import User
from .resources import POST_TYPE_CHOICES
from django.db.models.functions import Coalesce
from django.db.models import Sum


class Author(models.Model):
    author_name = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def generate(self):
        # rating_post = self.post_set.aggregate(post_rating_sum=Sum('post_rating'))
        # pRat = rating_post.get('post_rating_sum')

        # rating_comment = Comment.objects.filter(comment_author=self.author_name).aggregate(
        #     comment_rating_sum=Sum('comment_rating'))
        # cRat = rating_comment.get('comment_rating_sum')

        # rating_comment = self.author_name.comment_set.aggregate(comment_rating_sum=Sum('comment_rating'))
        # cRat = rating_comment.get('comment_rating_sum')
        #
        # self.author_rating = pRat * 3 + cRat
        # self.save()

        post_rating = Post.objects.filter(post_author=self.pk).aggregate(post_rating_sum=Coalesce(
            Sum('post_rating') * 3, 0))
        comment_rating = Comment.objects.filter(comment_author=self.author_name).aggregate(comment_rating_sum=Coalesce(
            Sum('comment_rating'), 0))
        post_comment_rating = Comment.objects.filter(comment_post__post_author__author_name=self.author_name).aggregate(
            comment_rating_sum=Coalesce(
                Sum('comment_rating'), 0))
        self.author_rating = (post_rating['post_rating_sum'] + comment_rating['comment_rating_sum']
                              + post_comment_rating['comment_rating_sum'])

        self.save()

    def __str__(self):
        return self.author_name.username


class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.category_name


class Post(models.Model):
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=1, choices=POST_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=256)
    content = models.TextField()
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return f'{self.content[:123]}...'

    def __str__(self):
        return self.title


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
