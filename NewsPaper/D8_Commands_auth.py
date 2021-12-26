
# D8_3 Для дженерика UpdateView. Реализуйте для него проверку наличия аутентификации с помощью миксина.
# В файле настроек проекта добавьте адрес,
# по которому Django будет перенаправлять пользователей после успешного входа в систему.


# Переходим в файл NewsPaper/news/views.py
# Правим представление  с UpdateView
# Добавим дженерик  LoginRequiredMixin
# Добавим строку для перенаправления login_url = '/admin/login/'

# Переходим в файл NewsPaper/setting.py
# Добавляем переменную LOGIN_URL = '/admin/login/'

# D8_4 займёмся созданием простого приложения, цель которого — показывать персональную информацию
# # для аутентифицированных пользователей и предлагать войти/зарегистрироваться, если пользователь ещё не авторизован.
# sign — приложение регистрации, аутентификации и авторизации;
# protect — приложение, в котором мы практически ничего не сделаем.
# В нём предполагается создать лишь одно представление для аутентифицированных пользователей.

# 1 Вводим:
# venv\scripts\activate

# 2.python manage.py startapp sign
# python manage.py startapp protect

# 3.Переходим в файл setting.py
# Вносим изменения:
# ALLOWED_HOSTS = ['127.0.0.1']
#
# INSTALLED_APPS = [  // ...
#     'sign',
#     'protect',]
# TEMPLATES = [ {'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [os.path.join(BASE_DIR, 'templates')],
#         // ...
#         },
#     },
# ]
#
# LOGIN_URL = 'sign/login/'
# LOGIN_REDIRECT_URL = '/'

# 4. Правим NewsPaper/urls.py:
# path('', include('protect.urls')),
# path('sign/', include('sign.urls'))

# 5. приложение protect. Переходим/создаем в файл NewsPaper/protect/urls.py
# from django.urls import path
# from .views import IndexView
# urlpatterns = [path('', IndexView.as_view()),]

# 6. приложение protect. Переходим/создаем в файл NewsPaper/protect/views.py
# from django.shortcuts import render
# from django.views.generic import TemplateView
# from django.contrib.auth.mixins import LoginRequiredMixin
# class IndexView(LoginRequiredMixin, TemplateView):
#     template_name = 'protect/index.html'

# 7. Рассмотрим структуру шаблонов.
# -----создан базовый шаблон, который будет расширять все остальные шаблоны. templates/main.html
# <html>
#     <head>
#         <title> Simple SignUp/SignIn app</title>
#     </head>
#     <body>
#         <div>
#             <h1><a href="/">Simple SignUp/SignIn app</a></h1>
#         </div>
#         {% block content %}
#         {% endblock %}
# #     </body>
# # </html>


# -------создан  шаблон  protect/index.html
# {% extends "main.html" %}
# {% block content %}
# <h2>Страница авторизованного пользователя {{request.user.username}}</h2>
# <div> Здесь может содержаться персональная информация для каждого пользователя </div>
# <button> <a href="sign/logout/">Выйти</a> </button>
# {% endblock %}


# Создание каркаса закончено,можно приступить к вопросам аутентификации и регистрации
# 8. Аутентификация
# В папке templates/sign создаем три шаблона login, logout, singup

# ----заполняем шаблон  login.html

# 8.1 А теперь перейдём к самому интересному: как этот процесс организован на уровне представлений. Аутентификация по
# username пользователя является самым базовым вариантом аутентификации, и она поддерживается решением «из коробки»
# Django. Для этого фреймворк предоставляет готовое представление на основе классов LoginView. Для его использования
# достаточно в файле конфигурации URL (приложения sign в этом примере) импортировать его и вставить в urlpatterns:
# sign/urls.py- создаем\заполняем

# 8.2 При выходе с сайта (вспоминаем кнопку, которую мы создали раньше в шаблоне index.html) Django перенаправит
# пользователя на страницу, указанную в параметре template_name класса LogoutView. А сам шаблон выглядит так:
# sign/logout.html -заполняем

# Тестируем ситему python manage.py createsuperuser

# 9-Регистрация
# 9.1 написать форму, с помощью которой мы будем создавать нового пользователя
# sign/forms.py (перенес из models.py, потому что не верно)

# 9.2 В файле представлений реализуем Create-дженерик.
# sign/views.py

# 9.3 мы должны модифицировать файл конфигурации URL, чтобы Django мог увидеть это представление.
# sign/urls.py

# 9.4 И наконец, мы должны «заглянуть» в шаблон, который создаёт форму.
# templates/sign/signup.html (Здесь мы использовали автоматически формируемое
# представление формы в виде набора тегов <p>:)

# test
# Username=piter
# Имя-Петя
# Фамилия:Сидоров
# Email-piter@mail.ru
# Password: hXNxDCXdi5efdDg

# 10 Подключение пакета allauth
# Вводим
# venv\scripts\activate
# pip install django-allauth -установим пакет
# cd NewsPaper

# 10.1  Согласно официальной документации в файле настроек нужно внести следующие изменения:
# 10.1 добавлено для пакета allauth
# AUTHENTICATION_BACKENDS = [
#     # Needed to login by username in Django admin, regardless of `allauth`
#     'django.contrib.auth.backends.ModelBackend',
#     # `allauth` specific authentication methods, such as login by e-mail
#     'allauth.account.auth_backends.AuthenticationBackend',
# ]
# INSTALLED_APPS = [
# # 10.1 добавлено для пакета allauth
#     'allauth',
#     'allauth.account',
#     'allauth.socialaccount',
#     # 10.1 выбираем провйдера
#     'allauth.socialaccount.providers.google',
#     остальные уже были
#
# LOGIN_URL = '/accounts/login/'

# 10.2 Выполняем миграцию
# python manage.py migrate

# # 11 Регистрация и вход по почте
# 11.1 В файл настроек проекта мы должны внести дополнительные параметры(вписываем в самый конец):
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_UNIQUE_EMAIL = True
# ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_EMAIL_VERIFICATION = 'none'

# 11.2 Правим файл конфигурации NewsPaper/url.py
# добавим  path('accounts/', include('allauth.urls')),

# 11.3 чтобы использовать этот пакет без дополнительных настроек как решение «из коробки» достаточно написать
# базовый шаблон, который будет использовать этот пакет в виде:
# templates/base.html

# 12 Регистрация по средствам провайдераб пошагово в тетради все расписано
# Client id: 619269392278-75ov298o675pieeisjnctkgvit9lacdd.apps.googleusercontent.com
# Secret key: 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

# 13 Группы пользователей
# 13.1 Группы
# 13.2 пошагово в тетради все расписано
# 13.3 пошагово в тетради все расписано
#
# # 13.4 Добавление в группы при регистрации
# Кастомизируем форму регистрации SignupForm, которую предоставляет пакет allauth.
# Переходим в файл sign/forms.py прописываем код
#
# 13.5 Чтобы allauth распознал нашу форму как ту, что должна выполняться вместо формы по умолчанию, необходимо добавить
# строчку в файл настроек проекта settings.py: (Вписываем в конец)
# # ACCOUNT_FORMS = {'signup': 'sign.forms.BasicSignupForm'}
#
# Проверяем механизм. Запустим сервер и перейдём на страницу регистрации.
# Sign Up
# test_common_user@example.com
# Password: hXNxDCXdi5efdDg
# User перемесился в группу  common автоматически
#
# 13.6 Добавление в группы в других случаях
#  добавим кнопку «Стать автором» на странице авторизованного пользователя,если он в этой группе не находится.
# Переходим в protect/views.py и модифицируем код
#
# 13.7 Переходим в temlates/protect/index.html В самом шаблоне мы добавляем кнопку «Стать автором», если переменная,
# которую мы определили ранее — True:
# {% if is_not_authors %}
# <button> <a href="sign/upgrade/"> Стать автором</a> </button>
# {% endif %}

# 13.8 нужно добавить ещё одно view для апгрейда аккаунта до authors. Иными словами, для добавления в группу authors.
# Для данной задачи не существует дженерика, а писать класс-представление для такой простой задачи кажет
# В файле sign/views.py добавим её


# 13.9 Нам осталось только связать нашу кнопку с этой функцией, добавляя соответствующую строку в файл конфигурации URL.
# # Переходим в sign/urls.py
# from news.models import Author (пусть подчеркивает красным)
# !!!    if not Author.objects.filter(user=user).exists():
#         Author.objects.create(user=user)
# добавил на стадии проверки не записвался в базу данных

# # # 14 Права доступа

# 14.1 Добавьте для группы authors права насоздание и редактирование объектов модели Post,используя панель
# # администратора.
# Предоставление прав отдельным пользователям и/или группам может производиться как через панель администратора,
# так и вручную. Рассмотрим лишь первый способ.
# Для того чтобы это сделать, необходимо войти на соответствующую страницу пользователя или группы и «перетащить»
# разрешения в правую колонку. Например, следующим образом:
# Однако назначение прав в админке никак не изменит ситуацию, ведь мы нигде не указали,
# где эти права должны проверяться и применяться!

# 14.2 В соответствующих представлениях добавьте миксин ограничения прав и в атрибуте класса-представления пропишите,
# какими правами должен обладать пользователь для доступа к этой странице.
# Переходим в файл new/views.py
# # обавляем миксин в представления CreateView и UpgateView
# from django.contrib.auth.mixins import PermissionRequiredMixin
# class PostCreate(PermissionRequiredMixin, CreateView):
#     permission_required = 'news.add_post'  # 14.2
#
# class PostUpdate(PermissionRequiredMixin, UpdateView):
#     permission_required = 'news.change_post'  # 14.2

