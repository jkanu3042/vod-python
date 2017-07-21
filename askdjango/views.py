#account/views.py
from django.shortcuts import render,redirect
# Create your views here.



def redirectblog(request):
    return redirect('blog:post_list')
