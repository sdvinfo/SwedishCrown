# coding: utf8

#field types:
#    string
#    text
#    blob
#    boolean
#    integer
#    double
#    decimal(n,m)
#    date
#    time
#    datetime
#    password
#    upload
#    reference <table>
#    list:string
#    list:integer
#    list:reference <table>
#    json
#    bigint
#    big-id
#    big-reference


db.define_table('house',
                Field('building', 'string', notnull=True, unique=True, label='Корпус'),
                Field('area_total', 'decimal(4,2)', label='Общая площадь дома',
                      comment='Сумма площадей ЖИЛЫХ и НЕЖИЛЫХ, без учета балконов, лестниц, подсобных и необорудованных помещений.'),
                Field('area_residental', 'decimal(4,2)', label='Площадь жилых помещений', comment='Без учета балконов'),
                Field('area_commercial', 'decimal(4,2)', label='Площадь нежилых помещений',
                      comment='Площадь коммерческих помещений, кладовок, колясочных, дворницких, ГРЩ, ИТП и пр. '),
                Field('area_balconies', 'decimal(4,2)', label='Площадь балконов',
                      comment='Площадь лоджий, балконов, веранд и терасс с коэффициентами.'),
                Field('area_stairs', 'decimal(4,2)', label='Площадь лестниц',
                      comment='Площадь лестниц, лифтов, коридоров.'),
                Field('area_unequipped', 'decimal(4,2)', label='Необорудованная площадь',
                      comment='Кто-нибудь знает что это такое?'),
                Field('flat_from', 'integer', label='Номера квартир С'),
                Field('flat_till', 'integer', label='Номера квартир ПО'),
                Field('pib_measurement_date', 'date', label='Дата ведомости обмеров ПИБ')
)

# Вид помещения
db.define_table('type_of_room',
                Field('name','string',label='Вид',comment='Вид объекта недвижимости'),
                )

# Собственник помещения
db.define_table('person',
                Field('last_name','string'),
                Field('first_name','string'),
                Field('middle_name','string'),
                Field('phone','string'),
                Field('user_id','reference auth_user'),
                )

# Квартира, кладовка, ком.помещение или что-либо еще?
db.define_table('room',
                Field('room_num', 'string', label='Номер'),
                Field('room_type', 'reference type_of_room', label='Вид', requires=IS_IN_DB(db,'type_of_room.id', '%(name)s',zero=None),default=1),
                Field('area', 'decimal(4,2)'),
                Field('house', 'reference house', label=T('House'), requires=IS_IN_DB(db, 'house.id', '%(building)s', zero='Выберите корпус дома')),
                Field('room_name', 'string', default=str('room_num'+' - '+'house.building')),
                )

# Собственность
db.define_table('ownership',
                Field('person', 'reference person', label='Собственник', requires=IS_IN_DB(db,'person.id', '%(last_name)s %(first_name)s %(middle_name)s', zero='Выберите собственника (возможно, себя?)')),
                Field('room', 'reference room', label='Объект недвижимости', requires=IS_IN_DB(db, 'room.id', '%(room_name)s', zero='Выберите объект недвижимости')),
                Field('quota', 'decimal(4,2)', label='Доля', comment='Доля этого собственника в %', default=100),
                Field('ownership_date', 'date', label='Дата', comment='Дата оформления в собственность', requires=IS_DATE(format=T('%d.%m.%Y'))),
                )

persons_and_spaces = db((db.person.id == db.ownership.person) & (db.room.id == db.ownership.room))


## ============ Для выборки из общей таблицы: =================
# for row in persons_and_things.select():
#    print row.person.name, row.thing.name
## ============================================================


# Статья сметы
db.define_table('budget_item',
                Field('name', 'string', label='Статья'),
                Field('item_type', 'integer', label='Тип', requires=IS_IN_SET({'1':'Расход','2':'Доход'}, zero=None), default=1),
                Field('tarif_live', 'decimal(6,2)',label='Тариф (жилые)', comment='Тариф за метр для жилых помещений'),
                Field('tarif_unlive', 'decimal(6,2)',label='Тариф (нежилые)', comment='Тариф за метр для нежилых помещений'),
                Field('tarif_parking', 'decimal(6,2)',label='Тариф (общие)', comment='Тариф за метр для паркинга'),
                Field('date_from','date',label='Действует с', comment='Тариф утвержден с даты'),
                Field('date_to','date',label='Действует по', comment='Тариф утвержден по дату'),
                auth.signature
                )


db.define_table('budget',
                Field('item', 'reference budget_item', label='Статья', requires=IS_IN_DB(db,'budget_item.id','%(name)s',zero='Выберите одну из статей Сметы')),
                Field('sum_plan', 'decimal(10,2)',label='Сумма (план)', comment='Запланированная сумма по статье'),
                Field('sum_fact', 'decimal(10,2)',label='Сумма (факт)', comment='Фактическая сумма по статье'),
                Field('saldo','decimal(10,2)', label='Сальдо', comment='Разница между планируемым и фактическим доходом/расходом'),
                Field('date_from','date',label='Действует с', comment='Смета утверждена с даты'),
                Field('date_to','date',label='Действует по', comment='Смета действует по дату'),
                )















## =================================================================
##
##  Вспомогательная функция для загрузки справочника квартир из
##  csv-файла.
##  Файл должен быть в формате: Номер_Квартиры ; Площадь_Квартиры
##
##  При загрузке необходимо указать ID дома в который мы загружаем квартиры
##
## =================================================================
#
# def upload_appartments(f):
#     import csv,pprint
#     infile = open(f,'r')
#     tab=[]
#     for row in csv.reader(infile,delimiter=';'):
#         tab.append(row)
#     infile.close()
#     for row in db(db.house.id==4).select():   # <--- ID корпуса дома !!!
#         house = row
#     # house = db(db.house.id==1).select()
#     for i in range(len(tab)):
#         print 'House='+house.building+' ID='+str(house.id)+' app='+str(tab[i][0])+'  square='+str(tab[i][1])
#         db.space.insert(space_num=tab[i][0], area=tab[i][1], house_id=house.id)
#     db.commit()

# upload_appartments('/Users/sdv/Development/GitHub/SwedishCrown/web2py/applications/SwedishCrown/static/tmp/12E.csv')

## =================================================================

def update_rooms():
    rooms = db(db.room).select()
    for room in rooms:
        # print room
        row = db(db.room.id==room.id).select().first()
        house = db(db.house.id==row.house).select().first()
        room_type = db(db.type_of_room.id==row.room_type).select().first()
        print 'ROOM_TYPE = '+str(room_type)
        print row
        row.room_name='Корпус: '+str(house.building)+' - '+str(room_type.name)+' №: '+str(room.room_num)
        # print row.room_name
        row.update_record()

# update_rooms()
