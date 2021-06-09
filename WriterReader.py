import csv
class WR:
    def Reader():
        with open('Counter.csv') as File:
            reader = csv.reader(File, delimiter=',', quotechar=',',
                            quoting=csv.QUOTE_MINIMAL)
            for Count in reader:
                if len(Count) <= 0:
                    break
                else:
                    print(reader)
                    count = str(Count[0])
                    print(Count)
                    print(count)

    def Writer():
        with open('sw_data_new.csv', 'w') as File:
            writer = csv.writer(File)
            count += 1
            writer.writerow(count)