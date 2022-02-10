from pyexpat import model
from django.shortcuts import get_object_or_404, redirect, render,HttpResponseRedirect
from django.http import Http404, JsonResponse
from django.urls import reverse_lazy,reverse
from django.views.generic import UpdateView,DeleteView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser,FormParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .forms import taskForm
from .models import Task
from .serializers import *
import datetime, requests

base_url = 'http://127.0.0.1:8000/'


@csrf_exempt
def json_list(request):
	if request.method == 'GET':
		tasks=Task.objects.all()
		serializer = taskSerializer(tasks, many=True)
		return JsonResponse({'tasks':serializer.data}, safe=False)

	elif request.method=='POST':
		data=JSONParser().parse(request)
		serializer = taskSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse("Added Successfully!", safe=False)
		return JsonResponse("Failed to add!", safe=False)


@csrf_exempt
def task_list(request):
    data={'task_list':Task.objects.all()}
    return render(request, 'tasks-list.html',data)

def task_create(request, id=0):
    if request.method == "GET":
        if id == 0:
            form=taskForm()
        else:
            task=Task.objects.get(taskId=id)
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
        return redirect('/tasks/')

def detail_view(request, id):
    task ={}
    task["data"] = Task.objects.get(taskId = id)
    return render(request, "task_update.html", task)

def task_update(request, id):
    context ={}
    task=Task.objects.get(pk=id)
    form = taskForm(request.POST or None, instance = task)
    if form.is_valid():
        form.save()
        return redirect('/tasks/')
    context["form"] = form
    return render(request, "tasks.html", context)

def task_delete(request, id):
    context ={}
    task=Task.objects.get(pk=id)
    if request.method == 'POST':
        task.delete()
        return redirect('/tasks/')
    return render(request, "delete-task.html", context)


def today_task(request):
    today=datetime.date.today()
    data={'task_list':Task.objects.all().filter(date=today)}
    return render(request, 'tasks-list.html',data)

#def today_task(request):
    today= Task.objects.filter(date=datetime.date.today())
    serializer = taskSerializer(today, many=True)
    today = {'today': serializer.data}
    return JsonResponse(today, status=200)

#class updateTask(UpdateView):
    model=Task
    template_name='task_update.html'
    fields=['name','description']
    def get_success_url(self):
        return reverse('task_list',)


@csrf_exempt
def create(request):
    context ={}
    req = requests.get(url=base_url)
    if request.method == 'POST':
        tasks = FormParser().parse(request)
        tasks = JSONRenderer().render(tasks)
        requests.post(url=base_url + 'tasks/create', data=tasks)
        return redirect('home')
    return render(request, 'tasks-list.html', context)


def get_all_tasks(request):
    context ={}
    req = requests.get(url=base_url)
    req.json()
    return render(request, 'tasks-list.html', context)

def get_today_tasks(request):
    context ={}
    req = requests.get(url=base_url + 'tasks/today' )
    req.json()
    return render(request, 'tasks-list.html',context)

def delete_task(request, pk):
    requests.delete(url=f'{base_url}tasks/{pk}/delete/')
    return redirect('task_list')