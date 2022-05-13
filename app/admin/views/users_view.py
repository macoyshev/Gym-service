from flask_admin.contrib.sqla import ModelView


class UserModal(ModelView):
    can_edit = True
    can_create = True
    can_delete = True
    can_view_details = True

    column_list = ['username']

    form_excluded_columns = ['password']
