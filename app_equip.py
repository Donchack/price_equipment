from flask import Flask, render_template, request, redirect
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
    return render_template('eqip_prices.html', the_title='CПИСОК ОБОРУДОВАНИЯ',
                           the_part1='equip', the_part2='prices',
                           the_results=result)


# Adding a equipment
@app.route('/add_eqip_form', methods=['GET','POST'])
def add_eqip():
    dbs = db_sqlite.EquipDB()
    name_equip = request.form.get('name_equip')
    type_equip = request.form.get('type_equip')
    if name_equip and type_equip:
        dbs.add_equip(name_equip, type_equip)
    return render_template('add_equip_form.html', the_title='ДОБАВЛЕНИЕ ОБОРУДОВАНИЯ',
                           the_part1='equip', the_part2='add')


# Removing a equipment
@app.route('/del_eqip_form', methods=['GET','POST'])
def del_eqip():
    dbs = db_sqlite.EquipDB()
    if request.form.get('ID_equip'):
        dbs.del_equip(request.form['ID_equip'])
    result = dbs.get_eqips()
    return render_template('del_equip_form.html', the_title='УДАЛЕНИЕ ОБОРУДОВАНИЯ',
                           the_results=result, the_part1='equip', the_part2='del')


# Adding the price of the selected equipment
@app.route('/1_equip', methods=['GET','POST'])
def add_price() -> str:
    dbs = db_sqlite.EquipDB()
    filter_id = request.form.get('id_1_eq','')
    # берем первое значение возвращаемое итерируемым объектом 
    # типа cursor SQlite. Если результат выполнения 
    # функции get_eqips сначала присвоить отдельной переменной 
    # и взять первое значение этой переменной,
    # то при выполнении следующей функции с добавлением данных
    # в таблицу возникнет блокировка БД
    equip = next(dbs.get_eqips(filter_id, '', ''))
    if request.form.get('price') and request.form.get('date'):
        dbs.add_price(filter_id, request.form['price'], request.form['date'])
    res_prices = dbs.get_prices(filter_id)
    return render_template('1_equip.html', the_title='Одна позиция',
                           the_part1='equip', the_part2='prices',
                           the_res1=equip, the_res2=res_prices)    


# list_prj_form
@app.route('/')
@app.route('/list_prj_form', methods=['GET','POST'])
def list_prj() -> str:
    dbs = db_sqlite.EquipDB()
    id_prj =''
    object =''
    prj_stat = ''
    result = dbs.get_prj(
                         id = id_prj, object = object, stat = prj_stat,
                         foreign_key=False)
    return render_template('list_prj_form.html', the_title='CПИСОК ПРОЕКТОВ',
                           the_results=result, the_part1='prj',
                           the_part2='prj')


# form add project
@app.route('/add_prj_form', methods=['GET','POST'])
def add_prj_form() -> str:
    dbs = db_sqlite.EquipDB()
    # get customer list (id, customer)
    cust = dbs.get_customer()
    # get region list (id, region)
    reg = dbs.get_region()
    # get project status list (id, prg_stat)
    stat = dbs.get_prj_stat()
    return render_template('add_prj_form.html', the_title='Добавление проекта',
                           the_part1='prj', the_part2='add', the_cust=cust,
                           the_reg=reg, the_stat=stat)


# add new project in database
@app.route('/add_prj', methods=['POST'])
def add_prj():
    dbs = db_sqlite.EquipDB()
    # сделать проверку с возвратом на форму ввода и 
    # выводом сообщения об добавлении или причине не добавления
    name_obj = request.form.get('name_prj','')
    id_cust = request.form.get('id_cust','')
    id_reg = request.form.get('id_reg','')
    date = request.form.get('date','')
    id_stat = request.form.get('id_stat','')
    dbs.add_prj(id_cust, name_obj, id_reg, date, id_stat)
    # return on list_prj_form 
    return redirect('/list_prj_form')


# form update prj 
@app.route('/upd_prj_form', methods=['GET','POST'])
def upd_prj_form():
    dbs = db_sqlite.EquipDB()
    if request.args.get('id'):
        result=next(dbs.get_prj(id=request.args.get('id'), object='', stat='',
                         foreign_key=True))
    # get customer list (id, customer)
    cust = dbs.get_customer()
    # get region list (id, region)
    reg = dbs.get_region()
    # get project status list (id, prg_stat)
    stat = dbs.get_prj_stat()
    return render_template('add_prj_form.html', the_title='Изменение проекта',
                            the_part1='prj', the_part2='prj',
                            the_result=result, the_cust=cust,
                            the_reg=reg, the_stat=stat)


# update prj in database
@app.route('/upd_prj', methods=['POST'])
def upd_prj():
    dbs = db_sqlite.EquipDB()
    # сделать проверку с возвратом на форму изменения с 
    # выводом сообщения об  причине отмены изменения
    id_prj = request.form.get('id_prj','')
    name_obj = request.form.get('name_prj','')
    id_cust = request.form.get('id_cust','')
    id_reg = request.form.get('id_reg','')
    date = request.form.get('date','')
    id_stat = request.form.get('id_stat','')
    dbs.upd_prj(id_prj, id_cust, name_obj, id_reg, date, id_stat)
    # return on list_prj_form 
    return redirect('/list_prj_form')

    
@app.route('/del_prj_form', methods=['GET','POST'])
def del_prj() -> str:
    return render_template('list_prj_form.html', the_title='Удаление проекта',
                           the_part1='prj', the_part2='del') 


# customer form
@app.route('/admin')
@app.route('/customer_form', methods=['GET','POST'])
def customer_form():
    # get values attributes for select customer 
    s_id = request.form.get('search_id','')
    s_name_cust = request.form.get('search_name_cust','')
    s_prof_cust = request.form.get('search_name_prof','')
    dbs = db_sqlite.EquipDB()
    # get result select customer
    result=dbs.get_customer(s_id, s_name_cust, s_prof_cust)
    return render_template('customer_form.html', the_title='Форма заказчиков',
                           the_part1='adm', the_part2='customer',
                           the_results=result)


# add customer 
@app.route('/add_cust', methods=['POST'])
def add_cust():
    dbs = db_sqlite.EquipDB()
    # if press button with name='button_add' then run adding customer
    if (request.form.get('button_add') 
                and request.form.get('add_name_cust')
                and request.form.get('add_name_prof')):
        dbs.add_customer(request.form.get('add_name_cust'),
                         request.form.get('add_name_prof'))
    return redirect('/customer_form')


# del customer 
@app.route('/del_cust', methods=['POST'])
def del_cust():
    dbs=db_sqlite.EquipDB()
    # if press button with name='del_cust' then run removal customer
    if request.form.get('del_cust'):
        dbs.del_customer(request.form.get('del_cust'))
    return redirect('/customer_form')


# update customer form
@app.route('/upd_cust_form', methods=['POST'])
def upd_cust_form():
    dbs = db_sqlite.EquipDB()
    if request.form.get('upd_cust'):
        result=next(dbs.get_customer(request.form.get('upd_cust'), "", ""))
        return render_template('upd_cust.html', the_title='Правка заказчика',
                               the_part1='adm', the_part2='customer',
                               the_result=result)


# update customer
@app.route('/upd_cust', methods=['POST'])
def upd_cust():
    dbs = db_sqlite.EquipDB()
    # if press button with name='button_upd' then run update customer
    if (request.form.get('button_upd') 
                and request.form.get('upd_name_cust')
                and request.form.get('upd_prof_cust')):
        dbs.upd_customer(request.form.get('upd_id'),
                         request.form.get('upd_name_cust'), 
                         request.form.get('upd_prof_cust'))
    return redirect('/customer_form')


# prj_stat form
@app.route('/prj_stat_form', methods=['GET','POST'])
def prj_stat_form():
    # get values attributes for select prj_stat 
    s_id = request.form.get('search_id','')
    s_name_prj_stat = request.form.get('search_prj_stat','')
    dbs = db_sqlite.EquipDB()
    # get result select prj_stat
    result=dbs.get_prj_stat(s_id, s_name_prj_stat)
    return render_template('prj_stat_form.html', the_title='Статусы',
                           the_part1='adm', the_part2='stat',
                           the_results=result)


# add prj_stat
@app.route('/add_prj_stat', methods=['POST'])
def add_prj_stat():
    dbs = db_sqlite.EquipDB()
    # if press button with name='button_add' then run adding prj_stat
    if request.form.get('button_add') and request.form.get('add_name_prj_stat'):
        dbs.add_prj_stat(request.form.get('add_name_prj_stat'))
    return redirect('/prj_stat_form')


# del prj_stat
@app.route('/del_prj_stat', methods=['POST'])
def del_prj_stat():
    dbs=db_sqlite.EquipDB()
    # if press button with name='del_cust' then run removal prj_stat
    if request.form.get('del_prj_stat'):
        dbs.del_prj_stat(request.form.get('del_prj_stat'))
    return redirect('/prj_stat_form')


# update prj_stat form
@app.route('/upd_prj_stat_form', methods=['POST'])
def upd_prj_stat_form():
    dbs = db_sqlite.EquipDB()
    if request.form.get('upd_prj_stat'):
        result=next(dbs.get_prj_stat(request.form.get('upd_prj_stat', '')))
        return render_template('upd_prj_stat.html', the_title='Правка статуса',
                               the_part1='adm', the_part2='stat',
                               the_result=result)


# update prj_stat
@app.route('/upd_prj_stat', methods=['POST'])
def upd_prj_stat():
    dbs = db_sqlite.EquipDB()
    # if press button with name='button_upd' then run update prj_stat
    if request.form.get('button_upd') and request.form.get('upd_name_prj_stat'):
        dbs.upd_prj_stat(request.form.get('upd_id'),
                         request.form.get('upd_name_prj_stat'))
    return redirect('/prj_stat_form')


# region form
@app.route('/region_form', methods=['GET','POST'])
def region_form():
    # get values attributes for select region 
    s_id = request.form.get('search_id','')
    s_region = request.form.get('search_region','')
    dbs = db_sqlite.EquipDB()
    # get result select region
    result=dbs.get_region(s_id, s_region)
    return render_template('region_form.html', the_title='Регионы',
                           the_part1='adm', the_part2='region',
                           the_results=result)


# add region
@app.route('/add_region', methods=['POST'])
def add_region():
    dbs = db_sqlite.EquipDB()
    # if press button with name='button_add' then run adding region
    if (request.form.get('button_add')
                and request.form.get('add_region_id')
                and request.form.get('add_region_name')):
        dbs.add_region(request.form.get('add_region_id'),
                       request.form.get('add_region_name'))
    return redirect('/region_form')


# del region
@app.route('/del_region', methods=['POST'])
def del_region():
    dbs=db_sqlite.EquipDB()
    # if press button with name='del_region' then run removal region
    if request.form.get('del_region'):
        dbs.del_region(request.form.get('del_region'))
    return redirect('/region_form')


# update region form
@app.route('/upd_region_form', methods=['POST'])
def upd_region_form():
    dbs = db_sqlite.EquipDB()
    if request.form.get('upd_region'):
        result=next(dbs.get_region(request.form.get('upd_region')))
        return render_template('upd_region.html', the_title='Правка статуса',
                               the_part1='adm', the_part2='region',
                               the_result=result)


# update region
@app.route('/upd_region', methods=['POST'])
def upd_region():
    dbs = db_sqlite.EquipDB()
    # if press button with name='button_upd' then run update region
    if request.form.get('button_upd') and request.form.get('upd_region'):
        dbs.upd_region(request.form.get('upd_id'),
                       request.form.get('upd_region'))
    return redirect('/region_form')


if __name__ == '__main__':
    app.run(debug=True)