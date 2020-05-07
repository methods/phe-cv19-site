from django.views import View
from django.shortcuts import render


class CreateCampaignView(View):

    def get(self, request):
        return render(request, 'create_campaign.html', status=200)
