from django.contrib import admin
from notes.models import Note, NoteUpdate

# Register your models here.
admin.site.register([Note, NoteUpdate])