from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.generic import TemplateView
from django.views.generic import View
from django.db.models import F,Q,Sum,Count
from .cricket import getBattingChart
from .export import getExportChart
# Create your views here.
class cricket(TemplateView):
  template_name="chart.html"

  def get(self, request, *args, **kwargs):
    context = locals()
    chartArray=[]
    myChart=getBattingChart()
    chartTitle="Cricket Batting Records"
    description="The interactive charts below show batting records of different players over last thirty years. Players are being measured on average (average runs per innings) and strikerate (runs per 100 balls). The left panel has top players for each year. Each mark represents the player. On selecting any mark, the right panel displays the performance of selected player over the years. The marks have been color coded based on country"
    postscript="""<ul><li>The above chart is powered by Django and Altair
                  </li><li>The code used to genrate this chart can be found <a href='https://github.com/rajesh241/djangoAltairViz'>here</a>.
                  </li><li>Minimum qualification of players to enter the left panel has been set to 450 runs per calendar year
               </li></ul>"""
    p={}
    p['name']=chartTitle
    p['chart']=myChart
    p['description']=description
    p['postscript']=postscript
    chartArray.append(p)

    context['chartArray']=chartArray
    return render(request, self.template_name, context)

class exportView(TemplateView):
  template_name="chart.html"

  def get(self, request, *args, **kwargs):
    context = locals()
    chartArray=[]
    myChart=getExportChart()
    chartTitle="Export Data"
    description="The interactive charts below show Export Data for India"
    p={}
    p['name']=chartTitle
    p['chart']=myChart
    p['description']=description
    chartArray.append(p)

    context['chartArray']=chartArray
    return render(request, self.template_name, context)


