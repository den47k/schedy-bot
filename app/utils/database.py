import sqlite3
import datetime


class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_users_table()
        self.create_schedy_tables()

    def create_users_table(self):
        try:
            query = ('CREATE TABLE IF NOT EXISTS users('
                     'telegram_id INTEGER PRIMARY KEY,'
                     'group_name TEXT);')
            self.cursor.execute(query)
            self.connection.commit()
        except sqlite3.Error as Error:
            print('Error', Error)

    def create_schedy_tables(self):
        try:
            create_groups_query = '''CREATE TABLE IF NOT EXISTS Groups (
                                     group_id INTEGER PRIMARY KEY,
                                     group_name TEXT UNIQUE)'''

            create_schedy_query = '''CREATE TABLE IF NOT EXISTS Schedules (
                                     schedule_id INTEGER PRIMARY KEY,
                                     group_id INTEGER,
                                     date DATE,
                                     class_time_start TIME,
                                     class_time_end TIME,
                                     day_of_week TEXT,
                                     class_name TEXT,
                                     class_type TEXT,
                                     FOREIGN KEY (group_id) REFERENCES Groups(group_id))'''
            self.cursor.execute(create_groups_query)
            self.cursor.execute(create_schedy_query)
            self.connection.commit()
        except sqlite3.Error as Error:
            print('Error', Error)

    def create_user(self, tg_id):
        user = self.cursor.execute("SELECT 1 FROM users WHERE telegram_id == '{key}'".format(key=tg_id)).fetchone()
        if not user:
            self.cursor.execute('INSERT INTO users (telegram_id) VALUES (?)', (tg_id,))
            self.connection.commit()

    def edit_created_user(self, tg_id, group_name):
        self.cursor.execute("UPDATE users SET group_name = '{}' WHERE telegram_id == '{}'".format(
            group_name, tg_id))
        self.connection.commit()

    def check_group_name(self, tg_id):
        return self.cursor.execute("SELECT group_name FROM users WHERE "
                                   "telegram_id = '{key}'".format(key=tg_id)).fetchone()

    def get_groups_list(self):
        return [x[0] for x in self.cursor.execute("SELECT group_name FROM Groups").fetchall()]

    def get_next_class(self, group_name):
        current_date = datetime.date.today()
        current_time = datetime.datetime.now().time()
        query = '''SELECT * FROM Schedules
                   WHERE group_id = (SELECT group_id FROM Groups WHERE group_name = ?)
                   AND date >= ?
                   AND class_time_start > ?
                   ORDER BY date, class_time_start ASC
                   LIMIT 1'''
        self.cursor.execute(query, (group_name, current_date, current_time.strftime('%H:%M')))
        next_class = self.cursor.fetchone()
        if next_class:
            class_start_time = datetime.datetime.strptime(next_class[3], '%H:%M').time()
            time_remaining = datetime.datetime.combine(datetime.date.today(),
                                                       class_start_time) - datetime.datetime.now()
            time_remaining_str = str(time_remaining).split('.')[0]  # Remove microseconds
            return f"Next class: {next_class[6]} ({next_class[7]})\nTime remaining: {time_remaining_str}"
        else:
            return "No upcoming classes."

    def get_today(self, group_name):
        yesterday = datetime.date.today()
        query = '''SELECT * FROM Schedules
                   WHERE group_id = (SELECT group_id FROM Groups WHERE group_name = ?)
                   AND date >= ?
                   AND date <= ?'''
        self.cursor.execute(query, (group_name, yesterday, yesterday + datetime.timedelta(days=1)))
        today_classes = self.cursor.fetchall()
        if today_classes:
            return "\n\n".join([f"{class_info[3]} - {class_info[4]}: {class_info[6]} ({class_info[7]})"
                                for class_info in today_classes])
        else:
            return 'Looks like you don`t have any classes today. You are lucky!'

    def get_tomorrow(self, group_name):
        today = datetime.date.today()
        query = '''SELECT * FROM Schedules
                   WHERE group_id = (SELECT group_id FROM Groups WHERE group_name = ?)
                   AND date >= ?
                   AND date <= ?'''
        self.cursor.execute(query, (group_name, today + datetime.timedelta(days=1),
                                    today + datetime.timedelta(days=2)))
        tomorrow_classes = self.cursor.fetchall()

        if tomorrow_classes:
            return "\n\n".join([f"{class_info[3]} - {class_info[4]}: {class_info[6]} ({class_info[7]})"
                                for class_info in tomorrow_classes])
        else:
            return 'Looks like you don`t have any classes tomorrow. You are lucky!'

    def get_next_week(self, group_name):
        current_date = datetime.date.today()
        next_week_date = current_date + datetime.timedelta(weeks=1)
        query = '''SELECT * FROM Schedules
                   WHERE group_id = (SELECT group_id FROM Groups WHERE group_name = ?)
                   AND date >= ?
                   AND date <= ?'''
        self.cursor.execute(query, (group_name, current_date, next_week_date))
        next_week_classes = self.cursor.fetchall()

        if next_week_classes:
            return "\n\n".join([f"{class_info[6]} ({class_info[5]}) - {class_info[3]} to {class_info[4]}"
                                for class_info in next_week_classes])
        else:
            return 'Looks like you don`t have any classes for the whole next week. You are REALLY lucky!'

    def __del__(self):
        self.cursor.close()
        self.connection.close()
