from django.core.checks import messages
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from .forms import UserSignupForm, LogForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import os
import uuid
import boto3
from .models import Comic, Log, Funko, Photo

def home(request):
    return render(request,'home.html')

def about(request):
    return render(request, 'about.html')

def comics_index(request):
    comics = Comic.objects.all()
    return render(request, 'comics/index.html', {'comics':comics})

@login_required
def comics_detail(request, comic_id):
    comic = Comic.objects.get(id = comic_id)
    return render(request, 'comics/detail.html', {'comic': comic})

class ComicCreate(LoginRequiredMixin,CreateView):
    model = Comic
    fields = ['title','author','genre','img','published']
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

    success_url = '/comics/'

class ComicUpdate(LoginRequiredMixin,UpdateView):
    model = Comic
    fields = ['title','author','genre','published']

class ComicDelete(LoginRequiredMixin,DeleteView):
    model = Comic
    success_url = '/comics/'

@login_required
def comics_detail(request, comic_id):
    comic = Comic.objects.get(id=comic_id)
    funkos_related = Funko.objects.exclude(id__in = comic.funkos.all().values_list('id'))
    log_form = LogForm()
    return render(request, 'comics/detail.html', {
        'comic':comic, 'log_form': log_form,
        'funkos':funkos_related
    })

@login_required
def add_log(request, comic_id):
    form = LogForm(request.POST)
    if form.is_valid():
        new_log = form.save(commit=False)
        new_log.comic_id = comic_id
        new_log.save()
    return redirect('detail', comic_id = comic_id)

class FunkoList(LoginRequiredMixin,ListView):
    model = Funko

class FunkoDetail(LoginRequiredMixin,DetailView):
    model = Funko

class FunkoCreate(LoginRequiredMixin,CreateView):
    model = Funko
    fields = ['name','img','price','description']

class FunkoUpdate(LoginRequiredMixin,UpdateView):
    model = Funko
    fields = ['name','img','price','description']

class FunkoDelete(LoginRequiredMixin,DeleteView):
    model = Funko
    success_url = "/funkos"

@login_required
def assoc_funko(request, comic_id, funko_id):
    Comic.objects.get(id = comic_id).funkos.add(funko_id)
    return redirect('detail', comic_id=comic_id)

@login_required
def add_photo(request, comic_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url,comic_id=comic_id)
        except:
            print('An error occurred uploading file to S3')
        return redirect('detail', comic_id=comic_id)

def signup(request):
    error_message=''
    if request.method =='POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            ## cleaned_data will always contain a key for fields defined in the Form.
            ## returns a dictionary of validated form input fields and their values
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            user = form.save()
            login(request,user)
            return redirect('home')
        else:
            error_message = 'invalid signup - try again'

    form = UserSignupForm()
    context = {'form':form, 'error_message':error_message}
    return render(request, 'registration/signup.html',context)

@login_required
def profile(request):
    if request.method =='POST':
        ##https://docs.djangoproject.com/en/3.2/intro/tutorial04/
        ## request.POST (call) is a dictionary-like object that allows the user to access submitted data by key name. 
        ## Two seperate variables grabbing the forms and having the arguments be the call and instance of the accessed user model object/profile
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            ## https://docs.djangoproject.com/en/3.2/ref/contrib/messages/
            ## message framework, allows messages to be display filtered by templates or displayed differently in views.
            ## operating like a one-time notification message also known as 'flash messages'
            messages.success(request, f'Account updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'registration/profile.html', context)
