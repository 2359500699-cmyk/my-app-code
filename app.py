import streamlit as st
import json
import datetime
def load_room_data():
    try:
        with open("roomdata.json", "r",encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("roomdata.json not found. Initializing empty data.")
        data = {}
    return data
def save_room_data(data):
    with open("roomdata.json", "w",encoding="utf-8") as f:
        json.dump(data, f, indent=4,ensure_ascii=False)
st.title("收租小助手")
room_data = load_room_data()
room_id=list(room_data.keys())
selected_room = st.selectbox("选择房间号", room_id)
if selected_room:
    info=room_data[selected_room]
    st.markdown(f"### 当前操作：{selected_room}房 ({info['姓名']})")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"上月水表读数: {info['上月水表读数']}")
        st.info(f"上月电表读数: {info['上月电表读数']}")
    with col2:
        st.info(f"水费单价: {info['水费单价']} 元/吨")
        st.info(f"电费单价: {info['电费单价']} 元/度")
        curent_water=st.number_input("本月水表读数",min_value=info['上月水表读数'],value=info['上月水表读数'])
        curent_electric=st.number_input("本月电表读数",min_value=info['上月电表读数'],value=info['上月电表读数'])
    if st.button("计算本月费用"):
        water_usage=curent_water - info['上月水表读数']
        electric_usage=curent_electric - info['上月电表读数']
        water_cost=water_usage * info['水费单价']
        electric_cost=electric_usage * info['电费单价']
        total_cost=water_cost + electric_cost + info['租金']
        st.success(f"本月水费: {water_cost} 元")
        st.success(f"本月电费: {electric_cost} 元")
        st.success(f"本月总费用: {total_cost} 元")
        bill_text=f"""
    =={datetime.datetime.now().strftime('%Y年%m月')}账单==
    房间号: {selected_room}房
    姓名: {info['姓名']}
    租金: {info['租金']} 元
    上月水表读数: {info['上月水表读数']} 吨
    本月水表读数: {curent_water} 吨
    本月用水量: {water_usage} 吨
    水费单价: {info['水费单价']} 元/吨
    本月水费: {water_cost} 元
    上月电表读数: {info['上月电表读数']} 度
    本月电表读数: {curent_electric} 度
    本月用电量: {electric_usage} 度
    电费单价: {info['电费单价']} 元/度
    本月电费: {electric_cost} 元
    本月总费用: {total_cost} 元
    管理费: {info['管理费']} 元
    合计费用: {total_cost + info['管理费']} 元
    """
        st.text_area("账单详情",value=bill_text,height=300)
    if st.checkbox("确认已收款/数据无误"):
        if st.button("更新读数为下月初始读数"):
            room_data[selected_room]['上月水表读数']=curent_water
            room_data[selected_room]['上月电表读数']=curent_electric
            save_room_data(room_data)
            st.balloons()
            st.info("已更新本月读数为下月初始读数。")
