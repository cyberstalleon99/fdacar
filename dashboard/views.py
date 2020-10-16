from django.shortcuts import render
from django.views import View
from .dashboard  import MasterlistSummary
from masterlist.models import Establishment
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardView(LoginRequiredMixin, View):
    template_name = 'dashboard/index.html'

    def get(self, request):
        context = {}
        context['masterlist_dashboard_active'] = "active"
        total_all = Establishment.objects.filter(status='Active').count()
        total_abra = MasterlistSummary.Provinces.Abra.get_total()
        total_apayao = MasterlistSummary.Provinces.Apayao.get_total()
        total_baguio =  MasterlistSummary.Provinces.Baguio_City.get_total()
        total_benguet = MasterlistSummary.Provinces.Benguet.get_total()
        total_ifugao = MasterlistSummary.Provinces.Ifugao.get_total()
        total_kalinga = MasterlistSummary.Provinces.Kalinga.get_total()
        total_mountainprov = MasterlistSummary.Provinces.Mountain_Province.get_total()

        if Establishment.objects.all():
            cfrr_summary = MasterlistSummary.Centers.Cfrr()
            cdrr_summary = MasterlistSummary.Centers.Cdrr()
            ccrr_summary = MasterlistSummary.Centers.Ccrr()
            cdrrhr_summary = MasterlistSummary.Centers.Cdrrhr()

            temp = MasterlistSummary.Provinces
            provinces = []

            for attr, value in temp.__dict__.items():
                if not attr.startswith('__'):
                    provinces.append([attr, value])

            context = {
                        'masterlist_dashboard_active': "active",
                        'cfrr': {'total':               cfrr_summary.get_total(),
                                 'total_m_p_r_t':       cfrr_summary.get_total_m_p_r_t(),
                                 'total_dist':          cfrr_summary.get_total_dist()

                        },

                        'cdrr': {'total':               cdrr_summary.get_total(),
                                 'total_ds_ronpd':      cdrr_summary.get_total_ds_ronpd(),
                                 'total_hp':            cdrr_summary.get_total_hp(),
                                 'total_dist':          cdrr_summary.get_total_dist()
                        },

                        'ccrr': {'total':               ccrr_summary.get_total(),
                                 'total_m_p_r_t':       ccrr_summary.get_total_m_p_r_t(),
                                 'total_dist':          ccrr_summary.get_total_dist()
                        },

                        'cdrrhr': {'total':             cdrrhr_summary.get_total(),
                                 'total_xray':          cdrrhr_summary.get_total_xray(),
                                 'total_m_p_r_t':       cdrrhr_summary.get_total_m_p_r_t(),
                                 'total_dist':          cdrrhr_summary.get_total_dist()
                        },

                        'total_all':        total_all,
                        'total_abra':       total_abra,
                        'total_apayao':     total_apayao,
                        'total_baguio':     total_baguio,
                        'total_benguet':    total_benguet,
                        'total_ifugao':     total_ifugao,
                        'total_kalinga':    total_kalinga,
                        'total_mountainprov':   total_mountainprov,

                        'provinces': provinces
                    }

        return render(request, self.template_name, context)
