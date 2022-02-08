from pyexpat import model
from django.shortcuts import redirect, render
from django.http.response import JsonResponse
from django.urls import reverse_lazy,reverse
from .forms import taskForm
from .models import Task
from .serializers import *
import datetime
from django.views.generic import UpdateView,DeleteView



def task_list(request):
    data={'task_list':Task.objects.all()}
    return render(request, 'tasks-list.html',data)


def task_create(request, id=0):
    if request.method == "GET":
        if id == 0:
            form=taskForm()
        else:
            task=Task.objects.get(taskId=id)
            #data=Task.objects.filter(taskId=id).first()
            form=taskForm(instance=task)
        form = taskForm()
        return render(request, 'tasks.html',{'form':form})
    else:
        if id == 0:
            form = taskForm(request.POST)
        else:
            task=Task.objects.get(pk=id)
            form = taskForm(request.POST,instance= task)
        if form.is_valid():
            form.save()
        return redirect('/tasks')


def task_delete(request, id):
    task=Task.objects.filter(pk=id).delete()
    #task.delete()
    return redirect('/tasks')


def today_task(request):
    today=datetime.date.today()
    data={'task_list':Task.objects.all().filter(date=today)}
    return render(request, 'tasks-list.html',data)

class updateTask(UpdateView):
    model=Task
    template_name='task_update.html'
    fields=['name','description']
    def get_success_url(self):
        return reverse('task_list',)
