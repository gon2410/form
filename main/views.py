import datetime
import json
import string
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from requests.exceptions import Timeout
from django.db import transaction
from .models import Group, Invited
from django.core import serializers
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_GET, require_POST
from reportlab.pdfgen.canvas import Canvas

# ===================== VALIDATION VIEWS =====================

invalid_characters = tuple(string.punctuation + string.digits + "¨" + "´" + "`")

@require_POST
def validate_input(request):
    try:
        input_data = json.loads(request.body)
        value = input_data["value"]
        if any((character in invalid_characters) for character in value):
            return JsonResponse({"error": True}, status=400)
        else:
            return JsonResponse({"success": True}, status=200)
    except Timeout:
        return JsonResponse({"error": "La conexion no es muy buena. Intente mas tarde."}, status=504)


# ===================== INDEX VIEWS =====================

@require_GET
def render_index(request):
    return render(request, "index.html")

@require_POST
def add_group(request):
    try:
        guests = json.loads(request.POST["guests"])
        mail = request.POST["mail"]
        note = request.POST["note"]
        with transaction.atomic():

            if Group.objects.filter(mail=mail).exists():
                raise Exception("Esa direccion de correo ya está registrada.")
            else:
                new_group = Group.objects.create(mail=mail, note=note)
                new_group.save()
                print(f"Created group data[mail: {mail} - note: {note}]")

            for guest in guests:
                guest_data = guests.get(guest)
                first_name = guest_data["firstname"]
                last_name = guest_data["lastname"]
                menu = guest_data["menu"]

                if len(first_name) != 0 and len(last_name) != 0:
                    new_guest = Invited.objects.create(first_name=first_name, last_name=last_name, menu=menu, group=new_group)
                    new_guest.save()
                    print(f"Created guest data[last_name: {last_name} - first_name: {first_name} - menu: {menu} - group: {mail}]")
        return JsonResponse({"success": f"Asistencia confirmada. Enviamos un email a {mail} con los detalles."}, status=200)
    except Timeout:
        return JsonResponse({"error": "La conexion no es muy buena. Intente mas tarde."}, status=504)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# ===================== ADMIN VIEWS =====================

@require_GET
def render_admin(request):
    if request.user.is_authenticated:
        groups = Group.objects.all()
        guests = Invited.objects.all()
        
        total_groups = Group.objects.all().count()
        total_guests = Invited.objects.all().count()
        sin_condicion = Invited.objects.filter(menu="sin_condicion").count()
        vegetariano = Invited.objects.filter(menu="vegetariano").count()
        vegano = Invited.objects.filter(menu="vegano").count()
        celiaco = Invited.objects.filter(menu="celiaco").count()

        download()
        return render(request, "admin.html", {"groups": groups, "guests":guests,
                                              "total_groups": total_groups, "total_guests": total_guests,
                                                "sin_condicion": sin_condicion, "vegetariano": vegetariano,
                                                "vegano": vegano, "celiaco": celiaco})
    else:
        return redirect("/login")

@require_GET
def get_guest(request, guest_id):
    try:
        guest = Invited.objects.select_related("group").get(id=guest_id)

        serialized_guest_data = {
            "id": guest.id,
            "first_name": guest.first_name,
            "last_name": guest.last_name,
            "menu": guest.menu,
            "group": {
                "id": guest.group.id,
                "mail": guest.group.mail,
                "note": guest.group.note
            }
        }

        return JsonResponse({"data": serialized_guest_data}, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@require_POST
def update_guest(request):
    try:
        id = request.POST["id"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        menu = request.POST["menu"]

        guest = Invited.objects.get(id=id)
        print(f"Guest data before update[id: {guest.id} - last_name: {guest.last_name} - first_name: {guest.first_name} - menu: {guest.menu}]")

        guest.first_name = first_name
        guest.last_name = last_name
        guest.menu = menu
        guest.save()
        print(f"Updated guest data[id: {guest.id} - last_name: {guest.last_name} - first_name: {guest.first_name} - menu: {guest.menu}]")

        return redirect("/administracion")
    except Exception:
        return JsonResponse({"error": "Algo salió mal"}, status=500)

@require_POST
def delete_guest(request, guest_id):
    try:
        guest = Invited.objects.get(id=guest_id)
        guest.delete()
        print(f"Deleted guest data[id: {guest.id} - last_name: {guest.last_name} - first_name: {guest.first_name} - menu: {guest.menu}]")
        return redirect("/administracion")
    except Exception:
        return JsonResponse({"error": "Algo salió mal"}, status=500)

@require_GET
def get_group(request, group_id):
    try:
        group_guests = Invited.objects.filter(group=group_id).values()
        return JsonResponse(list(group_guests), safe=False, status=200)
    except Exception:
        return JsonResponse({"error": "Algo salió mal"}, status=500)

@require_POST
def delete_group(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
        group.delete()
        print(f"Deleted group data[id: {group_id} - Note: {group.note}]. All the guests member of this group have been deleted.")
        return redirect("/administracion")
    except Group.DoesNotExist:
        return JsonResponse({"error": "Grupo no encontrado."}, status=404)
    except Exception:
        return JsonResponse({"error": "Algo salió mal"}, status=500)


# ===================== LOGIN VIEWS =====================

class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/administracion")
        else:
            return render(request, "login.html")

    def post(self, request):
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

@require_POST
def logout_admin(request):
    logout(request)
    return redirect("/login")

def download():
    all_guests = Invited.objects.all().order_by("last_name")

    canvas = Canvas("./static/invitados.pdf")
    canvas.drawString(230, 700, "NOMBRE DEL EVENTO")
    canvas.drawString(100, 620, "Lista de invitados")
    canvas.drawString(100, 580, "#")
    canvas.drawString(150, 580, "Nombre")
    canvas.drawString(330, 580, "Menú")
    counter = 1
    space = 550
    for guest in all_guests:
        canvas.drawString(100, space, str(counter))
        canvas.drawString(150, space, f"{guest.last_name}, {guest.first_name}")
        canvas.drawString(330, space, guest.menu)
        canvas.drawString(100, space-5, "_______________________________________________________")
        space -= 25
        counter += 1
    canvas.save()