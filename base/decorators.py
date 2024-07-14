from functools import wraps
from django.shortcuts import redirect

def redirect_if_authenticated(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:

                return redirect('dashboard')  # Replace 'home' with your desired redirect URL
            else:
                return redirect('index')
            
        return view_func(request, *args, **kwargs)
    return wrapper