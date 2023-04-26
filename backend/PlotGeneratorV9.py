#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Data processing libraries
import pandas as pd
import numpy as np
from datetime import datetime, date
import random
import os
# Data visulization libraries
import matplotlib.pyplot as plt
from matplotlib.offsetbox import (OffsetImage,AnnotationBbox)
import warnings
warnings.filterwarnings('ignore')


# In[2]:
def makepdf(pid,fileName):
    # Import data
    #file_name ='Unit Message Log.csv'
    #data_dir = './data/'
    #plot_dir = './plot/'
    #df = pd.read_csv(data_dir + file_name, delimiter=';')
    #Pid =sys.argv[1]
    #file_name =sys.argv[2]
    Pid =pid
    file_name =fileName.replace(' ','_')
    data_dir = './reportdata/CSVFILE/'+Pid+'/'
    plot_dir = './plot/'+Pid+'/'
    os.mkdir(plot_dir)
    df = pd.read_csv(data_dir + file_name, delimiter=';')


    # In[3]:


    # Put column name into variable
    Load_col = 'Load'
    TimeStamp_col = 'Timestamp'


    # In[4]:


    # Remove row with 'Load' == NAN
    without_load_nan = df[Load_col].notnull()
    df = df[without_load_nan]
    df.loc[(df[Load_col] == 'On Ground'),Load_col] = 0


    # In[5]:


    # Create a new col for int type load
    df['Load_col_int'] = df[Load_col].astype(int)


    # In[6]:


    # Timestamp processing
    timestamp_format = '%Y-%m-%d %H:%M:%S'

    # Generate TIME DATE WEEK DAY columns
    df[TimeStamp_col] = pd.to_datetime(df[TimeStamp_col], format=timestamp_format)
    df['Time'] = pd.to_datetime(df[TimeStamp_col], format=timestamp_format).dt.time
    df['Month'] = pd.to_datetime(df[TimeStamp_col], format=timestamp_format).dt.month
    df['Date'] = pd.to_datetime(df[TimeStamp_col], format=timestamp_format).dt.date
    df['Week'] = pd.to_datetime(df[TimeStamp_col], format=timestamp_format).dt.isocalendar().week
    df['Day'] = pd.to_datetime(df[TimeStamp_col], format=timestamp_format).dt.day


    # In[7]:


    # Generate a new 'LoadStatus' column with labelled load data
    # Load classification (kg)
    heavy_load = 1750
    light_load = 1000
    unit_weight = 750

    # Labels
    # 'Load over HEAVY KG', 'Load under LIGHT KG', 'Load between LIGHT KG to HEAVY KG', 'On Ground'
    labels = ['Load between '+ str(light_load-unit_weight) + ' to ' + str(heavy_load-unit_weight) + ' Kg',
            'Load over ' + str(heavy_load-unit_weight) + ' Kg', 
            'Load under '+ str(light_load-unit_weight) + ' Kg', 
            'Empty load']

    # over HEAVY
    df.loc[(df[Load_col].astype(int) > heavy_load), 'LoadStatus'] = labels[1]
    # under LIGHT
    df.loc[(df[Load_col].astype(int) > unit_weight) & (df[Load_col].astype(int) <= light_load), 'LoadStatus'] = labels[2]
    # between LIGHT and HEAVY
    df.loc[(df[Load_col].astype(int) >= light_load) & (df[Load_col].astype(int) <= heavy_load), 'LoadStatus'] = labels[0]
    # on Ground
    df.loc[(df[Load_col].astype(int) <= unit_weight), 'LoadStatus'] = labels[3]


    # In[8]:


    # Divide data into subdataframe
    # Group by month
    month_grouped = df.groupby(df.Month)
    # Pervious two month dataframe
    pervious_two_month = df['Month'].value_counts().index[0]
    df_pervious_two = month_grouped.get_group(pervious_two_month)
    # Last month dataframe
    pervious_one_month = df['Month'].value_counts().index[1]
    df_pervious_one = month_grouped.get_group(pervious_one_month)
    # Current month dataframe
    current_month = df['Month'].value_counts().index[2]
    # three months datafame to df_three_months
    df_three_months = df
    # Set current month dataframe as df to keep simple
    df = month_grouped.get_group(current_month)

    # Eight weeks dataframe
    eight_weeks = df_three_months['Week'].value_counts().index.sort_values()[-8:]
    df_eight_weeks = df_three_months[df_three_months['Week'].isin(eight_weeks)]
    # Eight week arange
    Week = df_eight_weeks['Week'].value_counts().shape[0]
    Week_Len = np.arange(Week+1)


    # In[9]:


    # Plot setting
    roborigger_blue = '#004099'
    figsize_hight = 6
    figsize_weight = 6
    width = 0.5
    align = 'center'
    fontsize = 10
    commentSize = 24
    bbox_inches = 'tight'
    dpi = 72

    line_label_size = 22
    commentSize = 30
    xy_label = 22
    tickSize = 17
    titleSize = 26
    containerFont=22


    # # Part 1

    # # 01 Lift per day

    # In[10]:


    # Draw lifts_per_day.png
    plot_name = 'lifts_per_day.png'


    # In[11]:


    df_lift = df_three_months.loc[df_three_months['Event']=='Load Lift']
    # Sum up gross Daily lift count
    df_daily_lift = df.groupby(df_lift['Day']).count()[Load_col]


    # In[12]:


    mean = round(df.groupby(df_lift['Day']).count()['Load'].sum()/df.groupby(df_lift['Day']).count()['Load'].count())
    df_daily_lift.index = df_daily_lift.index.astype(int)
    df_daily_lift_fill = df_daily_lift.reindex(list(range(1,31)),fill_value=0)

    # plot setting
    figsize_width = 12
    figsize_hight = 5
    fontsize = 22

    pd.set_option("display.precision", 0)
    max_value = df.groupby(df_lift['Day']).count()['Load'].index[-1]+1

    # Drawing
    fig, ax = plt.subplots()   
    df_daily_lift_fill.plot.bar(figsize=(figsize_width,figsize_hight),color=roborigger_blue)


    # Make spines invisible
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Set up grid
    plt.grid(axis = 'y')

    # Set up labels and ticks
    plt.xticks(rotation = 0)
    plt.ylabel('Lift Count (times)',fontsize=fontsize)
    plt.xlabel('Day',fontsize=fontsize)

    ax.hlines(mean, -1, max_value, linestyles='solid', colors='orangered')
    plt.text(max_value-13, mean+2, 'Monthly Average', dict(fontsize=24, color='orangered'))
    ax.hlines(mean+11, -1, max_value, linestyles='solid', colors='green')
    plt.text(max_value-13, mean+13, 'Industry Best', dict(fontsize=24, color='green'))
    msg5 = "Daily average lift count is "+str(mean)+" times this month."
    #plt.text(-1, -20, msg5, dict(fontsize=30, color='orangered'))

    ax.tick_params(labelsize=tickSize)
    # plt.title('Lifts Per Day', fontsize=titleSize)
    # Save the plot
    plt.savefig(plot_dir + plot_name, bbox_inches=bbox_inches, dpi=dpi)


    # # 02 Lift per week last 8 weeks

    # In[13]:


    # Draw lifts_per_week_last_8_weeks.png
    plot_name = 'lifts_per_week_last_8_weeks.png'


    # In[14]:


    # Count weekly 'Load Lift' event in eight weeks dataframe
    df_weeks_lift = df_eight_weeks.loc[df_eight_weeks['Event']=='Load Lift']
    df_weekly_lift = df_eight_weeks.groupby(df_weeks_lift['Week']).count()[Load_col]


    # In[15]:


    # Claculate the mean value
    mean2 = round(df_weekly_lift.sum()/df_weekly_lift.count())

    #Plot setting
    figsize_width = 7
    figsize_hight = 5

    pd.set_option("display.precision", 0)

    max_value2 = df_weekly_lift.index[-1]+1
    x = len(df_weekly_lift.index) -4.4

    fig, ax = plt.subplots()   
    df_weekly_lift.plot.bar(figsize=(figsize_width,figsize_hight),color=roborigger_blue)

    # Make spines invisible
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Set grid
    plt.grid(axis = 'y')

    # Set up labels and ticks
    plt.xticks(rotation = 0)
    plt.ylabel('Lift Count (times)', fontsize=fontsize)
    plt.xlabel('Week',fontsize=xy_label)

    ax.hlines(mean2, -1, max_value2, linestyles='solid', colors='orangered')
    plt.text(x, mean2+5, 'Monthly Average', 
            dict(fontsize=line_label_size, color='orangered'))
    ax.hlines(mean2+25, -1, max_value2, linestyles='solid', colors='green')
    plt.text(x, mean2+30, 'Industry Best', 
            dict(fontsize=line_label_size, color='green'))

    msg5 = "Weekly average is "+str(mean2)+" times."
    #plt.text(-0.5, -80, msg5, dict(fontsize=30, color='orangered'))
    ax.tick_params(axis='both', labelsize=tickSize)
    plt.xticks(list(range(len(range(1,9)))), range(1,9))
    # plt.title('Lift Counts Per Week', fontsize=titleSize)

    # Save the plot
    plt.savefig(plot_dir + plot_name, bbox_inches=bbox_inches, dpi=dpi)


    # # 03 Average time per lift

    # In[16]:


    # Draw average_time_per_lift.png
    plot_name = 'average_time_per_lift.png'


    # In[17]:


    df_lift_time = df_three_months.loc[(df_three_months['Event']=='Load Lift') | (df_three_months['Event']=='Load Set Down')]
    df_lift_time['group'] = (df_lift_time['Event'].eq('Load Set Down') & df_lift_time['Event'].shift(-1).eq('Load Lift'))[::-1].cumsum()[::-1]
    df_lift_time['diff'] = (df_lift_time[~df_lift_time.duplicated(['Event','group'])].groupby('group')['Timestamp'].transform(lambda d: d.diff()))
    df_lift_time = df_lift_time.query('diff != "NaT"')
    Total_Time = df_lift_time['diff'].groupby(df_three_months['Month']).sum()
    Total_Time = Total_Time / np.timedelta64(1, 'h')


    # In[18]:


    # Data processing
    # Calculate total lift time daily
    Total_Day_Time = df_lift_time['diff'].groupby(df['Day']).sum()
    Total_Day_Time = Total_Day_Time / np.timedelta64(1, 'm')

    # Calculate average time per lift
    avg_lift_time = pd.concat([Total_Day_Time , df_daily_lift], axis=1)
    avg_lift_time['Avg_Time'] = avg_lift_time['diff'] / avg_lift_time['Load']
    avg_lift_time = avg_lift_time.round(0).astype(int)['Avg_Time']
    avg_lift_time.index = avg_lift_time.index.astype(int)
    avg_lift_time_fill = avg_lift_time.reindex(list(range(1,31)),fill_value=0)


    # In[19]:


    # Plot setting
    figsize_width = 12
    figsize_hight = 5

    mean_avg_lift_time = avg_lift_time.sum()/avg_lift_time.count()
    maxV = avg_lift_time.index[-1]+1

    # Drawing
    fig, ax = plt.subplots()   
    avg_lift_time_fill.plot.bar(figsize=(figsize_width,figsize_hight),color=roborigger_blue)

    # Make spines invisible
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Set grid
    plt.grid(axis = 'y')

    # Set up labels and ticks
    plt.xticks(rotation = 0)
    ax.tick_params(labelsize=tickSize)
    plt.ylabel('Average Lift Time (mins)',fontsize=xy_label)
    plt.xlabel('Day',fontsize=xy_label)


    # plt.title('Average Daily Duration Time Per Lift', fontsize=titleSize)

    ax.hlines(mean_avg_lift_time, -1, maxV, linestyles='solid', colors='orangered')
    plt.text(maxV-10, mean_avg_lift_time+0.4, 'Monthly Average', dict(fontsize=line_label_size, color='orangered'))
    plt.text(maxV-10, mean_avg_lift_time-0.9, 'Industry Best', dict(fontsize=line_label_size, color='green'))
    ax.hlines(mean_avg_lift_time-1, -1, maxV, linestyles='solid', colors='green')
    # Save the plot
    plt.savefig(plot_dir + plot_name, bbox_inches=bbox_inches, dpi=dpi)


    # # 04 Average time per lift last 8 weeks

    # In[20]:


    # Draw average_timep_per_lift_last_8_weeks.png
    plot_name = 'average_timep_per_lift_last_8_weeks.png'


    # In[21]:


    df_lift_time_week = df_eight_weeks.loc[(df_eight_weeks['Event']=='Load Lift') | (df_eight_weeks['Event']=='Load Set Down')]
    df_lift_time_week['group'] = (df_lift_time_week['Event'].eq('Load Set Down') & df_lift_time_week['Event'].shift(-1).eq('Load Lift'))[::-1].cumsum()[::-1]
    df_lift_time_week['diff'] = (df_lift_time_week[~df_lift_time_week.duplicated(['Event','group'])].groupby('group')['Timestamp'].transform(lambda d: d.diff()))
    df_lift_time_week = df_lift_time.query('diff != "NaT"')
    Total_Time_week = df_lift_time_week['diff'].groupby(df_eight_weeks['Week']).sum()
    Total_Time_week_hr = Total_Time_week / np.timedelta64(1, 'h')
    Total_Time_week 


    # In[22]:


    # Data processing
    # Calculate total lift time daily
    Total_Week_Time = df_lift_time_week['diff'].groupby(df_eight_weeks['Week']).sum()
    Total_Week_Time_min = Total_Week_Time / np.timedelta64(1, 'm')
    Total_Week_Time_min


    # In[23]:


    # Calculate average time per lift
    avg_lift_time = pd.concat([Total_Week_Time_min  , df_weekly_lift], axis=1)
    avg_lift_time['Avg_Time'] = avg_lift_time['diff'] / avg_lift_time['Load']
    avg_lift_time = avg_lift_time.round(0).astype(int)['Avg_Time']
    avg_lift_time.index = avg_lift_time.index.astype(int)


    # In[24]:


    avg_lift_time.index[-1]+1


    # In[25]:


    figsize_width = 7
    figsize_hight = 5
    fontsize = 14
    mean = avg_lift_time.sum()/avg_lift_time.count()
    maxV = 8
    fig, ax = plt.subplots()   
    avg_lift_time.plot.bar(figsize=(figsize_width,figsize_hight),color=roborigger_blue)

    # Make spines invisible
    plt.xlabel('Week',fontsize=xy_label)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Set up grid
    plt.grid(axis = 'y')

    # # Set up labels and ticks
    plt.ylabel('Average Lift Time (mins)', fontsize=xy_label)
    plt.xticks(list(range(len(range(1,9)))), range(1,9),rotation = 0)
    ax.tick_params(axis='both', labelsize=tickSize)

    ax.hlines(mean, -1, maxV, linestyles='solid', colors='orangered')
    plt.text(maxV-2.3, mean+0.3, 'Average', dict(fontsize=line_label_size, color='orangered'))
    ax.hlines(mean+1, -1, maxV, linestyles='solid', colors='green')
    plt.text(maxV-3.5, mean+1.3, 'Industry Best', dict(fontsize=line_label_size, color='green'))


    # plt.title('Average Weekly Duration Time Per Lift', fontsize=titleSize)

    # Save the plot
    plt.savefig(plot_dir + plot_name, bbox_inches=bbox_inches, dpi=dpi)


    # # 07 WEATHER：Temperature / Wind Speed / Rainfall

    # In[26]:


    # data from bom.gov.au, Sep 2022
    # http://www.bom.gov.au/climate/dwo/202209/html/IDCJDW6111.202209.shtml
    # http://www.bom.gov.au/climate/dwo/202209/html/IDCJDW2124.202209.shtml
    file_name ='weather.txt'
    data_dir = './static/'

    df_weather = pd.read_csv(data_dir + file_name, delimiter='\t', header=0)
    df_weather['day']= range(1,31)
    df_weather.index = df_weather.index + 1

    # Day cannot work effect by weather
    weather = 2


    # In[27]:


    plot_name = 'temperature_wind_speed_rainfall.png'
    fig, ax = plt.subplots(figsize=[12,5])
    ax.plot(df_weather['MaxTemp'], label='MaxTemp',color='red')
    ax.plot(df_weather['MinTemp'], label='MinTemp',color='orange')
    ax.plot(df_weather['WindSpeed'], label='WindSpeed', color='green')
    ax.plot(df_weather['Rainfall'], label='Rainfall',color='blue')
    ax.fill_between(range(1,31), df_weather['Rainfall'], alpha = 0.3)

    # Set up labels and ticks
    plt.xticks(np.arange(1, 31, 1))
    ax.tick_params(axis='both', labelsize=tickSize)

    plt.grid(axis = 'y')

    # plt.title('Monthly Weather', fontsize=titleSize)

    plt.legend(bbox_to_anchor=(0.5,-0.3), loc="lower center", ncol=len(df.columns), fontsize=19)
    plt.savefig(plot_dir + plot_name,bbox_inches=bbox_inches, dpi=dpi)
    plt.show()


    # # 08 Mass lift per hour last 8 weeks

    # In[28]:


    # Draw mass_lifted_per_hour_last_8_weeks.png
    plot_name = 'mass_lifted_per_hour_last_8_weeks.png'


    # In[29]:


    # Weekly load mass
    df_lift_eight_weeks = df_eight_weeks.loc[df_three_months['Event']=='Load Lift']
    # Sum up gross weekly load
    df_weekly_load = df_lift.groupby(df_eight_weeks['Week'])['Load_col_int'].sum()
    # Get net weekly load
    df_weekly_load_net = df_weekly_load - unit_weight
    # Get net weekly load in ton
    df_weekly_load_net_ton = df_weekly_load_net / 1000
    # Calculate the mass per hr weekly
    df_mass_lift_per_hr = df_weekly_load_net_ton/Total_Time_week_hr


    # In[30]:


    # Plot setting
    figsize_width = 7
    figsize_hight = 5
    fontsize = 14

    # Drawing
    fig, ax = plt.subplots()   
    df_mass_lift_per_hr.plot.bar(figsize=(figsize_width,figsize_hight),color=roborigger_blue)

    # Set up labels and ticks
    plt.ylabel('Mass Lifted Per Hour (t)', fontsize=xy_label)
    plt.xlabel('Week',fontsize=xy_label)

    # Make spines invisible
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Set up grid
    plt.grid(axis = 'y')

    ax.tick_params(axis='both', labelsize=tickSize)
    plt.xticks(list(range(len(range(1,9)))), range(1,9), rotation = 0)
    # plt.title('Weekly Mass Lifted Per Hour', fontsize=titleSize)
    # Save the plot
    plt.savefig(plot_dir + plot_name, bbox_inches=bbox_inches, dpi=dpi)


    # # 09 Average mass per lift last 8 weeks

    # In[31]:


    # Draw average_mass_per_lift_last_8_weeks.png
    plot_name = 'average_mass_per_lift_last_8_weeks.png'


    # In[32]:


    # Pick up Load Lift Event in last eight weeks
    df_weekly_lift = df_eight_weeks.groupby(df_weeks_lift['Week']).count()[Load_col]
    # Sum up gross weekly load
    df_weekly_load = df_lift.groupby(df_eight_weeks['Week'])['Load_col_int'].sum()
    # Get net weekly load
    df_weekly_load_net = df_weekly_load - unit_weight
    # Get net weekly load in ton
    df_weekly_load_net_ton = df_weekly_load_net / 1000
    # Calculate mass per lift
    df_average_mass_per_lift = df_weekly_load_net_ton / df_weekly_lift


    # In[33]:


    # Plot setting
    number_fontsize= 100
    figsize_width = 8
    figsize_hight = 5
    plt.rcParams['font.size'] = 26.0

    # Drawing
    fig, ax = plt.subplots()
    df_average_mass_per_lift.plot.bar(figsize=(figsize_width,figsize_hight), color=roborigger_blue)

    # Make spines invisible
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Set up labels and ticks
    plt.xticks(rotation = 0)
    plt.ylabel('Mass (t)',fontsize=xy_label)
    plt.xlabel('Week',fontsize=xy_label)

    plt.grid(axis = 'y')
    ax.tick_params(axis='both', labelsize=tickSize)
    plt.xticks(list(range(len(range(1,9)))), range(1,9), rotation = 0)
    # plt.title('Average Mass Lifted Per Week', fontsize=titleSize)
    # Save the plot
    plt.savefig(plot_dir + plot_name, bbox_inches=bbox_inches, dpi=dpi)


    # # 10 Mass lift per week last 8 weeks

    # In[34]:


    # Draw mass_lifted_per_week_last_8_weeks.png
    plot_name = 'mass_lifted_per_week_last_8_weeks.png'


    # In[35]:


    # Pick up Load Lift Event in eight week dataframe
    df_weekly_lift = df_eight_weeks.groupby(df_weeks_lift['Week']).count()[Load_col]
    # Sum up gross weekly load
    df_weekly_load = df_lift.groupby(df_eight_weeks['Week'])['Load_col_int'].sum()
    # Get net weekly load
    df_weekly_load_net = df_weekly_load - unit_weight
    # Get net weekly load in ton
    df_weekly_load_net_ton = df_weekly_load_net / 1000


    # In[36]:


    # Plot parameter
    number_fontsize= 100
    figsize_width = 8
    figsize_hight = 5
    plt.rcParams['font.size'] = 26.0
    # Drawing
    fig, ax = plt.subplots()
    df_weekly_load_net_ton.plot.bar(figsize=(figsize_width,figsize_hight), color=roborigger_blue)

    # Make spines invisible
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Set up labels and ticks
    plt.ylabel('Total Mass (t)',fontsize=xy_label)
    plt.xlabel('Week',fontsize=xy_label)
    ax.tick_params(axis='both', labelsize=tickSize)
    plt.xticks(list(range(len(range(1,9)))), range(1,9), rotation = 0)

    plt.grid(axis = 'y')

    # plt.title('Total Mass Lifted Per Week', fontsize=titleSize)
    # Save the plot
    plt.savefig(plot_dir + plot_name, bbox_inches=bbox_inches, dpi=dpi)


    # # 14 Load level percentage

    # In[37]:


    # Draw loading_level_percentage.png
    plot_name = 'loading_level_percentage.png'


    # In[38]:


    # Set goal
    goal=[45,20,30,5]

    # Probability array for load over HEAVY KG for each week
    over=[]
    # Probability array for load Between LIGHT and HEAVY KG for each week
    between=[]
    # Probability array for load Between GROUND and LIGHT KG for each week
    under=[]
    # Probability array for GROUND for each week
    ground=[]

    for week in eight_weeks:
        # Total event in the weeks
        total = df_eight_weeks.loc[(df_eight_weeks['Week'] == week)].shape[0]
        # Probability array for load over HEAVY KG for each week
        data1 = df_eight_weeks.loc[(df_eight_weeks['Week'] == week) & (df_eight_weeks['LoadStatus'] == labels[1])].shape[0] / total * 100
        # Probability array for load Between GROUND and LIGHT KG for each week
        data2 = df_eight_weeks.loc[(df_eight_weeks['Week'] == week) & (df_eight_weeks['LoadStatus'] == labels[2])].shape[0] / total * 100
        # Probability array for load Between LIGHT and HEAVY KG for each week
        data3 = df_eight_weeks.loc[(df_eight_weeks['Week'] == week) & (df_eight_weeks['LoadStatus'] == labels[0])].shape[0] / total * 100
        # Probability array for GROUND for each week
        data4 = df_eight_weeks.loc[(df_eight_weeks['Week'] == week) & (df_eight_weeks['LoadStatus'] == labels[3])].shape[0] / total * 100 
        # Append data to array
        over.append(data1)
        under.append(data2)
        between.append(data3)
        ground.append(data4)
        
    # Append goal
    over.append(goal[0])
    under.append(goal[1])
    between.append(goal[2])
    ground.append(goal[3])

    # Keep data type in each array is float
    over = np.array(over,dtype = 'float')
    between = np.array(between,dtype = 'float')
    under = np.array(under,dtype = 'float')
    ground = np.array(ground,dtype = 'float')


    # In[39]:


    # Plot parameters
    figsize_width = 18
    figsize_hight = 5
    fontsize = 20

    # Colors: yellow (between) blue(over) orange(under) grey (ground)
    colors = ['#FFC003','#004099','#ED7F31','#A5A5A5']

    # Draw a cumulative bar chart
    fig, ax = plt.subplots(figsize=(figsize_width, figsize_hight))
    plt.bar(Week_Len,between,width=width,align=align,color=colors[0])
    plt.bar(Week_Len,over,width=width,align=align,bottom=between, color=colors[1])
    plt.bar(Week_Len,under,width=width,align=align,bottom=between+over, color=colors[2])
    plt.bar(Week_Len,ground,width=width,align=align,bottom=over+under+between, color=colors[3])

    # Make spines invisible
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Set up labels and ticks
    array = '1,2,3,4,5,6,7,8, Goal'
    x = array.split(',')
    plt.xticks(Week_Len,x)
    ax.tick_params(labelsize=17)
    plt.ylabel('Percentage (%)',fontsize =14)
    plt.xlabel('Week',fontsize =14)

    # Set Y aix limt
    plt.ylim(0, 100)

    # Set legend
    plt.legend(labels, bbox_to_anchor=(1.0, 0.5,0.3,0.2),ncol=1,fontsize = 20)

    # plt.title('Loading Level Percentage', fontsize=titleSize)

    # Save the plot to plot_dir
    fig.savefig(plot_dir + plot_name, bbox_inches=bbox_inches, dpi=dpi)


    # # part 2

    # # 11 Lift per month

    # In[40]:


    # Draw lifts_per_month.png
    plot_name = 'lifts_per_month.png'


    # In[41]:


    # Pick up Load Lift Event
    df_lift = df_three_months.loc[df_three_months['Event']=='Load Lift']
    # Sum up gross Monthly load
    df_monthly_count = df_lift.groupby(df_three_months['Month']).count()['Load']


    # In[42]:


    # Plot setting
    fontsize = 36
    number_fontsize= 100
    figsize_width = 6
    figsize_hight = 5

    # Drawing
    fig, ax = plt.subplots()
    df_monthly_count.plot.bar(figsize=(figsize_width,figsize_hight), color=roborigger_blue)

    # Make spines invisible
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Set up labels and ticks
    ax.get_yaxis().set_ticks([])
    plt.xticks(rotation = 0)
    plt.ylabel('Lift Count (times)',fontsize=xy_label)
    plt.xlabel('Month',fontsize=xy_label)
    ax.tick_params(axis='both', labelsize=22)

    # Write txt on bars
    for bars in ax.containers:
        ax.bar_label(bars, color = 'green', fontsize=containerFont)
        
    # plt.title('Lifts Per Month', fontsize=titleSize)

    # Save the plot
    plt.savefig(plot_dir + plot_name, bbox_inches=bbox_inches, dpi=dpi)


    # # 12 Lift time per month

    # In[43]:


    # Draw lift_time_per_month.png
    plot_name = 'lift_time_per_month.png'


    # In[44]:


    df_lift_time = df_three_months.loc[(df_three_months['Event']=='Load Lift') | (df_three_months['Event']=='Load Set Down')]
    df_lift_time['group'] = (df_lift_time['Event'].eq('Load Set Down') & df_lift_time['Event'].shift(-1).eq('Load Lift'))[::-1].cumsum()[::-1]
    df_lift_time['diff'] = (df_lift_time[~df_lift_time.duplicated(['Event','group'])].groupby('group')['Timestamp'].transform(lambda d: d.diff()))
    df_lift_time = df_lift_time.query('diff != "NaT"')
    Total_Time = df_lift_time['diff'].groupby(df_three_months['Month']).sum()
    Total_Time = round(Total_Time / np.timedelta64(1, 'h'))


    # In[45]:


    # Plot parameter
    figsize_width = 8
    figsize_hight = 6

    # Drawing
    fig, ax = plt.subplots()
    Total_Time.plot.bar(figsize=(figsize_width,figsize_hight), color=roborigger_blue)

    # Make spines invisible
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Set up labels and ticks
    plt.ylabel('Lift Time (hours)',fontsize=xy_label)
    plt.xlabel('Month',fontsize=xy_label)
    ax.get_yaxis().set_ticks([])
    plt.xticks(rotation = 0)
    ax.tick_params(axis='both', labelsize=22)

    # Write txt on bars
    for bars in ax.containers:
        ax.bar_label(bars, color = 'green', fontsize=containerFont)
        
    # plt.title('Lift Time Per Month', fontsize=titleSize)

    # Save the plot
    plt.savefig(plot_dir + plot_name, bbox_inches=bbox_inches, dpi=dpi)


    # # 13 Mass lifted per month

    # In[46]:


    # Draw mass_lifted_per_month.png
    plot_name = 'mass_lifted_per_month.png'


    # In[47]:


    # Sum up gross Monthly load
    df_monthly_load = df_lift.groupby(df_three_months['Month'])['Load_col_int'].sum()
    # Get net Monthly load
    df_monthly_load_net = df_monthly_load - unit_weight
    # Get net Monthly load in ton
    df_monthly_load_net_ton = round(df_monthly_load_net / 1000)


    # In[48]:


    # Plot setting
    figsize_width = 8
    figsize_hight = 6
    # Drawing
    fig, ax = plt.subplots()
    df_monthly_load_net_ton.plot.bar(figsize=(figsize_width,figsize_hight), color=roborigger_blue)

    # Make spines invisible
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Set up labels and ticks
    plt.ylabel('Mass (t)',fontsize=xy_label)
    plt.xlabel('Month',fontsize=xy_label)
    ax.tick_params(axis='both', labelsize=22)
    ax.get_yaxis().set_ticks([])
    plt.xticks(rotation = 0)

    # plt.title('Mass Per Month', fontsize=titleSize)

    # Write text on bars
    for bars in ax.containers:
        ax.bar_label(bars, color = 'green', fontsize=containerFont)
        
    # Save the plot
    plt.savefig(plot_dir + plot_name, bbox_inches=bbox_inches, dpi=dpi)


    # # 5 Lift time per day

    # In[49]:


    # Draw lift_time_per_day.png
    plot_name = 'lift_time_per_day.png'


    # In[50]:


    df_lift = df.loc[(df['Event']=='Load Lift') | (df['Event']=='Load Set Down')]
    df_lift['group'] = (df_lift['Event'].eq('Load Set Down') & df_lift['Event'].shift(-1).eq('Load Lift'))[::-1].cumsum()[::-1]
    df_lift['diff'] = (df_lift[~df_lift.duplicated(['Event','group'])].groupby('group')['Timestamp'].transform(lambda d: d.diff()))
    df_lift = df_lift.query('diff != "NaT"')
    Total_Time = df_lift['diff'].groupby(df['Day']).sum()
    Total_Time = Total_Time / np.timedelta64(1, 'h')


    # In[51]:


    Total_Time.index = Total_Time.index.astype(int)
    Total_Time_fill = Total_Time.reindex(list(range(1,31)),fill_value=0)


    # In[52]:


    # Plot setting
    figsize_width = 12
    figsize_hight = 5
    mean = Total_Time.sum()/Total_Time.count()
    maxV = Total_Time_fill.count()
    # Drawing
    fig, ax = plt.subplots()
    Total_Time_fill.plot.bar(figsize=(figsize_width,figsize_hight), color=roborigger_blue)

    # Make spines invisible
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Set up labels and ticks
    ax.tick_params(axis='both', labelsize=tickSize, rotation = 0)
    plt.ylabel('Lift Time (hours)',fontsize=xy_label)
    plt.xlabel('Day',fontsize=xy_label)

    plt.grid(axis = 'y')

    # plt.title('Lift Time Per Day', fontsize=titleSize)

    ax.hlines(mean, -1, maxV, linestyles='solid', colors='orangered')
    plt.text(maxV-9, mean+0.2, 'Monthly Average', dict(fontsize=line_label_size, color='orangered'))
    ax.hlines(mean+1, -1, maxV, linestyles='solid', colors='green')
    plt.text(maxV-9, mean+1.2, 'Industry Best', dict(fontsize=line_label_size, color='green'))
    # Save the plot
    plt.savefig(plot_dir + plot_name, bbox_inches=bbox_inches, dpi=dpi)
    plt.show()


    # # 6 Lift time per week last 8 weeks

    # In[53]:


    # Draw lift_time_per_week_last_8_weeks.png
    plot_name = 'lift_time_per_week_last_8_weeks.png'


    # In[54]:


    # Plot parameter
    figsize_width = 7
    figsize_hight = 5
    # Drawing
    fig, ax = plt.subplots()
    Total_Time_week_hr.plot.bar(figsize=(figsize_width,figsize_hight), color=roborigger_blue)

    # Make spines invisible
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Set up labels and ticks
    plt.xticks(rotation = 0)
    ax.tick_params(axis='both', labelsize=tickSize)
    plt.xticks(list(range(len(range(1,9)))), range(1,9))
    plt.ylabel('Lift Time (hours)',fontsize=xy_label)
    plt.xlabel('Week',fontsize=xy_label)

    # plt.title('Lift Time Per Week', fontsize=titleSize)
    plt.grid(axis = 'y')
    # Save the plot
    plt.savefig(plot_dir + plot_name, bbox_inches=bbox_inches, dpi=dpi)


    # # 18 Time per lift Historygram

    # In[55]:


    # Draw time_per_lift_histogram.png
    plot_name = 'time_per_lift_histogram.png'


    # In[56]:


    # Create col with the time before next event
    df['TimeBefore'] = df['Timestamp'].diff().shift(-1)
    # Create col with the time after last event
    df['TimeAfter'] = df['Timestamp'].diff().shift(+1)
    # Create the mode col with (0) Lift time (Lift up -> Set Down)(1) and waiting time (Set Down -> Lift up) (-1)
    df.loc[:,'mode'] = 0
    df.loc[(df['Event']=='Load Lift') & (df['Event'].shift(-1)=='Load Set Down'), 'mode'] = 1
    df.loc[(df['Event']=='Load Set Down') & (df['Event'].shift(-1)=='Load Lift'), 'mode'] = -1

    # Create 'LiftTime' column and initialization
    LiftTime_col = 'LiftTime'
    df.loc[:,LiftTime_col] = 0

    # Create 'TimeBefore' column
    # Add in Lift time and set in seconds and fill na with 0
    df[LiftTime_col] = df.loc[df['mode']==1,'TimeBefore']
    df[LiftTime_col] = df[LiftTime_col].dt.total_seconds()
    df[LiftTime_col] = df[LiftTime_col].fillna(0)


    # In[57]:


    # Set up the time range in sep equal to 1 minute
    time_range = 40
    minutes_label = list(range(time_range))

    for label in minutes_label:
        df.loc[(df[LiftTime_col].astype(int)> label*60) & (df[LiftTime_col].astype(int)<=(label+1)*60), 'TimePerLift'] = label+1
    df.loc[(df[LiftTime_col].astype(int)>(time_range-1)*60), 'TimePerLift'] = time_range

    # Remove the null value
    df_time_per_lift = df[df['TimePerLift'].notnull()]

    # Sort by index(minutes[1:timerange])
    data = df_time_per_lift['TimePerLift'].value_counts().sort_index()

    # Pick up index array (minutes:int) and value array(Lift count)
    data.index = data.index.astype(int)
    index_array = data.value_counts().sort_index().index
    value_array = data.value_counts().sort_index()

    # Set the top spine for the plot
    max_value = data.max()+10

    # Calculate the average time as threshold
    threshold = round((df_time_per_lift['TimePerLift'].sum()/df_time_per_lift['TimePerLift'].count()),2)

    # Setup plot size
    figsize_width = 7
    figsize_hight = 5

    # Drawing
    fig, ax = plt.subplots(figsize=(figsize_width, figsize_hight))
    data.plot.bar(figsize=(figsize_width,figsize_hight), color=roborigger_blue)

    # Make spines invisible
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.vlines(threshold-1, 0, max_value, linestyles='dashed', colors='red')

    # plt.title('Time Taken Per Lift Cycle', fontsize=28)

    plt.text(threshold-0.9, 150, 'Average time', 
            dict(fontsize=20, color='red'),rotation=90)

    low = "{:.0%}".format(round((df_time_per_lift['TimePerLift'].loc[df_time_per_lift['TimePerLift'] > threshold].count()/df_time_per_lift['TimePerLift'].count()),2))
    msg3 = str(low) +  " of lifts took longer than average."
    def_lift_cycle = "(Lift Cycle: the time between one load lift and the next load lift.)"
    # plt.text(-1, -50, msg3, dict(fontsize=23, color=roborigger_blue))
    # plt.text(-1, -70, def_lift_cycle, dict(fontsize=16, color="black"))

    # Set up labels and ticks
    plt.xticks(fontsize=11, rotation = 0)
    plt.yticks(fontsize=tickSize)
    plt.ylabel('Lift Count (times)', fontsize=xy_label)
    plt.xlabel('Lift Cycle Duration (mins)', fontsize=xy_label)
    plt.ylim(0, max_value)

    # Output the plot to plot_dir
    plt.savefig(plot_dir + plot_name,bbox_inches=bbox_inches, dpi=dpi)


    # # 17 Time per lift Exceedance

    # In[58]:


    # Draw time_per_lift_exceedance.png
    plot_name = 'time_per_lift_exceedance.png'


    # In[59]:


    dfex = pd.DataFrame()
    dfex['times'] = data.values
    dfex['count'] = data.index.values
    dfex.set_index('times', inplace=True)


    # In[60]:


    # Plot setting
    figsize_width = 12
    figsize_hight = 5

    # Drawing
    fig, ax = plt.subplots(figsize=(figsize_width, figsize_hight))
    sort = np.sort(dfex)[::-1]
    exceedence = np.arange(1.,len(sort)+1) / len(sort)
    # plt.title('Time Taken Per Lift Cycle ', fontsize=titleSize)
    ax.tick_params(axis='both', labelsize=tickSize)
    plt.plot(sort,exceedence*100,color=roborigger_blue)

    # Make spines invisible
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Set up labels and ticks
    plt.xlabel('Time (mins)', fontsize=23)
    plt.ylabel('% of Time Exceeding', fontsize=23)

    plt.grid(True)
    plt.ylim(0, 100)
    plt.xlim(1, dfex['count'].iloc[-1])
    plt.savefig(plot_dir + plot_name,bbox_inches=bbox_inches, dpi=dpi)
    plt.show()


    # # 20 Time since last lift Historgram

    # In[61]:


    # Draw time_since_last_lift_histogram.png
    plot_name = 'time_since_last_lift_histogram.png'


    # In[62]:


    # Create and initial 'WatingTime' col
    WaitingTime_col = 'WaitingTime'
    df.loc[:,WaitingTime_col] = 0
    df[WaitingTime_col] = df.loc[df['mode']==-1,'TimeAfter']
    df[WaitingTime_col] = df[WaitingTime_col].dt.total_seconds()
    df[WaitingTime_col] = df[WaitingTime_col].fillna(0)

    for label in minutes_label:
        df.loc[(df[WaitingTime_col].astype(int)> label*60) & (df[WaitingTime_col].astype(int)<=(label+1)*60), 'Time since Last Lift'] = label+1
    df.loc[(df[WaitingTime_col].astype(int)>(time_range-1)*60), 'Time since Last Lift'] = time_range

    df_time_since_last_lift = df[df['Time since Last Lift'].notnull()]


    # In[63]:


    threshold2 = round((df_time_since_last_lift['Time since Last Lift'].sum()/df_time_since_last_lift['Time since Last Lift'].count()),2)
    data = df_time_since_last_lift['Time since Last Lift'].value_counts().sort_index()
    max_value = data.max()+10

    # Setup plot size
    figsize_width = 7
    figsize_hight = 5

    # Drawing
    fig, ax = plt.subplots(figsize=(figsize_width, figsize_hight))
    data.index = data.index.astype(int)
    data.plot.bar(figsize=(figsize_width,figsize_hight), color=roborigger_blue)

    # Make spines invisible
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    low2 = "{:.0%}".format(round((df_time_since_last_lift['Time since Last Lift'].loc[df_time_since_last_lift['Time since Last Lift'] > threshold2].count()/df_time_since_last_lift['Time since Last Lift'].count()),2))
    msg4 = str(low2) + " of operations took a long gap in between."
    # plt.title('Idle Time Between Lifts', fontsize=28)
    # plt.text(-1, -50, msg4, dict(fontsize=23, color=roborigger_blue))
    def_idle_time = "(Idle Time”: time taken when hook is available to when lift occurs.)"
    # plt.text(-1, -70, def_idle_time, dict(fontsize=16, color="black"))
    plt.ylim(0, max_value)
    ax.vlines(threshold2-1, 0, max_value, linestyles='dashed', colors='red')
    plt.text(threshold2-1, 144, 'Average time', 
            dict(fontsize=20, color='red'),rotation=90)

    # Set up labels and ticks
    plt.xticks(fontsize=11, rotation = 0)
    plt.yticks(fontsize=tickSize)
    plt.ylabel('Lift Count (times)', fontsize=xy_label)
    plt.xlabel('Idle Time (mins)', fontsize=xy_label)

    # Save the plot to plot_dir
    plt.savefig(plot_dir + plot_name,bbox_inches=bbox_inches, dpi=dpi)


    # # 19 Time since last lift Excedence

    # In[64]:


    # Draw time_since_last_lift_exceedance.png
    plot_name = 'time_since_last_lift_exceedance.png'


    # In[65]:


    dfex2 = pd.DataFrame()
    dfex2['times'] = data.values
    dfex2['count'] = data.index.values
    dfex2.set_index('times', inplace=True)


    # In[66]:


    # Drawing
    figsize_width = 12
    figsize_hight = 5

    fig, ax = plt.subplots(figsize=(figsize_width, figsize_hight))
    sort = np.sort(dfex2)[::-1]
    exceedence = np.arange(1.,len(sort)+1) / len(sort)

    ax.tick_params(axis='both', labelsize=tickSize)
    plt.plot(sort, exceedence*100,color=roborigger_blue )

    # Make spines invisible
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Set up labels and ticks
    plt.xlabel('Idle Time (mins)', fontsize=23)
    plt.ylabel('% of Time Exceeding', fontsize=23)

    plt.grid(True)
    plt.ylim(0, 100)
    plt.xlim(1, dfex2['count'].iloc[-1])

    # plt.title('Idle Time Between Lifts', fontsize=titleSize)

    plt.savefig(plot_dir + plot_name,bbox_inches=bbox_inches, dpi=dpi)
    plt.show()


    # # 15 Percentage of Time with Load on Hook

    # In[67]:


    # Draw percentage_of_time_with_load_on_hook.png
    plot_name = 'percentage_of_time_with_load_on_hook.png'


    # In[68]:


    # Generate a new 'LoadStatus' column with labelled load data
    # Load classification (kg)
    unit_weight = 750

    # Labels
    # With Load:'Operating: in air with load' No Load:'Idle: in air with no load'
    labels = ['Operating: in air with load','Idle: in air with no load']

    # Create 'InAir' column and
    # when the load data greater than unit weight define as with load
    df.loc[(df[Load_col].astype(int) > unit_weight), 'InAir'] = labels[0]
    # when the load data less than unit weight define as no load
    df.loc[(df[Load_col].astype(int) <= unit_weight), 'InAir'] = labels[1]


    # In[69]:


    # Pick up date infomation from current month dataframe
    dates = df['Date'].value_counts().index.sort_values()
    Date = df['Date'].value_counts().shape[0]

    # Generate daily probability array for load
    # Probability array for 'with load' daily
    with_load_daily=[]
    # Probability array for 'no load' daily
    no_load_daily=[]

    # Generate the dataframe with total date for current month
    df_all_date = pd.DataFrame({"all_date":pd.date_range(df['Date'].values[1], df['Date'].values[len(df['Date'])-1], freq='D')})
    df_all_date["all_date"] = pd.to_datetime(df_all_date["all_date"]).dt.date
    # Count total dates in current month
    Dates_Len = np.arange(len(df_all_date))

    # Calculate the percentage
    for date in df_all_date['all_date']:
        if (date in dates):
            total = df.loc[(df['Date'] == date)].shape[0]
            # Calculate with load percentage
            data1 = df.loc[(df['Date'] == date) & (df['InAir'] == labels[0])].shape[0] / total * 100
            # Calculate no load percentage
            data2 = df.loc[(df['Date'] == date) & (df['InAir'] == labels[1])].shape[0] / total * 100
        else:
            # If there are not data in the date put with load 
            data1 = 0
            data2 = 100
        # Add into arrays
        with_load_daily.append(data1)
        no_load_daily.append(data2)


    # Count work days    
    day_used = 0

    for no_load in no_load_daily:
        if (no_load < 100):
            day_used += 1

    # Keep data type in each array is float
    with_load_daily = np.array(with_load_daily,dtype = 'float')
    no_load_daily = np.array(no_load_daily,dtype = 'float')


    # In[70]:


    # Plot parameters
    figsize_width = 12
    figsize_hight = 5
    colors = ['#004099','#FFC003']
    fontsize = 14

    # Draw a cumulative bar chart
    fig, ax = plt.subplots(figsize=(figsize_width, figsize_hight))
    plt.bar(Dates_Len,with_load_daily,width=width,align=align,color=colors[0])
    plt.bar(Dates_Len,no_load_daily,width=width,align=align,bottom=with_load_daily, color=colors[1])

    # Make spines invisible
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Set up labels and ticks
    plt.ylabel('Percentage (%)',fontsize=xy_label)
    plt.xticks(Dates_Len,Dates_Len+1)
    ax.tick_params(axis='both', labelsize=tickSize)

    # Set range of y aixs
    plt.ylim(0, 100)

    # Set legend
    plt.legend(labels, bbox_to_anchor=(0.8, -0.15,0.2,0.1),ncol=2,fontsize=20)

    # plt.title('Hours Per Day with Load on Hook', fontsize=titleSize)

    # Save the plot to plot_dir
    fig.savefig(plot_dir + plot_name, bbox_inches=bbox_inches, dpi=dpi)


    # # 16 Time in air with load, no load weekly last 8 weeks

    # In[71]:


    # Draw operating_vs_idle_last_8_weeks.png
    plot_name = 'operating_vs_idle_last_8_weeks.png'


    # In[72]:


    # Generate a new 'LoadStatus' column with labelled load data
    # Load classification (kg)
    unit_weight = 750

    # Labels
    # with load:'Operating: in air with load', no load:'Idle: in air with no load'
    labels = ['Operating: in air with load','Idle: in air with no load']


    # when the load data greater than unit weight define as with load
    df_eight_weeks.loc[(df_eight_weeks[Load_col].astype(int) > unit_weight), 'InAir'] = labels[0]
    # when the load data less than unit weight define as no load
    df_eight_weeks.loc[(df_eight_weeks[Load_col].astype(int) <= unit_weight), 'InAir'] = labels[1]


    # In[73]:


    # Count the length of week
    Week = df_eight_weeks['Week'].value_counts().shape[0]
    Week_Len = np.arange(Week)

    # Generate Probability array for load for each week
    # Probability array for with load weekly
    with_load_weekly=[]
    # Probability array for no load weekly
    no_load_weekly=[]

    # Calculate the percentage
    for week in eight_weeks:
        # 
        total = df_eight_weeks.loc[(df_eight_weeks['Week'] == week)].shape[0]
        # Calculate with load percentage
        data1 =df_eight_weeks.loc[(df_eight_weeks['Week'] == week) & (df_eight_weeks['InAir'] == labels[0])].shape[0] / total * 100
        # Calculate no load percentage
        data2 = df_eight_weeks.loc[(df_eight_weeks['Week'] == week) & (df_eight_weeks['InAir'] == labels[1])].shape[0] / total * 100
        # Add into arrays
        with_load_weekly.append(data1)
        no_load_weekly.append(data2)

    # Keep data type in each array is float
    with_load_weekly = np.array(with_load_weekly,dtype = 'float')
    no_load_weekly = np.array(no_load_weekly,dtype = 'float')


    # In[74]:


    # Plot parameters
    figsize_width = 7
    figsize_hight = 5
    colors = ['#004099','#FFC003']
    fontsize = 14
    # Draw a cumulative bar chart
    fig, ax = plt.subplots(figsize=(figsize_width, figsize_hight))

    # Make spines invisible
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.bar(Week_Len,with_load_weekly,width=width,align=align,color=colors[0])
    plt.bar(Week_Len,no_load_weekly,width=width,align=align,bottom=with_load_weekly, color=colors[1])

    #plt.title('Daily Activity')

    # Set up labels and ticks
    plt.ylabel('Percentage (%)',fontsize=xy_label)
    plt.xticks(Week_Len,Week_Len+1)
    ax.tick_params(axis='both', labelsize=tickSize)

    # Set up y aixs range
    plt.ylim(0, 100)

    # Set up legend
    plt.legend(labels, bbox_to_anchor=(0.7, -0.3,0.3,0.2),ncol=2,fontsize=13.5)


    # plt.title('Operating Vs. Idle Last 8 Weeks', fontsize=titleSize)

    # Output the plot to plot_dir
    fig.savefig(plot_dir + plot_name, bbox_inches=bbox_inches, dpi=dpi)


    # In[75]:


    import json


    # In[76]:


    # Total Lift Weight (t)
    total_lift_weight = df_monthly_load_net_ton.iloc[-1].round(0).astype(int).astype(str)
    print(total_lift_weight)


    # In[77]:


    # Total Lift Count
    total_lift_count = df_monthly_count.iloc[-1].astype(int).astype(str)
    print(total_lift_count)


    # In[78]:


    # Total Lift Time 
    total_lift_time = Total_Time.sum().astype(int).astype(str)
    print(total_lift_time)


    # In[79]:


    # Start date and end date
    start_date = np.datetime64(df['Date'].head(1).iloc[0]).astype(str)
    end_date = np.datetime64(df['Date'].tail(1).iloc[0]).astype(str)


    # In[80]:


    # Find abnormal data
    data_lift = df.sort_values(by=['LiftTime'],ascending=False)[:2]
    data_waiting = df.sort_values(by=['WaitingTime'],ascending=False)[:2]
    df_abnormal = pd.concat([data_lift,data_waiting])
    df_abnormal.drop(columns=['Control Mode','Coolant Temperature','Motor Temp'])
    data_abnormal = json.loads(df_abnormal.to_json(orient='records'))


    # In[81]:


    # JSON file framwwork
    outputJSON = {
        "partc":data_abnormal,
        "datavalue":[],
    }


    # In[82]:


    total_days = len(df_all_date)
    sundays = np.busday_count(start_date, end_date,weekmask='Sun')
    saterdays = np.busday_count(start_date, end_date,weekmask='Sat')
    weekends = (int(saterdays) + int(sundays))
    rdo_sunday_holiday = sundays
    days_available = (total_days - int(rdo_sunday_holiday) - int(weather))

    datavalue = json.loads('{' 
                    + '"Total_lift_weight":'+ '"' + str(total_lift_weight) + '"'+ ',' 
                    + '"Total_lift_count":' + '"' + str(total_lift_count) + '"' + ','
                    + '"Total_lift_time":'+ '"' + str(total_lift_time) + '"' + ','
                    + '"Total_days":' + '"' + str(total_days) + '"' + ','
                    + '"RDO_sunday_holiday":' + '"' + str(rdo_sunday_holiday) + '"' + ','
                    + '"Weather":' + '"' + str(weather) + '"' + ','
                    + '"Days_available":' + '"' + str(days_available) + '"' + ','
                    + '"Day_used":' + '"' + str(day_used) + '"' + ','
                    + '"weekends":'+ '"' + str(weekends) + '"' + ','
                    + '"Start_date":'+ '"' + str(start_date) + '"' + ','
                    + '"End_date":'+ '"' + str(end_date) + '"'
                    + '}')
    outputJSON["datavalue"].append(datavalue)
    print(outputJSON)
    # Wirte JOSN data to files
    with open('./static/json/data.json', 'w') as f:
        json.dump(outputJSON, f)


    # In[ ]:





    # In[ ]:




