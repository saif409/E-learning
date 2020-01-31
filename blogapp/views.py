from django.shortcuts import render, Http404, get_object_or_404, redirect
from .models import author, category, article, comment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .forms import createForm, createAuthor, categoryForm, commentForm
from django.contrib import messages


# Create your views here.
def index(request):
    post = article.objects.all()
    search = request.GET.get('q')
    if search:
        post = post.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    paginator = Paginator(post,6)  # Show 25 contacts per page

    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    context = {
        "post": total_article
    }
    return render(request, "index.html", context)

def getauthor(request, name):
    post_author = get_object_or_404(User, username=name)
    auth = get_object_or_404(author, name=post_author.id)
    post = article.objects.filter(article_author=auth.id)
    context = {
        "auth": auth,
        "post": post
    }
    return render(request, "profile.html", context)


def getsingle(request, id):
    post = get_object_or_404(article, pk=id)
    first = article.objects.first()
    last = article.objects.last()
    getComment=comment.objects.filter(post=id)
    related = article.objects.filter(category=post.category).exclude(id=id)[:6]
    form=commentForm(request.POST or None)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.post=post
        instance.save()
    context = {
        "post": post,
        "first": first,
        "last": last,
        "related": related,
        "form": form,
        "comment":getComment
    }
    return render(request, "single.html", context)


def getTopic(request, name):
    cat = get_object_or_404(category, name=name)
    post = article.objects.filter(category=cat.id)
    paginator = Paginator(post, 4)  # Show 25 contacts per page
    page = request.GET.get('page')
    total_article = paginator.get_page(page)
    return render(request, "category.html", {"post": total_article, "cat": cat})


def getLogin(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            user = request.POST.get('user')
            password = request.POST.get('pass')
            auth = authenticate(request, username=user, password=password)
            if auth is not None:
                login(request, auth)
                return redirect('index')
            else:
                messages.add_message(request, messages.ERROR, 'Username or password mismatch')
                return render(request, "login.html")
    return render(request, "login.html")


def getlogout(request):
    logout(request)
    return redirect('index')


def getcreate(request):
    if request.user.is_authenticated:
        u = get_object_or_404(author, name=request.user.id)
        form = createForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author = u
            instance.save()
            return redirect('index')
        return render(request, 'create.html', {"form": form})
    else:
        return redirect('login')


def getUpdate(request, pid):
    if request.user.is_authenticated:
        u = get_object_or_404(author, name=request.user.id)
        post = get_object_or_404(article, id=pid)
        form = createForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author = u
            instance.save()
            messages.success(request, 'Article is updated successfully')
            return redirect('profile')
        return render(request, 'create.html', {"form": form})
    else:
        return redirect('login')


def getDelete(request, pid):
    if request.user.is_authenticated:
        post = get_object_or_404(article, id=pid)
        post.delete()
        messages.warning(request, 'Article is deleted successfully')
        return redirect('profile')
    else:
        return redirect('login')


def getProfile(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        author_profile = author.objects.filter(name=user.id)
        if author_profile:
            authorUser = get_object_or_404(author, name=request.user.id)
            post = article.objects.filter(article_author=authorUser.id)
            return render(request, 'logged_in_profile.html', {"post": post, "user": authorUser})
        else:
            form = createAuthor(request.POST or None, request.FILES or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.name = user
                instance.save()
                messages.success(request, 'Author profile is created successfully')
                return redirect('profile')
            return render(request, "createauthor.html", {"form": form})

    else:
        return redirect('login')


def getRegister(request):
    if request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            password = request.POST.get('password')
            password2 = request.POST.get('confirm_password')
            email = request.POST.get('email')
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email,password=password)

            user.save()
            print('user created')
            return redirect('login')
        return render(request, "register.html")


def getsample(request):

    return render(request, 'sample.html')

def getcontact(request):
    return render(request, 'contact.html')
def getabout(request):
    return render(request, 'about.html')