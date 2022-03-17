import sqlite3
from time import sleep

class EquipDB:
    def __init__(self, database: str = 'equip.sqlite'):
        self._database = database
        with sqlite3.connect(self._database) as connection:
            connection.execute("""create table if not exists equips (
                            id integer not null primary key autoincrement,
                            equip text not null,
                            type text);""")
            connection.execute("""create table if not exists prices (
                            id integer not null primary key autoincrement,
                            id_eq integer not null,
                            price real not null,
                            date integer,
                            actual integer, 
                            foreign key (id_eq) references equips(id));""")                
            
            
    
    def get_eqips(self, id="", name_eq="", type_eq=""):
        with sqlite3.connect(self._database) as connection:
            result = connection.execute("""select * from equips where id LIKE ? and equip LIKE ? and type LIKE ?""", (f'%{id}%',f'%{name_eq}%', f'%{type_eq}%'))
        return result
    
    def add_equip(self, equip, type):
        with sqlite3.connect(self._database) as connection:
            connection.execute("""insert into equips (equip, type)
                            values(?, ?)""", (equip, type))
    
    def del_equip(self, id):
        with sqlite3.connect(self._database) as connection:
            connection.execute("""delete from equips 
                            where id = ?""", (id, ))

    def get_prices(self, id_eq=""):
        with sqlite3.connect(self._database) as connection:
            result = connection.execute("""select * from prices where id_eq=?""", (id_eq,))
        return result

    def add_price(self, id_eq, price=0.0, date=0, actual=''):
        with sqlite3.connect(self._database) as connection:
            cursor = connection.cursor()
            cursor.execute("""insert into prices (id_eq, price, date, actual)
                            values(?, ?, ?, ?)""", (id_eq, price, date, actual))



    



