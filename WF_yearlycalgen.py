#!/usr/bin/python3
# -*- coding: Utf-8 -
""" Generate yearly calendar on a specific name as a parameter in worflowy style"""

import datetime

convert_month = {'January': 'Janvier',
                 'February': 'Février',
                 'March': 'Mars',
                 'April': 'Avril',
                 'May': 'Mai',
                 'June': 'Juin',
                 'July': 'Juillet',
                 'August': 'Août',
                 'September': 'Septembre',
                 'October': 'Octobre',
                 'November': 'Novembre',
                 'December': 'Décembre'}


def list_days(year):
    """ return list of days as '2024-11-27'
    """
    start = datetime.date(year, 1, 1)
    res = []
    for day in range(366):
        date = (start + datetime.timedelta(days=day)).isoformat()
        res.append(date)
        if date == f'{year}-12-31':
            break
    return res


def format_date(mydate: datetime):
    """ format date '2024-11-27' as 'Sun, Nov 27, 2024'
    """
    mydate = datetime.date.fromisoformat(mydate)
    res = mydate.strftime("%a, %b ")
    d = mydate.strftime("%d")
    res += d[0].replace("0", "") + d[1] + mydate.strftime(", %Y")
    print(res)
    input()
    return res


def header():
    """return header of xml file"""
    return '<?xml version="1.0"?>\n<opml version="2.0">\n\t<body>\n'


def footer():
    return '\t\t\t</outline>\n\t\t</outline>\n\t</body>\n</opml>'


def format_day_line(mydate):
    """<outline text="&lt;time startYear=&quot;2026&quot; startMonth=&quot;1&quot
    ; startDay=&quot;1&quot;&gt;Thu, Jan 1, 2026&lt;/time&gt;" />"""
    fdate = format_date(mydate)
    d = datetime.date.fromisoformat(mydate).strftime("%d")
    d = d[0].replace("0", "") + d[1]
    m = datetime.date.fromisoformat(mydate).strftime("%m")
    m = m[0].replace("0", "") + m[1]
    y = mydate[:4]
    res = f'\t\t\t\t<outline text="&lt;time startYear=&quot;{y}&quot;' \
          f' startMonth=&quot;{m}&quot; startDay=&quot;{d}&quot;&gt;'
    res += fdate + '&lt;/time&gt;" />\n'
    return res


def format_month_line(mydate):
    """ return <outline text="Janvier">"""
    month = datetime.date.fromisoformat(mydate).strftime("%B")
    return f'\t\t\t<outline text="{convert_month[month]}">\n'


def format_year_line(mydate):
    """"return <outline text="2026">"""
    return f'\t\t<outline text="{mydate[:4]}">\n'


def format_outer_line():
    return '\t\t\t</outline>\n'


def main(year):
    days = list_days(year)  # list days of the year

    with open(f'workflowy-calendar-{year}.xml', 'w', encoding='utf8') as f:  # create file to write in
        f.write(header())  # write header
        f.write(format_year_line(days[0]))  # write year
        last_month = None
        for d in days:  # write each days line
            if d[5:7] != last_month:  # check if we change month
                if last_month is not None:
                    f.write(format_outer_line())
                last_month = d[5:7]
                f.write(format_month_line(d))
            f.write(format_day_line(d))
        f.write(footer())


if __name__ == "__main__":
    while True:
        ayear = input("Pour quelle année voulez-vous un calendrier (0 = Exit) ? ")
        if ayear == '0':
            print("\nMerci et au revoir...")
            break
        main(int(ayear))
        print(f'\t-> Fichier correctement généré : workflowy-calendar-{ayear}.xml\n')
