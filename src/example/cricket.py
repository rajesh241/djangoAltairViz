import pandas as pd
import altair as alt
from altair import datum
import json

from django.conf import settings
from example.models import Batting

def getBattingChart():
  filename="%s/batting.csv" % (settings.MEDIA_ROOT)
  source = pd.DataFrame(list(Batting.objects.all().values("name","country","average","year","strikerate","runs")))
  print(source.head())
  alt.data_transformers.disable_max_rows()
  slider = alt.binding_range(min=1990, max=2018, step=1)
  select_year = alt.selection_single(name="year", fields=['year'], on='none' ,clear='none',
                                             bind=slider, init={'year': 1998})
  singlePlayer = alt.selection_single(empty='none', fields=['name'] , init={'name':'SR Tendulkar'})
  domain=["INDIA","AUS","PAK","ENG","SA","NZ"]
  range_=["#6baed6","yellow","green","red","orange","black"]
  base=alt.Chart(source).mark_circle().encode(
#      x=alt.X('average',scale=alt.Scale(domain=[0, 200])),
#      y=alt.Y('strikerate',scale=alt.Scale(domain=[0, 200])),
      x='average',
      y='strikerate',
      #color='country',
      color=alt.Color('country', legend=alt.Legend(title='Country', orient = 'left'),scale=alt.Scale(domain=domain, range=range_)),
      tooltip=['name', 'country', 'average', 'strikerate']
  ).add_selection(
    select_year,
    singlePlayer
  ).transform_filter(
     datum.runs > 450        
  ).transform_filter(
    select_year
  ).properties(
   title="Batting Records Year Wise"
)

  titleLine = alt.Chart(source).mark_text(dy=100, size=30, opacity=0.5,text='foo-baz', color='#d6616b').encode(
      text='name:N',
      opacity=alt.value(0.5)
      ).transform_filter(
          singlePlayer
	  )

  combinedLine=alt.Chart(source).mark_line(point=True).encode(
          x='year:Q',
)

  z=alt.layer(
    combinedLine.mark_line(color='blue').encode(
        y='average',
        ),
    combinedLine.mark_line(color='red').encode(
        y='strikerate'
        )
).transform_filter(
singlePlayer
).properties(
  title='Selected Player Recored over Years'
 )
  myChart=base  | z + titleLine
  myChart1=myChart.configure_circle(
   filled=True,
   size=100,
).properties(
autosize='fit'
)
  return myChart1
