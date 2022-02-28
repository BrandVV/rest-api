from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Permission
from global_permissions.models import GlobalPermission

@csrf_exempt
def login(request):
    if request.method == "GET":
        htmlString = '<form method="post" action="login"> <div> <input type="text" placeholder="Username" name="username"> <input type="text" placeholder="Passwort" name="password"> <input type="text" placeholder="Action" name="action"> </div> <button type="submit">Log In</button> </form>'
        return HttpResponse(str(htmlString))
    if request.method == "POST":
        print("start")
        try:
            username = request.POST['username']
            print(username)
            password = request.POST['password']
            print(password)
            action = request.POST['action']
            print(action)
        except Exception:
            print(Exception())

        if username == None or username == "":
            return HttpResponse("ungültiger nutzername")
        if password == None or password == "":
            return HttpResponse("ungültiges Passwort")

        user = authenticate(request, username=username, password=password)
        print("user: " + str(user))
        if user is not None:
            handeledAction = handlingAction(request, action, user)
            return handeledAction
        else:
            return HttpResponse("001")

def createUser(name, email, passwort):
    try:
        user = User.objects.create_user(name, email, passwort) #name, passwort sind die Daten
        user.save()
    except:
        return HttpResponse('User ist fehlgeschlagen')

def handlingAction(request, action, user):
    print(user)
    loginUser = False
    if(action == "auth"):
        if user.has_perm('global_permissions.User'):
            perm = 'User'
        if user.has_perm('global_permissions.Admin'):
            perm = 'Admin'
        if perm == None or perm == "":
            return HttpResponse('002')
        res_string = f'"name": "{str(user)}", "permissions": "{str(perm)}"'
        res = f"{ res_string }"
        print(res)
        return HttpResponse(res)

#Fehlercodes: 001: Anmeldung Fehlgeschlagen | 002: Keine Berechtigungen
#Permissions: User
#user: kali, kali | Superuser - 
