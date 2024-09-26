from django.core.paginator import Paginator
from django.shortcuts import render
from .models import CustomUser, CustomUserManager

from django.core.paginator import Paginator
from django.shortcuts import render
from .models import CustomUser

# Vista para listar pacientes
def listar_pacientes(request):
    # Obtener todos los pacientes de la base de datos
    custom_users = CustomUser.objects.all()
    
    # Configurar la paginación
    paginator = Paginator(custom_users, 10)  # Mostrar 10 pacientes por página
    page_number = request.GET.get('page')  # Obtener el número de página de la URL
    paginated_custom_users = paginator.get_page(page_number)  # Obtener la página solicitada

    # Renderizar la plantilla con el contexto de pacientes
    return render(request, 'pacientes/listar.html', {'custom_users': paginated_custom_users})


