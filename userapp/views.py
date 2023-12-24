from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from .models import *
from .form import *
from django.contrib import messages
from django.shortcuts import get_object_or_404




def index(request):

    return render(request, 'index.html')


def profile(request, user_uuid):
    user = get_object_or_404(CustomUser, user_uuid=user_uuid)
    followers_count = user.followers.count()
    following_count = user.following.count()
    badges = user.badge.all()


    context = {
        'badges': badges,
        'user': user,
        'followers_count': followers_count,
        'following_count': following_count,
    }

    return render(request, 'profile.html', context)

def questions(request):
    context = {}
    arama = request.GET.get("ara")
    if arama:
        sorular = Post.objects.filter(title__icontains= arama).order_by("-createdAt")

    else:
        sorular = Post.objects.all().order_by("-createdAt")

            
        
   
    context["sorular"] = sorular

    return render(request, 'questions.html', context)

def error(request):
    return render(request, "404.html")

def questionDetails(request, questionId):
    context = {}
    if  request.user.is_authenticated == False:
        return redirect("404")

    form2 = CommentForm
    context["form2"] = form2
    form3 = AnswerForm
    context["form3"] = form3    

    soru = Post.objects.filter(id=questionId).first()
    tag_values = soru.tagleri.all().values_list('id', flat=True)
    related = Post.objects.filter(tagleri__in=tag_values).exclude(id=questionId)

    context["related"] = related
    yorumlar = Comments.objects.filter(post = soru)
    context["yorumlar"] = yorumlar

    görüntüledi_mi = Goruntulenme.objects.filter(post = soru) & Goruntulenme.objects.filter(user = request.user) 

    if görüntüledi_mi:
        pass
    else:
        Goruntulenme.objects.create(
            user = request.user,
            post = soru
        )
        soru.viewed +=1
        soru.save()

    yorumlar2 = Comments2.objects.filter(answer__post = soru)
    context["yorumlar2"] = yorumlar2
    if request.method == "POST":
        form = YourModelForm(request.POST)
        if form.is_valid():
            postform = form.save(commit=False)
            postform.user = request.user
            postform.post = soru
            postform.save()
            soru.answerCount = soru.answerCount + 1
            soru.save()
            messages.add_message(request, messages.INFO, "Cevabınız gönderildi.")
            return redirect ("questionDetails", questionId)

    else:
        
        context["sorular"] = soru
        cevaplar = Answer.objects.filter(post=soru)
        context["cevaplar"] = cevaplar
        context["form"] = YourModelForm
        return render(request, 'questionsDetail.html',context)


def commentCreate(request, questionId):
    context = {}
    if request.user.is_authenticated == False:
        return redirect("404")
    soru = Post.objects.filter(id=questionId).first()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            postform = form.save(commit=False)
            postform.user = request.user
            postform.post = soru
            postform.save()
            messages.add_message(request, messages.INFO, "Yorumunuz başarıyla oluşturuldu.")
            return redirect ("questionDetails" , questionId)

def commentCreate2(request, answerId , questionId):
    context = {}
    if request.user.is_authenticated == False:
        return redirect("404")
    
    

    if request.method == "POST":
        yorumlar2 = Answer.objects.filter(id = answerId).first()
        form = AnswerForm(request.POST)
        if form.is_valid():
            postform = form.save(commit=False)
            postform.user = request.user
            postform.answer = yorumlar2
            postform.save()
            messages.add_message(request, messages.INFO, "Yorumunuz başarıyla oluşturuldu.")
            return redirect ("questionDetails" , questionId)



def tags(request):
    context= {}
    
    arama = request.GET.get("tagAra")
    if arama:
        tagler = Tags.objects.filter(tagler__icontains= arama)

    else:
        tagler = Tags.objects.all()
    context["tagler"] = tagler
    return render(request, 'tags.html', context)

def tagDetail(request, tagId):
    context= {}
    tag = Tags.objects.get(id=tagId)  # tagId'ye sahip olan Tags nesnesini alır

    sorular = Post.objects.filter(tagleri = tag)
    context["sorular"] = sorular
    return render(request, 'tagDetail.html', context)

def users(request):

    return render(request, 'users.html')



def createpost(request):
    context = {}
    if request.user.is_authenticated == False:
        return redirect("404")
    
    if request.method == "POST":
        form = CreatePost(request.POST)
        if form.is_valid():
            postform = form.save(commit=False)
            postform.user = request.user
            postform.save()
            form.save_m2m()

            # Oluşturulan postun içerdiği taglerin view sayısını artırın
            for tag in postform.tagleri.all():
                    tag.view += 1
                    tag.save()
                    
            messages.add_message(request, messages.INFO, "Sorunuz başarıyla oluşturuldu.")
            return redirect("questions")
    
    else:
        context["form"] = CreatePost
        return render(request, "createPost.html", context)    
    
def addLike(request, userId, postId):
        
    if request.user.is_authenticated == False:
        return redirect("404")
  
    user = CustomUser.objects.filter(user_uuid=userId).first()
    post = Post.objects.filter(id=postId).first()
    
    dislikeModel = PostDislike.objects.filter(user=user) & PostDislike.objects.filter(post=post)

    is_liked = PostLikes.objects.filter(user=user) & PostLikes.objects.filter(post=post)

    if is_liked:
        
        messages.add_message(request, messages.INFO, "Zaten bunu beğenmiştiniz..")
        return redirect("questionDetails" , postId)
    
    if user and post:
        if dislikeModel:
            dislikeModel.delete()
        PostLikes.objects.create(
            user = user,
            post = post
           

        )
        postlike = post.like + 1
        
        post.like = postlike
        post.save(update_fields=['like'])



        return redirect("questionDetails" , postId)     
def dislike(request, userId, postId):

    if request.user.is_authenticated == False:
        return redirect("404")
  
    user = CustomUser.objects.filter(user_uuid=userId).first()
    post = Post.objects.filter(id=postId).first()

    likeModel = PostLikes.objects.filter(user=user) & PostLikes.objects.filter(post=post)

    is_disliked = PostDislike.objects.filter(user=user) & PostDislike.objects.filter(post=post)

    if is_disliked:
        
        messages.add_message(request, messages.INFO, "Zaten dislike atmışsınız..")
        return redirect("questionDetails" , postId)
    
    if user and post:
        if likeModel:
            likeModel.delete()
        PostDislike.objects.create(
            user = user,
            post = post
           

        )
        postlike = post.like - 1
        
        post.like = postlike
        post.save(update_fields=['like'])



        return redirect("questionDetails" , postId)         
    
def answerlike(request, userId, answerId):

    if request.user.is_authenticated == False:
        return redirect("404")
  
    user = CustomUser.objects.filter(user_uuid=userId).first()
    post = Answer.objects.filter(id=answerId).first()
    is_liked = AnswerLikes.objects.filter(user=user) & AnswerLikes.objects.filter(answer=post)
    dislikeModel = AnswerDislike.objects.filter(user=user) & AnswerDislike.objects.filter(answer=post)

    if is_liked:
        
        messages.add_message(request, messages.INFO, "Zaten bunu beğenmiştiniz..")
        return redirect("questionDetails" , post.post.id)
    
    if user and post:
        if dislikeModel:
            dislikeModel.delete()
            
        AnswerLikes.objects.create(
            user = user,
            answer = post
           

        )
        postlike = post.like + 1
        
        post.like = postlike
        post.save(update_fields=['like'])



        return redirect("questionDetails" , post.post.id)     
def answerdislike(request, userId, answerId):

    if request.user.is_authenticated == False:
        return redirect("404")
  
    user = CustomUser.objects.filter(user_uuid=userId).first()
    post = Answer.objects.filter(id=answerId).first()
    is_disliked = AnswerDislike.objects.filter(user=user) & AnswerDislike.objects.filter(answer=post)
    likeModel = AnswerLikes.objects.filter(user=user) & AnswerLikes.objects.filter(answer=post)

    if is_disliked:
        
        messages.add_message(request, messages.INFO, "Zaten dislike atmışsınız..")
        return redirect("questionDetails" , post.post.id)
    
    if user and post:
        if likeModel:
            likeModel.delete()        
        AnswerDislike.objects.create(
            user = user,
            answer = post
           

        )
        postlike = post.like - 1
        
        post.like = postlike
        post.save(update_fields=['like'])



        return redirect("questionDetails" , post.post.id)             
    

def save_question(request, questionId):
    question = get_object_or_404(Post, id=questionId)
    user = request.user

    # Kullanıcı daha önce bu soruyu kaydetti mi kontrol edin
    if not SavedQuestion.objects.filter(user=user, question=question).exists():
        saved_question = SavedQuestion(user=user, question=question)
        saved_question.save()
        messages.success(request, 'Soru başarıyla kaydedildi.')
    else:
        messages.info(request, 'Soru zaten kaydedilmiş.')

    # Kaydedilen sorunun detay sayfasına yönlendirin
    return redirect('questionDetails', questionId=questionId)

def saved_posts(request, questionId):
    user = request.user

    # Kullanıcının kaydettiği postları alın
    saved_posts = SavedQuestion.objects.filter(user=user)

    return render(request, 'questionDetails.html', {'saved_posts': saved_posts})

def saved_posts_processor(request):
    user = request.user
    saved_posts = SavedQuestion.objects.filter(user=user)
    return {'saved_posts': saved_posts}