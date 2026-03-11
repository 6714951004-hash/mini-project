import streamlit as st
import google.generativeai as genai
import os

# --- Configuration ---
st.set_page_config(page_title="AI Travel Planner", page_icon="✈️")

# ดึง API Key จาก Environment Variable (ที่ตั้งค่าไว้ใน Render)
# ถ้าหาไม่เจอจะใช้ค่าว่าง เพื่อไม่ให้แอปพังทันทีที่เปิด
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("❌ ไม่พบ API Key กรุณาตั้งค่า GEMINI_API_KEY ใน Environment Variables")
    st.stop()

# --- UI Layout ---
st.title("✈️ AI Personalized Travel Planner")
st.subheader("วางแผนเที่ยวตามใจคุณและงบในกระเป๋า")

with st.sidebar:
    st.header("📍 ข้อมูลการเดินทาง")
    destination = st.text_input("ไปที่ไหน? (เช่น โตเกียว, เชียงใหม่)", "โตเกียว")
    days = st.slider("จำนวนวัน", 1, 10, 3)
    budget = st.selectbox("งบประมาณ (ไม่รวมตั๋วเครื่องบิน)", 
                          ["ประหยัด (Hostel/Street Food)", 
                           "ปานกลาง (Hotel/Cafe)", 
                           "หรูหรา (Luxury/Fine Dining)"])
    style = st.multiselect("สไตล์ที่ชอบ", 
                           ["สายกิน", "สายถ่ายรูป", "สายมู", "สายธรรมชาติ", "ช้อปปิ้ง"], 
                           ["สายกิน", "สายถ่ายรูป"])

# --- AI Logic ---
if st.button("✨ สร้างแผนการเที่ยว"):
    # ตรวจสอบว่าเลือกสไตล์อย่างน้อยหนึ่งอย่าง
    style_text = ', '.join(style) if style else "ทั่วไป"
    
    prompt = f"""
    คุณเป็นไกด์มืออาชีพ ช่วยวางแผนเที่ยวที่ {destination} เป็นเวลา {days} วัน 
    งบประมาณระดับ: {budget} สไตล์การเที่ยว: {style_text}
    
    กรุณาตอบในรูปแบบ Markdown:
    1. สรุปภาพรวมทริปและงบประมาณที่คาดว่าต้องใช้ (เป็นเงินบาท)
    2. แผนการเดินทางรายวัน (Day 1, 2, 3...) แบ่งเป็นช่วง เช้า/กลางวัน/เย็น
    3. แนะนำที่พัก 2-3 แห่งที่เหมาะกับงบประมาณ
    4. ข้อควรระวังหรือ Tips สำหรับเมืองนี้
    
    เน้นการจัดตารางที่เดินทางได้จริง ไม่แน่นจนเกินไป
    """
    
    with st.spinner('กำลังจัดทริปที่ดีที่สุดให้คุณ...'):
        try:
            response = model.generate_content(prompt)
            
            st.divider()
            st.markdown(response.text)
            
            # ฟีเจอร์แถม: ปุ่มดาวน์โหลดแผน
            st.download_button(
                label="📩 ดาวน์โหลดแผนการเที่ยว",
                data=response.text,
                file_name=f"trip_to_{destination}.md",
                mime="text/markdown"
            )
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดในการสร้างแผน: {e}")