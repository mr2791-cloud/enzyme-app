import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="محلل تفاعل الإنزيمات", page_icon="🧬", layout="centered")

st.title("🧬 تطبيق محلل تأثير الإنزيم على المادة")
st.write("أدخل اسم الإنزيم والمادة الركيزة لمعرفة نوع التفاعل والتأثير الناتج.")

col1, col2 = st.columns(2)
with col1:
    enzyme_name = st.text_input("اسم الإنزيم (مثال: Amylase, Lactase, Pepsin):").strip()
with col2:
    substrate_name = st.text_input("اسم المادة (مثال: Starch, Lactose, Protein):").strip()

KNOWN_ENZYMES = {
    ("lactase", "lactose"): {
        "reaction": "تحلل السكر (Hydrolysis)",
        "product": "الجلوكوز + الجالاكتوز (Glucose + Galactose)",
        "optimal_ph": 6.5,
        "optimal_temp": 37,
        "description": "يقوم إنزيم اللاكتيز بتفكيك سكر اللاكتوز الموجود في الحليب إلى سكريات بسيطة أسهل في الهضم."
    },
    ("amylase", "starch"): {
        "reaction": "تحلل النشا (Starch Cleavage)",
        "product": "المالتوز والجلوكوز (Maltose & Glucose)",
        "optimal_ph": 6.8,
        "optimal_temp": 37,
        "description": "يعمل الأميليز (في اللعاب والبنكرياس) على تفكيك الروابط الجليكوسيدية في النشا لتحويله لسكر مالتوز."
    },
    ("pepsin", "protein"): {
        "reaction": "هضم البروتين (Proteolysis)",
        "product": "ببتيدات قصيرة (Short Peptides / Amino acids)",
        "optimal_ph": 2.0,
        "optimal_temp": 37,
        "description": "يعمل إنزيم البيبسين في المعدة في وسط حمضي قوي على تقطيع سلاسل البروتينات المعقدة."
    }
}

if st.button("🔍 تحليل التفاعل"):
    if enzyme_name and substrate_name:
        key = (enzyme_name.lower(), substrate_name.lower())
        st.markdown("---")
        st.subheader(f"📊 نتائج تحليل: {enzyme_name} ➔ {substrate_name}")
        
        if key in KNOWN_ENZYMES:
            data = KNOWN_ENZYMES[key]
            st.success(f"**نوع التفاعل:** {data['reaction']}")
            st.info(f"**النواتج (Products):** {data['product']}")
            st.write(f"**الشرح:** {data['description']}")
            
            m1, m2 = st.columns(2)
            m1.metric("الـ pH المثالي", data['optimal_ph'])
            m2.metric("الحرارة المثالية", f"{data['optimal_temp']} °C")
            
            ph_range = np.linspace(1, 14, 100)
            activity = np.exp(-0.5 * (ph_range - data['optimal_ph'])**2)
            
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.plot(ph_range, activity, color="crimson", linewidth=2)
            ax.axvline(data['optimal_ph'], color='gray', linestyle='--', label="الـ pH المثالي")
            ax.set_xlabel("درجة الحموضة (pH)")
            ax.set_ylabel("نسبة النشاط")
            ax.grid(True, alpha=0.3)
            ax.legend()
            st.pyplot(fig)
        else:
            st.warning("هذا التفاعل غير مسجل في قاعدة البيانات المحلية بعد.")
    else:
        st.error("رجاءً أدخل اسم الإنزيم والمادة أولاً.")
