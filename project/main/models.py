from django.db import models

class StandartUser(models.Model):
    password = models.CharField(max_length=256)
    username = models.CharField('username', max_length=150)
    last_name = models.CharField(max_length=150)
    date_joined  = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=150)

class Articles(models.Model):
    author = models.CharField('Автор', max_length=25)
    title = models.CharField('Название', max_length=255)
    intro = models.CharField('Анонс', max_length=250)
    content = models.TextField('Статья',blank=True)
    time_create = models.DateTimeField('Время создания',auto_now_add=True)
    time_update = models.DateTimeField('Время редакции',auto_now=True)
    is_published = models.BooleanField('Статус публикации',default=True)

class Friendship(models.Model):
    user = models.ForeignKey(StandartUser, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(StandartUser, on_delete=models.CASCADE, related_name='friend_of')
    date_added = models.DateTimeField(auto_now_add=True)

#переписки

class Chat(models.Model):
    name = models.CharField(max_length=150, blank=True)
    is_group_chat = models.BooleanField(default=False)

class UserChat(models.Model):
    user = models.ForeignKey(StandartUser, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

class MessageСhat(models.Model):
    user = models.ForeignKey(StandartUser, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

#каналы
    
class Channel(models.Model):
    user = models.ForeignKey(StandartUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)

class Media(models.Model):
    files = models.FileField()

class Article(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    text = models.TextField()

class ImageArticle(Article):
    images = models.ManyToManyField(Media, limit_choices_to={'file__startswith': 'images'}, related_name='image_articles')

class VideoArticle(Article):
    video = models.OneToOneField(Media, limit_choices_to={'file__startswith': 'videos'}, related_name='video_articles', on_delete=models.CASCADE)

class AudioArticle(Article):
    audios = models.ManyToManyField(Media, limit_choices_to={'file__startswith': 'audios'}, related_name='audio_articles')

class ChannelArticle(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

