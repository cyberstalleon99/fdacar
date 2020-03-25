from django.shortcuts import render
from django.views import View
from . import dashboard
from masterlist.models import Establishment

class DashboardView(View):
    template_name = 'dashboard/index.html'

    def get(self, request):
        # return HttpResponseRedirect(reverse('masterlist:summary'))
        cfrr_summary = dashboard.MasterlistSummary.CFRR('CFRR')
        cdrr_summary = dashboard.MasterlistSummary.CDRR('CDRR')
        ccrr_summary = dashboard.MasterlistSummary.CCRR('CCRR')
        cdrrhr_summary = dashboard.MasterlistSummary.CDRRHR('CDRRHR')

        context = {
                    'masterlist_dashboard_active': "active",
                    'cfrr': {'total':               cfrr_summary.get_total(),
                             'total_mfg':           cfrr_summary.get_total_mfg(),
                             'total_trader':        cfrr_summary.get_total_trader(),
                             'total_wholesaler':    cfrr_summary.get_total_wholesaler(),
                             'total_importer':      cfrr_summary.get_total_importer(),
                             'total_exporter':      cfrr_summary.get_total_exporter()},

                    'cdrr': {'total':               cdrr_summary.get_total(),
                             'total_hp':            cdrr_summary.get_total_hp(),
                             'total_ds':            cdrr_summary.get_total_ds(),
                             'total_mfg':           cdrr_summary.get_total_mfg(),
                             'total_trader':        cdrr_summary.get_total_trader(),
                             'total_wholesaler':    cdrr_summary.get_total_wholesaler(),
                             'total_importer':      cdrr_summary.get_total_importer(),
                             'total_exporter':      cdrr_summary.get_total_exporter()},

                    'ccrr': {'total':               ccrr_summary.get_total(),
                             'total_mfg':           ccrr_summary.get_total_mfg(),
                             'total_trader':        ccrr_summary.get_total_trader(),
                             'total_wholesaler':    ccrr_summary.get_total_wholesaler(),
                             'total_importer':      ccrr_summary.get_total_importer(),
                             'total_exporter':      ccrr_summary.get_total_exporter()},

                    'cdrrhr': {'total':             cdrrhr_summary.get_total(),
                             'total_xray':          cdrrhr_summary.get_total_xray(),
                             'total_mfg':           cdrrhr_summary.get_total_mfg(),
                             'total_trader':        cdrrhr_summary.get_total_trader(),
                             'total_wholesaler':    cdrrhr_summary.get_total_wholesaler(),
                             'total_importer':      cdrrhr_summary.get_total_importer(),
                             'total_exporter':      cdrrhr_summary.get_total_exporter()},
                }

        return render(request, self.template_name, context)
