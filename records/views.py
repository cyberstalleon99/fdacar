from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from masterlist.models import Establishment
from .foldergenerator import generate_folder
from .models import Record
from django.http import HttpResponseRedirect

def create_folder_view(request):
    est = get_object_or_404(Establishment, pk=request.POST.get('est_id', False))
    new_folder = generate_folder(est)
    # new_record = Record.objects.create(establishment=est, folder_id=new_folder)
    # new_record.save()

    return HttpResponseRedirect(reverse('masterlist:est-detail', kwargs={'id': est.id}))


