from django.shortcuts import render
from django.views import View

class EstablishmentSummaryView(View):
    template_name = 'listsummary/index.html'

    def get(self, request):
        # return HttpResponseRedirect(reverse('masterlist:summary'))
        context = {'masterlist_summary_active': "active"}
        return render(request, self.template_name, context)
