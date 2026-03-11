import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="AI Travel Planner", page_icon="✈️")

# 1. จัดการเรื่อง API Key
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.warning("⚠️ โปรดระบุ Gemini API Key ใน Environment Variable เพื่อเริ่มต้นใช้งาน")
    st.stop()

genai.configure(api_key=api_key)

# 2. ส่วนหน้าจอ Dashboard (UI)
st.title("🌍 AI Personalized Travel Planner")
st.subheader("วางแผนเที่ยวตามงบแบบเป๊ะๆ")

col1, col2 = st.columns(2)
with col1:
    destination = st.text_input("ไปที่ไหนดี?", placeholder="เช่น ญี่ปุ่น, เชียงใหม่")
    budget = st.number_input("งบประมาณต่อท่าน (บาท)", min_value=0)
with col2:
    days = st.slider("จำนวนวัน", 1, 14, 3)
    travel_style = st.selectbox("สไตล์การเที่ยว", ["สายกิน", "เน้นถ่ายรูป", "ธรรมชาติ", "ลุยๆ"])

# 3. ส่วนการทำงานของ AI (เมื่อกดปุ่มเท่านั้น)
if st.button("Generate My Plan! ✨"):
    # สร้าง Prompt จากข้อมูลที่ User กรอก
    prompt = f"จงวางแผนเที่ยว {destination} งบ {budget} บาท {days} วัน สไตล์ {travel_style}"
    
    try:
        # ใช้โมเดล 2.0 ล่าสุด
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        with st.spinner('กำลังคิดแผนเที่ยว...'):
            response = model.generate_content(prompt)
            st.markdown("---")
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {e}")
        st.info("หากเป็นปัญหาเรื่อง Model ไม่พบ ลองเปลี่ยนชื่อเป็น 'gemini-1.5-flash' ดูครับ")