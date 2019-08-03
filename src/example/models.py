from django.db import models

# Create your models here.
class Batting(models.Model):
  country=models.CharField(max_length=2048,blank=True,null=True)
  name=models.CharField(max_length=2048)
  year=models.IntegerField()
  average=models.IntegerField(null=True,blank=True)
  runs=models.IntegerField(default=0)
  strikerate=models.IntegerField(null=True,blank=True)
  def __str__(self):
    return "%s-%s-%s" % (self.name,self.country,str(self.value))

class Export(models.Model):
  country=models.CharField(max_length=1024)
  commodity=models.CharField(max_length=1024)
  finyear=models.CharField(max_length=256)
  year=models.IntegerField(null=True,blank=True)
  decimalValue=models.DecimalField(max_digits=16,decimal_places=4,null=True,blank=True)
  value=models.IntegerField(null=True,blank=True)
  isAboveThreshold=models.BooleanField(default=False)
  isOtherItem=models.BooleanField(default=False)
  isTopItem=models.BooleanField(default=False)
  def __str__(self):
    return "%s-%s-%s" % (self.country,self.commodity,str(self.value))
 
