"""
URL configuration for NoteTakingApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from notes.views import (
    signup, 
    login_view, 
    create_note, 
    get_note, 
    share_note, 
    update_note, 
    get_note_history
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup', signup, name='signup'),
    path('login', login_view, name='login'),
    path('notes/create', create_note, name='create_note'),
    path('notes/<int:note_id>', get_note, name='get_note'),
    path('notes/share', share_note, name='share_note'),
    path('notes/<int:note_id>/update', update_note, name='update_note'),
    path('notes/<int:note_id>/history', get_note_history, name='get_note_history'),
]
