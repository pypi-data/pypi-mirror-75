from datetime import datetime

def sort(emlmsglst):
    emlmsgdict = {datetime.strptime(msg.date, '%a, %d %b %Y %H:%M:%S '+\
                                    msg.date.split()[-1]): msg for msg in \
                                    emlmsglst}
    return [emlmsgdict[x] for x in list(sorted(list(emlmsgdict.keys())))]
