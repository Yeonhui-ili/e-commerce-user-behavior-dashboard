import pandas as pd
import numpy as np
from IPython.display import display
import matplotlib.pyplot as plt
import plotly.express as px
import folium

FILE_NAME = 'online_shoppers_intention.csv'

def operating_systems_data():
    df_all = pd.read_csv(FILE_NAME)
    df_all = df_all[['OperatingSystems']]
    
    # 'os' 칼럼의 값에 따라 각 운영 체제(OS)별로 개수를 계산하여 새로운 데이터프레임 생성
    df = df_all['OperatingSystems'].value_counts().reset_index()
    df.columns = ['OperatingSystems', 'count']
    df = df.rename(columns={'OperatingSystems': 'os'})
    
    # 각 os에 새로운 임의의 이름 부여
    os_mapping = {
    1: 'Macintosh',
    2: 'Windows',
    3: 'Android',
    4: 'iOS',
    5: 'Linux',
    6: 'Other',
    7: 'FreeBSD',
    8: 'SunOS'
    }
    df['os'] = df['os'].map(os_mapping)
    fig = px.pie(df, names='os', values='count', title='Percentage of Diffrent OS Used by visitors')
    fig.update_traces(textposition='inside', 
                      textinfo='percent+label',
                      hovertemplate='%{label} : %{percent} (%{value}회)',
                      hole=.3,
                      marker_colors=px.colors.cyclical.Twilight)
    return fig

def browser_data():
    df_all = pd.read_csv(FILE_NAME)
    df_all = df_all[['Browser']]
    # 'Browser' 칼럼의 값에 따라 각 운영 체제(OS)별로 개수를 계산하여 새로운 데이터프레임 생성
    df = df_all['Browser'].value_counts().reset_index()
    df.columns = ['Browser', 'count']
    # 각 Browser에 새로운 임의의 이름 부여
    browser_mapping = {
    1: 'Safari',
    2: 'Google Chrome',
    3: 'Opera',
    4: 'Internet Explorer',
    5: 'Mozilla Firefox',
    6: 'Microsoft Edge',
    7: 'Opera Mini',
    8: 'Android Browser',
    9: 'Vivaldi',
    10: 'Samsung Internet',
    11: 'Brave',
    12: 'Yandex Browser',
    13: 'UC Browser'
    }
    df['Browser'] = df['Browser'].map(browser_mapping)
    fig = px.pie(df, names='Browser', values='count', title='Percentage of Diffrent Browsers Used by visitors')
    fig.update_traces(textposition='inside', 
                      textinfo='percent+label',
                      hovertemplate='%{label} : %{percent} (%{value}회)',
                      hole=.3,
                      marker_colors=px.colors.cyclical.Twilight)
    return fig

def region_data():
    df_all = pd.read_csv(FILE_NAME)

    df_all = df_all[['Region']]

    # 'Region' 칼럼의 값에 따라 각 지역별로 개수를 계산하여 새로운 데이터프레임 생성
    df = df_all['Region'].value_counts().reset_index()
    df.columns = ['Region', 'count']
    
    # 각 Region에 새로운 임의의 이름 부여
    region_mapping = {
    1: 'South Korea',
    2: 'China',
    3: 'Japan',
    4: 'United States',
    5: 'Australia',
    6: 'United Kingdom',
    7: 'France',
    8: 'Canada',
    9: 'Germany'
    }
    df['Region'] = df['Region'].map(region_mapping)
    
    
    fig = px.pie(df, names='Region', values='count', title='Percentage of Diffrent Regions visitors')
    fig.update_traces(textposition='inside', 
                      textinfo='percent+label',
                      hovertemplate='%{label} : %{percent} (%{value}회)',
                      hole=.3,
                      marker_colors=px.colors.cyclical.Twilight)
    return fig

def region_map_data():
    df_all = pd.read_csv(FILE_NAME)
    df_all = df_all[['Region']]

    # 'Region' 칼럼의 값에 따라 각 지역별로 개수를 계산하여 새로운 데이터프레임 생성
    df = df_all['Region'].value_counts().reset_index()
    df.columns = ['Region', 'count']

    # 'Region' 열을 기준으로 오름차순으로 정렬
    df_sorted = df.sort_values(by='Region')
    
    # 각 Region에 새로운 임의의 이름 부여
    region_mapping = {
    1: 'South Korea',
    2: 'China',
    3: 'Japan',
    4: 'United States',
    5: 'Australia',
    6: 'United Kingdom',
    7: 'France',
    8: 'Canada',
    9: 'Germany'
    }
    df_sorted['Region'] = df_sorted['Region'].map(region_mapping)

    # map data 생성 : 위치와 경도 
    map_data = pd.DataFrame({
        'lat' : [36.5, 35.0, 36.0, 39.8, -25.0, 54.0, 46.0, 60.0, 51.0],
        'lon' : [127.5, 105.0, 138.0, -98.5, 135.0, -2.0, 2.0, -110.0, 9.0],
        'name': ['South Korea', 'China', 'Japan', 'United States', 'Australia', 'United Kingdom', 'France', 'Canada', 'Germany'],
        'value': df_sorted['count'] 
    })
    
    # 지도 객체 생성
    traffic_map = folium.Map(
        location=[map_data['lat'].mean(), map_data['lon'].mean()], 
        zoom_start=1)
        

    # 지도에 원형 마커와 값 추가
    for index, row in map_data.iterrows():
        # 원 표시
        folium.CircleMarker(                     
            location=[row['lat'], row['lon']],   
            radius=row['value'] / 100,            
            color='pink',                    
            fill=True,                         
            fill_opacity=0.5                   
        ).add_to(traffic_map)                         

        # 값 표시
        folium.Marker(                           
            location=[row['lat'], row['lon']], 
            icon=folium.DivIcon(
                html=f"<div>{row['name']} {row['value']}</div>"),
        ).add_to(traffic_map) 

    return traffic_map

# 각 traffic_type의 수가 month별로 어떻게 변하는지 보여주는 line 그래프 생성
def traffic_type_data():
    df_all = pd.read_csv(FILE_NAME)

    # 방문한 월, 트래픽 타입 추출
    df = df_all[['Month', 'TrafficType']]

    # 각 행을 1로 설정하여 'Month' 칼럼에 따라 각 'TrafficType'수 계산을 위한 열 추가
    df['Count'] = 1

    # 월별 'TrafficType'의 합산
    df_grouped = df.groupby(['Month', 'TrafficType']).sum().reset_index()

    # 월과 TrafficType의 고유한 값 추출
    months = df['Month'].unique()
    traffic_types = df['TrafficType'].unique()
    
    # 모든 월과 트래픽 타입의 조합을 만들기 위한 틀 생성
    index = pd.MultiIndex.from_product([months, traffic_types], names=['Month', 'TrafficType'])
    template_df = pd.DataFrame(index=index).reset_index()

    # 빈 count 값 0으로 채워서 명시적으로 모든 경우에 대한 count 값 입력
    result_df = pd.merge(template_df, df_grouped, how='left', on=['Month', 'TrafficType']).fillna(0)

    # 각 월별로 방문자 타입의 비율 계산
    result_df['Total'] = result_df.groupby('Month')['Count'].transform('sum')
    result_df['Percentage'] = result_df.apply(lambda row: row['Count'] / row['Total'] * 100 if row['Total'] != 0 else 0, axis=1)

    # 각 TrafficType에 새로운 임의의 이름 부여
    traffic_type_mapping = {
    1: 'Organic Search',
    2: 'Direct Traffic',
    3: 'Referral Traffic',
    4: 'Social Media Traffic',
    5: 'Mobile Traffic',
    6: 'Affiliate Traffic',
    7: 'Review Site Traffic',
    8: 'Mobile Traffic',
    9: 'Forum Traffic',
    10: 'Email Traffic',
    11: 'App Traffic',
    12: 'News Traffic',
    13: 'Paid Search',
    14: 'Content Syndication Traffic',
    15: 'Shopping Comparison Site Traffic',
    16: 'Podcast Traffic',
    17: 'Other Traffic',
    18: 'Webinar Traffic',
    19: 'Deal Site Traffic',
    20: 'Blog Traffic'
    }
    result_df['TrafficType'] = result_df['TrafficType'].map(traffic_type_mapping)

    # x축(월) 순서 지정 
    month_order = ['Feb', 'Mar', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    result_df['Month'] = pd.Categorical(result_df['Month'], categories=month_order, ordered=True)
    result_df = result_df.sort_values(by='Month')

    # 각 traffic 타입의 총 count를 계산
    traffic_type_ranks = result_df.groupby('TrafficType')['Count'].sum()

    # traffictype별 총 count를 기준으로 범례 내림차순 정렬
    sorted_traffic_types = traffic_type_ranks.sort_values(ascending=False).index

    # 라인 그래프 생성
    fig = px.line(result_df, 
                  x='Month', 
                  y='Count', 
                  color='TrafficType',
                  title='Trend of Traffic Types by Month',
                  labels={'Count': 'Number of Traffics'},
                  custom_data='Percentage',
                  category_orders={'TrafficType': sorted_traffic_types}                  
                  )

    fig.update_layout(hovermode="x unified")

    fig.update_traces(hovertemplate='<br>%{y}회(%{customdata[0]:.3}%)'
                    )
    
    # 범례 기준 상위 3개 traffictype의 visible 속성을 True로 설정하고 나머지는 False로 설정
    top = 0
    for trace in fig.data:
        if top < 3:
            trace.visible = True
            top += 1
        else:
            trace.visible = 'legendonly' 
    
    # # 그룹 바 그래프 생성
    # fig = px.bar(top3_df_grouped, x='Month', y='Count', color='TrafficType', text='Percentage', custom_data='Total' ,title='Monthly Visits by Visitor\'s Type',
    #              labels={'Count': 'Number of Visits'}, category_orders={'Month': month_order}, text_auto=True, barmode='stack')

    return fig, sorted_traffic_types[:3]

def visitor_type_data():
    df = pd.read_csv(FILE_NAME)

    # 방문한 월, 방문자 타입 추출
    df = df[['Month','VisitorType']]

    # 각 행을 1로 설정하여 방문자 수 계산을 위한 열 추가
    df['Count'] = 1   

    # 월별 방문자 수 및 방문 타입의 합산
    df_grouped = df.groupby(['Month', 'VisitorType']).sum().reset_index()

    # 각 월별로 방문자 타입의 비율 계산
    df_grouped['Total'] = df_grouped.groupby('Month')['Count'].transform('sum')
    df_grouped['Percentage'] = df_grouped.apply(lambda row: row['Count'] / row['Total'] * 100 if row['Total'] != 0 else 0, axis=1)

    # 월(x축) 순서 지정
    month_order = ['Feb', 'Mar', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # 스택 바 그래프 생성
    fig = px.bar(df_grouped, x='Month', y='Count', color='VisitorType', text='Percentage', custom_data=['Total', 'VisitorType'] ,title='Monthly Visits by Visitor\'s Type',
                 labels={'Count': 'Number of Visits'}, category_orders={'Month': month_order}, text_auto=True, barmode='stack')
    fig.update_traces(textposition='inside', 
                      texttemplate='%{text:.2}%',
                      hoverinfo='text',
                      hovertemplate='Total visitors in %{x} : %{customdata[0]}회<br>%{customdata[1]} in %{x} : %{y}회(%{text:.4}%)'
                      )
    fig.update_layout(hoverlabel=dict(align='left'))
    return fig

def session_data():
    df = pd.read_csv(FILE_NAME)

    # 각 페이지별로 데이터프레임 분할
    admin_df = df[['Administrative', 'Administrative_Duration']]
    info_df = df[['Informational', 'Informational_Duration']]
    prod_df = df[['ProductRelated', 'ProductRelated_Duration']]

    # 각 페이지별 방문수 계산
    admin_count = admin_df['Administrative'].sum()
    info_count = info_df['Informational'].sum()
    prod_count = prod_df['ProductRelated'].sum()

    # 각 페이지별 방문 평균 방문시간 계산
    admin_average_duration = admin_df['Administrative_Duration'].mean()
    info_average_duration = info_df['Informational_Duration'].mean()
    prod_average_duration = prod_df['ProductRelated_Duration'].mean()

    return admin_count, info_count, prod_count, admin_average_duration, info_average_duration, prod_average_duration



df = pd.read_csv(FILE_NAME)

# 각 페이지별로 데이터프레임 분할
admin_df = df[['Administrative', 'Administrative_Duration']]
info_df = df[['Informational', 'Informational_Duration']]
prod_df = df[['ProductRelated', 'ProductRelated_Duration']]

# 각 페이지별 방문수 계산
admin_count = admin_df['Administrative'].sum()
admin_average_duration = admin_df['Administrative_Duration'].mean()
print(type(admin_count))
display(admin_count)

print(type(admin_average_duration))
display(admin_average_duration)