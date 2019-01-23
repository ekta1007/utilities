
import urllib
from bs4 import BeautifulSoup
import pandas as pd

def return_url(region):
    modified_name=region.replace(", ","_").replace(" ","_")
    url="https://www.timetemperature.com/tzus/{}_time_zone.shtml".format(modified_name.lower())
    return url

def return_tz(region_url):
    if region_url != "N/A":
        # Get the HTML contents of the page and put it into BeautifulSoup
        opener = urllib.request.build_opener()
        #adding headers to let the browser think that this comes from a browser, instead of
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36')]

        page = opener.open(region_url).read()
        soup = BeautifulSoup(page.decode('utf-8', 'ignore'),features="lxml")
        # remove <br /> tags
        for e in soup.findAll('br'):
            e.extract()
        # Get the tz description - regular & dst tz from the soup object
        found=False
        try :
            for item in soup.find_all(class_='inforow2-right'):
                if str(item.find(class_="contentfont")).find('GMT/UTC')>-1 :
                    content=[x.replace('\n','') for x in item.find(class_="contentfont").contents]
                    regular=content[0].split('during ')[0].split('is')[-1].strip()
                    if len(content) >1 :
                        dst=content[1].split('during ')[0].split('is')[-1].strip()
                    else :
                        dst=''
                    found=True
                    return [regular, dst]
            if found is False :
                for item in soup.find_all(class_='inforow3-right'):
                    if str(item.find(class_="contentfont")).find('GMT/UTC')>-1 :
                        content=[x.replace('\n','') for x in item.find(class_="contentfont").contents]
                        regular,dst=content[0].split('during ')[0].split('is')[-1].strip(),content[1].split('during ')[0].split('is')[-1].strip()
                        return [regular, dst]
        except Exception as e:
            print(e, region_url )





#RUN

base_path='/Users/ekta.grover/codebase/utilities/'

df=pd.read_csv(base_path+'US_tz.csv',sep='\t',header='infer')
df['url']=df['Region'].map(lambda x : return_url(x))
df['regular'],df['dst']=zip(*df['url'].map(return_tz))
df.to_csv(base_path+'US_tz_processed.csv',index=False, header=df.columns, sep='\t', mode='a', encoding='utf8')

# getting distinct tz and their states
distinct_tz=set(df['regular'])
my_dict={}
for tz in distinct_tz :
    my_dict[tz]=list(df[df['regular']==tz]['Region'].values)
    
    
"""
TZ	States 
GMT/UTC - 6h	Alabama', 'Arkansas', 'Illinois', 'Iowa', 'Kansas', 'Louisiana', 'Minnesota', 'Mississippi', 'Missouri', 'Nebraska', 'North Dakota', 'Oklahoma', 'South Dakota', 'Texas', 'Wisconsin'
GMT/UTC - 7h	Arizona', 'Colorado', 'Idaho', 'Montana', 'New Mexico', 'Oregon', 'Utah', 'Wyoming'
GMT/UTC - 5h	Connecticut', 'Delaware', 'Florida', 'Georgia', 'Indiana', 'Kentucky', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'New Hampshire', 'New Jersey', 'New York', 'North Carolina', 'Ohio', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'Tennessee', 'Vermont', 'Virginia', 'West Virginia', 'Washington, DC'
GMT/UTC - 10h Standard Time	Hawaii'
GMT/UTC - 8h	California', 'Nevada', 'Washington'
GMT/UTC - 4h Standard Time	Puerto Rico'
GMT/UTC - 9h	Alaska'
"""
