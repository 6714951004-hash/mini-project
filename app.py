import streamlit as st
import google.generativeai as genai
import os

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="AI Travel Planner", page_icon="✈️")

# ใส่ API Key (ใน Render เราจะตั้งเป็น Environment Variable)
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    st.title("🌍 AI Personalized Travel Planner")
    st.subheader("วางแผนเที่ยวตามงบแบบเป๊ะๆ")

    # ส่วนรับข้อมูลจากผู้ใช้
    col1, col2 = st.columns(2)
    with col1:
        destination = st.text_input("ไปที่ไหนดี?", placeholder="เช่น ญี่ปุ่น, เชียงใหม่")
        budget = st.number_input("งบประมาณต่อท่าน (บาท)", min_value=0)
    
    with col2:
        days = st.slider("จำนวนวัน", 1, 14, 3)
        travel_style = st.selectbox("สไตล์การเที่ยว", ["สายกิน", "เน้นถ่ายรูป", "ธรรมชาติ", "ลุยๆ"])

    if st.button("Generate My Plan! ✨"):
        prompt = f"""
        จงเป็นนักวางแผนการท่องเที่ยวอาชีพ ออกแบบทริป {destination} 
        ระยะเวลา {days} วัน ด้วยงบประมาณ {budget} บาท (รวมค่าที่พักและเดินทางในเมือง)
        สไตล์ {travel_style} 
        ขอแผนการเดินทางเป็นรายวัน พร้อมประมาณการค่าใช้จ่ายแต่ละวัน และคำแนะนำในการประหยัดงบ
        """
        
        with st.spinner('กำลังคิดแผนเที่ยวสุดเจ๋งให้คุณ...'):
            response = model.generate_content(prompt)
            st.markdown("---")
            st.markdown(response.text)
else:
    st.info("กรุณาใส่ API Key ในแถบด้านซ้ายเพื่อเริ่มใช้งาน")