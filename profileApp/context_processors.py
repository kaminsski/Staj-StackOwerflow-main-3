from .models import CustomUser  # Kullanıcı modelini içeri aktarın

def follower_count_processor(request):
    if request.user.is_authenticated:
        user = CustomUser.objects.get(user_uuid=request.user.user_uuid)
        followers_count = user.followers.count()
        following_count = user.following.count()
    else:
        followers_count = 0
        following_count = 0

    return {'followers_count': followers_count, 'following_count': following_count}
