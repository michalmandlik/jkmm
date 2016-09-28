## jkmm

### data load
1000k radku je za 2.41 s

### cele zpracovani
1000k radku je za cca 60 s

### nastaveni 
- pro funkcnost skriptu je potreba do adresare data nahrat delay_dataset.csv
- spustit generate_data.py (vygeneruje zmensena data)

### skripty
```
support/delay_distribution.py
support/pandas_distribution.py 
```
vygeneruje v adresari output csv s rozlozenim zpozdeni, pomoci readline, nebo pandas

**Pandas**
time: 5105.373852 s
lines: 52628832
est 50mio: 97 min

**Readline**
time: 2298.222812 s
lines: 52628832
est 50mio: 43 min

```
support/generate_data.py
```
vygeneruje pomocna data
```
support/benchmark.py
```
porovnava zpusoby prochazeni dat
```
support/max_min.py 
```
hleda maximum a minimum zpozdeni
```
support/pandas_test.py
```
pokusny skript na prochazeni pomoci pandas a chunk
```
support/plot_hist.py 
```
vygeneruje graf z data/delay_distribution.csv
