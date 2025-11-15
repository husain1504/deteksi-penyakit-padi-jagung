# FILE INI KHUSUS BERISI DATA TEKS, GEJALA, DAN SOLUSI
# (Versi Padi + Jagung)

solusi_petani = {
    # ==========================================
    # --- DATA PENYAKIT PADI (UPDATED) ---
    # ==========================================
    'padi_bacterial_blight': {
        'nama': 'Hawar Daun Bakteri (Kresek) - Padi',
        'status': 'Bahaya',
        'style': 'danger',
        'icon': '🌾',
        'deskripsi': 'Penyakit yang disebabkan oleh bakteri Xanthomonas oryzae. Penyakit ini menyerang titik tumbuh dan daun, menyebabkan tanaman mengering seperti terbakar.',
        'gejala': '• Terdapat garis basah memanjang (water-soaked) pada tepi daun.\n• Daun berubah warna menjadi kuning-oranye, lalu mengering berwarna putih keabuan.\n• Pada serangan berat, seluruh tanaman layu (kresek).',
        'penanganan': '• **Kimia:** Semprotkan bakterisida berbahan aktif Tembaga Oksida (Copper Oxide) atau Tembaga Hidroksida.\n• **Alami:** Gunakan Paenibacillus polymyxa (bakteri antagonis).\n• Hindari pemupukan Urea (Nitrogen) berlebihan saat serangan terjadi.',
        'pencegahan': '• Gunakan varietas tahan (seperti Inpari 32/42).\n• Atur jarak tanam jajar legowo agar sirkulasi udara baik.\n• Lakukan pengairan berselang (intermittent) agar sawah tidak tergenang terus.'
    },
    'padi_brown_spot': {
        'nama': 'Bercak Coklat (Brown Spot) - Padi',
        'status': 'Penyakit Jamur',
        'style': 'warning',
        'icon': '🌾',
        'deskripsi': 'Penyakit jamur yang disebabkan oleh Helminthosporium oryzae. Sering terjadi pada tanah yang kurang hara (terutama Kalium dan Silika).',
        'gejala': '• Bercak berbentuk oval atau bulat seperti mata.\n• Bagian tengah bercak berwarna abu-abu/putih, tepi berwarna coklat kemerahan.\n• Menyerang daun dan bulir padi (menyebabkan bulir hampa/hitam).',
        'penanganan': '• **Kimia:** Semprot fungisida berbahan aktif Difenokonazol, Propikonazol, atau Mankozeb.\n• **Nutrisi:** Segera berikan pupuk Kalium (KCl) dan Silika untuk memperkuat dinding sel daun.',
        'pencegahan': '• Pemupukan berimbang (jangan cuma Urea).\n• Perbaiki kondisi tanah dengan bahan organik (kompos).'
    },
    'padi_leaf_blast': {
        'nama': 'Blast Daun (Potong Leher) - Padi',
        'status': 'Sangat Bahaya',
        'style': 'danger',
        'icon': '🔥',
        'deskripsi': 'Penyakit fungal oleh Pyricularia oryzae. Ini adalah salah satu penyakit padi paling merusak karena penyebarannya lewat udara sangat cepat.',
        'gejala': '• Bercak berbentuk belah ketupat (diamond shape) dengan ujung runcing.\n• Pusat bercak putih/abu-abu dengan tepi coklat kemerahan.\n• Bisa menyerang leher malai (Potong Leher) sehingga padi gagal panen.',
        'penanganan': '• **Kimia:** Gunakan fungisida sistemik berbahan aktif Tricyclazole, Isoprothiolane, atau Pyraclostrobin.\n• **Darurat:** Bakar sisa jerami tanaman yang terinfeksi parah agar spora tidak menyebar.',
        'pencegahan': '• Hindari tanam terlalu rapat.\n• Jangan gunakan pupuk Nitrogen (Urea) berlebihan.\n• Jaga sawah tetap tergenang air saat fase pertumbuhan.'
    },
    'padi_leaf_scald': {
        'nama': 'Hawar Pelepah (Leaf Scald) - Padi',
        'status': 'Penyakit',
        'style': 'warning',
        'icon': '🍂',
        'deskripsi': 'Penyakit yang disebabkan jamur Microdochium oryzae (atau Monographella albescens). Sering terjadi pada musim hujan dengan kelembapan tinggi.',
        'gejala': '• Pola zonasi (garis-garis) melingkar pada ujung daun atau pelepah.\n• Bagian yang sakit tampak basah lalu mengering coklat muda.\n• Daun tampak seperti tersiram air panas (melepuh).',
        'penanganan': '• **Kimia:** Semprot fungisida Benomyl, Karbendazim, atau Tiofanat Metil.\n• Potong dan buang bagian daun yang terinfeksi.',
        'pencegahan': '• Kurangi kelembapan dengan mengatur jarak tanam.\n• Bersihkan gulma yang bisa menjadi inang jamur.'
    },
    'padi_defisiensi_n': {
        'nama': 'Kekurangan Nitrogen (N) - Padi',
        'status': 'Defisiensi Hara',
        'style': 'warning',
        'icon': '🧪',
        'deskripsi': 'Tanaman padi kekurangan unsur Nitrogen, yang merupakan bahan utama pembentukan klorofil (zat hijau daun).',
        'gejala': '• Daun tanaman (terutama daun tua) menguning secara merata dari ujung ke pangkal.\n• Tanaman tumbuh kerdil dan kurus.\n• Anakan padi sedikit (jarang).',
        'penanganan': '• **Pupuk:** Segera taburkan pupuk Urea (46% N) atau ZA.\n• Gunakan Bagan Warna Daun (BWD) untuk mengukur dosis yang tepat.',
        'pencegahan': '• Lakukan pemupukan dasar sebelum tanam.\n• Gunakan pupuk kandang/organik untuk menjaga ketersediaan hara.'
    },
    'padi_defisiensi_p': {
        'nama': 'Kekurangan Fosfor (P) - Padi',
        'status': 'Defisiensi Hara',
        'style': 'warning',
        'icon': '🧪',
        'deskripsi': 'Kekurangan Fosfor menghambat pembentukan akar dan proses pembungaan/pengisian bulir pada padi.',
        'gejala': '• Daun berwarna hijau gelap kusam, kadang berubah menjadi ungu kemerahan.\n• Batang tanaman kecil dan pendek (kerdil).\n• Akar tanaman sedikit dan pendek.',
        'penanganan': '• **Pupuk:** Berikan pupuk SP-36, TSP, atau DAP.\n• Perbaiki pH tanah (jika tanah terlalu asam, Fosfor sulit diserap, tambahkan kapur dolomit).',
        'pencegahan': '• Pemberian pupuk Fosfor sebaiknya dilakukan di awal tanam (pupuk dasar).'
    },
    'padi_defisiensi_k': {
        'nama': 'Kekurangan Kalium (K) - Padi',
        'status': 'Defisiensi Hara',
        'style': 'warning',
        'icon': '🧪',
        'deskripsi': 'Kekurangan Kalium membuat tanaman padi lemah, mudah roboh, dan rentan terhadap serangan penyakit.',
        'gejala': '• Pinggiran daun (tepi) mengering berwarna coklat kemerahan (seperti terbakar/gosong).\n• Muncul bercak-bercak karat pada daun tua.\n• Batang padi lemah dan mudah rebah.',
        'penanganan': '• **Pupuk:** Berikan pupuk KCl atau NPK dengan kadar Kalium tinggi.\n• Bisa juga tambahkan abu sekam padi (sumber Kalium alami).',
        'pencegahan': '• Jangan buang jerami sisa panen, kembalikan ke sawah (jerami kaya Kalium).'
    },
    'padi_normal': {
        'nama': 'Padi Sehat',
        'status': 'Normal',
        'style': 'safe',
        'icon': '✅',
        'deskripsi': 'Tanaman padi dalam kondisi pertumbuhan optimal, tidak menunjukkan gejala serangan hama, penyakit, maupun kekurangan nutrisi.',
        'gejala': '• Daun berwarna hijau segar merata.\n• Helaian daun tegak dan tidak ada bercak.\n• Pertumbuhan tinggi tanaman dan jumlah anakan normal.',
        'penanganan': '• Lanjutkan perawatan rutin (pemupukan berimbang dan pengairan).\n• Lakukan pengamatan rutin (monitoring) seminggu sekali.',
        'pencegahan': '• Tetap waspada terhadap perubahan cuaca dan serangan hama sekitar.'
    },

    # ==========================================
    # --- DATA PENYAKIT JAGUNG (TAMBAHAN) ---
    # ==========================================
    'jagung_blight': {
        'nama': 'Hawar Daun (Leaf Blight) - Jagung',
        'status': 'Bahaya',
        'style': 'danger',
        'icon': '🌽',
        'deskripsi': 'Disebabkan oleh jamur Exserohilum turcicum (juga dikenal sebagai Helminthosporium turcicum). Penyakit ini sangat merusak dan bisa menurunkan hasil panen secara signifikan.',
        'gejala': '• Bercak oval panjang (bisa 5-15 cm) berwarna abu-abu kehijauan atau coklat.\n• Bercak terlihat seperti "cerutu" yang terbakar.\n• Pada kondisi lembab, bercak mungkin terlihat berjamur.',
        'penanganan': '• **Kimia:** Gunakan fungisida berbahan aktif Mankozeb, Propineb, atau Azoksistrobin segera setelah gejala pertama muncul.\n• Rotasi tanaman sangat disarankan.',
        'pencegahan': '• Tanam varietas hibrida yang tahan terhadap hawar daun.\n• Bersihkan sisa-sisa tanaman jagung (jerami) setelah panen karena jamur bertahan di sana.'
    },
    'jagung_common_rust': {
        'nama': 'Karat Daun (Common Rust) - Jagung',
        'status': 'Penyakit Jamur',
        'style': 'warning',
        'icon': '🌽',
        'deskripsi': 'Disebabkan oleh jamur *Puccinia sorghi*. Penyakit ini umum terjadi, terutama di cuaca lembab dan sejuk. Biasanya tidak terlalu fatal jika menyerang di akhir musim.',
        'gejala': '• Bercak (pustul) kecil berbentuk oval atau memanjang.\n• Bercak berwarna coklat kemerahan (seperti karat) pada permukaan atas dan bawah daun.\n• Jika digosok, serbuk karat akan menempel di jari.',
        'penanganan': '• **Kimia:** Jika serangan parah sebelum pembungaan, semprot fungisida berbahan aktif Propikonazol atau Triadimefon.\n• Biasanya tidak perlu ditangani jika sudah mendekati panen.',
        'pencegahan': '• Tanam varietas jagung yang tahan karat (sudah banyak tersedia).\n• Rotasi tanaman untuk memutus siklus jamur.'
    },
    'jagung_gray_leaf_spot': {
        'nama': 'Bercak Daun Abu-abu (Gray Spot) - Jagung',
        'status': 'Penyakit',
        'style': 'warning',
        'icon': '🌽',
        'deskripsi': 'Disebabkan oleh jamur *Cercospora zeae-maydis*. Penyakit ini berkembang pesat di kondisi cuaca yang hangat dan sangat lembab.',
        'gejala': '• Bercak kecil-kecil, awalnya titik, lalu memanjang menjadi persegi panjang (terbatas oleh tulang daun).\n• Bercak berwarna coklat muda hingga abu-abu.\n• Daun tampak "kotor" atau penuh bercak kecil.',
        'penanganan': '• **Kimia:** Fungisida berbahan aktif Piraklostrobin atau Flutriafol efektif mengendalikan penyakit ini.\n• Semprot segera jika penyakit muncul sebelum fase pembungaan.',
        'pencegahan': '• Tanam varietas yang tahan.\n• Lakukan pengolahan tanah (bajak) yang dalam untuk mengubur sisa tanaman terinfeksi.'
    },
    'jagung_healthy': {
        'nama': 'Jagung Sehat',
        'status': 'Normal',
        'style': 'safe',
        'icon': '✅',
        'deskripsi': 'Tanaman jagung dalam kondisi pertumbuhan optimal, tidak menunjukkan gejala serangan hama, penyakit, maupun kekurangan nutrisi.',
        'gejala': '• Daun berwarna hijau segar dan merata.\n• Batang tanaman kokoh dan tumbuh normal.',
        'penanganan': '• Lanjutkan perawatan rutin (pemupukan berimbang dan pengairan).',
        'pencegahan': '• Tetap waspada terhadap perubahan cuaca dan lakukan monitoring rutin.'
    }
}