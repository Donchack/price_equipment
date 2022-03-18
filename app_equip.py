from flask import Flask, render_template, request, escape
import db_sqlite

app = Flask(__name__)

@app.route('/')
@app.route('/eqip_prices', methods=['GET','POST'])
def eqip_prices() -> str:
    dbs = db_sqlite.EquipDB()
    s_id = request.form.get('search_id','')
    s_name_eq = request.form.get('search_name_eq','')
    s_type_eq = request.form.get('search_type_eq','')
    
    result = dbs.get_eqips(id = s_id, name_eq = s_name_eq, type_eq = s_type_eq)
    
    # result = {1: ('Трансформатор ТОЛ-10 III-2-0,5S/10Р-30/5 УХЛ1','Трансформатор'), 2: ('Трансформатор ТОЛ-10-III-2-0,5S/10P 75/5 УХЛ1','Трансформатор'), 3: ('Счетчик МИР С-03.02Т-ЕQTLBMN-RG-1T-H','Счетчик')}
    return render_template('eqip_prices.html', the_title='CПИСОК ОБОРУДОВАНИЯ', the_results=result)

@app.route('/add_eqip_form', methods=['GET'])
def add_eqip_f():
    return render_template('add_equip_form.html', the_title='ДОБАВЛЕНИЕ ОБОРУДОВАНИЯ')

@app.route('/add_eqip', methods=['POST'])
def add_eqip():
    dbs = db_sqlite.EquipDB()
    name_equip = request.form['name_equip']
    type_equip = request.form['type_equip']
    result = dbs.add_equip(name_equip, type_equip)
    return render_template('add_equip_form.html', the_title='ДОБАВЛЕНИЕ ОБОРУДОВАНИЯ')

@app.route('/del_eqip_form', methods=['GET','POST'])
def del_eqip():
    dbs = db_sqlite.EquipDB()
    if request.form.get('ID_equip'):
        dbs.del_equip(request.form['ID_equip'])
    result = dbs.get_eqips()
    return render_template('del_equip_form.html', the_title='УДАЛЕНИЕ ОБОРУДОВАНИЯ', the_results=result)

@app.route('/1_equip', methods=['GET','POST'])
def one_eqip() -> str:
    dbs = db_sqlite.EquipDB()
    filter_id = request.form.get('id_1_eq','')
    res_equip = dbs.get_eqips(filter_id, '', '')
    equip = next(res_equip)
    res_prices = dbs.get_prices(equip[0])
    return render_template('1_equip.html', the_title='Одна позиция', the_res1=equip, the_res2=res_prices)

@app.route('/add_price', methods=['POST'])
def add_price() -> str:
    dbs = db_sqlite.EquipDB()
    filter_id = request.form.get('id_1_eq','')
    # берем первое значение возвращаемое итерируемым объектом типа cursor SQlite
    # если результат выполнения функции get_eqips сначала присвоить отдельной переменной 
    # и взять первое значение этой переменной,
    # то при выполнении следующей функции с добавлением данных в таблицу возникнет блокировка БД
    equip = next(dbs.get_eqips(filter_id, '', ''))
    dbs.add_price(filter_id,request.form['price'], request.form['date'])
    res_prices = dbs.get_prices(equip[0])
    return render_template('1_equip.html', the_title='Одна позиция', the_res1=equip, the_res2=res_prices)    

if __name__ == '__main__':
    app.run(debug=True)