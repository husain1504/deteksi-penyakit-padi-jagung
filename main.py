import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers

# --- IMPORT DATABASE PENYAKIT ---
try:
    # Pastikan file 'kamus_penyakit.py' (versi Padi+Jagung) ada di folder yang sama
    from kamus_penyakit import solusi_petani
except ImportError:
    st.error("FATAL: File 'kamus_penyakit.py' tidak ditemukan.")
    solusi_petani = {} # Fallback


# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Dokter Tanaman AI",
    page_icon="🧑‍🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. CSS ADAPTIF (DARK & LIGHT MODE FRIENDLY)
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
# 3. LOGIKA MODEL (UPGRADE MULTI-TANAMAN)
# ==========================================

# FUNGSI UNTUK MEMBUAT "RANGKA" MODEL
def build_model(num_classes):
    """Membangun arsitektur MobileNetV2 yang sama dengan saat training."""
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    base_model.trainable = False
    
    model = tf.keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.3),
        layers.Dense(256, activation='relu'),
        layers.Dense(num_classes, activation='softmax') # Otomatis sesuai NUM_CLASSES
    ])
    return model

# FUNGSI BARU UNTUK LOAD "BOBOT"
@st.cache_resource
def load_model_with_weights():
    """Membuat rangka dan mengisinya dengan bobot."""
    # 1. Tentukan jumlah kelas (SESUAIKAN DENGAN JUMLAH FOLDER BARU ANDA)
    # 8 Padi + 4 Jagung = 12 Kelas
    NUM_CLASSES = 12 
    
    # 2. Buat "Rangka" Kosong
    model = build_model(num_classes=NUM_CLASSES)
    
    # 3. Tentukan nama file bobot BARU
    weights_file = 'model_bobot_padi_jagung.weights.h5' # <-- NAMA FILE BARU
    
    # 4. Isi "Rangka" dengan "Ilmu" (Bobot)
    try:
        model.load_weights(weights_file) 
        return model
    except Exception as e:
        st.error(f"Error: Tidak dapat memuat model. Pastikan file '{weights_file}' ada di folder yang sama.\nDetail: {e}")
        return None

# --- Panggil fungsi ---
with st.spinner('Sedang memuat model AI (Padi & Jagung)...'):
    model = load_model_with_weights()

# Nama kelas (HARUS URUT ABJAD SESUAI NAMA FOLDER BARU)
class_names = [
    'jagung_blight',
    'jagung_common_rust',
    'jagung_gray_leaf_spot',
    'jagung_healthy',
    'padi_bacterial_blight', 
    'padi_brown_spot', 
    'padi_defisiensi_k', 
    'padi_defisiensi_n', 
    'padi_defisiensi_p', 
    'padi_leaf_blast', 
    'padi_leaf_scald', 
    'padi_normal'
]

# Fungsi prediksi (DIPERBAIKI agar tidak error dimensi array)
def import_and_predict(image_data, model):
    # 1. Pastikan RGB
    image_data = image_data.convert('RGB')
    
    # 2. Resize
    size = (224, 224)
    image = ImageOps.fit(image_data, size, Image.Resampling.LANCZOS)
    
    # 3. Convert to Array & Normalize
    img_array = np.asarray(image)
    normalized_image_array = (img_array.astype(np.float32) / 255.0)
    
    # 4. Expand Dimensions (Membuat batch: (1, 224, 224, 3))
    # Ini menggantikan cara manual 'data[0] =' yang sering error
    data = np.expand_dims(normalized_image_array, axis=0)
    
    try:
        prediction = model.predict(data)
        index = np.argmax(prediction)
        confidence = np.max(prediction)
        return index, confidence
    except Exception as e:
        st.error(f"Error saat prediksi: {e}")
        return None, 0

# ==========================================
# 4. UI SIDEBAR
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3022/3022999.png", width=80)
    st.title("Dokter Tanaman")
    st.caption("Versi 2.0 - Petani Cerdas")
    st.markdown("---")
    st.info("Aplikasi ini dapat mendeteksi penyakit pada tanaman Padi dan Jagung.")
    st.markdown("© 2025 Petani Cerdas")

# ==========================================
# 5. UI UTAMA
# ==========================================
st.markdown("""
<div class="main-header">
    <h1>🧑‍🌾 Dokter Tanaman Cerdas</h1>
    <p>Sistem Pakar Deteksi Penyakit Padi & Jagung Berbasis AI</p>
</div>
""", unsafe_allow_html=True)

# Cek apakah model berhasil di-load
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
            st.info("Silakan upload foto untuk memulai analisis.")

    with col2:
        st.markdown("### 📊 Hasil Diagnosa")
        
        if analyze:
            with st.spinner("Sedang Menganalisis..."):
                idx, conf = import_and_predict(image, model)
                
                # ==========================================================
                # --- FITUR FILTER BARU (PENOLAK TANAMAN LAIN) ---
                # ==========================================================
                # Ambang batas keyakinan. Jika di bawah ini, anggap bukan Padi/Jagung
                MIN_CONFIDENCE = 0.70 
                
                if idx is not None and conf >= MIN_CONFIDENCE:
                    # JIKA YAKIN (DI ATAS 70%), TAMPILKAN HASIL
                    res = class_names[idx]
                    info = solusi_petani.get(res)
                    
                    css_class = f"status-{info['style']}"
                    
                    st.markdown(f"""
                    <div class="result-box {css_class}">
                        <div class="result-title">{info['icon']} {info['nama']}</div>
                        <p style="margin-top: 10px;">Status: <b>{info['status']}</b></p>
                        <p style="font-size: 0.8em; opacity: 0.7;">Tingkat Keyakinan: {conf*100:.2f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.progress(float(conf))
                    st.markdown("---")
                    
                    tab1, tab2, tab3 = st.tabs(["📖 Penjelasan", "💊 Solusi & Obat", "🛡️ Pencegahan"])
                    
                    with tab1:
                        st.markdown("#### Apa itu penyakit ini?")
                        st.info(info['deskripsi'])
                        st.markdown("#### Gejala Khas:")
                        st.markdown(info['gejala'])
                        
                    with tab2:
                        st.markdown("#### Langkah Pengobatan:")
                        if info['style'] == 'safe':
                            st.success(info['penanganan'])
                        else:
                            st.warning(info['penanganan'])
                            st.caption("⚠️ *Catatan: Gunakan pestisida sesuai dosis.*")
                            
                    with tab3:
                        st.markdown("#### Cara Mencegah:")
                        st.markdown(info['pencegahan'])
                        
                elif idx is not None and conf < MIN_CONFIDENCE:
                    # JIKA TIDAK YAKIN (DI BAWAH 70%), TOLAK GAMBAR
                    st.error(f"""
                    ### ⚠️ Gambar Tidak Dikenali
                    
                    **Tingkat Keyakinan AI: {conf*100:.0f}% (Terlalu Rendah)**
                    
                    Sistem kami mendeteksi bahwa gambar ini kemungkinan besar **bukan daun Padi atau Jagung**, atau kualitas gambarnya kurang jelas.
                    
                    **Mohon unggah ulang dengan ketentuan:**
                    1. Pastikan objek adalah **Daun Padi** atau **Daun Jagung**.
                    2. Pastikan gambar fokus dan pencahayaan cukup.
                    3. Hindari latar belakang yang terlalu ramai.
                    """)
                    
                else:
                    st.error("Terjadi masalah saat melakukan prediksi.")
        else:
            # Placeholder saat kosong
            st.markdown("""
            <div class="info-card" style="text-align: center; opacity: 0.5; padding: 40px;">
                <p>Hasil analisis akan muncul di sini</p>
            </div>
            """, unsafe_allow_html=True)
else:
    # Tampilan jika model GAGAL dimuat
    st.warning("Model AI belum siap. Harap periksa error di atas.")
    st.error("Jika Anda adalah developer, pastikan 'model_bobot_padi_jagung.weights.h5' ada di GitHub.")