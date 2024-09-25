from django.core.paginator import Paginator
from django.shortcuts import render
from .models import CustomUser

# Create your views here.

# Vista para listar pacientes
def listar_pacientes(request):
    # Obtener todos los pacientes de la base de datos
    Usuario_list = Usuario.objects.all()
    
    # Configurar la paginación
    paginator = Paginator(Usuario_list, 10)  # Mostrar 10 pacientes por página
    page_number = request.GET.get('page')  # Obtener el número de página de la URL
    Usuario = paginator.get_page(page_number)  # Obtener la página solicitada

    # Renderizar la plantilla con el contexto de pacientes
    return render(request, 'pacientes/listar.html', {'pacientes': Usuario})

