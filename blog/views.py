from django.shortcuts import render
from blog.models import Post

def blog(request):
    all_posts = Post.objects.all().order_by('-date')
    data = {'posts': all_posts,}

    return render(request, 'blog/index.html', data)

# Create your views here.
