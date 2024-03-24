# Импортируем необходимые модели
from django.contrib.auth.models import User
from .models import Author, Category, Post, Comment

# Создаем двух пользователей
user1 = User.objects.create_user('username1', password='password1')
user2 = User.objects.create_user('username2', password='password2')

# Создаем два объекта модели Author, связанные с пользователями
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

# Добавляем 4 категории в модель Category
cat1 = Category.objects.create(category_name='Политика')
cat2 = Category.objects.create(category_name='Экономика')
cat3 = Category.objects.create(category_name='Образование')
cat4 = Category.objects.create(category_name='Спорт')

# Добавляем 2 статьи и 1 новость
post1 = Post.objects.create(post_author=author1, post_type='A', title='Статья1', content='Текст статьи1')
post2 = Post.objects.create(post_author=author1, post_type='A', title='Статья2', content='Текст статьи2')
post3 = Post.objects.create(post_author=author2, post_type='N', title='Новость1', content='Текст новости1')

article1 = Post.objects.create(post_author=author1, post_type='A', title='Article 1', content='Content of Article 1')
article2 = Post.objects.create(post_author=author2, post_type='A', title='Article 2', content='Content of Article 2')
news1 = Post.objects.create(post_author=author1, post_type='N', title='News 1', content='Content of News 1')

# Присваиваем им категории
post1.categories.add(cat1, cat2)
post2.categories.add(cat3)
post3.categories.add(cat4)

# Создаем 4 комментария к разным объектам модели Post
comment1 = Comment.objects.create(post=post1, user=user1, text='Комментарий1')
comment2 = Comment.objects.create(post=post1, user=user2, text='Комментарий2')
comment3 = Comment.objects.create(post=post2, user=user1, text='Комментарий3')
comment4 = Comment.objects.create(post=post3, user=user2, text='Комментарий4')

# Применяем функции like() и dislike() к статьям/новостям и комментариям
post1.like()
post2.dislike()
comment1.like()
post1.like()
post1.dislike()
comment1.like()
comment2.dislike()
comment3.like()
comment3.like()
comment4.dislike()

# Обновляем рейтинги пользователей
author1.generate()
author2.generate()

# Выводим username и рейтинг лучшего пользователя
best_author = Author.objects.order_by('-rating').first()
print(best_author.user.username, best_author.rating)

# Выводим дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи
best_post = Post.objects.order_by('-rating').first()
print(best_post.created_at, best_post.author.user.username, best_post.rating, best_post.title, best_post.preview())

# Выводим все комментарии (дата, пользователь, рейтинг, текст) к этой статье
comments = Comment.objects.filter(post=best_post)
for comment in comments:
    print(comment.created_at, comment.user.username, comment.rating, comment.text)
