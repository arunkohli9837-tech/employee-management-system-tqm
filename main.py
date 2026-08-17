import customtkinter as ctk
from tkinter import messagebox

from database.database import (
    initialize_database,
    record_error,
)

from services.auth_service import create_default_admin

from ui.login import LoginFrame
from ui.dashboard import DashboardFrame
from services.backup_service import create_automatic_backup


class EmployeeManagementApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title(
            "Employee Management System - Q01 Improve Reliability"
        )

        self.geometry("1200x720")
        self.minsize(1000, 650)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.current_frame = None
        self.current_user = None

        self.initialize_system()
        self.show_login()

    def initialize_system(self):

        try:
            initialize_database()
            create_default_admin()
            create_automatic_backup()

        except Exception as error:

            try:
                record_error(
                    type(error).__name__,
                    str(error),
                    "main.initialize_system",
                )

            except Exception:
                pass

            messagebox.showerror(
                "System Error",
                (
                    "The application could not initialize "
                    "the database.\n\n"
                    f"Error: {error}"
                ),
            )

            self.destroy()

    def clear_current_frame(self):

        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = None

    def show_login(self):

        self.clear_current_frame()

        self.current_user = None

        self.current_frame = LoginFrame(
            self,
            self.login_successful,
        )

    def login_successful(self, user):

        self.current_user = user

        self.clear_current_frame()

        self.current_frame = DashboardFrame(
            self,
            user,
            self.logout,
        )

    def logout(self):

        self.current_user = None
        self.show_login()


if __name__ == "__main__":

    app = EmployeeManagementApp()

    if app.winfo_exists():
        app.mainloop()