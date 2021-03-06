"""todo_list URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    # Auth
    path('signup/', views.signup_user, name='signup_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),

    # Todos
    path('current_todos/', views.current_todos, name='current_todos'),
    path('add_todo/', views.add_todo, name='add_todo'),
    path('todo/<int:id>/', views.edit_todo, name='edit_todo'),
    path('todo/<int:id>/mark_complete/', views.mark_complete, name='mark_complete'),
    path('show_completed/', views.show_completed, name='show_completed'),
    path('todo/<int:id>/delete_todo/', views.delete_todo, name='delete_todo'),

]
