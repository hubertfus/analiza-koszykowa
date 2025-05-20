## 📄 **Dokumentacja programu – Analiza koszykowa i reguły asocjacyjne**

### 🧠 **Opis działania programu**

Program analizuje dane zakupowe sklepu internetowego z lat 2009–2011. Składa się z kilku głównych etapów:

---

### 1. 📥 **Wczytywanie danych**

Program importuje dane z dwóch arkuszy pliku `zakupy-online.xlsx`:

```python
df1 = pd.read_excel('zakupy-online.xlsx', sheet_name='Year 2009-2010')
df2 = pd.read_excel('zakupy-online.xlsx', sheet_name='Year 2010-2011')
df = pd.concat([df1, df2], ignore_index=True)
```

---

### 2. 🧹 **Czyszczenie danych**

* Konwersja daty faktury na format datetime.
* Usunięcie zwrotów (faktury zaczynające się na „C”).
* Usunięcie wierszy z brakującymi danymi.
* Obliczenie wartości sprzedaży dla każdej pozycji.
* Filtrowanie tylko pozytywnych wartości (ilość, cena, kwota).

```python
df['TotalPrice'] = df['Quantity'] * df['Price']
```

---

### 3. 📊 **Analiza statystyczna danych**

Wyświetlane są podstawowe informacje:

* Zakres dat w zbiorze danych
* Liczba krajów, klientów, faktur i produktów
* Lista najczęściej kupowanych produktów
* Lista najbardziej dochodowych produktów
* Dzienna zmienność sprzedaży

---

### 4. 🔍 **Analiza koszykowa per kraj**

Dla każdego kraju:

#### a) 🔄 Przygotowanie danych:

* Tworzenie macierzy koszykowej (invoice × product)
* Filtrowanie produktów rzadko kupowanych
* Ograniczenie liczby produktów do max. 2000 najczęstszych

#### b) 📘 Wydobywanie zbiorów częstych:

Za pomocą algorytmu **Apriori**:

```python
frequent_itemsets = apriori(basket, min_support=min_sup, use_colnames=True)
```

* `min_support` ustalany dynamicznie na podstawie progu 20% najczęstszych produktów

#### c) 📎 Generowanie reguł asocjacyjnych:

Za pomocą funkcji `association_rules()` z minimalną pewnością (`confidence`) ≥ 0.7:

```python
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)
```

---

### ⌛ **Czas wykonania**

Na końcu program podaje łączny czas działania:

```python
print(f"\nCzas wykonania: {end - start :.4f} sekund")
```

---

## 📈 **Opis wyników**

### 🔢 Statystyki ogólne:

* **Zakres dat**: od najwcześniejszej do najpóźniejszej daty w fakturach.
* **Kraje**: lista państw, z których pochodzą klienci.
* **Produkty**: liczba unikalnych produktów i ich popularność.
* **Klienci**: liczba unikalnych klientów.

### 🏆 Najpopularniejsze produkty:

Produkty o najwyższej liczbie sprzedanych sztuk. Przykład:

```
WHITE HANGING HEART T-LIGHT HOLDER    2310
REGENCY CAKESTAND 3 TIER              2118
```

### 💰 Najbardziej dochodowe produkty:

Produkty o najwyższej łącznej wartości sprzedaży. Przykład:

```
DOTCOM POSTAGE                        206247.46
REGENCY CAKESTAND 3 TIER              164762.06
```

---

### 🌍 Wyniki analizy koszykowej:

Dla każdego kraju program:

1. Tworzy zestawienie częstych zbiorów zakupowych.
2. Wyznacza reguły asocjacyjne typu:
   **Jeśli klient kupił \[A, B], to prawdopodobnie kupi \[C]**.
3. Podaje wskaźniki:

   * `support`: jak często zestaw występuje
   * `confidence`: jak często konsekwencja występuje przy zaistniałych przesłankach
   * `lift`: siła zależności (czy zakup jednego wpływa na drugi)

Przykładowa reguła:

```
antecedents: {REGENCY CAKESTAND 3 TIER}
consequents: {GREEN REGENCY TEACUP AND SAUCER}
support: 0.042
confidence: 0.83
lift: 3.12
```

---

## ❗ Uwagi

* Limit produktów (2000) zabezpiecza algorytm Apriori przed nadmiernym obciążeniem.
* Wartość `min_support` ustalana dynamicznie dla każdego kraju.

---

## ✅ Wnioski

* Program skutecznie analizuje duży zbiór danych sprzedażowych i wyodrębnia zależności zakupowe w poszczególnych krajach.
* Reguły asocjacyjne mogą wspierać działania marketingowe (np. rekomendacje produktów).
* Czas działania jest zależny od rozmiaru danych i liczby krajów.
