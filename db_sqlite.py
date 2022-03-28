import sqlite3

def sqlite_lower(value_):
        return value_.lower()

def sqlite_upper(value_):
        return value_.upper()

def ignore_case_collation(value1_, value2_):
        if value1_.lower() == value2_.lower():
            return 0
        elif value1_.lower() < value2_.lower():
            return -1
        else:
            return 1

class EquipDB:
    def __init__(self, database: str = 'equip.sqlite'):
        self._database = database
        with sqlite3.connect(self._database) as connection:
            connection.create_collation("NOCASE", ignore_case_collation)
            # таблица оборудования
            connection.execute("""create table if not exists equips (
                            id integer not null primary key autoincrement,
                            equip text not null COLLATE NOCASE,
                            type text COLLATE NOCASE);""")
            # таблица цен
            connection.execute("""create table if not exists prices (
                            id integer not null primary key autoincrement,
                            id_eq integer not null,
                            price real not null,
                            date date,
                            actual integer, 
                            foreign key (id_eq) references equips(id));""")
            # таблица заказчиков
            connection.execute("""create table if not exists customer (
                            id_cust integer not null primary key autoincrement,
                            name_customer text not null COLLATE NOCASE,
                            profile text COLLATE NOCASE);""")
            # таблица статусов проектов
            connection.execute("""create table if not exists prj_stat (
                            id_pstat integer not null primary key autoincrement,
                            name_status text not null COLLATE NOCASE);""")
            # таблица регионов
            connection.execute("""create table if not exists region (
                            id_region integer not null primary key,
                            name_region text not null COLLATE NOCASE);""")
            # таблица проектов
            connection.execute("""create table if not exists prj (
                            id_prj integer not null primary key autoincrement,
                            id_cust integer not null,
                            object text COLLATE NOCASE,
                            id_deliv_reg integer not null,
                            date_creat date,
                            id_status integer not null,
                            foreign key (id_cust) references customer(id_cust),
                            foreign key (id_deliv_reg) references region(id_region),
                            foreign key (id_status) references prj_stat(id_pstat));""")
            # таблица калькуляций
            
            #таблица истории  проекта                
    
    def get_eqips(self, id="", name_eq="", type_eq=""):
        with sqlite3.connect(self._database) as connection:
            #Redefining NOCASE, LOWER, UPPER to ignore the case of Russian letters in Unicode
            connection.create_collation("NOCASE", ignore_case_collation)
            connection.create_function("LOWER", 1, sqlite_lower)
            connection.create_function("UPPER", 1, sqlite_upper)
            result = connection.execute("""select eq.id, eq.equip, eq.type, pr.id_eq, pr.price, pr.date, pr.actual from equips as eq  
                        LEFT OUTER JOIN (select * from prices where actual=1) as pr
                        ON eq.id =pr.id_eq
                        where eq.id LIKE ? and LOWER(eq.equip) LIKE ? and LOWER(eq.type) LIKE ?""", (f'%{id}%',f'%{name_eq.lower()}%', f'%{type_eq.lower()}%'))
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
            result = connection.execute("""select * from prices where id_eq=? order by actual DESC, date DESC""", (id_eq,))
        return result

    def add_price(self, id_eq, price=0.0, date=0, actual=1):
        with sqlite3.connect(self._database) as connection:
            cursor = connection.cursor()
            #Removing a sign of the relevance of the old price
            cursor.execute("""update prices set actual = ? where id_eq = ?""",(0,id_eq))
            cursor.execute("""insert into prices (id_eq, price, date, actual)
                            values(?, ?, ?, ?)""", (id_eq, price, date, actual))

    def get_prj(self, id="", object="", type_eq=""):
        with sqlite3.connect(self._database) as connection:
            #Redefining NOCASE, LOWER, UPPER to ignore the case of Russian letters in Unicode
            connection.create_collation("NOCASE", ignore_case_collation)
            connection.create_function("LOWER", 1, sqlite_lower)
            connection.create_function("UPPER", 1, sqlite_upper)
            result = connection.execute("""select * from prj where
                            id_prj=? and LOWER(object) LIKE ?
                            """, (id, f'%{object.lower()}%'))
        return result
    
    def get_customer(self, id_cust="", customer="", prof=""):
        with sqlite3.connect(self._database) as connection:
            #Redefining LOWER to ignore the case of Russian letters in Unicode
            connection.create_function("LOWER", 1, sqlite_lower)
            # compare the lower symbols from the table with the lower symbols from the function parameters
            result = connection.execute("""select * from customer
                            where id_cust LIKE ? and LOWER(name_customer) LIKE ? and LOWER(profile) LIKE ?
                            order by id_cust""", (f'%{id_cust}%', f'%{customer.lower()}%', f'%{prof.lower()}%'))
        return result

    def add_customer(self, customer, prof):
        with sqlite3.connect(self._database) as connection:
            connection.execute("""insert into customer (name_customer, profile)
                            values(?, ?)""", (customer, prof))
    
    def del_customer(self, id):
        with sqlite3.connect(self._database) as connection:
            connection.execute("""delete from customer 
                            where id_cust = ?""", (id, ))

    def upd_customer(self, id, customer, prof):
        with sqlite3.connect(self._database) as connection:
            connection.execute("""update customer 
                            SET name_customer=?, profile=?
                            where id_cust = ?""", (customer, prof, id))

    



