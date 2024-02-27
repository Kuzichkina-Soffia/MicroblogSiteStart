from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.db.models import Q

def index(request):
   return render(request, 'main/index.html')

#  регистрация и вход
def reg(request):
    
    if request.method == 'POST':
        form = UsersForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if StandartUser.objects.filter(username=username).exists():
                form.add_error('username', 'Пользователь с таким логином уже существует. Пожалуйста, выберите другое имя пользователя.')
                data = {
                    'form': form,
                }
                return render(request, 'main/register.html', data)
            else:
               user = form.save(commit=False)
               user.password = make_password(form.cleaned_data['password'])
               user.save()
               return redirect('userpage',  id=user.id)
               # return redirect('login')
    else:
        form = UsersForm()
    
    data = {
        'form': form,
    }
    
    return render(request, 'main/register.html', data)

def log(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = StandartUser.objects.get(username=username)
                if check_password(password, user.password):
                    return redirect('userpage', id=user.id)
                else:
                    form.add_error('password', 'Неверный пароль. Пожалуйста, попробуйте еще раз.')
                    data = {
                        'form': form,
                    }
                    return render(request, 'main/login.html', data)
            except StandartUser.DoesNotExist:
                form.add_error('username', 'Пользователь с таким именем не существует. Пожалуйста, зарегистрируйтесь.')
                data = {
                    'form': form,
                }
                return render(request, 'main/login.html', data)
    else:
        form = LoginForm()
    
    data = {
        'form': form
    }
    
    return render(request, 'main/login.html', data)

# пользовательская страница
def userpage(request, id):
    user = get_object_or_404(StandartUser, id=id)
    return render(request, 'user/userpage.html', {'user': user})

def peoplepage(request, id, people_username):
    user = get_object_or_404(StandartUser, id=id)
    people = get_object_or_404(StandartUser, username=people_username)
    people_id = StandartUser.objects.get(username=people_username).id
    friendship_exists = Friendship.objects.filter(user_id=id, friend_id=people_id).exists()
    status = False if friendship_exists else True
    
    articles = Articles.objects.all()
    articles = Articles.objects.filter(author=people_username)
    data = {
       'user': user,
       'people': people,
       'articles': articles,
       'status': status
   }
    return render(request, 'user/peoplepage.html', data)

# спсиок разделов пользовательской страницы
def mychats(request, id):
    user = get_object_or_404(StandartUser, id=id)
    data = {
       'user': user,
   }
    return render(request, 'user/mychats.html', data)

def myfriends(request, id):
    user = get_object_or_404(StandartUser, id=id)
    users = StandartUser.objects.all().exclude(pk=id)
    friends = Friendship.objects.filter(user_id=id) | Friendship.objects.filter(friend_id=id)

    friend_ids = [friend.friend_id for friend in friends]
    friends_list = StandartUser.objects.filter(id__in=friend_ids)

    # friends_list = [friend.friend for friend in friends]

    data = {
       'user': user,
       'users': users,
       'friends': friends_list,
   }
    return render(request, 'user/myfriends.html', data)

def mysubscribes(request, id):
    user = get_object_or_404(StandartUser, id=id)
    data = {
       'user': user,
   }
    return render(request, 'user/mysubscribes.html', data)

def myarticles(request, id):
   user = get_object_or_404(StandartUser, id=id)
   form = ArticlesForm(request.POST)
   if form.is_valid():
      article = form.save(commit=False)
      article.author = user.username
      article.save()
      return redirect('myarticles', id=id)
   else:
      form = ArticlesForm()

   myaricles = Articles.objects.all()
   data = {
        'form': form,
        'user': user,
        'news': myaricles,
   }
   return render(request, 'user/myarticles.html', data)

def mychanels(request, id):
    user = get_object_or_404(StandartUser, id=id)
    data = {
       'user': user,
   }
    return render(request, 'user/mychanels.html', data)

def news(request, id):
   news = Articles.objects.all()
   user = get_object_or_404(StandartUser, id=id)

   data = {
       'news': news,
       'user': user,
   }
   return render(request, 'user/news.html', data)

#статьи
def articles(request):
   news = Articles.objects.all()

   return render(request, 'main/articles.html', {'news': news})

def delete_article(request, article_id):
    article = get_object_or_404(Articles, id=article_id)
    article.delete()
    return HttpResponse('Статья успешно удалена')

def article_detail(request, article_id):
   article = get_object_or_404(Articles, pk=article_id)
   return render(request, 'main/article.html', {'article': article})

# друзья
def add_friend(request, id, friend_id):
    user = get_object_or_404(StandartUser, id=id)
    friend = get_object_or_404(StandartUser, id=friend_id)
    friendship1 = Friendship(user=user, friend=friend)
    friendship2 = Friendship(user=friend, friend=user)
    friendship1.save()
    friendship2.save()

    return redirect('myfriends', id=id)

def remove_friend(request, id, friend_id):
    user = get_object_or_404(StandartUser, id=id)
    friend = get_object_or_404(StandartUser, id=friend_id)

    friendship1 = Friendship.objects.filter(user=user, friend=friend)
    friendship2 = Friendship.objects.filter(user=friend, friend=user)
    friendship1.delete()
    friendship2.delete()
    
    return redirect('myfriends', id=id)

#перпеписки
def open_personal_chat(request, id, people_username):
    user = get_object_or_404(StandartUser, id=id)
    people = get_object_or_404(StandartUser, username=people_username)
    form = WriteMessageForm(request.POST)
    data = {
        'form': form,
        'user': user,
        'people': people,
   }
    return render(request, 'expuser/chat.html', data)

def create_message_or_personal_chat(request):
    pass

def create_group_chat(request):
    pass

####################################