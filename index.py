// React Admin Panelinde (Örnek Kod Parçası)

const handleApprove = async (documentId, startDate) => {
    // Function 2'nin HTTP URL'si
    const functionUrl = 'https://[APPWRITE_ENDPOINT]/v1/functions/[FUNCTION_2_ID]/executions';

    try {
        const response = await fetch(functionUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Eğer function'ın izni gerektiriyorsa, API Key veya JWT Token eklenmeli
                // Basit bir örnek olduğu için burada atlanmıştır, ancak PRODUCTION'da GEREKLİ!
            },
            body: JSON.stringify({ documentId, startDate }),
        });

        if (response.ok) {
            alert('Kampanya başarıyla onaylandı!');
            // Listeyi güncelle
        } else {
            alert('Onaylama hatası!');
        }
    } catch (error) {
        console.error('API çağrısı hatası:', error);
    }
};

// ... JSX içinde kullanım
// <button onClick={() => handleApprove('belge_id_123', '2025-10-30')}>Onayla</button>