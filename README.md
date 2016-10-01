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
learn.py
```
Nacte soubor delays_dataset.csv a vygeneruje soubory vertList.csv
a nodeList.csv v adresari output.
```
generate_adv.py
```
Nacte soubor delays_dataset.csv a rozdeli ho na 52 sad souboru.
learn.csv - 1mio radku ucicich dat
test.csv - 1k radku testovacich dat bez actual_departure
control.csv - stejne jako test.csv, ale s doplnenymi hodnotami
```
support/generate_data.py
```
vygeneruje pomocna data

```
support/max_min.py 
```
hleda maximum a minimum zpozdeni


