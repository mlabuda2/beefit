import csv

with open('TABELA_WARTOSCI_ODZYWCZYCH.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    print("PRODUKT KALORIE BIAŁKO TŁUSZCZE WĘGLOWODANY w 100g")
    for row in reader:
        print(row[0], row[1], row[2], row[3])
