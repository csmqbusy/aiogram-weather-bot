from aiogram.filters.callback_data import CallbackData


class AdminsActionsCb(CallbackData, prefix="admins_actions"):
    action: str


class ReportsActionsCb(CallbackData, prefix="reports_actions"):
    action: str


class ReportViewCb(CallbackData, prefix="report_view"):
    action: str
    report_id: int
