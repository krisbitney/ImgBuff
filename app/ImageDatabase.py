import sqlite3

# For SQLite date storage tips see: https://www.sqlitetutorial.net/sqlite-date/


def dict_factory(cursor, row):
    row_dict = {}
    for i, col in enumerate(cursor.description):
        row_dict[col[0]] = row[i]
    return row_dict


class ImageDatabase:
    _database_uri = 'database.db'
    _connection = None
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ImageDatabase, cls).__new__(cls)
            cls._connection = sqlite3.connect(cls._database_uri)
            cls._connection.row_factory = dict_factory
            if not cls._instance.create_images_table():
                raise sqlite3.Error("Failed to create database table")
        return cls._instance

    def __del__(self):
        self._connection.close()

    def create_images_table(self) -> bool:
        try:
            self._connection.execute('''CREATE TABLE IF NOT EXISTS images
                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             user TEXT NOT NULL,
                             uri TEXT NOT NULL,
                             create_date TEXT NOT NULL,
                             rating INTEGER NOT NULL,
                             active INTEGER NOT NULL);''')
        except sqlite3.Error:
            return False
        return True

    async def insert_image(self, user: str, uri: str) -> bool:
        values = (user, uri)
        try:
            self._connection.execute("INSERT INTO images VALUES(NULL, ?, ?, datetime('now'), -1, 1);", values)
            self._connection.commit()
        except sqlite3.Error:
            raise
            return False
        return True

    async def delete_image(self, image_id: int) -> bool:
        values = (image_id,)
        try:
            self._connection.execute("DELETE FROM images WHERE id=?;", values)
            self._connection.commit()
        except sqlite3.Error:
            return False
        return True

    async def deactivate_image(self, image_id: int) -> bool:
        values = (image_id,)
        try:
            self._connection.execute("UPDATE images SET active=0 WHERE id=?;", values)
            self._connection.commit()
        except sqlite3.Error:
            return False
        return True

    async def get_image(self, user: str, uri: str) -> dict:
        '''
        :param user: username
        :param uri: image URL
        :return: a dictionary that can easily be converted to a json object
        '''
        values = (user, uri)
        try:
            cursor = self._connection.cursor()
            cursor.execute("SELECT id, uri, create_date, rating FROM images WHERE active=1 AND user=? AND uri=?;", values)
            result = cursor.fetchall()
        except sqlite3.Error:
            raise
            return {}
        return result[0]

    async def get_user_images(self, user: str) -> list:
        '''
        :param user: username
        :return: a list of dictionaries that can easily be converted to json
        '''
        values = (user,)
        try:
            cursor = self._connection.cursor()
            cursor.execute("SELECT id, uri, create_date, rating FROM images WHERE active=1 AND user=?;", values)
            result = cursor.fetchall()
        except sqlite3.Error:
            raise
            return []
        return result
