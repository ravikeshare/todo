from django.forms import ModelForm
from .models import ToDo


class ToDoForm(ModelForm):
    class Meta:
        model = ToDo
        fields = ('title','memo','imprtant', )

class ToDoEditForm(ModelForm):
    class Meta:
        model = ToDo
        # exclude = ('user', 'created', 'completed',)
        fields = ('title','memo','imprtant', )