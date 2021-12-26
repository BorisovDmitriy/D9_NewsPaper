from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin  # 14.2
from django.shortcuts import redirect
from django.contrib.auth.models import User


class PostsList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'posts.html'
    # указываем имя шаблона, где будет лежать HTML, в котором будут все инструкции о том,
    # как именно пользователю должны вывестись наши объекты
    context_object_name = 'posts'
    # это имя списка, в котором будут лежать все объекты,
    # его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by('-create_time')
    paginate_by = 10
    form_class = PostForm  # D9 (подписка) чтобы получить доступ к форме через POST

    # общий метод для создания дополнительных атрибутов, добавить атрибуты в html
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['form'] = PostForm()
        context['is_author'] = self.request.user.groups.filter(name='author').exists()
        context['is_auth'] = self.request.user.is_authenticated
        return context

        # переопределение метода чтобы хз что,
        # зачем это вообще всё? почему по-умолчанию всё не работает как надо?
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый пост
            form.save()

        return super().get(request, *args, **kwargs)


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['form'] = PostForm()
        context['is_author'] = self.request.user.groups.filter(name='author').exists()
        context['is_auth'] = self.request.user.is_authenticated
        context['current_user'] = self.request.user
        return context


class PostsSearchList(ListView):
    model = Post
    template_name = 'news/search/posts_filters.html'
    context_object_name = 'posts'
    ordering = '-create_time'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        # вписываем наш фильтр в контекст
        return context


class PostCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'news.add_post'  # 14.2
    template_name = 'news/post_create.html'
    form_class = PostForm


class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'news.change_post'  # 14.2
    login_url = '/admin/login/'
    template_name = 'news/post_update.html'
    form_class = PostForm
# метод get_object мы используем вместо queryset,
# чтобы получить информацию об объекте, который мы собираемся редактировать

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = 'news.delete_post'
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


@login_required
def subscription(request):
    user = request.user  # получаем из реквеста самого пользователя
    cat_id = request.POST['cat_id']  # получаем из реквеста то, что пришло из формы через ПОСТ
    category = Category.objects.get(
        pk=int(cat_id))  # получаем категорию через cat_id, который пришёл через ПОСТ через скрытое поле

    # если связь пользователя с категорией не создана,
    # второй вариант - проверять имя кнопки, которая пришла с реквестом
    # и условие строить уже на этом
    if user not in category.subscriptions.all():
        # добавляем пользователя в связь с категорией
        category.subscriptions.add(user)

    # а если связь уже есть, то отписываем, т.е. удаляем из этой связи
    else:
        category.subscriptions.remove(user)

    # после чего возвращаем на предыдущую страницу, которую берём из реквеста
    # она хранится в META, а это словарь, поэтому достаём через гет
    # если этого ключа нет, то возвращается рут и редирект кидает в корень
    return redirect(request.META.get('HTTP_REFERER', '/'))


