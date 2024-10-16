import requests
from bs4 import BeautifulSoup
import sqlite3
import datetime


r = requests.get('https://planzajec.uek.krakow.pl/index.php?typ=G&grupa=Modern%20Business%20Management%20(MB)')
main_html_text = r.content
soup = BeautifulSoup(main_html_text.decode('utf-8'), 'lxml')


links = {group_name.text: f"https://planzajec.uek.krakow.pl/{group_name['href'][:-1]}2"
         for group_name in soup.find_all('a', href=True)}

for k, v in links.items():
    print(f'{k}: {v}')


def get_schedule(group_name, url):
    r = requests.get(url)
    main_html_text = r.content
    soup = BeautifulSoup(main_html_text.decode('utf-8'), 'lxml')

    class_data_list = []

    classes = soup.find_all('tr')

    for course in classes:
        columns = course.find_all('td')

        if columns != [] and len(columns) == 6:
            class_datetime = datetime.datetime.strptime(f'{columns[0].text}', '%Y-%m-%d')
            class_time_start = datetime.datetime.strptime(columns[1].text[3:8], '%H:%M').time()
            class_time_end = datetime.datetime.strptime(columns[1].text[11:16], '%H:%M').time()
            class_day = columns[1].text[:2]
            class_name = columns[2].text
            class_type = columns[3].text
            class_prof = columns[4].text

            if class_prof == ' Językowe Centrum ':
                class_name = 'Language course'

            class_data_list.append((class_datetime, class_time_start, class_time_end, class_day, class_name, class_type))

    return {group_name: class_data_list}


def insert_data(schedule_data):
    conn = sqlite3.connect('C:\\schedyBotProto\\schedy_db.db')
    c = conn.cursor()

    for group_name, class_data_list in schedule_data.items():
        # Inserting group if not exists
        c.execute("INSERT OR IGNORE INTO Groups (group_name) VALUES (?)", (group_name,))
        conn.commit()

        # Getting group_id
        c.execute("SELECT group_id FROM Groups WHERE group_name=?", (group_name,))
        group_id = c.fetchone()[0]

        # Iterate over each class data
        for class_data in class_data_list:
            class_datetime, class_time_start, class_time_end, class_day, class_name, class_type = class_data

            # Convert time objects to strings
            class_time_start_str = class_time_start.strftime("%H:%M")
            class_time_end_str = class_time_end.strftime("%H:%M")

            # Inserting schedule
            c.execute("INSERT INTO Schedules "
                      "(group_id, date, class_time_start, class_time_end, day_of_week, class_name, class_type) "
                      "VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (group_id, class_datetime, class_time_start_str,
                       class_time_end_str, class_day, class_name, class_type))
            conn.commit()

    conn.close()


for k, v in links.items():
    schedule_data = get_schedule(k, v)
    insert_data(schedule_data)
