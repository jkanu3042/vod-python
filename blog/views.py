from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Post
from .forms import PostForm

# Create your views here.

def post_list(request):
    print(request.user.is_authenticated)

    qs = Post.objects.all()

    q = request.GET.get('q', '')
    if q:
        qs = qs.filter(title__icontains=q)

    response = render(request, 'blog/post_list.html', {
        'post_list': qs,
        'q': q,
    })
    # render의 반환값은 HttpResponse 인스턴스임.
    # render를 통해서, 좀 더 쉽게 탬플릿을 통한 랜더링
    return response

def post_detail(request, id):
    # try:
    #     post = Post.objects.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404

    post = get_object_or_404(Post, id=id)

    return render(request, 'blog/post_detail.html', {
        'post': post
    })

def post_new(request):
    if request.method=='POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid:
            post = form.save()
            messages.success(request, '새 포스팅을 저장했습니다.')
            return redirect(post) # post.get_absolute_url()로 이동
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {
        'form' : form,
    })

def post_edit(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method=='POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid:
            post = form.save()
            messages.success(request, '수정 되었습니다.')
            return redirect(post) # post.get_absolute_url()로 이동
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {
        'form': form,
    })
