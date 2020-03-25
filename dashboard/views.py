from django.shortcuts import render
from django.views import View
from . import dashboard
from masterlist.models import Establishment

class DashboardView(View):
    template_name = 'dashboard/index.html'

    def get(self, request):
        # return HttpResponseRedirect(reverse('masterlist:summary'))
        food_summary = dashboard.MasterlistSummary.Food('CFRR')
        drug_summary = dashboard.MasterlistSummary.Drug('CDRR')
        context = {
                    'masterlist_dashboard_active': "active",
                    'cfrr': {'total':               food_summary.get_total(),
                             'total_mfg':           food_summary.get_total_mfg(),
                             'total_trader':        food_summary.get_total_trader(),
                             'total_wholesaler':    food_summary.get_total_wholesaler(),
                             'total_importer':      food_summary.get_total_importer(),
                             'total_exporter':      food_summary.get_total_exporter()},

                    'cdrr': {'total':               drug_summary.get_total(),
                             'total_hp':            drug_summary.get_total_hp(),
                             'total_ds':            drug_summary.get_total_ds(),
                             'total_mfg':           drug_summary.get_total_mfg(),
                             'total_trader':        drug_summary.get_total_trader(),
                             'total_wholesaler':    drug_summary.get_total_wholesaler(),
                             'total_importer':      drug_summary.get_total_importer(),
                             'total_exporter':      drug_summary.get_total_exporter()},
                  }
                  
        return render(request, self.template_name, context)
