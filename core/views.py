from django.views import View
from django.shortcuts import render, redirect
from .forms import CreateForm


class CreateCampaignView(View):
    template_name = 'create_campaign.html'

    def get(self, request):
        return render(request, self.template_name, status=200)

    def post(self, request):
        form = CreateForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/admin/pages/{0}/'.format(9))

