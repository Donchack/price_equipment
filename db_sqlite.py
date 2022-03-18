import sqlite3
from time import sleep
def ignore_case_collation(value1_, value2_):
        if value1_.lower() == value2_.lower():
            return 0
        elif value1_.lower() < value2_.lower():
            return -1
        else:
            return 1 

def sqlite_lower(value_):
        return value_.lower()

def sqlite_upper(value_):
        return value_.upper()

class EquipDB:
    def __init__(self, database: str = 'equip.sqlite'):
        self._database = database
        with sqlite3.connect(self._database) as connection:
            connection.create_collation("NOCASE", ignore_case_collation)
            connection.execute("""create table if not exists equips (
                            id integer not null primary key autoincrement,
                            equip text not null COLLATE NOCASE,
                            type text COLLATE NOCASE);""")
            connection.execute("""create table if not exists prices (
                            id integer not null primary key autoincrement,
                            id_eq integer not null,
                            price real not null,
                            date date,
                            actual integer, 
                            foreign key (id_eq) references equips(id));""")                
            
    
    def get_eqips(self, id="", name_eq="", type_eq=""):
        with sqlite3.connect(self._database) as connection:
            connection.create_collation("NOCASE", ignore_case_collation)
            result = connection.execute("""select eq.id, eq.equip, eq.type, pr.id_eq, pr.price, pr.date, pr.actual from equips as eq  
                        LEFT OUTER JOIN (select * from prices where actual=1) as pr
                        ON eq.id =pr.id_eq
                        where eq.id LIKE ? and eq.equip LIKE ? and eq.type LIKE ?""", (f'%{id}%',f'%{name_eq}%', f'%{type_eq}%'))
        return result
    
    def add_equip(self, equip, type):
        with sqlite3.connect(self._database) as connection:
            connection.create_collation("NOCASE", ignore_case_collation)
            connection.execute("""insert into equips (equip, type)
                            values(?, ?)""", (equip, type))
    
    def del_equip(self, id):
        with sqlite3.connect(self._database) as connection:
            connection.create_collation("NOCASE", ignore_case_collation)
            connection.execute("""delete from equips 
                            where id = ?""", (id, ))

    def get_prices(self, id_eq=""):
        with sqlite3.connect(self._database) as connection:
            connection.create_collation("NOCASE", ignore_case_collation)
            result = connection.execute("""select * from prices where id_eq=? order by actual DESC, date DESC""", (id_eq,))
        return result

    def add_price(self, id_eq, price=0.0, date=0, actual=1):
        with sqlite3.connect(self._database) as connection:
            connection.create_collation("NOCASE", ignore_case_collation)
            cursor = connection.cursor()
            cursor.execute("""update prices set actual = ? where id_eq = ?""",(0,id_eq))
            cursor.execute("""insert into prices (id_eq, price, date, actual)
                            values(?, ?, ?, ?)""", (id_eq, price, date, actual))



    



