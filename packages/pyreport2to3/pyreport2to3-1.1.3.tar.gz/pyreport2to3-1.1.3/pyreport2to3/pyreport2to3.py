import logging
from datetime import date, datetime
import pandas as pd
import re
import matplotlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Error(Exception):
   """Base class for other exceptions"""
   pass

def split_section(result_list):
    result_list = [i for i in result_list if "RefactoringTool:" != i[:16] ]
    size = len(result_list)
    idx_list = [idx + 1 for idx, val in enumerate(result_list) if val[:3] == '---' and val[-10:] == '(original)']
    if len(idx_list) > 0:
        res = [result_list[i: j] for i, j in zip([0] + idx_list, idx_list + ([size] if idx_list[-1] != size else []))]
        return res
    else:
        return []

def make_clickable(url, name):
    return '<a href="{}" target="_blank">{}</a>'.format(url,name)

def get_HTMLreport(command, parameter):
    from future import standard_library
    standard_library.install_aliases()
    from subprocess import getoutput, getstatusoutput
    result= getoutput(command + " " + parameter)
    result_list=result.split('\n')
    #import pdb;pdb.set_trace()
    sections = split_section(result_list)
    if len(sections) == 0:
        print("no porting changes for the file/files")
        return

    df = pd.DataFrame()
    pd.set_option('display.max_colwidth', -1)
    pd.set_option('colheader_justify', 'center')


    #data = [['Alex',10],['Bob',12],['Clarke',13]]
    #import pdb;pdb.set_trace()
    if len(sections) >= 1:
        for each in sections:
            if each[0][:4] != '+++ ':
                continue;
            else:
                filename =  each[0][4:][:-12].replace('\t', '')
                size = len(each)
                idx_list = [idx + 1 for idx, val in enumerate(each) if val[:2] == '@@']
                idx_list = [i - 1 for i in idx_list]
                changes = [each[i: j] for i, j in zip([0] + idx_list, idx_list + ([size] if idx_list[-1] != size else []))]
                for cc in changes[1:]:
                    line_list = re.findall(r'\d+', cc[0])
                    #print line_list
                    line_number = line_list[0]
                    addedline = "\n".join([ i for i in cc if i[0] == '+'])
                    removedline = "\n".join([ i for i in cc if i[0] == '-'])
                    temp = cc[1:]
                    temp = []
                    for i in cc[1:]:
                        if i[0] == '-' and i[1] != '-':
                            temp.append("""<div class="minus">""" + i + """</div>""")
                        elif i[0] == '+' and i[1] != '+':
                            temp.append("""<div class="plus">""" + i + """</div>""")
                        else:
                            temp.append(i)

                    text = "\n".join(temp)

                    record = {"filename": filename, "lineno": line_number,
                                    "addedline": addedline, "removedline": removedline, "text": text}

                    df = df.append(record, ignore_index=True)


#def make_clickable(val):
    # target _blank to open new window
#    return '<a target="_blank" href="{}">{}</a>'.format(val, val)



    df['filename'] = df.apply(lambda x: make_clickable(x['filename'], x['filename']), axis=1)

#plot = df.groupby(['filename']).sum().plot(kind='pie', subplots=True)

#    import matplotlib.pyplot as plt
    import numpy as np

    df['removedline']=df['removedline'].replace({'':np.NAN})
    df['CHANGE COUNT'] =1
    group_data = df.groupby(['filename'])['CHANGE COUNT'].sum().rename_axis('filename')

    Tasks = [df['addedline'].count().sum(),df['removedline'].count().sum()]
    #print Tasks, "-----<>>>"
    '''
    my_labels = 'Lines Added','Lines Removed'
    plt.pie(Tasks,labels=my_labels,autopct='%1.1f%%')
    plt.title('Total Changes')
    plt.axis('equal')
    plt.savefig('./piechart.png')
    '''
    #group_data.plot(kind='pie', y='COUNTER')
    #group_data.plot(kind='pie', subplots=True, shadow = True,startangle=90,figsize=(15,10), autopct='%1.1f%%')

    df2 = group_data.to_frame()
    #print df2
    #import pdb;pdb.set_trace()

    '''
    #my_labels = 'Lines Added','Lines Removed'
    plt.pie(df2['COUNTER'], labels=df['filename'].unique(),autopct='%1.1f%%')
    #plt.bar(labels=df['filename'].unique(), height=df2['COUNTER'])
    plt.title('Changes per file')
    plt.axis('equal')
    plt.savefig('./piechart2.png')
    '''

    html_string = '''
    <html>
    <head><title>HTML Report of the Changes with python-modernize or 2to3</title>
    <style>
    .mystyle {
    font-size: 11pt;
    font-family: Arial;
    border-collapse: collapse;
    border: 1px solid silver;

    }

    .mystyle td, th {
     padding: 5px;
     }

    .mystyle tr:nth-child(even) {
       background: lightcyan;
     }

    .mystyle tr:hover {
      background: silver;
      cursor: pointer;
    }

    .minus{
    color: lightcoral;
    }
    .plus{
      color: lightseagreen;
    }
    </style>
    </head>
    <link rel="stylesheet" type="text/css" href="df_style.css"/>
    <body>
    
    {table}
    
    <br><br>
    
    <br><br>

    
    </body>
    </html>
    '''


    with open('pyportingreport.html', 'w') as f:
        f.write(html_string.format(table=df.to_html(escape=False, classes='mystyle').replace("\\n","<br>")))
        f.write("<br><br>")
        f.write(html_string.format(table=df2.to_html(escape=False, classes='mystyle')))
#        f.write("<br><br>")
#        f.write('<img src="piechart.png" alt="">')

    print('HTML Report is generated . File name is pyreporting.html')


#get_HTMLreport("python-modernize", "/Users/mallimuthu/dev/tools/releng/bin/rpscli/setup.py ")
#get_HTMLreport("python-modernize", "/Users/mallimuthu/dev/tools/releng/bin/rpscli/")