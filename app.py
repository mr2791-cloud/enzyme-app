import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="محلل كينتيكا وتفاعلات الإنزيمات", page_icon="🧪", layout="wide")

st.title("🧬 المنصة العلمية لتحليل وتنبؤ تفاعلات الإنزيمات")
st.markdown("تحليل التوافق الكيميائي للإنزيمات والركائز مع حسابات حركية التفاعل (Michaelis-Menten Kinetics).")

# قاعدة بيانات إنزيمية موسعة
ENZYME_DATABASE = {
    "amylase": {
        "substrates": ["starch", "glycogen", "amylose"],
        "name_ar": "الأميليز (Amylase)",
        "reaction": "تحلل الروابط الجليكوسيدية (Glycosidic cleavage)",
        "product": "المالتوز والجلوكوز (Maltose & Glucose)",
        "optimal_ph": 6.8,
        "optimal_temp": 37,
        "vmax": 100.0,  # µmol/min
        "km": 2.0,      # mM
        "desc": "يقوم بتفكيك الكربوهيدرات المعقدة مثل النشا إلى سكريات ثنائية وأحادية."
    },
    "pepsin": {
        "substrates": ["protein", "albumin", "casein"],
        "name_ar": "البيبسين (Pepsin)",
        "reaction": "هضم البروتينات (Proteolysis)",
        "product": "ببتيدات قصيرة وأحماض أمينية (Peptides & Amino Acids)",
        "optimal_ph": 2.0,
        "optimal_temp": 37,
        "vmax": 85.0,
        "km": 1.5,
        "desc": "إنزيم حمضي يعمل في المعدة لكسر الروابط الببتيدية في البروتينات."
    },
    "lactase": {
        "substrates": ["lactose"],
        "name_ar": "اللاكتيز (Lactase)",
        "reaction": "تحلل سكر الحليب (Hydrolysis)",
        "product": "جلوكوز + جالاكتوز (Glucose + Galactose)",
        "optimal_ph": 6.5,
        "optimal_temp": 37,
        "vmax": 120.0,
        "km": 5.0,
        "desc": "يحول سكر اللاكتوز المعقد إلى سكريات بسيطة أسهل في الامتصاص."
    },
    "trypsin": {
        "substrates": ["protein", "casein", "gelatin"],
        "name_ar": "التريبسين (Trypsin)",
        "reaction": "هضم البروتين بالقناة المعوية (Proteolysis)",
        "product": "أحماض أمينية وببتيدات",
        "optimal_ph": 8.0,
        "optimal_temp": 37,
        "vmax": 95.0,
        "km": 0.8,
        "desc": "إنزيم بنكرياسي يعمل في الوسط القلوي للأمعاء الدقيقة."
    },
    "catalase": {
        "substrates": ["hydrogen peroxide", "h2o2"],
        "name_ar": "الكاتاليز (Catalase)",
        "reaction": "أكسدة واختزال (Decomposition)",
        "product": "ماء + أكسجين (H2O + O2)",
        "optimal_ph": 7.0,
        "optimal_temp": 37,
        "vmax": 300.0,
        "km": 25.0,
        "desc": "يكسر فوق أكسيد الهيدروجين السام في الخلايا بسرعة عالية جداً."
    },
    "lipase": {
        "substrates": ["fat", "lipids", "triglycerides", "oil"],
        "name_ar": "اللايبين (Lipase)",
        "reaction": "تحلل الدهون (Lipolysis)",
        "product": "أحماض دهنية وجليسرول (Fatty acids & Glycerol)",
        "optimal_ph": 7.5,
        "optimal_temp": 37,
        "vmax": 75.0,
        "km": 3.2,
        "desc": "يمارس عمله في تفكيك الدهون الثلاثية إلى مكوناتها الأساسية."
    }
}

col1, col2 = st.columns(2)
with col1:
    enz_input = st.text_input("اسم الإنزيم (مثل: Amylase, Pepsin, Lactase, Catalase):", "Amylase").strip().lower()
with col2:
    sub_input = st.text_input("اسم المادة الركيزة Substrate (مثل: Starch, Protein, Lactose):", "Starch").strip().lower()

substrate_conc = st.slider("تركيز المادة الركيزة [S] بـ (mM):", min_value=0.1, max_value=50.0, value=10.0, step=0.5)

if st.button("🚀 تشغيل التحليل والمحاكاة"):
    st.markdown("---")
    
    if enz_input in ENZYME_DATABASE:
        enz_data = ENZYME_DATABASE[enz_input]
        
        # التأكد من التوافق الكيميائي
        if sub_input in enz_data["substrates"]:
            st.success(f"✅ **توافق كيميائي مثبت:** إنزيم {enz_data['name_ar']} يتفاعل مع مادة {sub_input.capitalize()}.")
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("نوع التفاعل", enz_data["reaction"])
            c2.metric("الـ pH المثالي", enz_data["optimal_ph"])
            c3.metric("الحرارة المثالية", f"{enz_data['optimal_temp']} °C")
            
            # حساب سرعة التفاعل معادلة ميكايليس-مينتن: V = (Vmax * [S]) / (Km + [S])
            v_max = enz_data["vmax"]
            k_m = enz_data["km"]
            v_current = (v_max * substrate_conc) / (k_m + substrate_conc)
            c4.metric("السرعة الحالية (V)", f"{v_current:.2f} µmol/min")
            
            st.info(f"**النواتج:** {enz_data['product']} | **الوصف:** {enz_data['desc']}")
            
            # رسم منحنيات كينتيكا والتأثير البيئي
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
            
            # منحنى Michaelis-Menten
            s_range = np.linspace(0, 50, 100)
            v_range = (v_max * s_range) / (k_m + s_range)
            ax1.plot(s_range, v_range, color="teal", linewidth=2.5, label="معادلة Michaelis-Menten")
            ax1.axvline(substrate_conc, color="orange", linestyle="--", label=f"التركيز الحالي [{substrate_conc} mM]")
            ax1.axhline(v_current, color="red", linestyle=":", label=f"السرعة V ({v_current:.1f})")
            ax1.set_title("منحنى حركية التفاعل (Kinetics Curve)")
            ax1.set_xlabel("تركيز المادة [S] (mM)")
            ax1.set_ylabel("سرعة التفاعل V (µmol/min)")
            ax1.grid(True, alpha=0.3)
            ax1.legend()
            
            # منحنى تأثير pH
            ph_range = np.linspace(1, 14, 100)
            ph_activity = np.exp(-0.5 * ((ph_range - enz_data["optimal_ph"]) / 1.2)**2) * 100
            ax2.plot(ph_range, ph_activity, color="purple", linewidth=2.5)
            ax2.axvline(enz_data["optimal_ph"], color="green", linestyle="--", label=f"الـ pH المثالي ({enz_data['optimal_ph']})")
            ax2.set_title("تأثير درجة الحموضة (pH Effect)")
            ax2.set_xlabel("درجة الحموضة pH")
            ax2.set_ylabel("نشاط الإنزيم (%)")
            ax2.grid(True, alpha=0.3)
            ax2.legend()
            
            st.pyplot(fig)
            
        else:
            st.error(f"❌ **عدم توافق كيميائي (Incompatible):** إنزيم {enz_data['name_ar']} لا يتفاعل كيميائياً مع مادة {sub_input.capitalize()}.")
            st.warning(f"💡 **التفسير العلمي:** الإنزيمات تتميز بالخاصية التخصصية (Enzyme Specificity)؛ حيث إن الموقع النشط (Active Site) لإنزيم {enz_input.capitalize()} مصمم فقط ليرتبط بـ {', '.join(enz_data['substrates'])}، ولن يتشكل مركب (Enzyme-Substrate Complex) مع {sub_input.capitalize()}.")
    else:
        st.warning("الإنزيم غير مدرج في قاعدة البيانات حالياً. جرب كتابة أحد الإنزيمات التالية: Amylase, Pepsin, Lactase, Trypsin, Catalase, Lipase.")
