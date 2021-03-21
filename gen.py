from pathlib import Path

import ads
from glob import glob
#import ads.sandbox as ads
#ads.config.token = 'secret token'
myORCID = '0000-0003-3345-9515'
things_wanted = ['abstract',
                'author',
                  'citation_count ',
                  'first_author',
                  'pubdate',
                  'title',
                  'volume',
                  'year',
                  'page',
                  'doi',
                 'journal',
                 'id'
                 
                
                ]

dois = []
citation_count = []
abstracts = []
pub_dates = []
ids = []

breaklines =  '---\n'

files = glob('science/*.md')
for md in files:
    
    with open(md,'r') as f:
        ll = f.readlines()
        
    info =ll[1:]
    
    jj= 0
    for x in info:
        if x == breaklines:
            break
        jj+=1
    info = info[:jj]
    
    
    for ele in info:
    
        x = ele.strip()
        tag, data = x.split(':')

        if tag == 'ref-doi':

            dois.append(data)

    
    
    
        
        


for doi in dois:

    search = list(ads.SearchQuery(doi=doi, fl=things_wanted))
    
    citation_count.append(search[0].citation_count)
    abstracts.append(search[0].abstract)
    pub_dates.append(search[0].pubdate)
    ids.append(search[0].id)
    

p = Path("science_push")
p.mkdir()
    
for i, md in enumerate(files):
    
    
    date = pub_dates[i]
    
    yr,mn,day = date.split('-')
    
    if day =='00':
        day = '01'
    
    date = '%s-%s-%s' %(yr,mn,day)
    
    new_name = '%s-%s.md' % (date, ids[i])
    
    
    with open(md,'r') as f:
        ll = f.readlines()
        
    info =ll[1:]
    
    jj= 0
    for x in info:
        if x == breaklines:
            break
        jj+=1
    info = info[:jj]
    
    
    for k, ele in enumerate(info):
    
        x = ele.strip()
        tag, data = x.split(':')

        if tag == 'date':
            kk = k
            print(data)
            print(date)
    
    info[kk] = 'date: %s\n' % date
    
    for k, ele in enumerate(info):
    
        x = ele.strip()
        tag, data = x.split(':')

        if tag == 'layout':
            kk=k
            
    info[kk] = 'layout: single\n'
    try:
        info.append('cite-count: %d\n' % citation_count[i]) 
    except:
        info.append('cite-count: %d\n' % 0) 
    
    
    info.append(breaklines)
    
    info.append('\n\n')
    
    info.append('##Abstract\n')
    #info.append('#' abstracts[i])
    
    
    # with open('/Users/jburgess/coding/grburgess.github.io/_posts/science/%s'%new_name, 'w') as f:
    #     f.write(breaklines)
    #     for ii in info:
    #         f.write(ii)

    
    with open('science_push/%s'%new_name, 'w') as f:
        f.write(breaklines)
        for ii in info:
            f.write(ii)

            



