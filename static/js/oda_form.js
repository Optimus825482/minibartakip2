/**
 * Oda Formu - Dinamik Kat Yükleme
 * Otel seçildiğinde otele ait katları AJAX ile yükler
 */

// Katları yükleyen yardımcı fonksiyon
function yukleKatlar(otelId, katSelectId, callback) {
    const katSelect = document.getElementById(katSelectId);
    
    if (!katSelect) return;
    
    // Kat dropdown'unu temizle
    katSelect.innerHTML = '<option value="">Yükleniyor...</option>';
    katSelect.disabled = true;
    
    if (!otelId || otelId === '0' || otelId === '') {
        katSelect.innerHTML = '<option value="">Önce otel seçin...</option>';
        return;
    }
    
    // AJAX ile katları yükle
    fetch(`/api/oteller/${otelId}/katlar`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Katlar yüklenemedi');
            }
            return response.json();
        })
        .then(katlar => {
            // Dropdown'u doldur
            katSelect.innerHTML = '<option value="">Kat Seçin...</option>';
            
            if (katlar.length === 0) {
                katSelect.innerHTML = '<option value="">Bu otelde kat bulunamadı</option>';
            } else {
                katlar.forEach(kat => {
                    const option = document.createElement('option');
                    option.value = kat.id;
                    option.textContent = `${kat.kat_adi} (${kat.kat_no})`;
                    katSelect.appendChild(option);
                });
                katSelect.disabled = false;
            }
            
            // Callback varsa çalıştır
            if (callback) callback(katlar);
        })
        .catch(error => {
            console.error('Hata:', error);
            katSelect.innerHTML = '<option value="">Hata oluştu, tekrar deneyin</option>';
        });
}

document.addEventListener('DOMContentLoaded', function() {
    // Form sayfası için (otel_id ve kat_id)
    const otelSelect = document.getElementById('otel_id');
    const katSelect = document.getElementById('kat_id');
    
    if (otelSelect && katSelect) {
        otelSelect.addEventListener('change', function() {
            yukleKatlar(this.value, 'kat_id');
        });
    }
    
    // Yeni Oda Modal için
    const yeniOtelSelect = document.getElementById('yeniOtelId');
    if (yeniOtelSelect) {
        yeniOtelSelect.addEventListener('change', function() {
            yukleKatlar(this.value, 'yeniKatId');
        });
    }
    
    // Oda Düzenle Modal için
    const duzenleOtelSelect = document.getElementById('duzenleOtelId');
    if (duzenleOtelSelect) {
        duzenleOtelSelect.addEventListener('change', function() {
            yukleKatlar(this.value, 'duzenleKatId');
        });
    }
});
