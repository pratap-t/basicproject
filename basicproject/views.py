from django.views import View
from django.contrib.auth import get_user
from genre.models import Genre, Genrefellow
from posts.models import Post
from django.shortcuts import render

class HomePage(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            association_list = []
            post_to_displayed = []
            user_logged_in = get_user(request)
            print(user_logged_in.username)
            for item in Genrefellow.objects.all():
                print(item)
                if item.user == user_logged_in:
                    print(item.user)
                    association_list.append(item.genre)
            for post_item in Post.objects.all():
                if post_item.genre in association_list:
                    post_to_displayed.append(post_item)
            return render(request, 'user_home.html',
                          {'post_list': post_to_displayed})
        else:
            return render(request, 'index.html')