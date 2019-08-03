import os
import csv
import re
import sys
import pandas as pd
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
from example.models import Export
from example.scripts.commons import loggerFetch


def argsFetch():
  '''
  Paser for the argument list that returns the args list
  '''
  import argparse

  parser = argparse.ArgumentParser(description='This implements the crawl State Machine')
  parser.add_argument('-l', '--log-level', help='Log level defining verbosity', required=False)
  parser.add_argument('-fn', '--filename', help='filename for importing data', required=False)
  parser.add_argument('-i', '--import', help='Import Export Data', required=False,action='store_const', const=1)
  parser.add_argument('-f', '--filter', help='filter the export records on percentile', required=False,action='store_const', const=1)
  parser.add_argument('-t', '--test', help='loop for running some tests', required=False,action='store_const', const=1)

  args = vars(parser.parse_args())
  return args



def main():
  args = argsFetch()
  logger = loggerFetch(args.get('log_level'))
  logger.info("Begin Processing")
  if args['filter']:
    years=[2015,2016,2017,2018]
    for year in years:
      objs=Export.objects.filter(year=year,isOtherItem=False).values("commodity").annotate(vsum=Sum('value')).order_by("-vsum")
      i=0
      for obj in objs:
        i=i+1
        if i <= 15:
          commodity=obj['commodity']
          logger.info(commodity)
          myobjs=Export.objects.filter(year=year,commodity=commodity)
          for eachObj in myobjs:
            eachObj.isTopItem=True
            eachObj.save()
    exit(0)
    objs=Export.objects.all().order_by("-id")
    for obj in objs:
      finyear=obj.finyear
      year=finyear[-4:]
      obj.year=year
      obj.save()
      logger.info(obj.id)
      logger.info(f"{finyear}-{year}")
    exit(0)
    objs=Export.objects.filter(isOtherItem=False).values("country","finyear").annotate(vsum=Sum('value')).order_by("-vsum")
    for obj in objs:
      totalValue=obj['vsum']
      country=obj['country']
      finyear=obj['finyear']
      logger.info(f"country-{country}  finyear-{finyear}  totalValue-{totalValue}")
      exportObjects=Export.objects.filter(country=country,finyear=finyear,isOtherItem=False).order_by("-value")
      j=0
      valueSum=0
      for e in exportObjects:
        if j < 20:
          j=j+1
          valueSum=valueSum+e.value
          e.isAboveThreshold=True
          e.save()
          logger.info(f"commodity-{e.commodity}  value-{e.value}")  
      diffValue=totalValue-valueSum
      logger.info(f"(totalValue-{totalValue} valueSum-{valueSum} diffValue-{diffValue}")
      if diffValue > 0:
        myobj=Export.objects.filter(country=country,finyear=finyear,commodity="otherItems").first()
        if myobj is None:
          myobj=Export.objects.create(country=country,finyear=finyear,commodity="otherItems")
        logger.info("object already created")
        myobj.value=diffValue
        myobj.isAboveThreshold=True
        myobj.isOtherItem=True
        myobj.save()
        logger.info("other item object create with id %s" % str(myobj.id))
    i=0    
    objs=Export.objects.filter(isOtherItem=False).values("country").annotate(vsum=Sum('value')).order_by("-vsum")
    for obj in objs:
      country=obj['country']
      if i> 19:
        exportObjects=Export.objects.filter(country=country)
        for e in exportObjects:
          e.isAboveThreshold=False
          e.save()
      else:
        logger.info(f"country-{country}")
      i=i+1
  if args['import']:
    logger.info("Import export Data")
    filename=args['filename']
    if filename is None:
      logger.info("File name not specified")
      exit(0)
    else:
      df=pd.read_csv(filename)
      logger.info(df.head())
      filenameArray=filename.split("-")
      finyear="%s-%s" % (filenameArray[3],filenameArray[4])
      finyear=finyear.rstrip(".csv")
      for index, row in df.iterrows():
        country=row['COUNTRY']
        commodity=row['COMMODITY']
        value=row['VALUE']
        logger.info(f"country-{country}  commodity-{commodity}  finyear-{finyear}  value-{value}")
        obj=Export.objects.filter(country=country,commodity=commodity,finyear=finyear).first()
        if obj is None:
          obj=Export.objects.create(country=country,commodity=commodity,finyear=finyear)
        obj.decimalValue=value
        obj.value=int(value)
        obj.save()
        logger.info(obj.id)
  if args['test']:
    logger.info("Running the test loop")
    objs=Export.objects.all().order_by("-id")
    for obj in objs:
      logger.info(obj.id)
      obj.value=int(obj.decimalValue)
      obj.save()
  logger.info("...END PROCESSING") 
  exit(0)
if __name__ == '__main__':
  main()
