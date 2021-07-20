#!/usr/bin/env python
# coding: utf-8

# In[184]:


import requests as r


# In[185]:


url = 'https://api.covid19api.com/dayone/country/brazil'
resp = r.get(url)


# In[186]:


resp.status_code


# In[187]:


raw_data = resp.json()


# In[188]:


raw_data[0]


# In[189]:


final_data = []
for obs in raw_data:
    final_data.append([obs['Confirmed'],obs['Deaths'], obs['Recovered'], obs['Active'], obs['Date']])


# In[ ]:





# In[190]:


final_data.insert(0, ['Casos Confirmados', 'Casos com Obito', 'Casos Recuperados', 'Casos Ativos', 'Data'])


# In[191]:


CASOS_CONFIRMADOS = 0
CASOS_COM_OBITO = 1
CASOS_RECUPERADOS = 2
CASOS_ATIVOS = 3
DATA = 4


# In[192]:


for i in range(1, len(final_data)):
    final_data[i][DATA] = final_data[i][DATA][:10]


# In[ ]:


final_data


# In[193]:


import datetime as dt


# In[194]:


print (dt.time(12, 6, 21, 7),'Hora:minuto:segundo:microsegundo')
print('----')
print (dt.date(2020, 4, 25),'Ano-mês-dia')
print('----')
print (dt.datetime(2020, 4, 25, 12, 6, 21, 7),'Ano-mês-dia Hora:minuto:segundo:microsegundo')


# In[195]:


natal = dt.date(2020, 12, 25)
reveillon = dt.date(2021, 1, 1)

print(reveillon - natal)
print((reveillon - natal).days)
print((reveillon - natal).seconds)
print((reveillon - natal).microseconds)


# In[111]:


import csv


# In[112]:


with open('Brasil-covid.cvs', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(final_data)


# In[118]:


for i in range(1, len(final_data)):
    final_data[i][DATA] = dt.datetime.strptime(final_data[i][DATA], '%Y-%m-%d')


# In[ ]:


final_data


# In[120]:


def get_datasets(y, labels):
    if type(y[0]) ==list:
        datasets = []
        for i in range(len(y)):
            datasets.append({
                'label': labels[i],
                'data': y[i]
            })
        return datasets
    else:
        return [
            {
                'label': labels[0],
                'data': y 
            }
        ]


# In[136]:


def set_title(title=''):
    if title !='':
        display = 'true'
    else:
        display = 'false'
    return {
        'title':title,
        'display': display
    }


# In[172]:


def create_chart(x, y, labels, kind='bar', title=''):
    
    datasets = get_datasets(y, labels)
    options = set_title(title)
    
    chart = {
            'type': kind,
            'data': {
                'labels': x,
                'datasets': datasets
            },
        'options': options
    }
    return chart


# In[173]:


def get_api_chart(chart):
    url_base = 'https://quickchart.io/chart'
    resp = r.get(f'{url_base}?c={str(chart)}')
    return resp.content


# In[174]:


def save_image(path, content):
    with open(path, 'wb') as image:
        image.write(content)


# In[175]:


from PIL import Image
from IPython.display import display


# In[176]:


def display_image(path):
    img_pil = Image.open(path)
    display(img_pil)


# In[178]:


y_data_1 = []
for obs in final_data[1::10]:
    y_data_1.append(obs[CASOS_CONFIRMADOS])
    
y_data_2 = []
for obs in final_data[1::10]:
    y_data_2.append(obs[CASOS_RECUPERADOS])

labels = ['Casos Confirmados', 'Casos Recuperados']

x = []
for obs in final_data[1::10]:
    x.append(obs[DATA].strftime('%d/%m/%Y'))

chart = create_chart(x, [y_data_1, y_data_2], labels, title='Grafico de Casos Confirmados x Recuperados')
chart_content = get_api_chart(chart)
save_image('grafico-covid-atualizado.png', chart_content)
display_image('grafico-covid-atualizado.png')


# In[179]:


from urllib.parse import quote


# In[180]:


def get_api_qrcode(link):
    text = quote(link) # parsing do link para url
    url_base = 'https://quickchart.io/qr'
    resp = r.get(f'{url_base}?text={text}')
    return resp.content


# In[183]:


url_base = 'https://quickchart.io/chart'
link = f'{url_base}?c={str(chart)}'
save_image('qrcode.png', get_api_qrcode(link))
display_image('qrcode.png')


# In[ ]:




