from django.urls import path, include
from .views import *

urlpatterns = [
    path('', task_list,name="task_list"),
    #path('<int:pk>/update/',updateTask.as_view(),name='task_update'),
    path('<int:id>/update',task_update,name='task_update'),
    path('<int:id>/delete',task_delete ,name='task_delete'),
    path('create', task_create,name="task_insert"),
    path('today', today_task,name="today_task"),


]