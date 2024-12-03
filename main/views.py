import json
import string
from django.shortcuts import render, redirect
from django.http import JsonResponse
from requests.exceptions import Timeout
from django.db import transaction
from .models import Group, Invited
from django.core import serializers
from django.views import View
from django.contrib.auth import authenticate, login, logout

invalid_characters = tuple(string.digits)

#invalid_characters = tuple(string.punctuation + string.digits + "¨" + "´" + "`")

def validate_input(request):
    if request.method == "POST":
        input_data = json.loads(request.body)
        value = input_data["value"]
        if any((character in invalid_characters) for character in value):
            return JsonResponse({"error": True}, status=400)
        else:
            return JsonResponse({"success": True}, status=200)

def render_index(request):
    if request.method == "GET":
        return render(request, "index.html")


def create_group(request):
    if request.method == "POST":
        print(request.POST)
        invites = json.loads(request.POST["invites"])
        mail = request.POST["mail"]
        note = request.POST["note"]

        try:
            with transaction.atomic():

                if Group.objects.filter(mail=mail).exists():
                    raise Exception("Esa direccion de correo ya está registrada.")
                else:
                    group = Group.objects.create(mail=mail, note=note)
                    group.save()

                for invite in invites:
                    invite_data = invites.get(invite)
                    first_name = invite_data["firstname"]
                    last_name = invite_data["lastname"]
                    menu = invite_data["menu"]

                    if len(first_name) != 0 and len(last_name) != 0:
                        invited = Invited.objects.create(first_name=first_name, last_name=last_name, menu=menu, group=group)
                        invited.save()
            return JsonResponse({"success": "Asistencia confirmada."}, status=200)
        
        except Timeout:
            return JsonResponse({"error": "La conexion no es muy buena. Intente mas tarde."}, status=504)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


def render_admin(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            invites = Invited.objects.all()
            groups = Group.objects.all().values()
            
            total = Invited.objects.all().count()
            sin_condicion = Invited.objects.filter(menu="sin_condicion").count()
            vegetariano = Invited.objects.filter(menu="vegetariano").count()
            vegano = Invited.objects.filter(menu="vegano").count()
            celiaco = Invited.objects.filter(menu="celiaco").count()

            # for i in groups:
            #     print(f"Grupo de {i["mail"]}")
            #     print(Invited.objects.filter(group=i["id"]))

            return render(request, "admin.html", {"invites":invites, "groups": groups,
                                                  "total": total, "sin_condicion": sin_condicion,
                                                  "vegetariano": vegetariano, "vegano": vegano,
                                                  "celiaco": celiaco})
        else:
            return redirect("/login")

def get_invite_data(request, invited_id):
    if request.method == "GET":
        try:
            invited = Invited.objects.get(id=invited_id)
            data = serializers.serialize("json", [invited])
            serialized_data = json.loads(data)
            return JsonResponse({"data": serialized_data}, safe=False, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


def update_invite(request):
    if request.method == "POST":
        print(request.POST)
        id = request.POST["id"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        menu = request.POST["menu"]
        try:
            invited = Invited.objects.get(id=id)
            invited.first_name = first_name
            invited.last_name = last_name
            invited.menu = menu
            invited.save()
            return redirect("/administracion")
        except Exception:
            return JsonResponse({"error": "Algo salió mal"}, status=500)


def delete_invite(request, invite_id):
    if request.method == "POST":
        print(invite_id)
        try:
            invite = Invited.objects.get(id=invite_id)
            invite.delete()
            return redirect("/administracion")
        except Exception:
            return JsonResponse({"error": "Algo salió mal"}, status=500)

class Login(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        print(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"success": True}, status=200)
            else:
                raise Exception("Usuario no identificado.")
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

def logout_admin(request):
    if request.method == "POST":
        logout(request)
        return redirect("/login")