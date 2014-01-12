# coding: utf8
# попробовать что-либо вида
def index():
    response.title = "Профиль пользователя"

    form = SQLFORM(db.person)
    form.vars.first_name=auth.user.first_name
    form.vars.last_name=auth.user.last_name
    

    if form.process().accepted:
        response.flash = 'form accepted'

    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'

    return dict(form=form)





@auth.requires_login()
def personal_page():
    response.title="Личный кабинет"
    message='Выберите необходимые Вам действия:'
    return locals()


@auth.requires_login()
def rooms():
    #user = response.args.user
    response.title = "Список ваших помещений"
    # form = crud.select(db.ownership)
    # grid = SQLFORM.grid(db.ownership)
    # db.room.room_num.represent = lambda value, row: DIV(value if value else '-', _class='room_num',
    #                                                     _id=str(row.id) + '.house')
    show_fields=['person','room','quota','ownership_date']
    db.ownership.room.represent=lambda id,row : row.room.room_name
    db.ownership.person.represent=lambda id,row : row.person.last_name+' '+row.person.first_name+' '+row.person.middle_name
    grid = SQLFORM.grid(db.ownership, searchable=True, csv=True, user_signature=True, maxtextlengths={'ownership.person':50, 'ownership.room':50})
    #fields=show_fields, field_id=db.ownership.id
    return locals()




def upd_dog_name():
    id, column = request.post_vars.id.split('.')
    value = request.post_vars.value
    db(db.dogs.id == id).update(**{column: value})
    return value
