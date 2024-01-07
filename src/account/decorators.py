from django.http import HttpResponse
from django.shortcuts import redirect

#from panel.models import Application

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('panel:home')
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func

def allowed_users(allowed_groups=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            if request.user.groups.exists():
                for g in request.user.groups.all():
                    if g.name in allowed_groups:
                        return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('Bu sayfayı görüntülemek için yetkili değilsiniz.') #TODO 403
            
        return wrapper_func
    return decorator

"""
def allow_if_approved(view_func):
    def wrapper_func(request, *args, **kwargs):

        if request.user.is_superuser or request.user.is_staff or request.user.is_operation:
            return view_func(request, *args, **kwargs)
        
        try:
            application = Application.objects.get(owner=request.user)
        except Application.DoesNotExist:
            return redirect('panel:apply', 1)
        
        if application.isApproved:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('panel:apply', 1)
        
    return wrapper_func
"""