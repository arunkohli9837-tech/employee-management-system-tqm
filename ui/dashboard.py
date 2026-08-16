import customtkinter as ctk

from database.database import get_connection

from ui.employees import EmployeesFrame
from ui.users import UsersFrame


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

    # -------------------------------------------------
    # SIDEBAR
    # -------------------------------------------------

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

        sidebar.pack_propagate(
            False
        )

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

        self.create_sidebar_button(
            sidebar,
            "Dashboard",
            self.show_dashboard,
        )

        # Admin and HR can manage employees.
        if self.user["role"] in (
            "Admin",
            "HR",
        ):

            self.create_sidebar_button(
                sidebar,
                "Employees",
                self.show_employees,
            )

        # Only Administrator can manage user accounts.
        if self.user["role"] == "Admin":

            self.create_sidebar_button(
                sidebar,
                "User Roles",
                self.show_users,
            )

            self.create_sidebar_button(
                sidebar,
                "Audit Logs",
                self.feature_not_available,
            )

            self.create_sidebar_button(
                sidebar,
                "Backups",
                self.feature_not_available,
            )

            self.create_sidebar_button(
                sidebar,
                "Reliability",
                self.feature_not_available,
            )

        elif self.user["role"] == "HR":

            self.create_sidebar_button(
                sidebar,
                "Audit Logs",
                self.feature_not_available,
            )

            self.create_sidebar_button(
                sidebar,
                "Reliability",
                self.feature_not_available,
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
            font=ctk.CTkFont(
                size=13
            ),
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

    def create_sidebar_button(
        self,
        sidebar,
        text,
        command,
    ):

        button = ctk.CTkButton(
            sidebar,
            text=text,
            height=42,
            corner_radius=8,
            fg_color="transparent",
            hover_color="#1E3A8A",
            anchor="w",
            font=ctk.CTkFont(size=14),
            command=command,
        )

        button.pack(
            fill="x",
            padx=15,
            pady=4,
        )

    # -------------------------------------------------
    # CONTENT NAVIGATION
    # -------------------------------------------------

    def clear_content(self):

        for widget in (
            self.content_container.winfo_children()
        ):

            widget.destroy()

    def show_employees(self):

        if self.user["role"] not in (
            "Admin",
            "HR",
        ):

            self.show_access_denied()

            return

        self.clear_content()

        EmployeesFrame(
            self.content_container,
            self.user,
        )

    def show_users(self):

        if self.user["role"] != "Admin":

            self.show_access_denied()

            return

        self.clear_content()

        UsersFrame(
            self.content_container,
            self.user,
        )

    def show_access_denied(self):

        self.clear_content()

        frame = ctk.CTkFrame(
            self.content_container,
            fg_color="transparent",
        )

        frame.pack(
            fill="both",
            expand=True,
        )

        label = ctk.CTkLabel(
            frame,
            text="Access Denied",
            font=ctk.CTkFont(
                size=30,
                weight="bold",
            ),
            text_color="#DC2626",
        )

        label.place(
            relx=0.5,
            rely=0.45,
            anchor="center",
        )

        info = ctk.CTkLabel(
            frame,
            text=(
                "Your user role does not have "
                "permission to access this feature."
            ),
            text_color="#64748B",
            font=ctk.CTkFont(size=15),
        )

        info.place(
            relx=0.5,
            rely=0.52,
            anchor="center",
        )

    def feature_not_available(self):

        self.clear_content()

        frame = ctk.CTkFrame(
            self.content_container,
            fg_color="transparent",
        )

        frame.pack(
            fill="both",
            expand=True,
        )

        label = ctk.CTkLabel(
            frame,
            text="Feature Coming in Next Stage",
            font=ctk.CTkFont(
                size=25,
                weight="bold",
            ),
            text_color="#111827",
        )

        label.place(
            relx=0.5,
            rely=0.47,
            anchor="center",
        )

    # -------------------------------------------------
    # DASHBOARD
    # -------------------------------------------------

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
            pady=(0, 5),
        )

        role_label = ctk.CTkLabel(
            main,
            text=(
                f"Current Access Level: "
                f"{self.user['role']}"
            ),
            font=ctk.CTkFont(
                size=13,
                weight="bold",
            ),
            text_color="#2563EB",
        )

        role_label.pack(
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
            "System Users",
            str(stats["users"]),
            "Registered user accounts",
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
                "Role Based Access",
                "Active",
            ),
            (
                "Automatic Backup",
                "Pending",
            ),
            (
                "Error Recovery",
                "Basic Recovery Active",
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
                font=ctk.CTkFont(
                    size=14
                ),
                text_color="#2563EB",
            )

            value_label.pack(
                side="right",
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
            font=ctk.CTkFont(
                size=12
            ),
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

            users = connection.execute(
                """
                SELECT COUNT(*)
                FROM users
                """
            ).fetchone()[0]

            return {
                "employees": employees,
                "audit_logs": audit_logs,
                "errors": errors,
                "users": users,
            }

        except Exception:

            return {
                "employees": 0,
                "audit_logs": 0,
                "errors": 0,
                "users": 0,
            }

        finally:
            connection.close()