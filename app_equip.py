from flask import Flask, render_template, request
import db_sqlite

app = Flask(__name__)


@app.route('/eqip_prices', methods=['GET','POST'])
def eqip_prices() -> str:
    dbs = db_sqlite.EquipDB()
    if request.form.get('bottom_clear'):
        s_id = s_name_eq = s_type_eq = ''
    else:
        s_id = request.form.get('search_id','')
        s_name_eq = request.form.get('search_name_eq','')
        s_type_eq = request.form.get('search_type_eq','')
    result = dbs.get_eqips(id = s_id, name_eq = s_name_eq, type_eq = s_type_eq)
    return render_template('eqip_prices.html', the_title='CПИСОК ОБОРУДОВАНИЯ', the_part1='equip', the_part2='prices', the_results=result)

#Adding a equipment
@app.route('/add_eqip_form', methods=['GET','POST'])
def add_eqip():
    dbs = db_sqlite.EquipDB()
    name_equip = request.form.get('name_equip')
    type_equip = request.form.get('type_equip')
    if name_equip and type_equip:
        dbs.add_equip(name_equip, type_equip)
    return render_template('add_equip_form.html', the_title='ДОБАВЛЕНИЕ ОБОРУДОВАНИЯ', the_part1='equip', the_part2='add')

#Removing a equipment
@app.route('/del_eqip_form', methods=['GET','POST'])
def del_eqip():
    dbs = db_sqlite.EquipDB()
    if request.form.get('ID_equip'):
        dbs.del_equip(request.form['ID_equip'])
    result = dbs.get_eqips()
    return render_template('del_equip_form.html', the_title='УДАЛЕНИЕ ОБОРУДОВАНИЯ', the_results=result, the_part1='equip', the_part2='del')

#Adding the price of the selected equipment
@app.route('/1_equip', methods=['GET','POST'])
def add_price() -> str:
    dbs = db_sqlite.EquipDB()
    filter_id = request.form.get('id_1_eq','')
    # берем первое значение возвращаемое итерируемым объектом типа cursor SQlite
    # если результат выполнения функции get_eqips сначала присвоить отдельной переменной 
    # и взять первое значение этой переменной,
    # то при выполнении следующей функции с добавлением данных в таблицу возникнет блокировка БД
    equip = next(dbs.get_eqips(filter_id, '', ''))
    if request.form.get('price') and request.form.get('date'):
        dbs.add_price(filter_id, request.form['price'], request.form['date'])
    res_prices = dbs.get_prices(filter_id)
    return render_template('1_equip.html', the_title='Одна позиция', the_part1='equip', the_part2='prices', the_res1=equip, the_res2=res_prices)    

# list_prj_form
@app.route('/')
@app.route('/list_prj_form', methods=['GET','POST'])
def list_prj() -> str:
    dbs = db_sqlite.EquipDB()
    id_prj =''
    object =''
    result = dbs.get_prj(id = id_prj, object = object)
    return render_template('list_prj_form.html', the_title='CПИСОК ПРОЕКТОВ', the_results=result, the_part1='prj', the_part2='prj')

@app.route('/add_prj_form', methods=['GET','POST'])
def add_prj() -> str:
    return render_template('list_prj_form.html', the_title='Добавление проекта', the_part1='prj', the_part2='add')

@app.route('/del_prj_form', methods=['GET','POST'])
def del_prj() -> str:
    return render_template('list_prj_form.html', the_title='Удаление проекта', the_part1='prj', the_part2='del') 

# customer form
@app.route('/admin')
@app.route('/customer_form', methods=['GET','POST'])
def customer_form():
    dbs = db_sqlite.EquipDB()
    # if press button with name='button_upd' then run update customer
    print(f"'button_upd': {request.form.get('button_upd')}, 'button_add': {request.form.get('button_add')}, 'del_cust': {request.form.get('del_cust')}")
    if request.form.get('button_upd') and request.form.get('upd_name_cust') and request.form.get('upd_prof_cust'):
        dbs.upd_customer(request.form.get('upd_id'), request.form.get('upd_name_cust'), request.form.get('upd_prof_cust'))
        #print in console attributes from the update form
        print(f"'button_upd': {request.form.get('button_upd')}, upd_id: {request.form.get('upd_id')} 'add_name_cust': {request.form.get('upd_name_cust')}, 'add_name_prof': {request.form.get('upd_prof_cust')}")
    # if press button with name='button_add' then run adding customer
    if request.form.get('button_add') and request.form.get('add_name_cust') and request.form.get('add_name_prof'):
        dbs.add_customer(request.form.get('add_name_cust'), request.form.get('add_name_prof'))
        print(f" 'add_name_cust': {request.form.get('add_name_cust')}, 'add_name_prof': {request.form.get('add_name_prof')}")
    # if press button with name='del_cust' then run removal customer
    if request.form.get('del_cust'):
        dbs.del_customer(request.form.get('del_cust'))
    # get values attributes for select customer 
    s_id = request.form.get('search_id','')
    s_name_cust = request.form.get('search_name_cust','')
    s_prof_cust = request.form.get('search_name_prof','')
    # get result select customer
    result=dbs.get_customer(s_id, s_name_cust, s_prof_cust)
    return render_template('customer_form.html', the_title='Форма заказчиков', the_part1='adm', the_part2='customer', the_results=result, the_req=str(request.form))

@app.route('/upd_customer', methods=['POST'])
def upd_customer():
    dbs = db_sqlite.EquipDB()
    if request.form.get('upd_cust'):
        result=next(dbs.get_customer(request.form.get('upd_cust'), "", ""))
        for i in result:
            print(i, end=' ')
        print()
        return render_template('upd_cust.html', the_title='Правка заказчика', the_part1='adm', the_part2='customer', the_result=result)

@app.route('/prj_stat_form')
def prj_stat_form():
    return render_template('base_adm.html', the_title='Статусы', the_part1='adm', the_part2='stat')

@app.route('/region_form')
def region_form():
    return render_template('base_adm.html', the_title='Регионы', the_part1='adm', the_part2='region')

if __name__ == '__main__':
    app.run(debug=True)