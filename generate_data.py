import csv, random, time, datetime, math


def nb_wave(second_of_day, pep):
    t = second_of_day / 600
    t -= 68
    if t <= 4:
        return int(pep * t / 4);
    else:
        t -= 1
        return int(pep - (pep * (t - 4) / 5))


def temp_wave(second_of_day, predTemp):
    t = second_of_day / 600
    if t <= 72:
        return predTemp * t / 72;
    else:
        return predTemp - (predTemp * (t - 72) / 72)


def main():
    with open('data.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # Timestamp : au format unix +10 minutes par ligne
        # Day : de 0 à 6 (lundi au dimanche)
        # Nb : historique du nombre de personne pour chaque timestamp
        # Venir : 0 ou 1
        filewriter.writerow(['Hour', 'Minute', 'Day', 'Temperature', 'Nb', 'Venir'])

        # on demarre le 1 janvier 2019
        timestamp = 1546300800

        pep = 0
        for i in range(49104): # generer 341 jours (341 * 144 [144 est 24h divisé en 10 min]) du 01/01/2019 au 08/12/2019 (debut du projet)
            nb = 0
            venir = 1
            day = datetime.datetime.fromtimestamp(timestamp).weekday() # jour de la semaine (lundi = 0, dimanche = 6)
            second_of_day = timestamp % 86400

            # si 11h30 à 13h et pas le week-end
            if second_of_day in range(41400, 46800) and day != 5 and day != 6:
                if pep == 0 :
                    pep = random.randint(80, 160) 
                nb = nb_wave(second_of_day, pep)
            else:
                pep = 0

            if second_of_day == 0 :
                predTemp = random.randint(10, 25)

            temperature = int(temp_wave(second_of_day, predTemp))

            if temperature > 18:
                nb = int(nb * 0.7)

            if nb >= 90 or not second_of_day in range(41400, 46800) or day == 5 or day == 6:
                venir = 0
            
            if second_of_day in range(36000, 50400):
                filewriter.writerow([math.floor(second_of_day/3600), math.floor(second_of_day%3600/60),  day, temperature, nb, venir])
            
            timestamp += 600 # increment de 10 min


if __name__ == '__main__':
    main()