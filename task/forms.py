from django import forms
from .models import Status, Tag, Task, Priority
from account.models import User
from django.utils.timezone import now

class TaskForm(forms.Form):
    name = forms.CharField(max_length=150, label="Tarea")
    status = forms.ChoiceField()
    tag = forms.ChoiceField()
    description = forms.CharField(max_length=500, label="Descripción", required=False)
    expire_date = forms.DateField(label="Fecha límite", widget=forms.DateInput(attrs={'type': 'date'}),initial=now().today())
    priority = forms.ChoiceField(label="Prioridad", choices=[('alta', 'Alta'), ('baja', 'Baja')])
    assigned_to = forms.ModelChoiceField(queryset=User.objects.all(), label="Asignar a")
    
    def __init__(self,*args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields["status"].choices=[(obj.id,obj.status) for obj in Status.objects.all()]
        self.fields["tag"].choices=[(obj.id,obj.name) for obj in Tag.objects.all()]

class TaskModelForm(forms.ModelForm):
    expire_date = forms.DateField(label="Fecha límite", widget=forms.DateInput(attrs={'type': 'date'}), initial=now().today())
    priority = forms.ModelChoiceField(queryset=Priority.objects.all(), label="Prioridad")
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Asignar a")

    class Meta:
        model = Task
        fields = ['name', 'status', 'tag', 'description', 'expire_date', 'priority', 'user']

    def __init__(self, *args, **kwargs):
        super(TaskModelForm, self).__init__(*args, **kwargs)
        self.fields["status"].choices = [(obj.id, obj.status) for obj in Status.objects.all()]
        self.fields["tag"].choices = [(obj.id, obj.name) for obj in Tag.objects.all()]