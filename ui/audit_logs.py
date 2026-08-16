import customtkinter as ctk
from tkinter import ttk

from services.audit_service import (
    get_audit_logs,
    get_audit_statistics,
)


class AuditLogsFrame(ctk.CTkFrame):

    def __init__(
        self,
        master,
        current_user,
    ):

        super().__init__(
            master,
            fg_color="#F4F6F8",
        )

        self.current_user = current_user

        self.pack(
            fill="both",
            expand=True,
        )

        self.create_ui()
        self.load_audit_logs()

    def create_ui(self):

        # ----------------------------------------
        # HEADER
        # ----------------------------------------

        header = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        header.pack(
            fill="x",
            padx=25,
            pady=(20, 10),
        )

        title = ctk.CTkLabel(
            header,
            text="Audit Logs",
            font=ctk.CTkFont(
                size=26,
                weight="bold",
            ),
            text_color="#111827",
        )

        title.pack(
            side="left",
        )

        subtitle = ctk.CTkLabel(
            header,
            text=(
                "Trace system activities, "
                "successful operations and failures."
            ),
            font=ctk.CTkFont(
                size=13
            ),
            text_color="#64748B",
        )

        subtitle.pack(
            side="left",
            padx=(18, 0),
        )

        # ----------------------------------------
        # STATISTICS
        # ----------------------------------------

        self.statistics_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        self.statistics_frame.pack(
            fill="x",
            padx=25,
            pady=(5, 12),
        )

        self.statistics_frame.grid_columnconfigure(
            (0, 1, 2, 3),
            weight=1,
        )

        self.total_value = self.create_stat_card(
            self.statistics_frame,
            0,
            "Total Events",
        )

        self.success_value = self.create_stat_card(
            self.statistics_frame,
            1,
            "Successful",
        )

        self.failed_value = self.create_stat_card(
            self.statistics_frame,
            2,
            "Failed",
        )

        self.login_value = self.create_stat_card(
            self.statistics_frame,
            3,
            "Login Events",
        )

        # ----------------------------------------
        # FILTERS
        # ----------------------------------------

        controls = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12,
        )

        controls.pack(
            fill="x",
            padx=25,
            pady=(0, 12),
        )

        self.search_entry = ctk.CTkEntry(
            controls,
            height=40,
            placeholder_text=(
                "Search username, action, "
                "target or description"
            ),
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(15, 10),
            pady=15,
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.load_audit_logs(),
        )

        self.status_filter = ctk.CTkOptionMenu(
            controls,
            values=[
                "All",
                "Success",
                "Failed",
            ],
            width=130,
            height=40,
            command=lambda value:
                self.load_audit_logs(),
        )

        self.status_filter.set(
            "All"
        )

        self.status_filter.pack(
            side="left",
            padx=5,
            pady=15,
        )

        refresh_button = ctk.CTkButton(
            controls,
            text="Refresh",
            width=100,
            height=40,
            command=self.load_audit_logs,
        )

        refresh_button.pack(
            side="left",
            padx=(5, 15),
            pady=15,
        )

        # ----------------------------------------
        # TABLE
        # ----------------------------------------

        table_card = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12,
        )

        table_card.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20),
        )

        table_container = ctk.CTkFrame(
            table_card,
            fg_color="transparent",
        )

        table_container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15,
        )

        columns = (
            "id",
            "username",
            "action",
            "target",
            "description",
            "status",
            "created",
        )

        self.audit_table = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
        )

        self.audit_table.heading(
            "id",
            text="ID",
        )

        self.audit_table.heading(
            "username",
            text="Username",
        )

        self.audit_table.heading(
            "action",
            text="Action",
        )

        self.audit_table.heading(
            "target",
            text="Target",
        )

        self.audit_table.heading(
            "description",
            text="Description",
        )

        self.audit_table.heading(
            "status",
            text="Status",
        )

        self.audit_table.heading(
            "created",
            text="Date / Time",
        )

        self.audit_table.column(
            "id",
            width=50,
            anchor="center",
        )

        self.audit_table.column(
            "username",
            width=110,
        )

        self.audit_table.column(
            "action",
            width=150,
        )

        self.audit_table.column(
            "target",
            width=120,
        )

        self.audit_table.column(
            "description",
            width=350,
        )

        self.audit_table.column(
            "status",
            width=90,
            anchor="center",
        )

        self.audit_table.column(
            "created",
            width=155,
        )

        vertical_scroll = ttk.Scrollbar(
            table_container,
            orient="vertical",
            command=self.audit_table.yview,
        )

        horizontal_scroll = ttk.Scrollbar(
            table_container,
            orient="horizontal",
            command=self.audit_table.xview,
        )

        self.audit_table.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set,
        )

        self.audit_table.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        vertical_scroll.grid(
            row=0,
            column=1,
            sticky="ns",
        )

        horizontal_scroll.grid(
            row=1,
            column=0,
            sticky="ew",
        )

        table_container.grid_rowconfigure(
            0,
            weight=1,
        )

        table_container.grid_columnconfigure(
            0,
            weight=1,
        )

    def create_stat_card(
        self,
        parent,
        column,
        title,
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=12,
        )

        card.grid(
            row=0,
            column=column,
            padx=6,
            sticky="nsew",
        )

        value_label = ctk.CTkLabel(
            card,
            text="0",
            font=ctk.CTkFont(
                size=27,
                weight="bold",
            ),
            text_color="#1D4ED8",
        )

        value_label.pack(
            pady=(15, 0),
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=12,
                weight="bold",
            ),
            text_color="#64748B",
        )

        title_label.pack(
            pady=(0, 15),
        )

        return value_label

    def load_audit_logs(self):

        search_text = (
            self.search_entry.get()
            if hasattr(
                self,
                "search_entry",
            )
            else ""
        )

        status_filter = (
            self.status_filter.get()
            if hasattr(
                self,
                "status_filter",
            )
            else "All"
        )

        logs = get_audit_logs(
            search_text,
            status_filter,
        )

        for item in (
            self.audit_table.get_children()
        ):

            self.audit_table.delete(
                item
            )

        for log in logs:

            target_type = (
                log["target_type"]
                or "-"
            )

            target_id = (
                log["target_id"]
                or "-"
            )

            if (
                target_type != "-"
                or target_id != "-"
            ):

                target = (
                    f"{target_type} "
                    f"#{target_id}"
                )

            else:

                target = "-"

            self.audit_table.insert(
                "",
                "end",
                values=(
                    log["id"],
                    log["username"] or "System",
                    log["action"],
                    target,
                    log["description"] or "-",
                    log["status"],
                    log["created_at"],
                ),
            )

        self.refresh_statistics()

    def refresh_statistics(self):

        statistics = (
            get_audit_statistics()
        )

        self.total_value.configure(
            text=str(
                statistics["total"]
            )
        )

        self.success_value.configure(
            text=str(
                statistics["successful"]
            )
        )

        self.failed_value.configure(
            text=str(
                statistics["failed"]
            )
        )

        self.login_value.configure(
            text=str(
                statistics["login_events"]
            )
        )