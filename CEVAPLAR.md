# Algoritma Analizi ve Tasarımı — Ödev 3 Cevapları

**Ad-Soyad:** Samed Bilgin
**Numara:** —

---

## Soru 1 (20 puan) — İkili Arama Ağacı (BST) ve Gezintiler

Verilen ekleme sırası: **n, z, d, f, a, k, o, m, e, l, t, g**

### Adım Adım Ekleme

| Adım | Eklenen | Karar |
|------|---------|-------|
| 1 | n | Kök |
| 2 | z | z > n → n'in sağı |
| 3 | d | d < n → n'in solu |
| 4 | f | f < n, f > d → d'nin sağı |
| 5 | a | a < n, a < d → d'nin solu |
| 6 | k | k < n, k > d, k > f → f'nin sağı |
| 7 | o | o > n, o < z → z'nin solu |
| 8 | m | m < n, m > d, m > f, m > k → k'nın sağı |
| 9 | e | e < n, e > d, e < f → f'nin solu |
| 10 | l | l < n, l > d, l > f, l > k, l < m → m'nin solu |
| 11 | t | t > n, t < z, t > o → o'nun sağı |
| 12 | g | g < n, g > d, g > f, g < k → k'nın solu |

### Oluşan İkili Arama Ağacı

```
                     n
                   /   \
                  d     z
                /  \   /
               a    f o
                   / \  \
                  e   k  t
                     / \
                    g   m
                       /
                      l
```

### Gezintiler (Traversals)

- **Preorder** (Kök → Sol → Sağ):
  **n, d, a, f, e, k, g, m, l, z, o, t**

- **Inorder** (Sol → Kök → Sağ):
  **a, d, e, f, g, k, l, m, n, o, t, z**
  *(Beklendiği gibi alfabetik sıralı, çünkü BST in-order = sıralı çıktı verir.)*

- **Postorder** (Sol → Sağ → Kök):
  **a, e, g, l, m, k, f, d, t, o, z, n**

---

## Soru 2 (20 puan) — DFS Tabanlı Topological Sort

> **Not:** Aşağıda her grafın okunan kenar listesi ile birlikte çözüm verilmiştir.
> Grafiğinizde farklı bir kenar varsa, aynı algoritma akışını kendi kenar listenize uygulayın.
> Bu cevap koddan da otomatik olarak doğrulanmıştır — bkz. [`q2_topological.py`](q2_topological.py).

### Graf (a)

**Kenarlar:** `a→b, a→f, d→a, d→b, d→c, d→f, d→g, b→e, e→g, g→f`

**In-degree analizi:**
- a: 1 (d'den)
- b: 2 (a, d)
- c: 1 (d)
- d: **0** (kaynak)
- e: 1 (b)
- f: 3 (a, d, g)
- g: 2 (d, e)

Hiçbir düğüm bir back-edge oluşturmuyor (d'ye gelen kenar yok), dolayısıyla **döngü yoktur → DAG**, topolojik sıralama mümkündür.

**DFS (kaynak = d, alfabetik komşu sırası):**

```
DFS(d):
  DFS(a):
    DFS(b):
      DFS(e):
        DFS(g):
          DFS(f) ─ finish f          → yığın: [f]
          finish g                   → yığın: [f, g]
        finish e                     → yığın: [f, g, e]
      finish b                       → yığın: [f, g, e, b]
    DFS(f) zaten ziyaret
    finish a                         → yığın: [f, g, e, b, a]
  DFS(b) zaten ziyaret
  DFS(c) ─ finish c                  → yığın: [f, g, e, b, a, c]
  DFS(f), DFS(g) zaten ziyaret
  finish d                           → yığın: [f, g, e, b, a, c, d]
```

Bitiş zamanlarının **tersi** topolojik sıralamayı verir:

> **Topological order (a):  d → c → a → b → e → g → f**

### Graf (b)

**Kenarlar:** `a→b, b→c, c→d, a→e, b→f, c→f, e→f, f→g, d→g`

**In-degree analizi:**
- a: **0** (kaynak)
- b: 1 (a)
- c: 1 (b)
- d: 1 (c)
- e: 1 (a)
- f: 3 (b, c, e)
- g: 2 (d, f)

Geri kenar yok → **DAG**, topolojik sıralama mümkündür.

**DFS (kaynak = a, alfabetik komşu sırası):**

```
DFS(a):
  DFS(b):
    DFS(c):
      DFS(d):
        DFS(g) ─ finish g            → yığın: [g]
        finish d                     → yığın: [g, d]
      DFS(f):
        DFS(g) zaten
        finish f                     → yığın: [g, d, f]
      finish c                       → yığın: [g, d, f, c]
    DFS(f) zaten
    finish b                         → yığın: [g, d, f, c, b]
  DFS(e):
    DFS(f) zaten
    finish e                         → yığın: [g, d, f, c, b, e]
  finish a                           → yığın: [g, d, f, c, b, e, a]
```

Bitiş zamanlarının tersi:

> **Topological order (b):  a → e → b → c → f → d → g**

Doğrulama: bütün kenarlar (u→v) için u, sıralamada v'den önce gelir ✓.

### Döngü olsaydı ne olurdu?

DFS sırasında, **henüz finish olmamış (gri renkli) bir düğüme tekrar gidilmesi back-edge'dir**. Back-edge keşfedilirse graf döngü içerir → **topolojik sıralama tanımsızdır**, çünkü topolojik sıralama tüm kenarları "geriye dönmeyecek" şekilde dizmeyi gerektirir; döngüde her düğüm hem önce hem sonra olmak zorunda kalır ki bu çelişir.

---

## Soru 3 (60 puan) — BST, AVL, 2-3 Ağacı Karşılaştırması

Kod: [`q3_trees.py`](q3_trees.py) (Python 3)

### Çalıştırma

```bash
python3 q3_trees.py
```

> Kodda `random.seed(42)` sabitlenmiştir; aşağıdaki çıktı bu seed ile yeniden üretilebilir. Seed satırı kaldırılırsa her çalıştırmada farklı bir veri seti üretilir.

### Çıktı

```
======================================================================
VERİ SETİ (0-1000 arası 20 rastgele sayı, bir defa üretildi)
======================================================================
[654, 114, 25, 759, 281, 250, 228, 142, 754, 104, 692, 758, 913, 558, 89, 604, 432, 32, 30, 95]

======================================================================
BINARY SEARCH TREE
======================================================================
└── root: 654
    ├── L: 114
    │   ├── L: 25
    │   │   ├── L: ·
    │   │   └── R: 104
    │   │       ├── L: 89
    │   │       │   ├── L: 32
    │   │       │   │   ├── L: 30
    │   │       │   │   └── R: ·
    │   │       │   └── R: 95
    │   │       └── R: ·
    │   └── R: 281
    │       ├── L: 250
    │       │   ├── L: 228
    │       │   │   ├── L: 142
    │       │   │   └── R: ·
    │       │   └── R: ·
    │       └── R: 558
    │           ├── L: 432
    │           └── R: 604
    └── R: 759
        ├── L: 754
        │   ├── L: 692
        │   └── R: 758
        └── R: 913

→ Karşılaştırma: 62, Swap: 0

======================================================================
AVL TREE
======================================================================
└── root: 281 (h=5)
    ├── L: 114 (h=4)
    │   ├── L: 89 (h=3)
    │   │   ├── L: 30 (h=2)
    │   │   │   ├── L: 25 (h=1)
    │   │   │   └── R: 32 (h=1)
    │   │   └── R: 104 (h=2)
    │   │       ├── L: 95 (h=1)
    │   │       └── R: ·
    │   └── R: 228 (h=2)
    │       ├── L: 142 (h=1)
    │       └── R: 250 (h=1)
    └── R: 754 (h=4)
        ├── L: 654 (h=3)
        │   ├── L: 558 (h=2)
        │   │   ├── L: 432 (h=1)
        │   │   └── R: 604 (h=1)
        │   └── R: 692 (h=1)
        └── R: 759 (h=2)
            ├── L: 758 (h=1)
            └── R: 913 (h=1)

→ Karşılaştırma: 60, Rotation (swap): 10

======================================================================
2-3 TREE
======================================================================
└── root: [250]
    ├── C0: [89]
    │   ├── C0: [30]
    │   │   ├── C0: [25]
    │   │   └── C1: [32]
    │   └── C1: [114]
    │       ├── C0: [95, 104]
    │       └── C1: [142, 228]
    └── C1: [754]
        ├── C0: [558, 654]
        │   ├── C0: [281, 432]
        │   ├── C1: [604]
        │   └── C2: [692]
        └── C1: [759]
            ├── C0: [758]
            └── C1: [913]

→ Karşılaştırma: 65, Split (swap): 12
```

### Karşılaştırma Tablosu

| Veri (özet) | Binary Search Tree | AVL Tree | 2-3 Tree |
|---|---|---|---|
| 654, 114, 25, 759, 281, 250, 228, 142, 754, 104, 692, 758, 913, 558, 89, 604, 432, 32, 30, 95 | **62 karşılaştırma, 0 swap** | **60 karşılaştırma, 10 rotation** | **65 karşılaştırma, 12 split** |

### Yorum

- **BST**: hiçbir dengeleme yapmadığı için en az karşılaştırma ile kurulur ve 0 swap yapar; ancak veriler kötü dağılmışsa yüksek (dengesiz) ağaç oluşur.
- **AVL**: her insertion sonrası dengeyi kontrol ettiği için karşılaştırma sayısı BST'ye yakındır, fakat **rotation (swap)** maliyeti vardır; karşılığında en sıkı yükseklik garantisi (≈ 1.44·log n) elde edilir.
- **2-3 Ağacı**: bir düğümde 1 veya 2 anahtar tutabildiği için **toplam yükseklik en azdır**. Karşılaştırma sayısı AVL ile yarışır; "swap" yerine **split** sayılır.

> Veri rastgele üretildiğinden her çalıştırmada sayılar değişebilir, ancak göreli sıralama (BST swap=0, AVL ve 2-3 dengeleme maliyeti olur) genellikle korunur.
