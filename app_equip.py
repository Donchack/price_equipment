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
    
    result = dbs.get_eqips(s_id, s_name_eq, s_type_eq)
    # result = {1: ('Трансформатор ТОЛ-10 III-2-0,5S/10Р-30/5 УХЛ1','Трансформатор'), 2: ('Трансформатор ТОЛ-10-III-2-0,5S/10P 75/5 УХЛ1','Трансформатор'), 3: ('Счетчик МИР С-03.02Т-ЕQTLBMN-RG-1T-H','Счетчик')}
    return render_template('eqip_prices.html', the_title='CПИСОК ОБОРУДОВАНИЯ', the_results=result)

@app.route('/add_eqip_form', methods=['GET'])
def add_eqip_f():
    return render_template('add_equip_form.html')

@app.route('/add_eqip', methods=['POST'])
def add_eqip():
    dbs = db_sqlite.EquipDB()
    name_equip = request.form['name_equip']
    type_equip = request.form['type_equip']
    result = dbs.add_equip(name_equip, type_equip)
    return render_template('add_equip_form.html')

@app.route('/del_eqip_form', methods=['GET','POST'])
def del_eqip():
    dbs = db_sqlite.EquipDB()
    if request.form.get('ID_equip'):
        dbs.del_equip(request.form['ID_equip'])
        
    result = dbs.get_eqips()
    return render_template('del_equip_form.html', the_title='УДАЛЕНИЕ ОБОРУДОВАНИЯ', the_results=result)

if __name__ == '__main__':
    app.run(debug=True)