# AT_03 — Algoritma Analizi ve Tasarımı, Ödev 3

Veritabanı/Algoritma dersi 3. ödev — BST, AVL, 2-3 Ağacı + Topological Sort + BST Traversals.

## Dosyalar

| Dosya | Açıklama |
|---|---|
| `AT_A_2025_26_Bahar_Odev3.pdf` | Ödev sorularının orijinal dosyası |
| `CEVAPLAR.md` | Üç sorunun cevabı (Markdown kaynak) |
| `CEVAPLAR.pdf` | EDS'ye yüklenecek PDF (UTF-8 Türkçe) |
| `q1_verify.py` | Soru 1 BST traversal'larını koddan doğrular |
| `q2_topological.py` | Soru 2 DFS tabanlı topological sort + döngü tespiti |
| `q3_trees.py` | Soru 3: BST + AVL + 2-3 ağacı karşılaştırması |

## Çalıştırma

Python 3 gerekir. Ek bağımlılık yoktur (sadece standart kütüphane).

```bash
python3 q1_verify.py        # Soru 1 doğrulaması (preorder/inorder/postorder)
python3 q2_topological.py   # Soru 2 doğrulaması (DFS topological sort)
python3 q3_trees.py         # Soru 3: 20 rastgele sayıyla 3 ağacın karşılaştırması
```

`q3_trees.py` içinde `random.seed(42)` sabittir → çıktı `CEVAPLAR.md` ile birebir aynıdır. Her seferinde farklı veri istenirse seed satırı silinebilir.

## PDF üretmek (isteğe bağlı)

`CEVAPLAR.md`'i PDF'e çevirmek için:

```bash
sudo apt-get install -y pandoc wkhtmltopdf
pandoc CEVAPLAR.md -o CEVAPLAR.html --standalone -V lang=tr
wkhtmltopdf --encoding utf-8 CEVAPLAR.html CEVAPLAR.pdf
```
