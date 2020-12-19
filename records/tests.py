from django.test import TestCase

from .models import *
from masterlist.models import *
from .foldergenerator import get_last_number

est = Establishment.objects.filter(ltos__lto_number='LTO-3000003010427')
get_last_number(est)