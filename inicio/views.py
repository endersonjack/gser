from django.shortcuts import render

# Create your views here.

def inicio_sistema(request, template_name = 'inicio/inicio_sistema.html'):

    if request.method == 'GET':
        context = {

            
        }

    return render(request, template_name , context)