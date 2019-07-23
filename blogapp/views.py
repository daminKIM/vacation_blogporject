from django.shortcuts import render, get_object_or_404,redirect
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Blog
from .form import BlogPost


# Create your views here.
def home(request) : #쿼리셋
    blogs = Blog.objects 
    #블로그 모든 글들을 대상으로
    blog_list = Blog.objects.all()
    #블로그 객체 세 개를 한 페이지로 자르기 
    paginator = Paginator(blog_list, 4)
    #request된 페이지가 뭔지를 알아내고 
    page = request.GET.get('page')
    #request된 페이지를 얻어온 뒤 return 해 준다.
    posts = paginator.get_page(page)
    return render(request, 'home.html', {'blogs':blogs, 'posts' :posts})

def detail(request, blog_id) :
    details =get_object_or_404(Blog, pk=blog_id)
    return render (request, 'detail.html', {'details' : details})

def introduce(request) :
    return render(request, 'introduce.html')

def new(request) : #new.html을 화면에 띄어주는 간단한 함수
    return render(request, 'new.html')

def create(request) : #입력받은 내용을 데이터베이스에 넣어주는 함수
    blog = Blog()
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()
    blog.save()  #쿼리셋 메소드 중에 하나, 위에서 입력받은 내용을 데이터 베이스에 저장하라는 메소드 명령어
    return redirect('/blog/'+str(blog.id))
   
def blogpost(request) :
    # 1. 입력된 내용을 처리 ->POST
    if request.method == 'POST' :
        form = BlogPost(request.POST)
        if form.is_valid() :
            post = form.save(commit=False)
            post.pub_date = timezone.now()
            post.save()
            return redirect('home')
    # 2. 빈 페이지를 띄어주는 기능 ->GET
    else :
        form = BlogPost()
        return render(request, 'new.html', {'form' : form})