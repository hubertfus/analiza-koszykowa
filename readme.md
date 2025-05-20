# 📄 Analiza koszykowa danych transakcyjnych sklepu internetowego (2009–2011)

## 1. 🎯 Cel badania

Celem przeprowadzonego badania było wykrycie ukrytych wzorców współwystępowania produktów w zamówieniach klientów sklepu internetowego. W tym celu zastosowano **analizę koszykową** opartą na algorytmie **Apriori** oraz wygenerowano **reguły asocjacyjne**, pozwalające zidentyfikować zestawy produktów, które są często kupowane wspólnie. Dodatkowym celem była analiza zmienności tych wzorców w zależności od kraju pochodzenia klienta.

---

## 2. 📥 Zestaw danych

Dane obejmują transakcje sklepu internetowego dokonane w latach **2009–2011**. Zostały one wczytane z dwóch arkuszy pliku `zakupy-online.xlsx`, obejmujących odpowiednio okresy:

* **2009–2010** (`Year 2009-2010`)
* **2010–2011** (`Year 2010-2011`)

Po scaleniu zbioru otrzymano następujące statystyki ogólne:

| Miara                       | Wartość                         |
| --------------------------- | ------------------------------- |
| Zakres dat                  | 1 grudnia 2009 – 9 grudnia 2011 |
| Liczba transakcji (faktur)  | 36 969                          |
| Liczba unikalnych klientów  | 5 878                           |
| Liczba unikalnych produktów | 4 631                           |
| Liczba krajów               | 41                              |

Wśród krajów obecnych w zbiorze danych znalazły się m.in.: **United Kingdom**, **France**, **Germany**, **USA**, **Australia**, **Netherlands**, **Sweden**, **Italy** i inne.

---

## 3. 🧹 Przetwarzanie i czyszczenie danych

W celu zapewnienia spójności i wiarygodności analizy przeprowadzono szereg kroków przygotowawczych:

1. **Konwersja typu danych** – kolumna `InvoiceDate` została przekształcona na typ `datetime`.
2. **Usunięcie zwrotów** – faktury oznaczone jako zwroty (identyfikatory rozpoczynające się od „C”) zostały odrzucone.
3. **Usunięcie braków danych** – usunięto rekordy zawierające wartości `NaN`.
4. **Filtracja transakcji** – uwzględniono tylko te, w których `Quantity`, `Price` oraz obliczona `TotalPrice` były większe od zera.
5. **Utworzenie zmiennej TotalPrice** – iloczyn ilości i ceny jednostkowej dla danego produktu w transakcji.

---

## 4. 📊 Analiza opisowa

### 4.1 Zmienność sprzedaży w czasie

Obliczono dzienną liczbę transakcji oraz dzienny przychód. Przykładowe wartości:

| Data       | Liczba transakcji | Sprzedaż (GBP) |
| ---------- | ----------------- | -------------- |
| 2009-12-01 | 98                | 44 048,69      |
| 2009-12-02 | 110               | 52 941,99      |
| 2009-12-03 | 122               | 67 479,08      |

### 4.2 Najczęściej kupowane produkty (liczba sztuk)

| Produkt                            | Ilość   |
| ---------------------------------- | ------- |
| WORLD WAR 2 GLIDERS ASSTD DESIGNS  | 109 169 |
| WHITE HANGING HEART T-LIGHT HOLDER | 93 640  |
| PAPER CRAFT , LITTLE BIRDIE        | 80 995  |

### 4.3 Najbardziej dochodowe produkty (łączna sprzedaż)

| Produkt                            | Przychód (GBP) |
| ---------------------------------- | -------------- |
| REGENCY CAKESTAND 3 TIER           | 286 486,30     |
| WHITE HANGING HEART T-LIGHT HOLDER | 252 072,46     |
| PAPER CRAFT , LITTLE BIRDIE        | 168 469,60     |

---

## 5. 🔍 Analiza koszykowa (market basket analysis)

### 5.1 Metodyka

Dla każdego kraju osobno przeprowadzono analizę koszykową:

1. **Utworzenie macierzy koszykowej** – reprezentacja transakcji jako macierzy *faktura × produkt* z wartościami binarnymi (czy dany produkt wystąpił w transakcji).
2. **Filtrowanie rzadkich produktów** – uwzględniono tylko produkty występujące w co najmniej 5 koszykach; ograniczono liczbę produktów do 2000 najpopularniejszych.
3. **Wyznaczenie progu wsparcia (support)** – ustalany dynamicznie jako próg 80. percentyla częstości występowania produktów podzielony przez liczbę transakcji.
4. **Algorytm Apriori** – identyfikacja zbiorów częstych (*frequent itemsets*).
5. **Generowanie reguł asocjacyjnych** – reguły oparte na metrykach: `support`, `confidence` i `lift`.

---

## 🌍 6. Studium przypadku: Wielka Brytania

### 6.1 Statystyki

| Miara             | Wartość                         |
| ----------------- | ------------------------------- |
| Zakres dat        | 1 grudnia 2009 – 9 grudnia 2011 |
| Liczba faktur     | 33 541                          |
| Liczba produktów  | 4 616                           |
| Liczba klientów   | 5 350                           |
| Próg min\_support | 0.0124                          |

### 6.2 Zbiory częste (najpopularniejsze itemsets)

| Support | Zestaw produktów                   |
| ------- | ---------------------------------- |
| 0.1402  | WHITE HANGING HEART T-LIGHT HOLDER |
| 0.0852  | REGENCY CAKESTAND 3 TIER           |
| 0.0747  | ASSORTED COLOUR BIRD ORNAMENT      |
| 0.0713  | JUMBO BAG RED RETROSPOT            |
| 0.0579  | PARTY BUNTING                      |

### 6.3 Reguły asocjacyjne

| Antecedents (Jeśli...)     | Consequents (to...) | Support | Confidence | Lift  |
| -------------------------- | ------------------- | ------- | ---------- | ----- |
| GREEN TEACUP + PINK TEACUP | ROSES TEACUP        | 0.028   | 0.88       | 36.05 |
| PINK TEACUP                | ROSES TEACUP        | 0.032   | 0.83       | 33.65 |
| GREEN TEACUP               | PINK TEACUP         | 0.035   | 0.79       | 28.97 |

**Interpretacja:** wysoka wartość wskaźnika *lift* (>30) wskazuje na bardzo silną zależność pomiędzy zakupami elementów tej samej serii porcelany.

---

## 7. ⏱ Wydajność programu

Całkowity czas wykonania analizy (dla wszystkich krajów):

```python
Czas wykonania: 98.6341 sekund
```

---

## 8. ✅ Wnioski

* Dane sprzedażowe zawierają liczne wzorce zakupowe, które można z powodzeniem wykrywać za pomocą analizy koszykowej.
* W krajach takich jak **Wielka Brytania** zauważalna jest silna współzależność zakupów produktów tej samej kategorii (np. zastawy stołowej).
* Zidentyfikowane reguły asocjacyjne mogą być wykorzystane do:

  * rekomendacji produktów (systemy rekomendacyjne),
  * optymalizacji ekspozycji towarów,
  * analiz zachowań konsumenckich.
* Dynamiczne dopasowywanie progu `support` umożliwia elastyczną analizę nawet w krajach o mniejszej liczbie transakcji.

---
