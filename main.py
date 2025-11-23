import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers

# --- IMPORT DATABASE PENYAKIT ---
try:
    from kamus_penyakit import solusi_petani
except ImportError:
    st.error("FATAL: File 'kamus_penyakit.py' tidak ditemukan.")
    solusi_petani = {}

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Dokter Tanaman AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. CSS ADAPTIF
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    .main-header {
        background: linear-gradient(135deg, #1b5e20 0%, #4caf50 100%);
        padding: 20px; border-radius: 15px; color: white;
        text-align: center; margin-bottom: 30px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .info-card {
        background-color: var(--secondary-background-color);
        padding: 20px; border-radius: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 20px;
    }
    .result-box {
        padding: 20px; border-radius: 10px; margin-bottom: 15px;
        background-color: var(--secondary-background-color);
        border-left-width: 10px; border-left-style: solid;
    }
    .status-danger { border-left-color: #d32f2f; }
    .status-warning { border-left-color: #ffa000; }
    .status-safe { border-left-color: #388e3c; }
    .result-title { font-size: 1.5rem; font-weight: bold; margin: 0; }
    div[data-testid="stFileUploader"] {
        border: 1px dashed var(--primary-color);
        border-radius: 10px; padding: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. LOGIKA MODEL
# ==========================================

def build_model(num_classes):
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    base_model.trainable = False
    model = tf.keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.3),
        layers.Dense(256, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])
    return model

@st.cache_resource
def load_model_with_weights():
    NUM_CLASSES = 12 
    model = build_model(num_classes=NUM_CLASSES)
    weights_file = 'model_bobot_padi_jagung.weights.h5'
    
    try:
        model.load_weights(weights_file) 
        return model
    except Exception as e:
        st.error(f"Error: Tidak dapat memuat bobot model '{weights_file}'.\nDetail: {e}")
        return None

model = load_model_with_weights()

# Pastikan urutan ini SESUAI ABJAD dengan nama folder dataset Anda
class_names = [
    'jagung_blight', 'jagung_common_rust', 'jagung_gray_leaf_spot', 'jagung_healthy',
    'padi_bacterial_blight', 'padi_brown_spot', 'padi_defisiensi_k', 'padi_defisiensi_n', 
    'padi_defisiensi_p', 'padi_leaf_blast', 'padi_leaf_scald', 'padi_normal'
]

# --- FUNGSI PREDIKSI ---
def import_and_predict(image_data, model):
    try:
        # 1. Perbaiki Orientasi
        image_data = ImageOps.exif_transpose(image_data)
        # 2. Pastikan RGB
        image_data = image_data.convert('RGB')
        # 3. Resize & Preprocess
        size = (224, 224)
        image = ImageOps.fit(image_data, size, Image.Resampling.LANCZOS)
        img_array = np.asarray(image)
        normalized_image_array = (img_array.astype(np.float32) / 255.0)
        # 4. Buat Batch
        data = np.expand_dims(normalized_image_array, axis=0)
        # 5. Prediksi
        prediction = model.predict(data)
        index = np.argmax(prediction)
        confidence = np.max(prediction)
        return index, confidence
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses gambar: {e}")
        return None, 0

# ==========================================
# 4. TAMPILAN APLIKASI
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3022/3022999.png", width=80)
    st.title("Dokter Tanaman")
    st.caption("v2.2 - Threshold 60%")
    st.markdown("---")
    st.info("Aplikasi deteksi penyakit Padi & Jagung.")
    st.markdown("© 2025 Project Skripsi")

st.markdown("""
<div class="main-header">
    <h1>🧑‍🌾 Dokter Tanaman Cerdas</h1>
    <p>Sistem Pakar Deteksi Penyakit Padi & Jagung Berbasis AI</p>
</div>
""", unsafe_allow_html=True)

if model is not None:
    col1, col2 = st.columns([1, 1.5], gap="large")

    with col1:
        st.markdown("### 📸 Foto Tanaman")
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        file = st.file_uploader("Upload foto daun (Padi / Jagung)", type=["jpg", "png", "jpeg"])
        st.markdown('</div>', unsafe_allow_html=True)

        if file is not None:
            image = Image.open(file)
            st.image(image, caption="Preview Citra", use_container_width=True)
            analyze = True
        else:
            analyze = False
            st.info("Silakan upload foto untuk memulai.")

    with col2:
        st.markdown("### 📊 Hasil Diagnosa")
        
        if analyze:
            with st.spinner("Sedang Menganalisis..."):
                idx, conf = import_and_predict(image, model)
                
                # --- FILTER KEYAKINAN (THRESHOLD 60%) ---
                MIN_CONFIDENCE = 0.60 
                
                if idx is not None:
                    res = class_names[idx]
                    info = solusi_petani.get(res)
                    confidence_percent = conf * 100
                    
                    # KATEGORI 1: YAKIN (> 80%) -> Tampil Hijau/Normal
                    if conf >= 0.80:
                        css_class = f"status-{info['style']}"
                        header_icon = info['icon']
                        header_text = f"{info['nama']}"
                        
                        st.markdown(f"""
                        <div class="result-box {css_class}">
                            <div class="result-title">{header_icon} {header_text}</div>
                            <p style="margin-top: 10px;">Status: <b>{info['status']}</b></p>
                            <p style="font-size: 0.8em; opacity: 0.7;">Tingkat Keyakinan: {confidence_percent:.2f}% (Sangat Yakin)</p>
                        </div>
                        """, unsafe_allow_html=True)

                    # KATEGORI 2: RAGU-RAGU (60% - 79%) -> Tampil Kuning (Peringatan)
                    elif conf >= MIN_CONFIDENCE:
                        st.warning(f"""
                        ⚠️ **Hasil Analisis (Keyakinan Sedang: {confidence_percent:.0f}%)**
                        
                        Sistem mendeteksi kemiripan dengan **{info['nama']}**, namun tidak terlalu yakin. Pastikan pencahayaan foto cukup dan lakukan pengambilan foto ulang agar hasil yang maksimal.
                        """)
                        
                        st.markdown(f"""
                        <div class="result-box status-warning" style="opacity: 0.8;">
                            <div class="result-title">? {info['nama']}</div>
                            <p style="margin-top: 10px;">Status: <b>{info['status']}</b></p>
                        </div>
                        """, unsafe_allow_html=True)

                    # KATEGORI 3: TIDAK TAHU (< 60%) -> Tampil Merah (Tolak)
                    else:
                        st.error(f"""
                        ### ❌ Gambar Tidak Dikenali
                        **Tingkat Keyakinan: {confidence_percent:.0f}% (Terlalu Rendah)**
                        
                        Sistem tidak dapat mengenali tanaman ini dengan pasti.
                        **Saran:**
                        1. Pastikan foto fokus pada **satu lembar daun**.
                        2. Pastikan pencahayaan cukup.
                        3. Pastikan objek adalah Padi atau Jagung.
                        """)
                        st.stop()

                    # --- TABS SOLUSI (Hanya jika lolos threshold) ---
                    st.progress(float(conf))
                    st.markdown("---")
                    
                    tab1, tab2, tab3 = st.tabs(["📖 Penjelasan", "💊 Solusi & Obat", "🛡️ Pencegahan"])
                    
                    with tab1:
                        st.info(info.get('deskripsi', '-'))
                        st.markdown("**Gejala Khas:**")
                        st.markdown(info.get('gejala', '-'))
                    with tab2:
                        if info['style'] == 'safe':
                            st.success(info.get('penanganan', '-'))
                        else:
                            st.warning(info.get('penanganan', '-'))
                    with tab3:
                        st.markdown(info.get('pencegahan', '-'))
                        
                else:
                    st.error("Terjadi masalah teknis saat prediksi.")
        else:
            st.markdown("""
            <div class="info-card" style="text-align: center; opacity: 0.5; padding: 40px;">
                <p>Hasil analisis akan muncul di sini</p>
            </div>
            """, unsafe_allow_html=True)
else:
    st.warning("Model AI belum siap.")