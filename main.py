import streamlit as st
from PIL import Image, ImageOps
import numpy as np
import tensorflow as tf

# ==========================================
# 1. KONFIGURASI HALAMAN & MODEL
# ==========================================
st.set_page_config(page_title="Deteksi Penyakit Padi", page_icon="🌾")

# CSS Sederhana untuk mempercantik tampilan
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .hasil-box {
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Load Model (Cache supaya tidak load berulang kali)
@st.cache_resource
def load_model():
    # Pastikan nama file sesuai dengan yang didownload dari Colab
    # Anda mungkin perlu mengganti 'model_padi_komplit.h5' jika namanya berbeda
    try:
        model = tf.keras.models.load_model('model_padi_komplit.h5')
        return model
    except Exception as e:
        st.error(f"Error: Tidak dapat memuat model. Pastikan file 'model_padi_komplit.h5' ada di folder yang sama.\nDetail: {e}")
        return None

with st.spinner('Sedang memuat model AI...'):
    model = load_model()

# ==========================================
# 2. DEFINISI KELAS & SOLUSI (DATABASE)
# ==========================================
# PENTING: Urutan nama kelas harus SESUAI ABJAD folder dataset kamu
# Cek lagi folder dataset kamu, urutkan A-Z
class_names = [
    'bacterial_blight', 
    'brown_spot', 
    'defisiensi_k', 
    'defisiensi_n', 
    'defisiensi_p', 
    'leaf_blast', 
    'leaf_scald', 
    'normal'
]

# Kamus Solusi (Database Saran Pengobatan)
solusi_petani = {
    'bacterial_blight': {
        'nama': 'Hawar Daun Bakteri (Kresek)',
        'status': 'Bahaya',
        'style': 'danger',
        'icon': '🚨',
        'deskripsi': 'Penyakit yang disebabkan oleh bakteri Xanthomonas oryzae. Penyakit ini menyerang titik tumbuh dan daun, menyebabkan tanaman mengering seperti terbakar.',
        'gejala': '• Terdapat garis basah memanjang (water-soaked) pada tepi daun.\n• Daun berubah warna menjadi kuning-oranye, lalu mengering berwarna putih keabuan.\n• Pada serangan berat, seluruh tanaman layu (kresek).',
        'penanganan': '• **Kimia:** Semprotkan bakterisida berbahan aktif Tembaga Oksida (Copper Oxide) atau Tembaga Hidroksida.\n• **Alami:** Gunakan Paenibacillus polymyxa (bakteri antagonis).\n• Hindari pemupukan Urea (Nitrogen) berlebihan saat serangan terjadi.',
        'pencegahan': '• Gunakan varietas tahan (seperti Inpari 32/42).\n• Atur jarak tanam jajar legowo agar sirkulasi udara baik.\n• Lakukan pengairan berselang (intermittent) agar sawah tidak tergenang terus.'
    },
    'brown_spot': {
        'nama': 'Bercak Coklat (Brown Spot)',
        'status': 'Penyakit Jamur',
        'style': 'warning',
        'icon': '🍄',
        'deskripsi': 'Penyakit jamur yang disebabkan oleh Helminthosporium oryzae. Sering terjadi pada tanah yang kurang hara (terutama Kalium dan Silika).',
        'gejala': '• Bercak berbentuk oval atau bulat seperti mata.\n• Bagian tengah bercak berwarna abu-abu/putih, tepi berwarna coklat kemerahan.\n• Menyerang daun dan bulir padi (menyebabkan bulir hampa/hitam).',
        'penanganan': '• **Kimia:** Semprot fungisida berbahan aktif Difenokonazol, Propikonazol, atau Mankozeb.\n• **Nutrisi:** Segera berikan pupuk Kalium (KCl) dan Silika untuk memperkuat dinding sel daun.',
        'pencegahan': '• Pemupukan berimbang (jangan cuma Urea).\n• Perbaiki kondisi tanah dengan bahan organik (kompos).'
    },
    'leaf_blast': {
        'nama': 'Blast Daun (Potong Leher)',
        'status': 'Sangat Bahaya',
        'style': 'danger',
        'icon': '🔥',
        'deskripsi': 'Penyakit fungal oleh Pyricularia oryzae. Ini adalah salah satu penyakit padi paling merusak karena penyebarannya lewat udara sangat cepat.',
        'gejala': '• Bercak berbentuk belah ketupat (diamond shape) dengan ujung runcing.\n• Pusat bercak putih/abu-abu dengan tepi coklat kemerahan.\n• Bisa menyerang leher malai (Potong Leher) sehingga padi gagal panen.',
        'penanganan': '• **Kimia:** Gunakan fungisida sistemik berbahan aktif Tricyclazole, Isoprothiolane, atau Pyraclostrobin.\n• **Darurat:** Bakar sisa jerami tanaman yang terinfeksi parah agar spora tidak menyebar.',
        'pencegahan': '• Hindari tanam terlalu rapat.\n• Jangan gunakan pupuk Nitrogen (Urea) berlebihan.\n• Jaga sawah tetap tergenang air saat fase pertumbuhan.'
    },
    'leaf_scald': {
        'nama': 'Hawar Pelepah (Leaf Scald)',
        'status': 'Penyakit',
        'style': 'warning',
        'icon': '🍂',
        'deskripsi': 'Penyakit yang disebabkan jamur Microdochium oryzae (atau Monographella albescens). Sering terjadi pada musim hujan dengan kelembapan tinggi.',
        'gejala': '• Pola zonasi (garis-garis) melingkar pada ujung daun atau pelepah.\n• Bagian yang sakit tampak basah lalu mengering coklat muda.\n• Daun tampak seperti tersiram air panas (melepuh).',
        'penanganan': '• **Kimia:** Semprot fungisida Benomyl, Karbendazim, atau Tiofanat Metil.\n• Potong dan buang bagian daun yang terinfeksi.',
        'pencegahan': '• Kurangi kelembapan dengan mengatur jarak tanam.\n• Bersihkan gulma yang bisa menjadi inang jamur.'
    },
    'defisiensi_n': {
        'nama': 'Kekurangan Nitrogen (N)',
        'status': 'Defisiensi Hara',
        'style': 'warning',
        'icon': '🧪',
        'deskripsi': 'Tanaman kekurangan unsur Nitrogen, yang merupakan bahan utama pembentukan klorofil (zat hijau daun).',
        'gejala': '• Daun tanaman (terutama daun tua) menguning secara merata dari ujung ke pangkal.\n• Tanaman tumbuh kerdil dan kurus.\n• Anakan padi sedikit (jarang).',
        'penanganan': '• **Pupuk:** Segera taburkan pupuk Urea (46% N) atau ZA.\n• Gunakan Bagan Warna Daun (BWD) untuk mengukur dosis yang tepat.',
        'pencegahan': '• Lakukan pemupukan dasar sebelum tanam.\n• Gunakan pupuk kandang/organik untuk menjaga ketersediaan hara.'
    },
    'defisiensi_p': {
        'nama': 'Kekurangan Fosfor (P)',
        'status': 'Defisiensi Hara',
        'style': 'warning',
        'icon': '🧪',
        'deskripsi': 'Kekurangan Fosfor menghambat pembentukan akar dan proses pembungaan/pengisian bulir.',
        'gejala': '• Daun berwarna hijau gelap kusam, kadang berubah menjadi ungu kemerahan.\n• Batang tanaman kecil dan pendek (kerdil).\n• Akar tanaman sedikit dan pendek.',
        'penanganan': '• **Pupuk:** Berikan pupuk SP-36, TSP, atau DAP.\n• Perbaiki pH tanah (jika tanah terlalu asam, Fosfor sulit diserap, tambahkan kapur dolomit).',
        'pencegahan': '• Pemberian pupuk Fosfor sebaiknya dilakukan di awal tanam (pupuk dasar).'
    },
    'defisiensi_k': {
        'nama': 'Kekurangan Kalium (K)',
        'status': 'Defisiensi Hara',
        'style': 'warning',
        'icon': '🧪',
        'deskripsi': 'Kekurangan Kalium membuat tanaman lemah, mudah roboh, dan rentan terhadap serangan penyakit.',
        'gejala': '• Pinggiran daun (tepi) mengering berwarna coklat kemerahan (seperti terbakar/gosong).\n• Muncul bercak-bercak karat pada daun tua.\n• Batang padi lemah dan mudah rebah.',
        'penanganan': '• **Pupuk:** Berikan pupuk KCl atau NPK dengan kadar Kalium tinggi.\n• Bisa juga tambahkan abu sekam padi (sumber Kalium alami).',
        'pencegahan': '• Jangan buang jerami sisa panen, kembalikan ke sawah (jerami kaya Kalium).'
    },
    'normal': {
        'nama': 'Tanaman Sehat',
        'status': 'Normal',
        'style': 'safe',
        'icon': '✅',
        'deskripsi': 'Tanaman padi dalam kondisi pertumbuhan optimal, tidak menunjukkan gejala serangan hama, penyakit, maupun kekurangan nutrisi.',
        'gejala': '• Daun berwarna hijau segar merata.\n• Helaian daun tegak dan tidak ada bercak.\n• Pertumbuhan tinggi tanaman dan jumlah anakan normal.',
        'penanganan': '• Lanjutkan perawatan rutin (pemupukan berimbang dan pengairan).\n• Lakukan pengamatan rutin (monitoring) seminggu sekali.',
        'pencegahan': '• Tetap waspada terhadap perubahan cuaca dan serangan hama sekitar.'
    }
}

# ==========================================
# 3. LOGIKA PREDIKSI GAMBAR
# ==========================================
def import_and_predict(image_data, model):
    # 1. Resize gambar ke 224x224 (Sesuai training)
    size = (224, 224)
    image = ImageOps.fit(image_data, size, Image.Resampling.LANCZOS)
    
    # 2. Ubah ke Array & Normalisasi (0-1)
    img_array = np.asarray(image)
    normalized_image_array = (img_array.astype(np.float32) / 255.0)
    
    # 3. Buat Batch (1, 224, 224, 3)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array
    
    # 4. Prediksi
    prediction = model.predict(data)
    
    # Ambil index dengan probabilitas tertinggi
    index = np.argmax(prediction)
    confidence = np.max(prediction) # Tingkat keyakinan (0.0 - 1.0)
    
    return index, confidence

# ==========================================
# 4. TAMPILAN UTAMA (FRONTEND)
# ==========================================
st.title("🌾 Dokter Padi Cerdas")
st.write("Upload foto daun padi untuk mendeteksi penyakit atau kekurangan pupuk.")

file = st.file_uploader("Pilih gambar dari galeri...", type=["jpg", "png", "jpeg"])

# Hanya jalankan jika model berhasil dimuat
if model is not None:
    if file is not None:
        # Tampilkan gambar user
        image = Image.open(file)
        st.image(image, caption='Foto Tanaman', use_container_width=True)
        
        # Tombol Analisis
        if st.button("🔍 Analisis Sekarang"):
            with st.spinner('Sedang menganalisis gambar...'):
                idx, conf = import_and_predict(image, model)
                class_result = class_names[idx] # Nama folder hasil prediksi
                
                # Ambil info dari database solusi
                info = solusi_petani.get(class_result, {
                    'nama': class_result.replace('_', ' ').title(), 
                    'status': 'Tidak Diketahui',
                    'style': 'warning',
                    'icon': '❓',
                    'deskripsi': 'Data untuk penyakit ini belum ada di database.',
                    'gejala': 'Tidak ada data gejala.',
                    'penanganan': 'Hubungi penyuluh pertanian setempat untuk informasi lebih lanjut.',
                    'pencegahan': 'Tidak ada data pencegahan.'
                })
                
                # Tampilkan Hasil
                st.markdown("---")
                st.subheader(f"🔬 Hasil Diagnosa: {info['nama']} {info['icon']}")
                
                # Warna alert tergantung status
                # DIPERBAIKI: Menggunakan 'status' dari kamus
                if info['status'] == 'Normal':
                    st.success(f"**Kondisi:** {info['nama']}")
                elif 'Defisiensi' in info['status']:
                    st.warning(f"**Kondisi:** {info['nama']} (Kekurangan Nutrisi)")
                else: # 'Bahaya', 'Penyakit', dll.
                    st.error(f"**Kondisi:** {info['nama']} (Terdeteksi Penyakit)")
                    
                st.write(f"**Tingkat Keyakinan:** {conf*100:.2f}%")
                st.info(f"**Deskripsi:**\n{info['deskripsi']}")
                
                # Tampilkan Solusi Box dengan Tabs
                # DIPERBAIKI: Menggunakan 'penanganan' dan 'gejala'
                tab1, tab2, tab3 = st.tabs(["Gejala", "Penanganan", "Pencegahan"])

                with tab1:
                    st.markdown(info['gejala'])

                with tab2:
                    st.markdown(info['penanganan'])
                
                with tab3:
                    st.markdown(info['pencegahan'])

else:
    st.warning("Model AI belum siap. Harap periksa error di atas.")