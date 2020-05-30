from django.shortcuts import render
from django.views import View
from .dashboard  import MasterlistSummary
from masterlist.models import Establishment

class DashboardView(View):
    template_name = 'dashboard/index.html'

    def get(self, request):
        context = {}
        context['masterlist_dashboard_active'] = "active"
        total_all = Establishment.objects.filter(status='Active').count()
        total_abra = MasterlistSummary.Provinces.Abra.get_total()
        total_apayao = MasterlistSummary.Provinces.Apayao.get_total()
        total_baguio =  MasterlistSummary.Provinces.Baguio.get_total()
        total_benguet = MasterlistSummary.Provinces.Benguet.get_total()
        total_ifugao = MasterlistSummary.Provinces.Ifugao.get_total()
        total_kalinga = MasterlistSummary.Provinces.Kalinga.get_total()
        total_mountainprov = MasterlistSummary.Provinces.Mountain.get_total()

        if Establishment.objects.all():
            cfrr_summary = MasterlistSummary.Centers.Cfrr()
            cdrr_summary = MasterlistSummary.Centers.Cdrr()
            ccrr_summary = MasterlistSummary.Centers.Ccrr()
            cdrrhr_summary = MasterlistSummary.Centers.Cdrrhr()

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
                                 
                                    'total_all':        total_all,
                                    'total_abra':       total_abra,
                                    'total_apayao':     total_apayao,
                                    'total_baguio':     total_baguio,
                                    'total_benguet':    total_benguet,
                                    'total_ifugao':     total_ifugao,
                                    'total_kalinga':    total_kalinga,
                                    'total_mountainprov':   total_mountainprov,
                    }

        return render(request, self.template_name, context)
