# Isometric Bursa (prototip)

OSM verisinden üretilen, tarayıcıda çizilen izometrik Bursa haritası. Bağımsız statik site.

## Çalıştırma
    python3 -m http.server 8765   # sonra http://localhost:8765

## Veriyi yenileme
OSM `api/0.6/map?bbox=...` parçalarını (<=0.005 derece) indirip:

    python3 tools/build_data.py <osm_klasoru> data/bursa.json

Kapsam: Bursa merkezi, yaklaşık 29.055-29.080 D, 40.178-40.193 K.

## Bilinen sınırlar
- OSM'de Bursa'nın birçok yerinde bina verisi seyrek, yükseklik çoğunlukla tahmini.
- Bu bir "çizim" değil, stilize 3B render; Isometric Istanbul'daki AI çizim katmanı yok.
- Tüm veri tek JSON; büyük alan için karo (tile) sistemine geçmek gerekir.
