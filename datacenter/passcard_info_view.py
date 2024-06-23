from django.shortcuts import get_object_or_404, render

from datacenter.models import Passcard, Visit


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    passcard_visits = Visit.objects.filter(passcard=passcard)

    this_passcard_visits = []

    for visit in passcard_visits:
        this_passcard_visit = {
                "entered_at": visit.entered_at,
                "duration": visit.get_duration,
                "is_strange": visit.is_long,
            }
        this_passcard_visits.append(this_passcard_visit)

    context = {
        "passcard": passcard,
        "this_passcard_visits": this_passcard_visits,
    }

    return render(request, "passcard_info.html", context)
