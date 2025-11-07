/**
 * Oda Kontrol ve Yeniden Dolum JavaScript Modülü
 */

console.log('=== ODA KONTROL JS BAŞLADI ===');

// Global değişkenler
let secilenOdaId = null;
let secilenOdaNo = null;
let secilenKatAdi = null;
let aktifUrun = null;
let qrScanner = null;

// CSRF Token
const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
console.log('CSRF Token:', csrfToken);

/**
 * Sayfa yüklendiğinde
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('Oda kontrol JS yüklendi');
    
    // Kat seçimi event listener
    const katSelect = document.getElementById('kat_id');
    if (katSelect) {
        katSelect.addEventListener('change', katSecildi);
        console.log('Kat select event listener eklendi');
    } else {
        console.error('kat_id elementi bulunamadı!');
    }
    
    // Oda seçimi event listener
    const odaSelect = document.getElementById('oda_id');
    if (odaSelect) {
        odaSelect.addEventListener('change', odaSecildi);
        console.log('Oda select event listener eklendi');
    } else {
        console.error('oda_id elementi bulunamadı!');
    }
});

/**
 * Kat seçildiğinde odaları yükle
 */
async function katSecildi() {
    const katId = document.getElementById('kat_id').value;
    const odaSelect = document.getElementById('oda_id');
    
    console.log('Kat seçildi:', katId);
    
    // Reset
    odaSelect.innerHTML = '<option value="">Oda seçiniz...</option>';
    odaSelect.disabled = true;
    urunListesiniGizle();
    
    if (!katId) {
        console.log('Kat ID boş, işlem iptal');
        return;
    }
    
    try {
        console.log('Odalar getiriliyor...');
        const response = await fetch(`/kat-odalari?kat_id=${katId}`);
        const data = await response.json();
        
        console.log('API yanıtı:', data);
        
        if (data.success && data.odalar && data.odalar.length > 0) {
            console.log(`${data.odalar.length} oda bulundu`);
            data.odalar.forEach(oda => {
                const option = document.createElement('option');
                option.value = oda.id;
                option.textContent = oda.oda_no;
                odaSelect.appendChild(option);
            });
            odaSelect.disabled = false;
        } else {
            console.log('Oda bulunamadı');
            odaSelect.innerHTML = '<option value="">Bu katta oda yok</option>';
        }
    } catch (error) {
        console.error('Hata:', error);
        hataGoster('Odalar yüklenirken bir hata oluştu');
    }
}

/**
 * Oda seçildiğinde ürünleri getir
 */
async function odaSecildi() {
    const odaId = document.getElementById('oda_id').value;
    
    if (!odaId) {
        urunListesiniGizle();
        return;
    }
    
    secilenOdaId = odaId;
    await minibarUrunleriniGetir(odaId);
}

/**
 * Minibar ürünlerini API'den getir
 */
async function minibarUrunleriniGetir(odaId) {
    loadingGoster();
    
    try {
        const response = await fetch('/api/kat-sorumlusu/minibar-urunler', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ oda_id: odaId })
        });
        
        const data = await response.json();
        
        if (data.success) {
            secilenOdaNo = data.data.oda_no;
            secilenKatAdi = data.data.kat_adi;
            
            if (data.data.urunler.length === 0) {
                bosDurumGoster();
            } else {
                urunListesiGoster(data.data.urunler);
            }
        } else {
            hataGoster(data.message || 'Ürünler yüklenirken hata oluştu');
        }
    } catch (error) {
        console.error('Hata:', error);
        hataGoster('Ürünler yüklenirken bir hata oluştu');
    } finally {
        loadingGizle();
    }
}

/**
 * Ürün listesini göster
 */
function urunListesiGoster(urunler) {
    // Container'ı göster
    document.getElementById('urun_listesi_container').classList.remove('hidden');
    document.getElementById('bos_durum_mesaji').classList.add('hidden');
    document.getElementById('urun_tablosu').classList.remove('hidden');
    
    // Oda bilgilerini güncelle
    document.getElementById('secili_oda_no').textContent = secilenOdaNo;
    document.getElementById('secili_kat_adi').textContent = secilenKatAdi;
    
    // Tablo body'sini temizle
    const tbody = document.getElementById('urun_tbody');
    tbody.innerHTML = '';
    
    // Ürünleri ekle
    urunler.forEach(urun => {
        const tr = document.createElement('tr');
        tr.className = 'cursor-pointer transition-colors';
        tr.onclick = () => uruneTiklandi(urun);
        
        tr.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-900">
                ${urun.urun_adi}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                ${urun.mevcut_miktar}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                ${urun.birim}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                <button onclick="event.stopPropagation(); uruneTiklandi(${JSON.stringify(urun).replace(/"/g, '&quot;')})"
                    class="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700">
                    <svg class="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                    </svg>
                    Dolum Yap
                </button>
            </td>
        `;
        
        tbody.appendChild(tr);
    });
}

/**
 * Boş durum mesajını göster
 */
function bosDurumGoster() {
    document.getElementById('urun_listesi_container').classList.remove('hidden');
    document.getElementById('bos_durum_mesaji').classList.remove('hidden');
    document.getElementById('urun_tablosu').classList.add('hidden');
    
    // Oda bilgilerini güncelle
    document.getElementById('secili_oda_no').textContent = secilenOdaNo;
    document.getElementById('secili_kat_adi').textContent = secilenKatAdi;
}

/**
 * Ürün listesini gizle
 */
function urunListesiniGizle() {
    document.getElementById('urun_listesi_container').classList.add('hidden');
    secilenOdaId = null;
    secilenOdaNo = null;
    secilenKatAdi = null;
}

/**
 * Ürüne tıklandığında yeniden dolum modalını aç
 */
function uruneTiklandi(urun) {
    aktifUrun = urun;
    yenidenDolumModalAc(urun);
}

/**
 * Yeniden dolum modalını aç
 */
function yenidenDolumModalAc(urun) {
    document.getElementById('modal_urun_adi').textContent = urun.urun_adi;
    document.getElementById('modal_mevcut_miktar').textContent = urun.mevcut_miktar;
    document.getElementById('modal_birim').textContent = urun.birim;
    document.getElementById('eklenecek_miktar').value = '';
    
    document.getElementById('yeniden_dolum_modal').classList.remove('hidden');
    document.getElementById('eklenecek_miktar').focus();
}

/**
 * Yeniden dolum modalını kapat
 */
function yenidenDolumModalKapat() {
    document.getElementById('yeniden_dolum_modal').classList.add('hidden');
    // NOT: aktifUrun'u burada null yapma, onay modalı için gerekli!
}

/**
 * Dolum yap butonuna tıklandığında
 */
function dolumYap() {
    const eklenecekMiktar = parseFloat(document.getElementById('eklenecek_miktar').value);
    
    // Validasyon
    if (!eklenecekMiktar || eklenecekMiktar <= 0) {
        hataGoster('Lütfen geçerli bir miktar giriniz');
        return;
    }
    
    // Onay modalını aç
    onayModalAc(eklenecekMiktar);
}

/**
 * Onay modalını aç
 */
function onayModalAc(eklenecekMiktar) {
    const mevcutMiktar = aktifUrun.mevcut_miktar;
    const yeniMiktar = mevcutMiktar + eklenecekMiktar;
    
    document.getElementById('onay_urun_adi').textContent = aktifUrun.urun_adi;
    document.getElementById('onay_mevcut_miktar').textContent = `${mevcutMiktar} ${aktifUrun.birim}`;
    document.getElementById('onay_eklenecek_value').textContent = eklenecekMiktar;
    document.getElementById('onay_yeni_miktar').textContent = `${yeniMiktar} ${aktifUrun.birim}`;
    document.getElementById('onay_zimmet_dusum').textContent = `${eklenecekMiktar} ${aktifUrun.birim} ${aktifUrun.urun_adi}`;
    
    // Yeniden dolum modalını kapat
    yenidenDolumModalKapat();
    
    // Onay modalını göster
    document.getElementById('onay_modal').classList.remove('hidden');
}

/**
 * Onay modalını kapat
 */
function onayModalKapat() {
    document.getElementById('onay_modal').classList.add('hidden');
    aktifUrun = null;  // Onay modalı kapanınca temizle
}

/**
 * İşlemi onayla ve API'ye gönder
 */
async function islemOnayla() {
    const eklenecekMiktar = parseFloat(document.getElementById('eklenecek_miktar').value);
    
    // Butonları disable et
    document.getElementById('onay_btn').disabled = true;
    
    try {
        const response = await fetch('/api/kat-sorumlusu/yeniden-dolum', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                oda_id: secilenOdaId,
                urun_id: aktifUrun.urun_id,
                eklenecek_miktar: eklenecekMiktar
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            basariGoster(data.message || 'Dolum işlemi başarıyla tamamlandı');
            onayModalKapat();
            aktifUrun = null;  // İşlem başarılı, temizle

            // Ürün listesini yenile
            await minibarUrunleriniGetir(secilenOdaId);
        } else {
            hataGoster(data.message || 'İşlem sırasında bir hata oluştu');
        }
    } catch (error) {
        console.error('Hata:', error);
        hataGoster('İşlem sırasında bir hata oluştu. Lütfen tekrar deneyiniz');
    } finally {
        document.getElementById('onay_btn').disabled = false;
    }
}

/**
 * HTTPS kontrolü yap
 */
function checkHttps() {
    return window.location.protocol === 'https:';
}

/**
 * Kamera izni kontrol et
 */
async function checkCameraPermission() {
    try {
        // Permissions API destekleniyor mu?
        if (navigator.permissions && navigator.permissions.query) {
            const permission = await navigator.permissions.query({ name: 'camera' });
            console.log('Kamera izni durumu:', permission.state);
            return permission.state;
        }
        return 'prompt'; // Varsayılan olarak sor
    } catch (err) {
        console.log('Permission API desteklenmiyor:', err);
        return 'prompt';
    }
}

/**
 * Manuel oda seçimi
 */
function manuelOdaSecimi() {
    qrModalKapat();
    // Kullanıcıyı manuel seçim alanına yönlendir
    document.getElementById('kat_id').focus();
}

/**
 * QR kod okutmayı başlat
 */
async function qrIleBaslat() {
    document.getElementById('qr_modal').classList.remove('hidden');

    // HTTPS kontrolü
    if (!checkHttps()) {
        console.warn('HTTPS bağlantısı yok, kamera erişimi engellenebilir');
        document.getElementById('https_uyari').classList.remove('hidden');
    }

    if (!qrScanner) {
        qrScanner = new Html5Qrcode("qr_reader");
        console.log('Yeni QR scanner oluşturuldu');
    }

    // Eğer scanner zaten çalışıyorsa önce durdur
    if (qrScanner) {
        try {
            // isScanning metodu varsa kontrol et
            const state = qrScanner.getState();
            console.log('QR Scanner state:', state);

            // State 2 = SCANNING
            if (state === 2) {
                console.log('Scanner zaten çalışıyor, önce durduruluyor...');
                await qrScanner.stop();
                console.log('Scanner durduruldu');
                // Durdurulduktan sonra kısa bir bekleme
                await new Promise(resolve => setTimeout(resolve, 100));
            }
        } catch (err) {
            console.log('Scanner state kontrolü yapılamadı veya zaten durdurulmuş:', err.message);
        }
    }

    // Optimize edilmiş QR okuma ayarları
    const config = {
        fps: 5,  // Daha yavaş tara (daha iyi algılama)
        qrbox: { width: 300, height: 300 },  // Daha büyük tarama alanı
        aspectRatio: 1.0,
        disableFlip: false,
        // Daha agresif tarama
        experimentalFeatures: {
            useBarCodeDetectorIfSupported: true
        }
    };

    // Kamera ayarları - SADECE facingMode kullan (tek key)
    const cameraConfig = { facingMode: "environment" };

    try {
        await qrScanner.start(
            cameraConfig,
            config,
            onQrCodeScanned,
            onQrCodeError
        );
        console.log('QR scanner başarıyla başlatıldı');
    } catch (err) {
        console.error('QR okuyucu başlatılamadı:', err);

        // Hata tipine göre mesaj göster
        if (err.name === 'NotAllowedError' || err.message.includes('Permission')) {
            // Kamera izni reddedildi
            document.getElementById('kamera_izin_uyari').classList.remove('hidden');
            hataGoster('Kamera iznini lütfen verin veya manuel oda seçimi yapın');
        } else if (err.name === 'NotFoundError') {
            // Kamera bulunamadı
            hataGoster('Kamera bulunamadı. Manuel oda seçimi yapabilirsiniz');
        } else if (err.name === 'NotSupportedError' || !checkHttps()) {
            // HTTPS gerekli
            document.getElementById('https_uyari').classList.remove('hidden');
            hataGoster('HTTPS bağlantısı gerekli. Manuel oda seçimi yapabilirsiniz');
        } else {
            // Diğer hatalar
            hataGoster('Kamera erişimi sağlanamadı. Manuel oda seçimi yapabilirsiniz');
        }

        console.log('Manuel oda seçimi için kullanıcı yönlendiriliyor...');
        // Modal'ı kapatma, kullanıcı kendisi kapatabilir veya manuel seçim yapabilir
    }
}

/**
 * QR kod okunduğunda
 */
async function onQrCodeScanned(decodedText) {
    console.log('✅ QR kod başarıyla okundu:', decodedText);
    console.log('QR kod uzunluğu:', decodedText.length);
    console.log('QR kod tipi:', typeof decodedText);

    // QR scanner'ı durdur
    if (qrScanner) {
        try {
            const state = qrScanner.getState();
            console.log('QR okunduktan sonra scanner state:', state);

            // State 2 = SCANNING, sadece çalışıyorsa durdur
            if (state === 2) {
                await qrScanner.stop();
                console.log('QR scanner durduruldu');
            } else {
                console.log('Scanner zaten durdurulmuş, state:', state);
            }
        } catch (err) {
            console.log('QR scanner durdurma kontrolü hatası:', err.message);
        }
    }

    // Modalı kapat
    document.getElementById('qr_modal').classList.add('hidden');
    console.log('QR modal kapatıldı');

    try {
        const response = await fetch('/api/kat-sorumlusu/qr-parse', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ token: decodedText })
        });

        const data = await response.json();
        console.log('QR parse yanıtı:', data);

        if (data.success) {
            // Önce kat seç
            const katSelect = document.getElementById('kat_id');
            katSelect.value = data.data.kat_id;
            console.log('Kat dropdown değeri set edildi:', data.data.kat_id);

            // Kat seçilince odaları yükle
            await katSecildi();
            console.log('Odalar yüklendi');

            // Odaların yüklenmesi için kısa bir bekleme
            await new Promise(resolve => setTimeout(resolve, 300));

            // Sonra oda seç
            const odaSelect = document.getElementById('oda_id');
            odaSelect.value = data.data.oda_id;
            console.log('Oda dropdown değeri set edildi:', data.data.oda_id);

            // Oda seçilince ürünleri yükle
            await odaSecildi();
            console.log('Ürünler yüklendi');

            basariGoster(`Oda ${data.data.oda_no} seçildi`);
        } else {
            hataGoster(data.message || 'QR kod okunamadı');
        }
    } catch (error) {
        console.error('QR kod hatası:', error);
        hataGoster('QR kod işlenirken hata oluştu');
    }
}

/**
 * QR kod okuma hatası
 */
function onQrCodeError(errorMessage, error) {
    // Sadece gerçek hataları logla (sürekli scan hataları değil)
    if (errorMessage && !errorMessage.includes('NotFoundException')) {
        console.warn('QR okuma hatası:', errorMessage, error);
    }
}

/**
 * QR modalını kapat
 */
async function qrModalKapat() {
    if (qrScanner) {
        try {
            const state = qrScanner.getState();
            console.log('QR Modal kapatılırken scanner state:', state);

            // State 2 = SCANNING, sadece çalışıyorsa durdur
            if (state === 2) {
                await qrScanner.stop();
                console.log('QR scanner durduruldu (manuel)');
            } else {
                console.log('Scanner zaten durdurulmuş, state:', state);
            }
        } catch (err) {
            console.log('QR durdurma kontrolü hatası:', err.message);
        }
    }
    document.getElementById('qr_modal').classList.add('hidden');
    console.log('QR modal kapatıldı (manuel)');
}

/**
 * Test QR kodu (Debug amaçlı)
 */
function testQrCode() {
    // İlk odanın test token'ını oluştur
    const testToken = 'MINIBAR_ODA_1_KAT_1';
    console.log('Test QR kodu simüle ediliyor:', testToken);

    // QR okuma fonksiyonunu çağır
    onQrCodeScanned(testToken);
}

/**
 * Loading spinner göster
 */
function loadingGoster() {
    document.getElementById('loading_spinner').classList.remove('hidden');
}

/**
 * Loading spinner gizle
 */
function loadingGizle() {
    document.getElementById('loading_spinner').classList.add('hidden');
}

/**
 * Başarı mesajı göster (Toast)
 */
function basariGoster(mesaj) {
    // Basit toast notification
    const toast = document.createElement('div');
    toast.className = 'fixed top-4 right-4 bg-green-600 text-white px-6 py-3 rounded-lg shadow-lg z-50 animate-fade-in';
    toast.innerHTML = `
        <div class="flex items-center">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
            <span>${mesaj}</span>
        </div>
    `;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

/**
 * Hata mesajı göster (Toast)
 */
function hataGoster(mesaj) {
    // Basit toast notification
    const toast = document.createElement('div');
    toast.className = 'fixed top-4 right-4 bg-red-600 text-white px-6 py-3 rounded-lg shadow-lg z-50 animate-fade-in';
    toast.innerHTML = `
        <div class="flex items-center">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
            <span>${mesaj}</span>
        </div>
    `;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// ESC tuşu ile modal kapatma (accessibility)
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        if (!document.getElementById('yeniden_dolum_modal').classList.contains('hidden')) {
            yenidenDolumModalKapat();
        }
        if (!document.getElementById('onay_modal').classList.contains('hidden')) {
            onayModalKapat();
        }
        if (!document.getElementById('qr_modal').classList.contains('hidden')) {
            qrModalKapat();
        }
    }
});
