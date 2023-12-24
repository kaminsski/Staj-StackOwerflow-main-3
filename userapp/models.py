from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from datetime import datetime
from ckeditor.fields import RichTextField
from profileApp.models import CustomUser, Badge
from django.db.models.signals import post_save
from django.dispatch import receiver



class Tags(models.Model):
    tagler = models.CharField(("Tagler"), max_length=10)
    tagDescription = models.TextField(("Açıklma"), max_length=100,null=True)
    view = models.IntegerField(("Görüntülenme Sayısı"), default=0)


    def __str__(self):
        return self.tagler

class Post(models.Model):
    title = models.CharField(("Başlık"), max_length=50, null=True)
    description = models.TextField(("Açıklama"), max_length=500, null=True)
    createdAt = models.DateTimeField(("Oluşturma tarihi"), auto_now=True)
    viewed = models.IntegerField(("Görüntülenme Sayısı"), default=0)
    like = models.IntegerField(("Beğeni Sayısı"), default=0)
    comment = models.IntegerField(("Yorum Sayısı"), default=0)
    user = models.ForeignKey(CustomUser, verbose_name=("Yazarı"), on_delete=models.CASCADE)
    tagleri = models.ManyToManyField(Tags,("Tagleri"))
    kodalanı = RichTextField("Kod Bloğu", max_length=1500, null=True)
    answerCount = models.IntegerField(("Görüntülenme Sayısı"), default=0)



    def __str__(self):
        return self.title
class Answer(models.Model):
    post = models.ForeignKey(Post, verbose_name=("Post"), on_delete=models.CASCADE)
    
    description = models.TextField(("Açıklama"), max_length=500, null=True)
    createdAt = models.DateTimeField(("Oluşturma tarihi"), auto_now=True)
    like = models.IntegerField(("Beğeni Sayısı"), default=0)
    comment = models.IntegerField(("Yorum Sayısı"), default=0)
    user = models.ForeignKey(CustomUser, verbose_name=("Yazarı"), on_delete=models.CASCADE)
    kodalanı = RichTextField("Kod Bloğu", max_length=1500, null=True)
    def __str__(self):
        return self.description    


class Comments(models.Model):
    post = models.ForeignKey(Post, verbose_name=("Post"), on_delete=models.CASCADE)
    
    description = models.TextField(("Açıklama"), max_length=500, null=True)
    createdAt = models.DateTimeField(("Oluşturma tarihi"), auto_now=True)
    user = models.ForeignKey(CustomUser, verbose_name=("Yazarı"), on_delete=models.CASCADE)
    def __str__(self):
        return self.description
class Comments2(models.Model):
    answer = models.ForeignKey(Answer, verbose_name=("Post"), on_delete=models.CASCADE)
    
    description = models.TextField(("Açıklama"), max_length=500, null=True)
    createdAt = models.DateTimeField(("Oluşturma tarihi"), auto_now=True)
    user = models.ForeignKey(CustomUser, verbose_name=("Yazarı"), on_delete=models.CASCADE)

    def __str__(self):
        return self.description    
    
@receiver(post_save, sender=Post)
def check_likes_and_award_badge(sender, instance, created, **kwargs):
    if created:
        like = instance.like
        like_count = Post.objects.filter(like=like).count()

        user = instance.user  # User is the same for all cases

        if like_count >= 1 and like_count < 2:
            # Award the bronze badge to the user.
            bronze_badge = Badge.objects.get(pk=1)  # Use the appropriate primary key for the Bronze Badge
            user.badge.add(bronze_badge)

        if like_count >= 2 and like_count < 3:
            # Award the silver badge to the user.
            silver_badge = Badge.objects.get(pk=2)  # Use the appropriate primary key for the Silver Badge
            user.badge.add(silver_badge)

        if like_count >= 3:
            # Award the gold badge to the user.
            gold_badge = Badge.objects.get(pk=3)  # Use the appropriate primary key for the Gold Badge
            user.badge.add(gold_badge)
            
class PostLikes(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)    

class PostDislike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)    

class AnswerLikes(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)    

class AnswerDislike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)    

class Goruntulenme(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class SavedQuestion(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_saved = models.DateTimeField(auto_now_add=True)