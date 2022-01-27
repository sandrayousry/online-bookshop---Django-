from django.shortcuts import redirect
# take user request with all arguments and check if he is_authenticated redirect to home 
# else redirect wherevre he wants
def notloggedUsers(view_func):
    def wrapper_func(request, *args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args,**kwargs)  
    return wrapper_func         

# diffrantiate betw. admin and users
  # lazm ykon aluser gwa group either admin or customer
def allowedUsers(allowedGroups=[]):
    def decorator(view_func):
        def wrapper_func(request, *args,**kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowedGroups:
                return view_func(request, *args,**kwargs)  
            else:
                return redirect('userProfile')    
        return wrapper_func
    return decorator


def forAdmins(view_func):
    def wrapper_func(request, *args,**kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'admin':
            return view_func(request, *args,**kwargs)  
        if group == 'customer':
            return redirect('userProfile')    
    return wrapper_func
 