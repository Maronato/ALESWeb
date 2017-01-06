from django.shortcuts import render, get_object_or_404  
from blog.models import Post


def index(request):
    all_posts = Post.objects.all().order_by('-created')
    if len(all_posts) >= 5:
        posts = all_posts[:5]
    else:
        posts = all_posts
    return render(request, 'blog/index.html', {
    'posts': posts,
    })
    
    
def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/detail.html', {
        'post': post,
        })

