from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import ToDo
from .forms import ToDoForm, ToDoEditForm
from django.utils import timezone
# Create your views here.

def signup_user(requests):
	if requests.method=="GET":
		return render(requests, 'todo/signup_user.html', {'form': UserCreationForm()})
	else:
		if requests.POST.get('password1') == requests.POST.get('password2'):
			try:
				user =  User.objects.create_user(
							username=requests.POST.get('username'),
							password=requests.POST.get('password1')
							)
				user.save()
				login(requests, user)
				return redirect('current_todos')
			except IntegrityError:
				return render(requests, 'todo/signup_user.html', {'form': UserCreationForm(), 'error': "Username already exist, Please retry with another username !!!!"})

		else:
			return render(requests, 'todo/signup_user.html', {'form': UserCreationForm(), 'error': "Both passwords fields should be same !!!!"})


def login_user(requests):
	if requests.method=="GET":
		return render(requests, 'todo/login_user.html', {'form': AuthenticationForm()})
	else:

		user = authenticate(
				requests, 
				username=requests.POST.get('username'),
				password=requests.POST.get('password')
				)

		if not user:
			return render(requests, 'todo/login_user.html', {'form': AuthenticationForm(), 'error': 'user not found !!!'})
		else:
			login(requests, user)
			return redirect('current_todos')			



def home(requests):
	return render(requests, 'todo/home.html')

@login_required
def logout_user(requests):
	if requests.method == 'POST':

		logout(requests)
		return redirect('home')


@login_required
def current_todos(requests):
	current_user = requests.user
	todo_list = ToDo.objects.filter(user=current_user, completed__isnull=True)
	return render(requests, 'todo/current_todos.html', {'todo_list':todo_list})


@login_required
def add_todo(requests):
	if requests.method=="POST":
		form = ToDoForm(requests.POST)
		if form.is_valid():
			todo = form.save(commit=False)
			todo.user = requests.user
			todo.save()
			return redirect('current_todos')
		else:
			return render(requests, 'todo/add_todo.html', {'form': form, 'error': 'Bad info'}) 
	else:
		return render(requests, 'todo/add_todo.html', {'form': ToDoForm()})


@login_required
def edit_todo(requests, id):
	obj = get_object_or_404(ToDo, pk=id, user=requests.user)
	if requests.method=="POST":
		form = ToDoEditForm(requests.POST,  instance=obj)
		if form.is_valid():
			todo = form.save()
			return redirect('current_todos')
		else:
			return render(requests, 'todo/add_todo.html', {'form': form, 'todo':obj, 'error': 'Bad info'}) 

	else:
		form = ToDoEditForm(instance=obj)
		return render(requests, 'todo/add_todo.html', {'form': form, 'todo': obj })


@login_required
def mark_complete(requests, id):
	todo = get_object_or_404(ToDo, pk=id, user=requests.user)
	if requests.method=="POST":
		todo.completed = timezone.now()
		todo.save()
		return redirect('current_todos')
	else:
		return render(requests, 'todo/add_todo.html', {'todo': todo, 'error': 'Bad info'}) 


@login_required
def show_completed(requests):
	todos = ToDo.objects.filter(completed__isnull=False, user=requests.user)
	return render(requests, 'todo/show_completed.html', {'todo_list': todos})


@login_required
def delete_todo(requests, id):
	todo = get_object_or_404(ToDo, pk=id, user=requests.user)
	if requests.method=="POST":
		todo.delete()
		return redirect('current_todos')
	else:
		form = ToDoEditForm(requests.POST,  instance=todo)
		return render(requests, 'todo/add_todo.html', {'todo': todo, 'form': form, 'error': 'Somthing bad happened'}) 

