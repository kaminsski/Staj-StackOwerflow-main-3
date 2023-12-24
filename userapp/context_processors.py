def saved_posts_processor(request):
    from userapp.models import SavedQuestion
    if request.user.is_authenticated:
        user = request.user
        saved_posts = SavedQuestion.objects.filter(user=user)
    else:
        saved_posts = None  # Oturum açmamış kullanıcı için saved_posts'ü None olarak ayarlayabilirsiniz
    return {'saved_posts': saved_posts}

