#!/usr/bin/env python
# coding: utf-8

# # Roaller Coaster Analysis
# 

# ### 0- Import libraries

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('ggplot')
import plotly.express as px


# ### 1 - Pull Data about Roller Coasters from Wikipedia aprox 691
# https://en.wikipedia.org/wiki/Category:Roller_coaster_introductions_by_year
# 

# #### Gathering from Wikipedia
# #### 1- Get a list of all the roaler coasters from the category
# #### 2- Iterate over each and load  the page using the wiki api
# #### 3- Pull keys statistics and gather into a dataset
# 
# 

# ### 1- Import data 
# (https://www.kaggle.com/datasets/robikscube/rollercoaster-database?resource=download)

# In[2]:


columns= ['coaster_name','Length','Speed']
df = pd.read_excel('C:\LOCAL-KATHERIN\Project-Kath\RollerCoaster\coaster_db.xlsx')

df


# ### 2 - Data Understanding

# In[3]:


df.shape


# In[4]:


df.columns


# In[5]:


df.dtypes


# In[6]:


df.describe()


# ### 3- Data Preparation
# - Dropping irrelevant columns and rows
# - Identifying duplicated columns
# - Renaming Columns
# - Feature Creation

# In[7]:


df=df[['coaster_name', 
    #'Length', 'Speed', 
    'Location', 'Status', 
    #'Opening date',
    #'Type', 
    'Manufacturer', 
    #'Height restriction', 'Model', 'Height',
    #   'Inversions', 'Lift/launch system', 'Cost', 'Trains', 'Park section',
    #  'Duration', 'Capacity', 'G-force', 'Designer', 'Max vertical angle',
    # 'Drop', 'Soft opening date', 'Fast Lane available', 'Replaced',
    #'Track layout', 'Fastrack available', 'Soft opening date.1',
    #'Closing date', 
    #'Opened', 'Replaced by', 'Website',
    #  'Flash Pass Available', 'Must transfer from wheelchair', 'Theme',
    # 'Single rider line available', 'Restraint Style',
    #'Flash Pass available', 'Acceleration', 'Restraints', 'Name',
    'year_introduced', 'latitude', 'longitude', 'Type_Main',
    'opening_date_clean',
    #'speed1', 'speed2', 'speed1_value', 'speed1_unit',
    'speed_mph', 
    #'height_value', 'height_unit', 
    'height_ft',
     'Inversions_clean', 'Gforce_clean'
   ]].copy()


# In[8]:


df.shape


# In[9]:


df.dtypes


# In[10]:


#convert a column opening_date_clean in data type

# We can set errors='coerce' to convert invalid parsing to NaT (Not-a-Time), which represents missing or unknown dates.
df['opening_date_clean']=pd.to_datetime(df['opening_date_clean'],errors='coerce')
df


# In[11]:


#Rename columns
df=df.rename(columns={'coaster_name':'Coaster_Name',
                  'year_introduced':'Year_Introduced',
                  'opening_date_clean':'Opening_date',
                  'speed_mph':'Speed_mph',
                  'height_ft':'Height_ft',
                  'Inversions_clean':'Inversions',
                  'Gforce_clean;;;':'Gforce'})


# In[12]:


df


# In[13]:


#Identify missing values or null values
df.isna().sum()


# In[14]:


#check for duplicated Coaster_name
df.loc[df.duplicated(subset='Coaster_Name')]


# In[15]:


#cheking an example duplicated
df.query('Coaster_Name=="Wipeout (roller coaster)"')


# In[16]:


#dropping duplicated rows 
df=df.loc[~df.duplicated(subset=['Coaster_Name','Location','Opening_date'])]
df=df.reset_index(drop=True)
df


# In[17]:


df.shape


# ### 4- Feature Understanding
# 

# #### Top Years Coasters Introduced

# In[18]:



ax= df['Year_Introduced'].value_counts().head(10).plot(kind='bar',title='Top Years Coasters Introduced',color='skyblue',figsize=(10,5))
ax.set_xlabel('Year Introduced',color='black')
ax.set_ylabel('Count',color='black')
ax


# #### Distribution of roller coaster speeds in km/h.

# In[19]:


#add Speed km/h
df['Speed_km/h']=df['Speed_mph']*1.60934


# In[20]:


#HISTOGRAM
plt.figure(figsize=(10,5))
plt.hist(df['Speed_km/h'], bins=30, color='skyblue', edgecolor='black')

# Add title and labels
plt.title(' Speed Histogram')
plt.xlabel('Speed km/h')
plt.ylabel('Frequency')

# Show the plot
plt.show()


# ### 5- Feature Relationships
# -Scatterplot
# -Heatmap Correlation
# -Pairplot

# In[64]:


#Correlation between all variables in the data frame.
df.dropna().corr()

#We can see that the higher correlation between variables is in the speed and height


# In[30]:


#add Height in meter
df['Height_meters']=df['Height_ft']*0.3048


# In[57]:


plt.figure(figsize=(10,5))
sns.scatterplot(x=df['Speed_km/h'], y=df['Height_meters'],
                edgecolor='black', alpha=1,hue='Year_Introduced',data=df).set(title="Coaster Speed vs Height")

plt.show()


# In[74]:


plt.figure(figsize=(15,5))
sns.pairplot(df,vars=['Year_Introduced','Speed_km/h', 'Height_meters'],hue='Type_Main')
plt.show()


# In[58]:


df.columns


# In[69]:


sns.heatmap(df[['Year_Introduced','Speed_km/h', 'Height_meters','Inversions','Gforce_clean']].dropna().corr(),annot=True)
plt.show()


# ### 6- Ask a question about the data
# 
# 

# #### What are the locations with the fastest roller coasters?

# In[73]:


# Ordering the DataFrame using speed
df10= df[['Location','Speed_km/h']].query('Location!="Other"').sort_values(by='Speed_km/h',ascending=False).head(10)

#plot using seaborn
plt.figure(figsize=(10,5))
ax=sns.barplot(data=df10,x='Location',y='Speed_km/h',palette='Set2').set(title="The 10 locations with higher speed")
#rotar o rotulo do eixo x
plt.xticks(rotation=71)
plt.show()


# In[ ]:




