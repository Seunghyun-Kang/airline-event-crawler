from datetime import date
import pandas as pd
from event_crawler import EventCrawler

airTags = ['jinair', 'jejuair','airseoul','airbusan','tway']
df = pd.DataFrame(columns=['airline', 'url', 'date',  'header','content'])  

for tag in airTags:
    df = pd.concat([df,EventCrawler(tag).getEventList()])

df = df.reset_index()
df = df.drop('index', axis=1)
print(df)
today = date.today().isoformat()
file_name = f'AirLines_Event_{today}.xlsx'
df.to_excel(file_name)