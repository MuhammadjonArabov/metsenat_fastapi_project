from sqladmin import Admin, ModelView
from app.models import student_sponsor


class StudentAdmin(ModelView, model=student_sponsor.Student):
    column_list = ['id', 'full_name', 'contract_amount']
    column_searchable_list = ['full_name', 'phone', 'contract_amount']


class SponsorAdmin(ModelView, model=student_sponsor.Sponsor):
    column_list = ['id', 'fill_name', 'phone', 'amount', 'organization']
    column_searchable_list = ['fill_name', 'phone', 'amount', 'organization']