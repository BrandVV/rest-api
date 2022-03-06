import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Permission
from global_permissions.models import GlobalPermission

@csrf_exempt
def login(request):
    username = "None"
    password = "None"
    action = "None"
    if request.method == "GET":
        htmlString = '<form method="post" action="login"> <div> <input type="text" placeholder="Username" name="username"> <input type="text" placeholder="Passwort" name="password"> <input type="text" placeholder="Action" name="action"> </div> <button type="submit">Log In</button> </form>'
        return HttpResponse(str(htmlString))
    if request.method == "POST":
        print("start")
        print(request.body)
        json_data = json.loads(request.body)
        try:
            data = json_data['username']
        except KeyError:
            print("Kein Json")
        try:
            if json_data['username'] != None and json_data['username'] != "":
                username = json_data['username']
            print(username)
            if json_data['password'] != None and json_data['password'] != "":
                password = json_data['password']
            print(password)
            if json_data['action'] != None and json_data['action'] != "":
                action = json_data['action']
            print(action)
        except Exception:
            print(Exception())

        user = authenticate(request, username=username, password=password)
        print("user: " + str(user))
        if user is not None:
            handeledAction = handlingAction(request, action, user)
            return handeledAction
        else:
            return HttpResponse('{"error": "001"}')

def createUser(name, email, passwort):
    try:
        user = User.objects.create_user(name, email, passwort) #name, passwort sind die Daten
        user.save()
    except:
        return HttpResponse('User ist fehlgeschlagen')

def handlingAction(request, action, user):
    print(user)
    if(action == "auth"):
        if user.has_perm('global_permissions.User'):
            perm = 'User'
        if user.has_perm('global_permissions.Admin'):
            perm = 'Admin'
        if perm == None or perm == "":
            return HttpResponse('{"error": "002"}')
        res_string = f'"name": "{str(user)}", "permissions": "{str(perm)}", "error": "000"'
        res = "{" + f" {res_string}" + "}"
        print(res)
        return HttpResponse(res)

#Fehlercodes: 001: Anmeldung Fehlgeschlagen | 002: Keine Berechtigungen
#Permissions: User
#user: kali, kali | Superuser - 
