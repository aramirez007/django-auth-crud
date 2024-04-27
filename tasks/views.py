from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Tarea
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, "home.html")


def singup(request):
    if request.method == 'GET':
        return render(request, 'singup.html', {
            "form": UserCreationForm 
        })
    
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                                            username=request.POST['username'],
                                            password=request.POST['password1']
                                        )
                user.save()
                login(request, user)
                return redirect('tareas') #Toma el name de las urls que esta en el archivo urls.py
            except IntegrityError:
                return render(request, 'singup.html', {
                                "form": UserCreationForm,
                                "error": "El usuario ya existe."
                            })
            

        return render(request, 'singup.html', {
                        "form": UserCreationForm,
                        "error": "Las contraseñas no coinciden."
                    })
    
@login_required
def tareas(request):
    las_tareas = Tarea.objects.filter(usuario = request.user, fechaCompletado__isnull = True)

    return render(request, "tareas.html", {"tareas": las_tareas})

@login_required
def tareas_completadas(request):
    tareas = Tarea.objects.filter(usuario = request.user, fechaCompletado__isnull = False).order_by('-fechaCompletado')
    return render(request, 'tareas.html', {'tareas': tareas})


@login_required
def crear_tarea(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {"form": TaskForm})
    
    else:
        try:
            form = TaskForm(request.POST)
            nueva_tarea = form.save(commit=False)
            nueva_tarea.usuario = request.user
            nueva_tarea.save()
            
            return redirect('tareas')
        
        except ValueError:
            return render(request, 'create_task.html', {
                    "form": TaskForm,
                    'error': 'Por favor ingrese datos validos.'
                })


@login_required
def detalle_tarea(request, tarea_id):
    if request.method == 'GET':
        tarea = get_object_or_404(Tarea, pk = tarea_id, usuario = request.user)
        form = TaskForm(instance=tarea)

        return render(request, 'tarea_detalle.html', {"tarea": tarea, "form": form})
    
    else:
        try:
            tarea = get_object_or_404(Tarea, pk = tarea_id, usuario = request.user)
            form = TaskForm(request.POST, instance=tarea)
            form.save()

            return redirect('tareas')
        except ValueError:
            return render(request, 'tarea_detalle.html', {"tarea": tarea, "form": form, 
                                                          'error': 'Error al actualizar la tarea.'})


@login_required
def tarea_completada(request, tarea_id):
    tarea = get_object_or_404(Tarea, pk = tarea_id, usuario = request.user)

    if request.method == "POST":
        tarea.fechaCompletado = timezone.now()
        tarea.save()

        return redirect("tareas")


@login_required
def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, pk = tarea_id, usuario = request.user)

    if request.method == "POST":
        tarea.delete()
        return redirect("tareas")


@login_required
def singout(request):
    logout(request)

    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm})
    
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        
        if user is None:
            return render(request, 'signin.html', {'form': AuthenticationForm, 
                                                   'error': 'Usuario o contraseña incorrecto.'})
        
        else:
            login(request, user)
            return redirect('tareas')
        
       

