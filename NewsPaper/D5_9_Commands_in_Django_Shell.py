# python manage.py shell

from django.contrib.auth.models import User
from news.models import Author, Category, Post, PostCategory, Comment
import random

# Создание двух пользователей, с заполнением всех обязательных полей
dima_user = User.objects.create_user(username='dima', email='dima_user@mail.ru', password='12345')
sasha_user =User.objects.create_user(username='sasha', email='sasha_user@mail.ru', password='54321')

# Создание двух объектов модели Author
dima = Author.objects.create(user=dima_user)
sasha = Author.objects.create(user=sasha_user)

# Добавлякм 4 категории в модель Category
film = Category.objects.create(name='Кино')
sport = Category.objects.create(name='Спорт')
politic = Category.objects.create(name='Политика')
music = Category.objects.create(name='Музыка')

# Добавлякм две статьи и одну новость в модель Post
article_1_film = "Статья №1 в категории  фильм от автора Дима"
article_2_sport = "Сатья №2 в категории спорт от автора Саша"
news_1_music = "Новость №1 в категории музыка от автора Дима"

article_dima = Post.objects.create(author=dima, view=Post.article, heading='Статья №1 в категории  фильм от автора Дима', text_post=article_1_film)
article_sasha = Post.objects.create(author=sasha, view=Post.article,heading='Сатья №2 в категории спорт от автора Саша', text_post=article_2_sport)
news_dima = Post.objects.create(author=dima, view=Post.news, heading='Новость №1 в категории музыка от автора Дима', text_post=news_1_music)

# Присваиваем им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий)
PostCategory.objects.create(post=article_dima, category=film)
PostCategory.objects.create(post=article_dima, category=politic)
PostCategory.objects.create(post=article_sasha, category=sport)
PostCategory.objects.create(post=news_dima, category=music)

# Создаем комментарии
comment1 = Comment.objects.create(post=article_dima, user=sasha.user, comment_text='Коментарий №1 от автора Саши к статье №1 в категории  фильм от автора Дима')
comment2 = Comment.objects.create(post=article_sasha, user=dima.user, comment_text='Комментарий №2 от автора Дима к статье №2 в категории спорт от автора Саша')
comment3 = Comment.objects.create(post=news_dima, user=sasha.user, comment_text='Комментарий №3 от автора Саша к новости №1 в категории музыка от автора Дима')
comment4 = Comment.objects.create(post=news_dima, user=dima.user, comment_text='Комментарий №4 от автора Дима к новости №1 в категории музыка от автора Дима')

# Список всех объектов, которые можно лайкать
list_for_like = [article_sasha,
                 article_sasha,
                 news_dima,
                 comment1,
                 comment2,
                 comment3,
                 comment4
                 ]
# 100 рандомных лайков\дислайков (по четности счетчика)
for i in range(100):
    random_odj = random.choice(list_for_like)
    if i % 2:
        random_odj.like()
    else:
        random_odj.dislike()

# Подсчет рейтинга  Димы
rating_dima = (sum([Post.rating_post*3 for Post in Post.objects.filter(author=dima)])
             + sum([Comment.rating_comment for Comment in Comment.objects.filter(user=dima.user)])
             + sum([Comment.rating_comment for Comment in Comment.objects.filter(post__author=dima)])
               )

# Обновляем рейтинг
dima.update_rating(rating_dima)
# Подсчет рейтинга  Саши
rating_sasha= (sum([Post.rating_post*3 for Post in Post.objects.filter(author=sasha)])
               + sum(Comment.rating_comment for Comment in Comment.objects.filter(user=sasha.user))
               + sum([Comment.rating_comment for Comment in Comment.objects.filter(post__author=sasha)])
               )
sasha.update_rating(rating_sasha)

# лучший автор
best_author = Author.objects.all().order_by('-rating')[0]
print("Лудший автор")
print("username:", best_author.user.username)
print("РУйтинг:", best_author.rating)
print("")

# Лучщая статья
best_article = Post.objects.filter(view=Post.article).order_by('-rating_post')[0]
print("Лучшая статья")
print("Дата:", best_article.create_time)
print("Автор:", best_article.author.user.username)
print("Рейтирг:", best_article.author.rating)
print("Загаловок:", best_article.heading)
print("Превью:", best_article.preview())
print("")

# Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
print("Комментарии к ней")
for Comment in Comment.objects.filter(post=best_article):
    print("Дата:", Comment.create_time)
    print("Автор:", Comment.user.username)
    print("Рейтинг", Comment.rating_comment)
    print("Комментарий", Comment.comment_text)
    print("")
