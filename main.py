from datetime import date
import pandas as pd
from event_crawler_level_1 import EventCrawlerLevel1
from event_crawler_level_2 import EventCrawlerLevel2

airTags = ['jinair', 'jejuair','airseoul','airbusan','tway']
# airTags = ['jinair']
df = pd.DataFrame(columns=['airline', 'url', 'date',  'header','content', 'level2', 'level3'])  

for tag in airTags:
    df = pd.concat([df,EventCrawlerLevel1(tag).get_data_level_1()])
    
df = df.reset_index()
df = df.drop('index', axis=1)
print(df)

for i in range(len(df.url)-1):
    url = df.url.values[i]
    airline = df.airline.values[i]
    df['level2'].values[i] = EventCrawlerLevel2(url, airline).get_data_level_2()
print(df)


today = date.today().isoformat()
file_name = f'AirLines_Event_{today}.xlsx'
df.to_excel(file_name)