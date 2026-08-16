import customtkinter as ctk

from database.database import get_connection
from ui.employees import EmployeesFrame


class DashboardFrame(ctk.CTkFrame):

    def __init__(
        self,
        master,
        user,
        logout_callback,
    ):

        super().__init__(
            master,
            fg_color="#F4F6F8",
        )

        self.user = user
        self.logout_callback = logout_callback

        self.pack(
            fill="both",
            expand=True,
        )

        self.create_sidebar()

        self.content_container = ctk.CTkFrame(
            self,
            fg_color="#F4F6F8",
            corner_radius=0,
        )

        self.content_container.pack(
            side="left",
            fill="both",
            expand=True,
        )

        self.show_dashboard()

    def create_sidebar(self):

        sidebar = ctk.CTkFrame(
            self,
            width=230,
            corner_radius=0,
            fg_color="#172554",
        )

        sidebar.pack(
            side="left",
            fill="y",
        )

        sidebar.pack_propagate(False)

        title = ctk.CTkLabel(
            sidebar,
            text=(
                "Employee\n"
                "Management System"
            ),
            font=ctk.CTkFont(
                size=22,
                weight="bold",
            ),
            text_color="white",
        )

        title.pack(
            pady=(35, 35),
            padx=20,
        )

        dashboard_button = ctk.CTkButton(
            sidebar,
            text="Dashboard",
            height=42,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#1E3A8A",
            anchor="w",
            font=ctk.CTkFont(size=14),
            command=self.show_dashboard,
        )

        dashboard_button.pack(
            fill="x",
            padx=15,
            pady=4,
        )

        employees_button = ctk.CTkButton(
            sidebar,
            text="Employees",
            height=42,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#1E3A8A",
            anchor="w",
            font=ctk.CTkFont(size=14),
            command=self.show_employees,
        )

        employees_button.pack(
            fill="x",
            padx=15,
            pady=4,
        )

        future_buttons = [
            "User Roles",
            "Audit Logs",
            "Backups",
            "Reliability",
        ]

        for button_name in future_buttons:

            button = ctk.CTkButton(
                sidebar,
                text=button_name,
                height=42,
                corner_radius=8,
                fg_color="transparent",
                hover_color="#1E3A8A",
                anchor="w",
                font=ctk.CTkFont(size=14),
            )

            button.pack(
                fill="x",
                padx=15,
                pady=4,
            )

        spacer = ctk.CTkLabel(
            sidebar,
            text="",
        )

        spacer.pack(
            expand=True,
        )

        user_label = ctk.CTkLabel(
            sidebar,
            text=(
                f"{self.user['full_name']}\n"
                f"{self.user['role']}"
            ),
            text_color="#CBD5E1",
            font=ctk.CTkFont(size=13),
        )

        user_label.pack(
            padx=20,
            pady=(10, 15),
        )

        logout_button = ctk.CTkButton(
            sidebar,
            text="Logout",
            height=40,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.logout_callback,
        )

        logout_button.pack(
            fill="x",
            padx=20,
            pady=(0, 25),
        )

    def clear_content(self):

        for widget in self.content_container.winfo_children():
            widget.destroy()

    def show_dashboard(self):

        self.clear_content()

        main = ctk.CTkScrollableFrame(
            self.content_container,
            fg_color="#F4F6F8",
        )

        main.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20,
        )

        welcome = ctk.CTkLabel(
            main,
            text=(
                f"Welcome, "
                f"{self.user['full_name']}"
            ),
            font=ctk.CTkFont(
                size=27,
                weight="bold",
            ),
            text_color="#111827",
        )

        welcome.pack(
            anchor="w",
            pady=(5, 5),
        )

        subtitle = ctk.CTkLabel(
            main,
            text=(
                "Employee Management System • "
                "Q01 Improve Reliability"
            ),
            font=ctk.CTkFont(size=15),
            text_color="#6B7280",
        )

        subtitle.pack(
            anchor="w",
            pady=(0, 25),
        )

        stats = self.get_dashboard_stats()

        cards_frame = ctk.CTkFrame(
            main,
            fg_color="transparent",
        )

        cards_frame.pack(
            fill="x",
            pady=(0, 25),
        )

        cards_frame.grid_columnconfigure(
            (0, 1, 2),
            weight=1,
        )

        self.create_card(
            cards_frame,
            0,
            0,
            "Employees",
            str(stats["employees"]),
            "Total employee records",
        )

        self.create_card(
            cards_frame,
            0,
            1,
            "Audit Events",
            str(stats["audit_logs"]),
            "Recorded system activities",
        )

        self.create_card(
            cards_frame,
            0,
            2,
            "Recorded Errors",
            str(stats["errors"]),
            "Errors captured by system",
        )

        reliability_title = ctk.CTkLabel(
            main,
            text="Reliability Overview",
            font=ctk.CTkFont(
                size=21,
                weight="bold",
            ),
            text_color="#111827",
        )

        reliability_title.pack(
            anchor="w",
            pady=(5, 15),
        )

        reliability_frame = ctk.CTkFrame(
            main,
            fg_color="white",
            corner_radius=12,
        )

        reliability_frame.pack(
            fill="x",
            pady=(0, 20),
        )

        reliability_items = [
            (
                "Database Status",
                "Healthy",
            ),
            (
                "Input Validation",
                "Active",
            ),
            (
                "Audit Logging",
                "Active",
            ),
            (
                "Automatic Backup",
                "Next Stage",
            ),
            (
                "Error Recovery",
                "In Development",
            ),
            (
                "Role Based Access",
                "Basic Role System Active",
            ),
        ]

        for name, value in reliability_items:

            row = ctk.CTkFrame(
                reliability_frame,
                fg_color="transparent",
            )

            row.pack(
                fill="x",
                padx=22,
                pady=10,
            )

            name_label = ctk.CTkLabel(
                row,
                text=name,
                font=ctk.CTkFont(
                    size=14,
                    weight="bold",
                ),
                text_color="#374151",
            )

            name_label.pack(
                side="left",
            )

            value_label = ctk.CTkLabel(
                row,
                text=value,
                font=ctk.CTkFont(size=14),
                text_color="#2563EB",
            )

            value_label.pack(
                side="right",
            )

    def show_employees(self):

        self.clear_content()

        EmployeesFrame(
            self.content_container,
            self.user,
        )

    def create_card(
        self,
        parent,
        row,
        column,
        title,
        value,
        description,
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=12,
            height=140,
        )

        card.grid(
            row=row,
            column=column,
            padx=8,
            pady=8,
            sticky="nsew",
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                size=30,
                weight="bold",
            ),
            text_color="#1D4ED8",
        )

        value_label.pack(
            anchor="w",
            padx=20,
            pady=(18, 2),
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=15,
                weight="bold",
            ),
            text_color="#111827",
        )

        title_label.pack(
            anchor="w",
            padx=20,
        )

        description_label = ctk.CTkLabel(
            card,
            text=description,
            font=ctk.CTkFont(size=12),
            text_color="#6B7280",
        )

        description_label.pack(
            anchor="w",
            padx=20,
            pady=(2, 15),
        )

    def get_dashboard_stats(self):

        connection = get_connection()

        try:

            employees = connection.execute(
                """
                SELECT COUNT(*)
                FROM employees
                """
            ).fetchone()[0]

            audit_logs = connection.execute(
                """
                SELECT COUNT(*)
                FROM audit_logs
                """
            ).fetchone()[0]

            errors = connection.execute(
                """
                SELECT COUNT(*)
                FROM error_logs
                """
            ).fetchone()[0]

            return {
                "employees": employees,
                "audit_logs": audit_logs,
                "errors": errors,
            }

        except Exception:

            return {
                "employees": 0,
                "audit_logs": 0,
                "errors": 0,
            }

        finally:
            connection.close()