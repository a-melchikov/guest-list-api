from sqladmin import ModelView

from app.models import GuestList, Table


class GuestListAdmin(ModelView, model=GuestList):
    name = "Гость"
    name_plural = "Гости"
    icon = "fa-solid fa-users"

    column_list = [GuestList.id, GuestList.name, GuestList.is_present, GuestList.table]

    column_formatters = {
        GuestList.table: lambda m, a: f"Стол {m.table.num}" if m.table else "Без стола"
    }

    column_formatters_detail = {
        GuestList.table: lambda m, a: f"Стол {m.table.num}" if m.table else "Без стола"
    }

    column_searchable_list = [
        GuestList.id,
        GuestList.name,
        GuestList.is_present,
        GuestList.table,
    ]

    column_sortable_list = [
        GuestList.id,
        GuestList.name,
        GuestList.is_present,
        GuestList.table,
    ]

    column_details_list = [
        GuestList.id,
        GuestList.name,
        GuestList.is_present,
        GuestList.table,
    ]

    form_columns = [GuestList.name, GuestList.is_present, GuestList.table]

    column_labels = {
        GuestList.id: "ID",
        GuestList.name: "ФИО",
        GuestList.is_present: "Присутствие",
        GuestList.table: "Стол",
    }

    save_as = True

    form_widget_args = {
        "table": {
            "widget": "sqladmin.widgets.Select2Widget",
            "args": {"placeholder": "Выберите стол"},
        }
    }

    can_export = True
    column_export_list = [GuestList.id, GuestList.name, GuestList.is_present]
    export_types = ["csv", "json"]

    page_size = 25
    page_size_options = [10, 25, 50, 100]


class TableAdmin(ModelView, model=Table):
    name = "Стол"
    name_plural = "Столы"
    icon = "fa-solid fa-utensils"

    column_list = [
        Table.id,
        Table.num,
        Table.description,
        Table.max_guests,
        Table.guests_def,
        Table.guests_now,
    ]

    column_searchable_list = [Table.id, Table.num, Table.description]

    column_sortable_list = [Table.id, Table.num, Table.description, Table.max_guests]

    column_details_list = [
        Table.id,
        Table.num,
        Table.description,
        Table.max_guests,
        Table.guests_def,
        Table.guests_now,
    ]

    form_columns = [Table.num, Table.description, Table.max_guests]

    column_labels = {
        Table.id: "ID",
        Table.num: "Номер стола",
        Table.description: "Описание",
        Table.max_guests: "Макс. количество гостей",
        Table.guests_def: "Ожидаемое количество гостей",
        Table.guests_now: "Текущее количество гостей",
    }

    save_as = True

    can_export = True
    column_export_list = [Table.id, Table.num, Table.description, Table.max_guests]
    export_types = ["csv", "json"]

    page_size = 25
    page_size_options = [10, 25, 50, 100]
