import sqlite3

class EquipDB:
    def __init__(self, database: str = 'equip.sqlite'):
        self._database = database
        with sqlite3.connect(self._database) as connection:
            cursor = connection.cursor()
            cursor.execute("""create table if not exists equips (
                            id integer not null primary key autoincrement,
                            equip text not null,
                            type text);""")
            connection.commit()
    
    def get_eqips(self):
        with sqlite3.connect(self._database) as connection:
            cursor = connection.cursor()
            result = cursor.execute("""select * from equips""")
        return result
    
    def add_equip(self, equip, type):
        with sqlite3.connect(self._database) as connection:
            cursor = connection.cursor()
            cursor.execute("""insert into equips (equip, type)
                            values(?, ?)""", (equip, type))
            connection.commit()
    


    



