import os
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.generic import DetailView

from .forms import PostForm
from .models import Post
# Create your views here.

# Case1 - FBV 버전
# def post_detail(request, id):
#     post = get_object_or_404(Post,id=id)
#     return render(request, 'dojo/post_detail.html', {
#         'post':post,
#     })

'''
Case 2 - 함수를 통해, 뷰 생성 버전
def generate_view_fn(model):
    def view_fn(request, id):
        instance = get_object_or_404(model, id=id)
        instance_name = model._meta.model_name
        template_name = '{}/{}_detail.html'.format(model._meta.app_label, instance_name)
        return render(request, template_name, {
            instance_name: instance,
        })

    return view_fn

#post_detail은 generate_view_fn이 가지고 있는 함수를 리턴받으므로 함수이다.
post_detail = generate_view_fn(Post)
'''

'''
# Case 3 - CBV형태로 컨셉만 구현한 버전
class DetailView(object):
    def __init__(self, model):
        self.model = model

    def get_object(self, *args, **kwargs):
        return get_object_or_404(self.model, id=kwargs['id'])

    def get_template_name(self):
        return '{}/{}_detail.html'.format(self.model._meta.app_label, self.model._meta.model_name)

    def dispatch(self, request, *args, **kwargs):
        return render(request, self.get_template_name(), {
            self.model._meta.model_name: self.get_object(*args, **kwargs),
        })

    @classmethod
    def as_view(cls, model):
        def view(request, *args, **kwargs):
            self = cls(model)
            return self.dispatch(request, *args, **kwargs)
        return view

post_detail = DetailView.as_view(Post)
'''

# Case 4 - 장고 기본 제공 DetailView CBV 쓰기

#post_detail = DetailView.as_view(model = Post, pk_url_kwarg='id')

#url 설정을 (?P<id>\d+) 에서 DetailView의 기본키인 pk로 변경 -> (?P<pk>\d+)
post_detail = DetailView.as_view(model=Post)






def post_new(request):
    if request.method == 'POST':
        #이 form은 유저가 어떤 값을 입력했는지 알고 있는 form이다.
        #request.POST와 request.FILES의 인자의 순서가 뒤 바뀌면 안된다.
        #파일 첨부 기능을 빼려면 request.FILES를 생략 가능.
        form = PostForm(request.POST, request.FILES)
        #모든 유효성 검사를 통과하지 못하면 False를 return 한다.
        if form.is_valid():
            # 방법 4를 채택, save로직을 forms.py에 구현하기 위한 작업 실시
            post = form.save(commit=False)
            #ip 확인 후에 최종 저장 할 것이므로 commit을 False로 둔것.
            post.ip = request.META['REMOTE_ADDR']
            post.save()
            return redirect('/dojo/')




            # 방법 1)
            '''
            post = Post()
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.save()
            '''

            # 방법 2)
            '''
            post = Post(title=form.cleaned_data['title'],
                        content=form.cleaned_data['content'])
            post.save()
            '''

            # 방법 3)
            '''
            post = Post.objects.create(title=form.cleaned_data['title'],
                        content=form.cleaned_data['content'])
            '''


            # 방법 4)
            '''
            post = Post.objects.create(**form.cleaned_data)
            return redirect('/dojo/')
            '''
        else:
            form.errors
    else:
        form = PostForm()
    return render(request, 'dojo/post_form.html', {
        'form' : form,
    })

def post_edit(request, id):
    # post 모델을 불러오고, 단순히 form에 instance 값을 인자로 추가로 넣었을뿐,
    # 처리는 post_new와 비슷하다.
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.ip = request.META['REMOTE_ADDR']
            post.save()
            return redirect('/dojo/')
        else:
            form.errors
    else:
        form = PostForm(instance=post)
    return render(request, 'dojo/post_form.html', {
        'form' : form,
    })

def mysum(request, numbers):
    result = sum(map(lambda i: int(i or 0), numbers.split('/')))
    return HttpResponse(result)

def hello(request, name, age):
    result = "안녕하세요. {}. {}살 이시네요".format(name, age)
    return HttpResponse(result)

def post_list1(request):
    name = '공유'
    return HttpResponse('''
    <h1>AskDjango</h1>
    <p>{name}</p>
    <p>여러분들을 찰지게 때려드립니다.</p>
    '''.format(name=name))


def post_list2(request):
    name = '공유'
    return render(request, 'dojo/post_list.html', {'name':name} )


def post_list3(request):
    return JsonResponse({
        'message': '안녕 파이썬 맨',
        'items': ['파이썬', '장고', 'Celery', 'Asure', 'AWS']
    }, json_dumps_params={'ensure_ascii': False})

def excel_download(request):
    filepath = os.path.join(settings.BASE_DIR, 'ang.xls')
    filename = os.path.basename(filepath)
    with open(filepath, 'rb') as f:
        response = HttpResponse(f, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        return response