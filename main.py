import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
import plotly.graph_objects as go

from plotly.subplots import make_subplots

data= pd.read_csv("russia_losses_equipment.csv")
df= pd.read_csv("russia_losses_personnel.csv")

#MERGING BOTH THE DATAFRAME.
data= pd.merge(data,df, on='date', how='inner' )

#DROPPING UNNECESSARY COLUMNS.
data.drop(columns=['day_x','personnel*'], inplace=True)

#RENAMING THE COLUMN.
data.rename(columns={"day_y":"War_day"}, inplace=True)

#CHANGING THE FORMAT
data['date']=pd.to_datetime(data['date'])

#DATA REFINING

data['vehicles and fuel tanks']=data['vehicles and fuel tanks'].replace(np.nan, 0)
data['military auto']= data['military auto'].replace(np.nan,0)
data['fuel tank']= data['fuel tank'].replace(np.nan,0)

data['mobile SRBM system']= data['mobile SRBM system'].replace(np.nan, 0)
data['cruise missiles']= data['cruise missiles'].replace(np.nan,0)


#COMBINING THE DATA
data['vehicles and fuel tanks']= data['military auto']+data['fuel tank']+data['vehicles and fuel tanks']
data['cruise missiles']= data['cruise missiles']+data['mobile SRBM system']

data['cruise missiles']=data['cruise missiles'].replace(0, np.nan)

#DROPPING NOT USEFUL COLUMNS
data.drop(columns= ['mobile SRBM system','military auto','fuel tank'], inplace=True)

#Our data is cumulative data so, converting it into individual values
cum_sum= ['aircraft','helicopter','tank','APC','field artillery','MRL','drone','naval ship','anti-aircraft warfare',
          'vehicles and fuel tanks','personnel','POW']

for i in cum_sum:
    data[i]= data[i].diff().fillna(data[i].iloc[0]).astype(int)

data.loc[585,'aircraft']=0
data.loc[457,'tank']=0
data.loc[230,'APC']=0

#WEBSITE CREATION
st.sidebar.title("Select An Option.")
user_input= st.sidebar.radio(
    "",
    ("Data Overview","Ariel Losses","Navel Losses","Personnel Losses","Multi- Domain Integrated Force Losses","Strategic Firepower and Support Division Losses")
)
if user_input=='Data Overview':
    st.title("RUSSIAN WAR LOSSES (UKRAIN RUSSIS WAR)")
    st.divider()
    st.header("Project Overview and Data Description.")
    st.write(" ")
    st.write(" ")
    st.write("Embarking on a profound exploration, this project meticulously analyzes "
             "Russia's military losses throughout the Ukraine war, unraveling the intricate threads of conflict. "
             "Through a chronological lens, I tried to observe the evolving dynamics on diverse fronts, portraying the "
             "trajectory of Russia's diminishing military loss and casualies over time. Graphical representations further "
             "illuminate the nuanced patterns, providing a visual grasp of the shifting landscapes. Beyond data points,"
             " At its core, this project is not merely an analysis but a contribution to the global understanding of the"
             " Russia-Ukraine conflict. By shedding light on the military losses sustained by Russia,I aimed to foster a"
             " more informed discourse that transcends borders and perspectives."
             "In a world fraught with uncertainty, this project stands as a beacon of clarity, offering a comprehensive"
             " examination of Russia's military losses in the Ukraine war. This project strives to foster a more "
             "informed discourse on the Russia-Ukraine war, encapsulating the essence of a conflict that resonates far"
             " beyond national borders. By shedding light on the intricacies of military losses, I seek to facilitate "
             "a deeper understanding of the human, strategic, and geopolitical dimensions of this ongoing struggle,"
             " urging a collective effort towards peace and resolution.")
    st.divider()
    st.header("Data Description")
    st.write(" ")
    st.write(" ")
    data_dsc = {
        "Content": ["Date", "Aircraft", "Helicopter", "Tank", "APC", "Field Artillery", "MRL", "Drone", "Naval Ship", \
                    "Anti-Aircraft Warfare", "Special Equipment", "Greatest Losses Direction",
                    "Vehicles And Fuel Tanks", \
                    "Cruise Missiles", "Submarines", "War_day", "Personnel", "POW"],

        "Description": ["Date from  25th of februray to  21st Januray 2024 ", \
                        "Fighter Aircraft Loss by Russia.", \
                        "Helicopter Lost by Russia.", \
                        "Tanks Lost by Russia.", \
                        "Armored Personnel Carrier(APC), is a military vehicle designed and built to transport troops and their equipment in a protected environment.", \
                        "Military artillery that is designed to support and enhance the maneuverability and effectiveness of ground forces on the battlefield.field artillery is specifically configured for mobility and rapid deployment on the front lines of a conflict.", \
                        "Multiple Rocket Launcher(MRL)is a type of military artillery system that can launch multiple rockets in rapid succession. an MRL can saturate an area with a rapid and simultaneous barrage of rockets.", \
                        "Includes both [UAV(Unmanned Aerial Vehicle),RPA(Remotely Piloted Aircraft)]", \
                        "Includes Navy Warships and War boats.", \
                        "Anti-aircraft warfare (AAW) refers to the military tactics, techniques, and equipment designed to defend against and neutralize aerial threats, it inlcudes Anti-Aircraft Artillery, Surface-to-Air Missiles (SAMs),Electronic Warfare (EW) etc.", \
                        "Refer to a wide range of military hardware and technology used in the conflict. This includes specialized equipment designed for various purposes, such as reconnaissance, communication, electronic warfare, and specific combat scenarios.", \
                        "Region In which Russia Suffered Greatest loss.", \
                        "Refers to a combination of transportation equipment and the containers that store fuel for these vehicles.", \
                        "These  are guided missiles that are designed for long-range, precision strikes against specific targets.cruise missiles fly at relatively low altitudes, often hugging the terrain to avoid detection and interception.", \
                        "Navy Submarines", \
                        "Day count of war , with 25th February the day 1.", \
                        "Human Casualties in war.", \
                        "Prisoner of War (POW) has not been tracked since 2022-04-28 "]
    }

    for i in range(18):
        st.subheader(data_dsc["Content"][i])
        st.write(data_dsc["Description"][i])
        st.write("")


if user_input=='Ariel Losses':
    st.header("Russian Militray Ariel Losses")
    st.divider()
    col1, col2, col3 = st.columns(3)
    ariel_df = data.loc[:, ['date', 'aircraft', 'helicopter', 'drone','greatest losses direction']]
    ariel_df['Combined_ariel_loss'] = ariel_df['aircraft'] + ariel_df['helicopter'] + ariel_df['drone']
    ariel_df['year'] = ariel_df['date'].dt.year
    with col1:
        st.subheader("***Total Fighter Aircraft Lost***")
        st.subheader(data['aircraft'].sum())
    with col1:
        st.subheader("***Total Helicopter Lost***")
        st.subheader(data['helicopter'].sum())
    with col3:
        st.subheader("***Total fighter Drone Lost***")
        st.subheader(data['drone'].sum())
    st.divider()

    #line chart for combined loss
    fig = px.line(ariel_df, x="date", y="Combined_ariel_loss", title='COMBINED ARIEL LOSSES FOR RUSSIA',height= 600, width= 1000)
    st.plotly_chart(fig)
    st.divider()

    #line chart showing individual loss over time
    traces = []
    for column in ['aircraft', 'helicopter', 'drone']:
        trace = go.Scatter(x=ariel_df['date'], y=ariel_df[column], mode='lines', name=column)
        traces.append(trace)
    layout = go.Layout(title='Russian Military Aviation Losses: Tracking Aircraft, Drones, and Helicopters',
                       xaxis=dict(title='X-axis'),
                       yaxis=dict(title='Y-axis'),
                       legend=dict(x=1, y=1), height= 600, width= 1100)
    fig = go.Figure(data=traces, layout=layout)
    st.plotly_chart(fig)
    st.divider()

    #bar chart showing red area for  aircraft, helicopter , drone loss over time
    df_a = ariel_df.groupby('greatest losses direction')[['aircraft', 'helicopter', 'drone']].sum().reset_index()
    aircraft = df_a.sort_values(by='aircraft', ascending=False).head(10)
    helicopter = df_a.sort_values(by='helicopter', ascending=False).head(10)
    drone = df_a.sort_values(by='drone', ascending=False).head(10)
    fig = make_subplots(rows=1, cols=3)
    fig.add_trace(go.Bar(x=aircraft['greatest losses direction'], y=aircraft['aircraft'].values, name='Aircraft Lost'),
                  row=1, col=1)
    fig.add_trace(
        go.Bar(x=helicopter['greatest losses direction'], y=helicopter['helicopter'].values, name='Helicopter Lost'),
        row=1, col=2)
    fig.add_trace(go.Bar(x=drone['greatest losses direction'], y=drone['drone'].values, name='Drone Lost'), row=1,
                  col=3)
    fig.update_layout(title_text='Red Zone for Russian Airforce', showlegend=True, height= 600, width=1100)
    st.plotly_chart(fig)
    st.divider()

    #bar chart
    df = ariel_df.groupby("year")[['aircraft', 'helicopter', 'drone']].sum().reset_index()
    df['Combined'] = df['aircraft'] + df['helicopter'] + df['drone']
    df_long = pd.melt(df, id_vars=['year'], var_name='category', value_name='count')

    fig = px.bar(df_long, x="year", y="count", color='category', title="Year wise comparison of losses",height= 500, width=1000)
    st.plotly_chart(fig)

if user_input =='Navel Losses':
    st.header("Russian Navel Losses.")
    st.divider()
    navel_df = data[['date', 'naval ship', 'submarines']]
    navel_df['sub'] = navel_df['submarines'].replace(np.nan, 0)
    navel_df['Combined'] = navel_df['naval ship'] + navel_df['sub']
    navel_df['year'] = navel_df['date'].dt.year
    navel_df['Year'] = navel_df['date'].dt.year
    navel_df['Month'] = navel_df['date'].dt.month_name()
    df = navel_df.groupby('year')[['naval ship', 'sub', 'Combined']].sum().reset_index()
    df_long = pd.melt(df, id_vars=['year'], var_name='Combined', value_name='count')
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("***Total Naval Assets Lost***")
        st.subheader(navel_df["Combined"].sum())
    with col2:
        st.subheader("***Total Naval Ship lost***")
        st.subheader(navel_df['naval ship'].sum())
    with col3:
        st.subheader("***Total Submarine Lost***")
        st.subheader(navel_df['sub'].sum())

    #LINE CHART FOR THE COMBINED NAVY LOSS FOR RUSSIA
    st.divider()
    fig = px.line(navel_df, x="date", y="Combined", title='Combined naval loss for Russia')
    fig.update_layout(showlegend=False, height=400, width=1000)
    st.plotly_chart(fig)

    #BAR CHART FOR YEAR WISE COMPARISON OF LOSSES
    st.divider()
    colors = ['#66b3ff', '#99ff99', '#ffcc99']
    fig = px.bar(df_long, x="year", y="count", color='Combined', title="Year wise Comparison of Losses",color_discrete_sequence=colors)
    fig.update_layout(height=450, width=900)
    st.plotly_chart(fig)
    st.divider()

    #BAR CHARTS FOR INDEPTH YEAR WISE LOSS
    n_groupby = navel_df.groupby(['Year', 'Month'])['Combined'].sum().reset_index()
    n_groupby_2022 = n_groupby[n_groupby['Year'] == 2022].sort_values(by='Combined')
    n_groupby_2023 = n_groupby[n_groupby['Year'] == 2023].sort_values(by='Combined')
    n_groupby_2024 = n_groupby[n_groupby['Year'] == 2024].sort_values(by='Combined')
    fig = make_subplots(rows=1, cols=3,subplot_titles=['Naval Assets Loss in 2022', 'Naval Assets Loss in 2023', 'Naval Assets Loss in 2024'])
    fig.add_trace(
        go.Bar(x=n_groupby_2022['Month'], y=n_groupby_2022['Combined'].values, name='2022'), row=1,
        col=1)
    fig.add_trace(go.Bar(x=n_groupby_2023['Month'], y=n_groupby_2023['Combined'], name='2023'),
                  row=1, col=2)
    fig.add_trace(go.Bar(x=n_groupby_2024['Month'], y=n_groupby_2024['Combined'], name='2024'),
                  row=1, col=3)

    fig.update_layout(showlegend=True, height=400, width=1000, title='Navel Assets Loss Year Wise Month Wise')
    st.plotly_chart(fig)
    st.divider()


    #PIE CHART FOR YEAR WISE SHARE OF NAVEL LOSS
    df = df.rename(columns={'Combined': 'Total Loss'})
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    fig = px.pie(df, values='Total Loss', names='year', title='Share of Naval  Assets loss for Russia Year Wise',color_discrete_sequence=colors)
    fig.update_layout( showlegend = True,height=600, width=1100)
    st.plotly_chart(fig)



if user_input=="Personnel Losses":
    st.header("Human Loss for Russia")
    st.divider()
    human_df = data[['date', 'personnel', 'POW', 'greatest losses direction']]
    human_df['year'] = human_df['date'].dt.year
    human_df['prisoners'] = data['POW'].replace(np.nan, 0)
    human_df['Combined Human Loss for Russia'] = human_df['personnel'] + human_df['prisoners']
    st.subheader("***Total Foot soldier Loss for Russia***")
    st.subheader(human_df["Combined Human Loss for Russia"].sum())
    st.divider()


    #LIINE PLOT FOR HUMAN LOSS
    traces = []
    for column in ['personnel', 'POW', 'Combined Human Loss for Russia']:
        trace = go.Scatter(x=human_df['date'], y=human_df[column], mode='lines', name=column)
        traces.append(trace)
        layout = go.Layout(title='Russian Infnatary Loss: Tracking martyr, Prisoner of war(POW)',
                           xaxis=dict(title='X-axis'),
                           yaxis=dict(title='Y-axis'),
                           legend=dict(x=1, y=1), height=600, width=1100)
    fig = go.Figure(data=traces, layout=layout)
    st.plotly_chart(fig)
    st.divider()

    #BAR CHART FOR RED ZONE FOR HUMAN CASUALTIES
    new_df = human_df.groupby('greatest losses direction')[
        'Combined Human Loss for Russia'].sum().reset_index().sort_values(by="Combined Human Loss for Russia",
                                                                          ascending=False).head(20)
    plt.figure(figsize=(10,10))
    fig = px.bar(new_df, x='greatest losses direction', y='Combined Human Loss for Russia', title='Red Zone Area for human Casualties.', text_auto='.2s',color='Combined Human Loss for Russia')
    fig.update_layout(width=1000, height=600)
    st.plotly_chart(fig)
    st.divider()

    st.text("NO DATA AVAILABLE FOR POW(PRISONER OF WAR) SINCE APRIL 23, 2022")

if  user_input=="Multi- Domain Integrated Force Losses":
    st.header("Multi- Domain Integrated Force Losses")
    st.divider()
    multi_domain = data[
        ['date', 'tank', 'APC', 'cruise missiles', 'anti-aircraft warfare', 'greatest losses direction']]
    multi_domain["cruise missiles"] = multi_domain["cruise missiles"].replace(np.nan, 0)
    multi_domain['cruise missiles'] = multi_domain['cruise missiles'].diff().fillna(
        multi_domain['cruise missiles'].iloc[0])

    col1,col2= st.columns(2)
    col3,col4= st.columns(2)

    with col1:
        st.subheader("***Total Tank Lost***")
        st.subheader(multi_domain["tank"].sum())

    with col2:
        st.subheader("***Armored Personal Car Loss***")
        st.subheader(multi_domain["APC"].sum())

    with col3:
        st.subheader("***Total Missile Loss***")
        st.subheader(multi_domain["cruise missiles"].sum())

    with col4:
        st.subheader("***Total anti-aircraft warfare***")
        st.subheader(multi_domain["anti-aircraft warfare"].sum())

    st.divider()

    #LINE CHART
    traces = []
    for column in ["tank", "APC", "cruise missiles","anti-aircraft warfare"]:
        trace = go.Scatter(x=multi_domain['date'], y=multi_domain[column], mode='lines', name=column)
        traces.append(trace)
        layout = go.Layout(title='Russian  Multi_domain Integrated force Loss',
                           xaxis=dict(title='X-axis'),
                           yaxis=dict(title='Y-axis'),
                           legend=dict(x=1, y=1), height=600, width=1100)
    fig = go.Figure(data=traces, layout=layout)
    st.plotly_chart(fig)
    st.divider()


    #BAR CHART
    st.subheader("Bastion of Defense Devastation")
    new_df = multi_domain.groupby('greatest losses direction')[
        ['tank', 'APC', 'cruise missiles', 'anti-aircraft warfare']].sum().reset_index()
    fig = make_subplots(rows=1, cols=4, subplot_titles=['Tank', 'APC', 'cruise missiles', 'anti-aircraft warfare'])

    fig.add_trace(
        go.Bar(x=new_df['greatest losses direction'], y=new_df.sort_values(by='tank', ascending=False).head(20)['tank'],
               name='Tank'), row=1, col=1)
    fig.add_trace(
        go.Bar(x=new_df['greatest losses direction'], y=new_df.sort_values(by='APC', ascending=False).head(20)['APC'],
               name='APC'), row=1, col=2)
    fig.add_trace(go.Bar(x=new_df['greatest losses direction'],
                         y=new_df.sort_values(by='cruise missiles', ascending=False).head(20)['cruise missiles'],
                         name='cruise missiles'), row=1, col=3)
    fig.add_trace(go.Bar(x=new_df['greatest losses direction'],
                         y=new_df.sort_values(by='anti-aircraft warfare', ascending=False).head(20)[
                             'anti-aircraft warfare'], name='anti-aircraft warfare'), row=1, col=4)

    fig.update_layout(title_text='Multi domian integrated losses over time', showlegend=False,height=500, width=1000,
                      yaxis=dict(title='count'),
                      xaxis=dict(title='Region'),
                      xaxis2=dict(title='Region'),
                      xaxis3=dict(title='Region'),
                      xaxis4=dict(title='Region'))

    st.plotly_chart(fig)
    st.divider()

    # SHARE OF LOSS OF MULTI-DOMAIN AS PER YEAR
    multi_domain['year'] = multi_domain['date'].dt.year
    multi_domain['month'] = multi_domain['date'].dt.month_name()

    domain_ = st.selectbox(
        "Select Domain",
        ("tank", "APC", "cruise missiles","anti-aircraft warfare")
    )
    mul_df= multi_domain.groupby('year')[domain_].sum().reset_index()
    fig = px.pie(mul_df, values=domain_, names='year', title=f'{domain_} Share of loss with years.')
    fig.update_layout(height=500, width=700)
    st.plotly_chart(fig)



if user_input=="Strategic Firepower and Support Division Losses":
    st.header('Strategic Firepower and Support Division Loss for Russia')
    st.divider()
    strategic_df = data[['date', 'field artillery', 'MRL', 'special equipment', 'vehicles and fuel tanks']]
    strategic_df['Year'] = strategic_df['date'].dt.year
    strategic_df['Month'] = strategic_df['date'].dt.month_name()
    strategic_df['special'] = strategic_df['special equipment'].replace(np.nan, 0)
    strategic_df['special'] = strategic_df['special'].diff().fillna(strategic_df['special'].iloc[0])
    strategic_df['Total loss'] = strategic_df['field artillery'] + strategic_df['MRL'] + strategic_df[
        'vehicles and fuel tanks'] + strategic_df['special']
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        st.subheader("***Total Field Artillery Lost***")
        st.subheader(strategic_df["field artillery"].sum())

    with col2:
        st.subheader("***Total Multiple Rocket Launcher Lost***")
        st.subheader(strategic_df["MRL"].sum())

    with col3:
        st.subheader("***Total Special Equipment Lost***")
        st.subheader(strategic_df["special equipment"].sum())

    with col4:
        st.subheader("***Total Vehicles and Fuel Tanks Lost***")
        st.subheader(strategic_df["vehicles and fuel tanks"].sum())

    st.divider()

    #LINE GRAPH.
    traces = []
    for column in ['field artillery', 'MRL', 'special','vehicles and fuel tanks', 'Total loss']:
        trace = go.Scatter(x=strategic_df['date'], y=strategic_df[column], mode='lines', name=column)
        traces.append(trace)
        layout = go.Layout(title='Russian  Multi_domain Integrated force Loss',
                           xaxis=dict(title='X-axis'),
                           yaxis=dict(title='Y-axis'),
                           legend=dict(x=1, y=1), height=600, width=1100)
    fig = go.Figure(data=traces, layout=layout)
    st.plotly_chart(fig)
    st.divider()


    #BAR CHART

    fig = px.bar(strategic_df, x=strategic_df.groupby("Month")['Total loss'].sum().reset_index().sort_values(by='Total loss')['Month'], y=
    strategic_df.groupby("Month")['Total loss'].sum().reset_index().sort_values(by='Total loss')['Total loss'],
                 title='Month wise loss of strategic Firepower and support division loss for Russia.')

    fig.update_layout(height=600, width=900)
    st.plotly_chart(fig)

    #pie chart
    df = strategic_df.groupby("Year")[
        ['field artillery', 'MRL', 'vehicles and fuel tanks', 'special']].sum().reset_index()

    df_long = pd.melt(df, id_vars=['Year'], var_name='Combined', value_name='count')

    year = st.selectbox(
        "Select Domain",
        ("2022","2023","2024")
    )
    df_long['Year']=df_long['Year'].astype('str')
    fig= px.pie( df_long, values=df_long[df_long['Year']==year]['count'],names=df_long[df_long['Year']==year]['Combined'],
                 title=f'Strategic Firepower and Support Division loss share for the year : {year}')
    st.plotly_chart(fig)















