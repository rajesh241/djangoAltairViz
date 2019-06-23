from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.generic import TemplateView
from django.views.generic import View
from django.db.models import F,Q,Sum,Count
from .cricket import getBattingChart
# Create your views here.
class cricket(TemplateView):
  template_name="chart.html"

  def get(self, request, *args, **kwargs):
    context = locals()
    chartArray=[]
    myChart=getBattingChart()
    chartTitle="Batting Records"
    description="The interactive charts below show batting records of different players over last thirty years. The left panel has player recoards for each year, year can be changed by the slider below. Each mark represents the player. On selecting any mark, the right panel displays the performance of selected player over the years. The marks have been color coded based on country"
    p={}
    p['name']=chartTitle
    p['chart']=myChart
    p['description']=description
    chartArray.append(p)

    context['chartArray']=chartArray
    return render(request, self.template_name, context)


