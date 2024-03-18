import streamlit as st
import graph_data as gp
from pyparsing import empty

# 전제 화면 넓기 지정
st.set_page_config(layout="wide")

LEFT_GAP = 0.2
RIGHT_GAP = 0.2

# 전체 레이아웃
left, con1, right = st.columns([0.15,1.0,0.15])

left,traffic,right = st.columns([0.15,1.0,0.15])
left,t1,right = st.columns([LEFT_GAP,1.0,RIGHT_GAP])
left,t2,t3,right = st.columns([LEFT_GAP,0.6,0.4,RIGHT_GAP])

left,engagement,right = st.columns([0.15,1.0,0.15])
left,e1,e2,e3,e4,right = st.columns([LEFT_GAP,0.2,0.2,0.2,0.2,RIGHT_GAP])
left,e5,right = st.columns([LEFT_GAP,1.0,RIGHT_GAP])

left,system,right = st.columns([0.15,1.0,0.15])
left,s1,s2,right = st.columns([LEFT_GAP,0.5,0.5,RIGHT_GAP])


def main() :
    # 사이드바
    st.sidebar.header("REPORTS")

    # 사이드바에서 각 섹션으로 이동하는 링크 생성
    st.sidebar.markdown("### ABOUT")
    st.sidebar.markdown("### Navigate to")
    st.sidebar.markdown("[Traffic](#traffic)")
    st.sidebar.markdown("[Engagement](#engagement)")
    st.sidebar.markdown("[System](#system)")

    # 여백 부분
    with left :
        empty()

    # 전체 제목    
    with con1 :
        title()
        st.divider()

    # 트레픽 부분
    with traffic :
        st.header(":orange[TRAFFIC]")   
    with t1 :
        traffic_type() 
    with t2 :
        traffic_region()      
    with t3 :
        traffic_map()

    # 활동 부분
    with engagement :
        st.divider()
        st.header(":orange[ENGAGEMENT]")      
    with e1 :
        empty()
    with e2 :
        engagement_session_admin()
    with e3 :
        engagement_session_info()
    with e4 :
        engagement_session_prod()
    with e5 :
        engagement_visitor()


    # 시스템 부분
    with system :
        st.divider()
        st.header(":orange[SYSTEM]")           
    with s1 :
        system_os()
    with s2 :
        system_browser()
    st.divider()

    # 여백부분
    with right :
        empty() 

# 전체 제목  
def title():
    st.title(":blue[User Behavior Analysis] of SHOP-A")
    st.caption('''This website provides a comprehensive web dashboard for Shopping Mall SHOP-A's annual customer traffic analysis, 
               offering actionable insights and interactive graphs visualizations to understand website performance and customer behavior effectively.''')

# 트래픽 타입별 추이 라인 차트
def traffic_type():
    st.subheader("Sources")
    tf_data, top3 =gp.traffic_type_data()
    st.markdown(f'Top 3 Traffic Sources : *{top3[0]}* / *{top3[1]}* / *{top3[2]}*')
    st.plotly_chart(tf_data, use_container_width=True)    

# 트래픽 발생 지역 비율 파이 차트
def traffic_region():
    st.subheader("Came From")
    st.plotly_chart(gp.region_data(), use_container_width=True)

# 트래픽 발생 지역 지도
def traffic_map():
    # 위치 조정
    for i in range(4):
        st.text(" ")
    # 지도 표시
    st.subheader('Map')
    st.caption("Map with Locations of Traffic")
    # 지도 시각화
    traffic_map = gp.region_map_data()
    st.components.v1.html(traffic_map._repr_html_(), width=400, height=400)

# Administrative Page 방문 수, 평균 방문 시간
def engagement_session_admin():
    st.subheader("Administrative Page")
    st.markdown("The number of visits to the administrative page during a specified period and the average time a user spends on the page within a single session")
    admin_count, info_count, prod_count, admin_average_duration, info_average_duration, prod_average_duration = gp.session_data()
    st.success(f"Visit Count: {admin_count}")
    st.success(f"Average Duration: {admin_average_duration:.3}")

# Informational Page 방문 수, 평균 방문 시간
def engagement_session_info():
    st.subheader("Informational Page")
    st.markdown("The number of visits to the informational page during a specified period and the average time a user spends on the page within a single session")
    admin_count, info_count, prod_count, admin_average_duration, info_average_duration, prod_average_duration = gp.session_data()
    st.success(f"Visit Count: {info_count}")
    st.success(f"Average Duration: {info_average_duration:.3}")

# ProductRelated Page 방문 수, 평균 방문 시간
def engagement_session_prod():
    st.subheader("ProductRelated Page")
    st.markdown("The number of visits to the product related page during a specified period and the average time a user spends on the page within a single session")
    admin_count, info_count, prod_count, admin_average_duration, info_average_duration, prod_average_duration = gp.session_data()
    st.success(f"Visit Count: {prod_count}")
    st.success(f"Average Duration: {prod_average_duration:.5}")

# 월별 방문자 타입 스택 차트
def engagement_visitor():
    st.subheader("Returning Visits")
    st.plotly_chart(gp.visitor_type_data(), use_container_width=True)

# os 비율 파이 차트
def system_os():
    st.subheader("OS")
    st.plotly_chart(gp.operating_systems_data(), use_container_width=True)

# 브라우저 비율 파이 차트     
def system_browser():
    st.subheader("Browser")
    st.plotly_chart(gp.browser_data(), use_container_width=True)
	

main()

