from sqladmin import ModelView
from app.models.guest_lists import GuestList
from app.models.tables import Table


class GuestListAdmin(ModelView, model=GuestList):
    name = "Гость"
    name_plural = "Гости"
    icon = "fa-solid fa-users"

    # Перечень колонок для отображения на странице списка
    column_list = [GuestList.id, GuestList.name, GuestList.is_present, GuestList.table]

    # Форматирование для отображения "Стол {num}"
    column_formatters = {
        GuestList.table: lambda m, a: f"Стол {m.table.num}" if m.table else "Без стола"
    }

    # Форматирование для отображения "Стол {num}" на странице деталей
    column_formatters_detail = {
        GuestList.table: lambda m, a: f"Стол {m.table.num}" if m.table else "Без стола"
    }

    # Поля, которые можно искать
    column_searchable_list = [GuestList.id, GuestList.name, GuestList.is_present]

    # Поля, которые можно сортировать
    column_sortable_list = [GuestList.id, GuestList.name, GuestList.is_present]

    # Отображение всех полей в деталях
    column_details_list = [
        GuestList.id,
        GuestList.name,
        GuestList.is_present,
        GuestList.table,
    ]

    # Используем для создания и редактирования формы все поля
    form_columns = [GuestList.name, GuestList.is_present, GuestList.table]

    # Локализация на русском языке (метки для столбцов)
    column_labels = {
        GuestList.id: "ID",
        GuestList.name: "Имя гостя",
        GuestList.is_present: "Присутствует",
        GuestList.table: "Стол",
    }

    # Дополнительные настройки
    save_as = True

    # Для выбора стола в форме можно использовать поле для выбора с отображением списка столов
    form_widget_args = {
        "table": {
            "widget": "sqladmin.widgets.Select2Widget",
            "args": {"placeholder": "Выберите стол"},
        }
    }

    # Опции экспорта (CSV, JSON)
    can_export = True
    column_export_list = [GuestList.id, GuestList.name, GuestList.is_present]
    export_types = ["csv", "json"]

    # Пагинация
    page_size = 25
    page_size_options = [10, 25, 50, 100]

    # Делаем поле "is_present" редактируемым прямо на главной странице
    column_editable_list = [GuestList.is_present]


class TableAdmin(ModelView, model=Table):
    name = "Стол"
    name_plural = "Столы"
    icon = "fa-solid fa-utensils"

    # Перечень колонок для отображения на странице списка
    column_list = [
        Table.id,
        Table.num,
        Table.description,
        Table.max_guests,
        Table.guests_def,
        Table.guests_now,
    ]

    # Поля, которые можно искать
    column_searchable_list = [Table.id, Table.num, Table.description]

    # Поля, которые можно сортировать
    column_sortable_list = [Table.id, Table.num, Table.max_guests]

    # Отображение всех полей в деталях
    column_details_list = [
        Table.id,
        Table.num,
        Table.description,
        Table.max_guests,
        Table.guests_def,
        Table.guests_now,
    ]

    # Используем для создания и редактирования формы все поля
    form_columns = [Table.num, Table.description, Table.max_guests]

    # Локализация на русском языке (метки для столбцов)
    column_labels = {
        Table.id: "ID",
        Table.num: "Номер стола",
        Table.description: "Описание",
        Table.max_guests: "Макс. количество гостей",
        Table.guests_def: "Ожидаемое количество гостей",
        Table.guests_now: "Текущее количество гостей",
    }

    # Дополнительные настройки
    save_as = True

    # Опции экспорта (CSV, JSON)
    can_export = True
    column_export_list = [Table.id, Table.num, Table.description, Table.max_guests]
    export_types = ["csv", "json"]

    # Пагинация
    page_size = 25
    page_size_options = [10, 25, 50, 100]
