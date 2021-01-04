import cutecharts.charts as ctc
import pandas as pd
import numpy as np

# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
df=pd.read_csv('catsshouldnt.csv', sep=',')

# https://github.com/cutecharts/cutecharts.py#-usage
chart = ctc.Bar('Follower count for @catsshouldnt',width='500px',height='400px')
chart.set_options(
 labels=list(df["date"]),
 x_label="Date",
 y_label="Follower count" ,
 colors=['#FFF1C9','#F7B7A3','#EA5F89','#9B3192','#57167E','#47B39C','#00529B']
)

chart.add_series("Follower count",list(df["Follower count"]))
chart.render()