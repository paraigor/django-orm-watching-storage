from django.shortcuts import render

from datacenter.models import Visit


def storage_information_view(request):
    visits_active = Visit.objects.filter(leaved_at__isnull=True)
    non_closed_visits = []

    for visit in visits_active:
        non_close_visit = {
            "who_entered": visit.passcard.owner_name,
            "entered_at": visit.entered_at,
            "duration": visit.get_duration,
        }
        non_closed_visits.append(non_close_visit)

    context = {
        "non_closed_visits": non_closed_visits,
    }
    return render(request, "storage_information.html", context)
