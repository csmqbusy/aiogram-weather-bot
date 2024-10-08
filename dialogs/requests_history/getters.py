import math

from aiogram.types import User
from aiogram_dialog import DialogManager

from database.orm import db_client


async def get_reports_data(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    reports_orm = db_client.get_user_reports(event_from_user.id)
    reports = prepare_reports_for_dialog(reports_orm)
    n_items_per_page = 5
    n_of_reports = len(reports)
    current_page = dialog_manager.start_data.get("history_page")
    n_of_pages = math.ceil(n_of_reports / n_items_per_page)
    slice_ = slice(current_page * n_items_per_page,
                   current_page * n_items_per_page + n_items_per_page)
    dialog_manager.start_data.update(n_of_history_pages=n_of_pages)
    return {
        "reports": reports[slice_],
        "count": n_of_reports,
        "page": current_page + 1,
        "n_of_pages": n_of_pages
    }


def prepare_reports_for_dialog(reports_orm: list):
    reports = []
    for report in reports_orm:
        report_info = (report.id, report.city, report.date.day, report.date.month, report.date.year)
        reports.append(report_info)
    return reports


async def get_report_data(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    report_id = dialog_manager.dialog_data.get("report_id")
    report = db_client.get_report(report_id)
    data = {"city": report.city,
            "temp": report.temp,
            "feels_like": report.feels_like,
            "wind_speed": report.wind_speed,
            "pressure": report.pressure_mm}
    return data
