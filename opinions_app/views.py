from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import OpinionForm
from .models import Opinion


def random_opinion():
    quantity = Opinion.query.count()
    if quantity:
        offset_value = randrange(quantity)
        opinion = Opinion.query.offset(offset_value).first()
        return opinion


@app.route('/')
def index_view():
    # # print(app.config)
    # # Определить количество мнений в базе данных.
    # quantity = Opinion.query.count()
    # # Если мнений нет...
    # if not quantity:
    #     # Если в базе пусто - при запросе к главной странице
    #     # пользователь увидит ошибку 500.
    #     abort(500)
    #     # # ...то вернуть сообщение:
    #     # return 'В базе данных мнений о фильмах нет.'
    # # Иначе выбрать случайное число в диапазоне от 0 до quantity...
    # offset_value = randrange(quantity)
    # # ...и определить случайный объект.
    # opinion = Opinion.query.offset(offset_value).first()
    # return render_template('opinion.html', opinion=opinion)
    opinion = random_opinion()
    # Если random_opinion() вернула None, значит, в БД нет записей.
    if opinion is None:
        abort(500)
    return render_template('opinion.html', opinion=opinion)


@app.route('/add', methods=['GET', 'POST'])
def add_opinion_view():
    # Создать новый экземпляр формы.
    form = OpinionForm()
    # Если ошибок не возникло...
    if form.validate_on_submit():

        text = form.text.data
        # Если в БД уже есть мнение с текстом, который ввёл пользователь...
        if Opinion.query.filter_by(text=text).first() is not None:
            # ...вызвать функцию flash и передать соответствующее сообщение.
            flash('Такое мнение уже было оставлено ранее!')
            # Вернуть пользователя на страницу «Добавить новое мнение».
            return render_template('add_opinion.html', form=form)

        # ...то нужно создать новый экземпляр класса Opinion...
        opinion = Opinion(
            # ...и передать в него данные, полученные из формы.
            title=form.title.data,
            text=form.text.data,
            source=form.source.data
        )
        # Затем добавить его в сессию работы с базой данных...
        db.session.add(opinion)
        # ...и зафиксировать изменения.
        db.session.commit()
        # Затем переадресовать пользователя на страницу добавленного мнения.
        return redirect(url_for('opinion_view', id=opinion.id))
    # Если валидация не пройдена - просто отрисовать страницу с формой.
    # Передать объект формы в шаблон add_opinion.html.
    return render_template('add_opinion.html', form=form)


# Тут указывается конвертер пути для id.
@app.route('/opinions/<int:id>')
# Параметром указывается имя переменной.
def opinion_view(id):
    # Теперь можно запросить нужный объект по id...
    opinion = Opinion.query.get_or_404(id)
    # ...и передать его в шаблон (шаблон - тот же, что и для главной страницы).
    return render_template('opinion.html', opinion=opinion)
