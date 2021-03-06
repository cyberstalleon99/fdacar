from django.shortcuts import render
from django.views import View
from .dashboard  import MasterlistSummary
from masterlist.models import Establishment
from pms.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from appsreceived.models import Application
from pli.models import Pli
from accounts.models import Profile

def get_inspector_data(inspector):
    today = datetime.date.today()
    today_year = today.year
    today_month = today.month
    
    appsreceived_count = Application.objects.filter(group__year=today_year, group__month=today_month, inspection__est_inspectors__inspector=inspector.user).count()
    pli_count = Pli.objects.filter(group__year=today_year, group__month=today_month, inspection__est_inspectors__inspector=inspector.user).count()
    product_count = Product.objects.filter(group__year=today_year, group__month=today_month, product_inspectors__product_inspector=inspector.user).count()
    
    appsreceived_yearly_count = Application.objects.filter(group__year=today_year, inspection__est_inspectors__inspector=inspector.user).count()
    pli_yearly_count = Pli.objects.filter(group__year=today_year, inspection__est_inspectors__inspector=inspector.user).count()
    product_yearly_count = Product.objects.filter(group__year=today_year, product_inspectors__product_inspector=inspector.user).count()

    data = {
        'inspector': inspector.user,
        # 'img': inspector.img.url,
        'appsreceived': appsreceived_count,
        'pli':  pli_count,
        'products': product_count,

        'appsreceived_yearly': appsreceived_yearly_count,
        'pli_yearly':  pli_yearly_count,
        'products_yearly': product_yearly_count,
    }
    try:
        inspector.img.url
    except:
        data['img'] = "/static/darkadmin/img/user-icon.png"
    else:
        data['img'] = inspector.img.url
        

    return data

class DashboardView(LoginRequiredMixin, View):
    template_name = 'dashboard/index.html'

    def get(self, request):

        context = {}
        context['masterlist_dashboard_active'] = "active"
        total_all = Establishment.objects.filter(status='Active').count()

        if Establishment.objects.all():
            cfrr_summary = MasterlistSummary.Centers.Cfrr()
            cdrr_summary = MasterlistSummary.Centers.Cdrr()
            ccrr_summary = MasterlistSummary.Centers.Ccrr()
            cdrrhr_summary = MasterlistSummary.Centers.Cdrrhr()
            pendings_summary = MasterlistSummary.Pendings()

            temp = MasterlistSummary.Provinces
            provinces = []

            for attr, value in temp.__dict__.items():
                if not attr.startswith('__'):
                    provinces.append([attr, value])

            context = {
                        'masterlist_dashboard_active': "active",
                        'total_all':        total_all,
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
                        'pendings': {
                            'expired': pendings_summary.get_total_expired(),
                            'awaiting_results': pendings_summary.get_total_awaiting_result(),
                            'awaiting_closure': pendings_summary.get_total_awaiting_closure(),
                            'awaiting_capa': pendings_summary.get_total_awaiting_capa(),
                        },
                        'provinces': provinces
                    }

        today = datetime.date.today()
        inspectors = Profile.objects.filter(designation__name="FDRO II")
        context['inspectors'] = list(map(get_inspector_data, inspectors))
        context['curr_date'] = today

        # Data for Charts
        context['chart_labels'] = ['DS/RONPD', 'DD', 'HP', 'FM/P/R/T', 'FD', 'MM/P/R/T', 'MD', 'XRay', 'CM/P/R/T', 'CD']
        province_totals = {}
        provinces_data = {}
        # print(provinces)
        for prov in provinces:
            provinces_data[prov[0]] = [prov[1].cdrr().get_total_ds_ronpd(), prov[1].cdrr().get_total_dist(), prov[1].cdrr().get_total_hp(), 
                                prov[1].cfrr().get_total_m_p_r_t(), prov[1].cfrr().get_total_dist(), prov[1].cdrrhr().get_total_m_p_r_t(), prov[1].cdrrhr().get_total_dist(), 
                                prov[1].cdrrhr().get_total_xray(), prov[1].ccrr().get_total_m_p_r_t(), prov[1].ccrr().get_total_dist()]
            province_totals[prov[0]] = prov[1].get_total()
        context['province_totals'] = province_totals
        context['provinces_data'] = provinces_data
        context['masterlist_data'] = [cdrr_summary.get_total_ds_ronpd(), cdrr_summary.get_total_dist(), cdrr_summary.get_total_hp(), 
                                      cfrr_summary.get_total_m_p_r_t(), cfrr_summary.get_total_dist(),
                                      cdrrhr_summary.get_total_m_p_r_t(), cdrrhr_summary.get_total_dist(), cdrrhr_summary.get_total_xray(), 
                                      ccrr_summary.get_total_m_p_r_t(), ccrr_summary.get_total_dist()]

        # context['provinces'] = 
        return render(request, self.template_name, context)
