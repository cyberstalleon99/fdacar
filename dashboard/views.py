from django.shortcuts import render
from django.views import View

class DashboardView(View):
    template_name = 'dashboard/index.html'

    def get(self, request):
        # return HttpResponseRedirect(reverse('masterlist:summary'))
        context = {'masterlist_dashboard_active': "active"}
        return render(request, self.template_name, context)
