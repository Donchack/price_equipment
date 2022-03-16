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
    
    def get_eqips(self, s_id="", s_name_eq="", s_type_eq=""):
        with sqlite3.connect(self._database) as connection:
            cursor = connection.cursor()
            result = cursor.execute("""select * from equips where id LIKE ? and equip LIKE ? and type LIKE ?""", (f'%{s_id}%',f'%{s_name_eq}%', f'%{s_type_eq}%'))
        return result
    
    def add_equip(self, equip, type):
        with sqlite3.connect(self._database) as connection:
            cursor = connection.cursor()
            cursor.execute("""insert into equips (equip, type)
                            values(?, ?)""", (equip, type))
            connection.commit()
    
    def del_equip(self, id):
        with sqlite3.connect(self._database) as connection:
            cursor = connection.cursor()
            cursor.execute("""delete from equips 
                            where id = ?""", (id, ))
            connection.commit()


    



