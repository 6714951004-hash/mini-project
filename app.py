import streamlit as st
from groq import Groq
import os

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="AI Travel Planner (Groq)", page_icon="✈️")

# 1. จัดการเรื่อง API Key (ดึงจาก Render)
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    st.warning("⚠️ ไม่พบ API Key: โปรดระบุ GROQ_API_KEY ใน Environment Variable")
    st.stop()

# สร้าง Client ของ Groq
client = Groq(api_key=api_key)

# 2. ส่วนหน้าจอ Dashboard (UI)
st.title("🌍 AI Travel Planner (Powered by Groq)")
st.subheader("วางแผนเที่ยวเร็วแรงด้วย LPU")

col1, col2 = st.columns(2)
with col1:
    destination = st.text_input("ไปที่ไหนดี?", placeholder="เช่น ญี่ปุ่น, เชียงใหม่")
    budget = st.number_input("งบประมาณต่อท่าน (บาท)", min_value=0, value=10000)
with col2:
    days = st.slider("จำนวนวัน", 1, 14, 3)
    travel_style = st.selectbox("สไตล์การเที่ยว", ["สายกิน", "เน้นถ่ายรูป", "ธรรมชาติ", "ลุยๆ", "เน้นประหยัด"])

# 3. ส่วนการทำงานของ AI
if st.button("Generate My Plan! ⚡"):
    if not destination:
        st.error("กรุณาระบุสถานที่ท่องเที่ยวด้วยครับ")
    else:
        prompt = f"""
        จงเป็นผู้เชี่ยวชาญด้านการวางแผนเที่ยว (Professional Travel Planner)
        ช่วยออกแบบทริปไปที่ {destination} ระยะเวลา {days} วัน 
        งบประมาณรวม {budget} บาทต่อคน เน้นสไตล์ {travel_style}
        
        ตอบในรูปแบบ Markdown ให้สวยงาม:
        - สรุปไฮไลท์
        - แผนการเดินทางรายวัน (ละเอียด)
        - ประมาณการค่าใช้จ่าย
        """
        
        try:
            with st.spinner('กำลังคำนวณแผนเที่ยวด้วย Groq...'):
                # เรียกใช้โมเดล llama-3.3-70b-versatile (ฉลาดและเสถียรมากใน Groq)
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are a professional travel planner who speaks Thai."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2048
                )
                
                st.markdown("---")
                st.markdown(completion.choices[0].message.content)
                
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")