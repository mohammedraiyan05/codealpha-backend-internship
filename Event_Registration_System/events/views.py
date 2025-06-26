from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Event, Registration
import json

def event_list(request):
    events = list(Event.objects.all().values())
    return JsonResponse(events, safe=False)

def event_detail(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        return JsonResponse({
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "date": event.date,
            "location": event.location,
        })
    except Event.DoesNotExist:
        return JsonResponse({"error": "Event not found"}, status=404)

@csrf_exempt
def register_event(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            event = Event.objects.get(id=data['event_id'])
            reg = Registration.objects.create(
                event=event,
                name=data['name'],
                email=data['email']
            )
            return JsonResponse({"message": "Registered successfully", "reg_id": reg.id})
        except Event.DoesNotExist:
            return JsonResponse({"error": "Event does not exist"}, status=404)
    return JsonResponse({"error": "POST request required"}, status=400)

def view_registrations(request):
    regs = list(Registration.objects.all().values())
    return JsonResponse(regs, safe=False)

@csrf_exempt
def cancel_registration(request, reg_id):
    try:
        reg = Registration.objects.get(id=reg_id)
        reg.delete()
        return JsonResponse({"message": "Registration cancelled"})
    except Registration.DoesNotExist:
        return JsonResponse({"error": "Registration not found"}, status=404)
