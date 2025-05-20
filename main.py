import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import time

start = time.time()
# ------------------------------
# 📥 Wczytywanie danych
# ------------------------------
df1 = pd.read_excel('zakupy-online.xlsx', sheet_name='Year 2009-2010')
df2 = pd.read_excel('zakupy-online.xlsx', sheet_name='Year 2010-2011')
df = pd.concat([df1, df2], ignore_index=True)

# ------------------------------
# 🧹 Czyszczenie danych
# ------------------------------
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df = df[~df['Invoice'].astype(str).str.startswith('C')]
df = df.dropna()
df['TotalPrice'] = df['Quantity'] * df['Price']
df = df[(df['Quantity'] > 0) & (df['Price'] > 0) & (df['TotalPrice'] > 0)]
# ------------------------------
# 📊 Podstawowe statystyki zbioru
# ------------------------------
print("📅 Zakres dat:", df['InvoiceDate'].min(), "→", df['InvoiceDate'].max())
print("🌍 Liczba krajów:", df['Country'].nunique())
print("🌍 Lista krajów:", df['Country'].unique())
print("📦 Liczba unikalnych produktów:", df['StockCode'].nunique())
print("🧾 Liczba unikalnych faktur:", df['Invoice'].nunique())
print("👤 Liczba unikalnych klientów:", df['Customer ID'].nunique())

# 🔄 Zmienność sprzedaży w czasie
sprzedaz_dzienna = df.groupby(df['InvoiceDate'].dt.date).agg({
    'Invoice': 'nunique',
    'TotalPrice': 'sum'
}).rename(columns={'Invoice': 'LiczbaTransakcji', 'TotalPrice': 'Sprzedaz'})

print("\n📈 Sprzedaż dzienna (pierwsze dni):\n", sprzedaz_dzienna.head())

# 🏆 Najpopularniejsze produkty
top_produkty = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)
print("\n🏆 Najpopularniejsze produkty:\n", top_produkty)

# 💰 Najbardziej dochodowe produkty
top_przychod = df.groupby('Description')['TotalPrice'].sum().sort_values(ascending=False).head(10)
print("\n💰 Najbardziej dochodowe produkty:\n", top_przychod)

# ------------------------------
# 🔍 ANALIZA KOSZYKOWA PER KRAJ
# ------------------------------
kraje = df['Country'].unique()

for kraj in kraje:

    print(f"\n============================\n🌍 KRAJ: {kraj}\n============================")

    df_kraj = df[df['Country'] == kraj]

    if df_kraj.empty:
        print("⚠️ Brak danych dla tego kraju.")
        continue

    print("📅 Zakres dat:", df_kraj['InvoiceDate'].min(), "→", df_kraj['InvoiceDate'].max())
    print("📦 Liczba unikalnych produktów:", df_kraj['StockCode'].nunique())
    print("🧾 Liczba unikalnych faktur:", df_kraj['Invoice'].nunique())
    print("👤 Liczba unikalnych klientów:", df_kraj['Customer ID'].nunique())

    # 🧺 Macierz koszykowa (Invoice x Product)
    basket = df_kraj.groupby(['Invoice', 'Description'])['Quantity'].sum().unstack().fillna(0)
    basket = basket > 0

    if basket.empty or basket.shape[1] < 2:
        print("⚠️ Zbyt mało danych do analizy koszykowej.")
        continue

    # 🔁 Filtrowanie rzadkich produktów
    min_liczba_transakcji = 5
    product_counts = basket.sum()
    popularne_produkty = product_counts[product_counts >= min_liczba_transakcji]
    popularne_produkty = popularne_produkty.sort_values(ascending=False)

    # 🔒 LIMIT: maksymalnie 500 najczęstszych produktów
    popularne_produkty = popularne_produkty.head(2000).index
    basket = basket[popularne_produkty]

    if basket.shape[1] < 2:
        print("⚠️ Za mało popularnych produktów w koszykach.")
        continue

    # 🔢 min_support = próg 20% najpopularniejszych
    product_freq = basket.sum().sort_values(ascending=False)
    threshold = product_freq.quantile(0.8)
    min_sup = threshold / basket.shape[0]
    print(f"🔢 min_support (20% najpopularniejszych): {min_sup:.4f}")

    # 📘 Zbiory częste
    frequent_itemsets = apriori(basket, min_support=min_sup, use_colnames=True)
    frequent_itemsets = frequent_itemsets.sort_values(by='support', ascending=False)

    if frequent_itemsets.empty:
        print("⚠️ Brak zbiorów częstych.")
        continue

    print("📘 Zbiory częste:\n", frequent_itemsets.head())

    # 📎 Reguły asocjacyjne
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)
    rules = rules.sort_values(by='confidence', ascending=False)

    if rules.empty:
        print("⚠️ Brak reguł asocjacyjnych dla tego kraju.")
        continue

    print("📐 Reguły asocjacyjne:\n", rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head())

end = time.time()

print(f"\nCzas wykonania: {end - start :.4f} sekund")