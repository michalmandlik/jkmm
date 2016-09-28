## jkmm

### data load
1000k radku je za 2.41 s

### cele zpracovani
1000k radku je za cca 60 s

### nastaveni 
- pro funkcnost skriptu je potreba do adresare data nahrat delay_dataset.csv
- spustit generate_data.py (vygeneruje zmensena data)

### skripty
'''
support/benchmark.py
porovnava zpusoby prochazeni dat
'''
support/delay_distribution.py vygeneruje v adresari output csv s rozlozenim zpozdeni
support/generate_data.py vygeneruje pomocna data
support/max_min.py hleda maximum a minimum zpozdeni
support/pandas_distribution.py vygeneruje sobor s rozlozenim zpozdeni pomoci pandas
support/pandas_test.py pokusny skript na prochazeni pomoci pandas a chunk
support/plot_hist.py vygeneruje graf z data/delay_distribution.csv
support/template.py
