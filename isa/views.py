from django.http import HttpResponse, Http404, JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist

from .models import *

def course_detail(request, mne, num):
    if request.method == 'GET':
        try:
            target_course = Course.objects.get(
                mnemonic=mne.upper(),
                number=num,
            )
        except ObjectDoesNotExist:
            raise Http404('Class does not exist')

        data = model_to_dict(target_course)
        return JsonResponse(data)
    else:
        raise Http404('Not a GET request')
