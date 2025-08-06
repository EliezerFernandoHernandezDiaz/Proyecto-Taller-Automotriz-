"""
URL configuration for login project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from login import settings # Importando la configuración del proyecto
from django.conf .urls.static import static # Importando static para servir archivos estáticos en modo DEBUG

urlpatterns = [
     path('admin/', admin.site.urls),
     path('',include ('accounts.urls')),

]
#se agrega la parte para servir archivos media 
#esta parte es muy importante para que las imagenes se puedan mostrar en el navegador
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
