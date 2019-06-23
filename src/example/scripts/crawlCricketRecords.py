import os
import csv
import re
import sys
import requests
from bs4 import BeautifulSoup
fileDir = os.path.dirname(os.path.realpath(__file__))
rootDir=fileDir+"/../../"
sys.path.insert(0, rootDir)
djangoSettings="djangoviz.settings"
import django
from django.core.wsgi import get_wsgi_application
from django.db import models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", djangoSettings)
django.setup()
from django.db.models import F,Q,Sum,Count
from django.contrib.auth.models import User
from django.utils import timezone
from example.scripts.commons import loggerFetch
from example.models import Batting

def argsFetch():
  '''
  Paser for the argument list that returns the args list
  '''
  import argparse

  parser = argparse.ArgumentParser(description='This implements the crawl State Machine')
  parser.add_argument('-l', '--log-level', help='Log level defining verbosity', required=False)
  parser.add_argument('-t', '--test', help='Test Loop', required=False,action='store_const', const=1)
  parser.add_argument('-c', '--crawl', help='Crawl Cricket Records', required=False,action='store_const', const=1)

  args = vars(parser.parse_args())
  return args



def main():
  args = argsFetch()
  logger = loggerFetch(args.get('log_level'))
  logger.info("Begin Processing")
  if args['test']:
    logger.info("Running the test loop")
  if args['crawl']:
    maxPages=41
    for i in range(1,maxPages+1):
      url="http://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;filter=advanced;size=200;spanmax1=31+Dec+2018;spanmin1=01+Jan+1991;spanval1=span;template=results;type=batting;view=year"
      if i != 1:
        url="%s;page=%s" % (url,str(i))
      logger.info(url)
      r=requests.get(url)
      if r.status_code == 200:
        myhtml=r.content
        mysoup=BeautifulSoup(myhtml,"lxml")
        tables=mysoup.findAll('table')
        for table in tables:
          if "By year of match start" in str(table):
            logger.info("Found the table")
            rows=table.findAll('tr')
            for row in rows:
              cols=row.findAll('td')
              if len(cols) > 5:
                nameCountry=cols[0].text.lstrip().rstrip()
                nameCountryArray=nameCountry.split("(")
                if len(nameCountryArray) == 2:
                  name=nameCountryArray[0]
                  country=nameCountryArray[1].replace(")","")
                  logger.info(f"{name}-{country}")
                  matches=cols[1].text.lstrip().rstrip()
                  innings=cols[2].text.lstrip().rstrip()
                  notout=cols[3].text.lstrip().rstrip()
                  runs=cols[4].text.lstrip().rstrip()
                  matches=cols[1].text.lstrip().rstrip()
                  innings=cols[2].text.lstrip().rstrip()
                  notout=cols[3].text.lstrip().rstrip()
                  runs=cols[4].text.lstrip().rstrip().replace("*","")
                  try:
                    average=int(float(cols[6].text.lstrip().rstrip()))
                  except:
                    average=None
                  try:
                    strikerate=int(float(cols[8].text.lstrip().rstrip()))
                  except:
                    strikerate=None
                  try:
                    year=int(cols[12].text.lstrip().rstrip())
                  except:
                    year=None
                  logger.info(f"average - {average} strikerate {strikerate} year {year}")
                  if (average is not None) and (strikerate is not None) and (year is not None):
                    logger.info("valid Record")
                    obj=Batting.objects.filter(year=year,name=name).first()
                    if obj is None:
                      obj=Batting.objects.create(year=year,name=name)
                    obj.country=country
                    obj.average=average
                    obj.strikerate=strikerate
                    obj.runs=runs
                    obj.save()

  logger.info("...END PROCESSING") 
  exit(0)
if __name__ == '__main__':
  main()
