from django.shortcuts import render
from .models import Curso
from . import views
from .forms import CursoFormulario, ProfesorFormulario
from .models import Curso, Profesor
# Create your views here.


from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.urls import reverse_lazy

# Para el loging

from django.contrib.auth.forms import AuthenticationForm,UserCreationForm   
from django.contrib.auth import login, authenticate

from .forms import UserCreationFormCustom

def inicio_view(request):
    return render(request, "AppCoder/inicio.html")


def cursos_view(request):
    if request.method == "GET":
        
        return render(
            request,
            "AppCoder/curso_formulario_avanzado.html",
            {"form": CursoFormulario()}
        )
    else:
        print("*" * 90)     #  Imprimimos esto para ver por consola
        print(request.POST) #  Imprimimos esto para ver por consola
        print("*" * 90)     #  Imprimimos esto para ver por consola

        modelo = Curso(curso=request.POST["curso"], camada=request.POST["camada"])
        modelo.save()
        return render(
            request,
            "AppCoder/inicio.html",
        )


def cursos_crud_read_view(request):
    cursos = Curso.objects.all()
    return render(request, "AppCoder/cursos_lista.html", {"cursos": cursos})


def profesor_view(request):
    if request.method == "GET":
        return render(
            request,
            "AppCoder/profesor_formulario_avanzado.html",
            {"form": ProfesorFormulario()}
        )
    else:
        formulario = ProfesorFormulario(request.POST)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            modelo = Profesor(
                nombre=informacion["nombre"],
                apellido=informacion["apellido"],
                email=informacion["email"],
                profesion=informacion["profesion"]
            )
            modelo.save()
        return render(
            request,
            "AppCoder/inicio.html",
        )

def profesores_crud_read_view(request):
    profesores = Profesor.objects.all()
    return render(request, "AppCoder/profesores_lista.html", {"profesores": profesores})


def profesores_crud_delete_view(request, profesor_email):
    profesor_a_eliminar = Profesor.objects.filter(email=profesor_email).first()
    profesor_a_eliminar.delete()
    return profesores_crud_read_view(request)


def profesores_crud_update_view(request, profesor_email):
    profesor = Profesor.objects.filter(email=profesor_email).first()
    if request.method == "GET":
        formulario = ProfesorFormulario(
            initial={
                "nombre": profesor.nombre,
                "apellido": profesor.apellido,
                "email": profesor.email,
                "profesion": profesor.profesion
            }
        )
        return render(request, "AppCoder/profesores_formulario_edicion.html", {"form": formulario, "profesor": profesor})
    else:
        formulario = ProfesorFormulario(request.POST)
        if formulario.is_valid():
            informacion = formulario.cleaned_data
            profesor.nombre=informacion["nombre"]
            profesor.apellido=informacion["apellido"]
            profesor.email=informacion["email"]
            profesor.profesion=informacion["profesion"]
            profesor.save()
        return profesores_crud_read_view(request)



####################  ClassBasedViews (CBV)  - Vistas basadas en Clases #########################################

class CursoListView(ListView):
    model = Curso
    context_object_name = "cursos"
    template_name = "AppCoder/cbv_curso_list.html"


class CursoDetail(DetailView):
    model = Curso
    template_name = "AppCoder/cbv_curso_detail.html"


class CursoCreateView(CreateView):
    model = Curso
    template_name = "AppCoder/cbv_curso_create.html"
    success_url = reverse_lazy("curso-list")
    fields = ["curso", "camada"]


class CursoUpdateView(UpdateView):
    model = Curso
    template_name = "AppCoder/cbv_curso_update.html"
    success_url = reverse_lazy("curso-list")
    fields = ["curso"]

class CursoDeleteView(DeleteView):
    model = Curso
    template_name = "AppCoder/cbv_curso_delete.html"
    success_url = reverse_lazy("curso-list")

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request,data=request.POST)


        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contrasenia = form.cleaned_data.get('contrasenia')

            user = authenticate(username=usuario,password=contrasenia)

            login(request,user)

            return render(request,"AppCoder/inicio.html",{"mensaje":f'Bienvenido {user.username}'})
        else:
            form = AuthenticationForm()
        return render(request,"AppCoder/login.html",{"form":form})
    

def registro(request):
    if request.method == "POST":
        form = UserCreationFormCustom(request.POST)
        if form.is_valid():

              username = form.cleaned_data["username"]
              form.save()
              return render(request,"AppCoder/inicio.html",{"mensaje":"Usuario Creado:)"})
        else:
            form = UserCreationFormCustom()

            return render(request,"AppCoder/registro.html",{"form":form})