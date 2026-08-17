import customtkinter as ctk
from tkinter import ttk, messagebox

from services.backup_service import (
    create_database_backup,
    get_backup_history,
    get_available_backups,
    get_backup_statistics,
    restore_database,
)


class BackupsFrame(ctk.CTkFrame):

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
        self.selected_backup_path = None

        self.pack(
            fill="both",
            expand=True,
        )

        self.create_ui()
        self.load_data()

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
            text="Database Backup & Recovery",
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
                "Protect system data and recover "
                "from database failures."
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

        stats_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        stats_frame.pack(
            fill="x",
            padx=25,
            pady=(5, 12),
        )

        stats_frame.grid_columnconfigure(
            (0, 1, 2),
            weight=1,
        )

        self.total_value = self.create_stat_card(
            stats_frame,
            0,
            "Total Backup Operations",
        )

        self.success_value = self.create_stat_card(
            stats_frame,
            1,
            "Successful",
        )

        self.failed_value = self.create_stat_card(
            stats_frame,
            2,
            "Failed",
        )

        # ----------------------------------------
        # ACTIONS
        # ----------------------------------------

        actions = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12,
        )

        actions.pack(
            fill="x",
            padx=25,
            pady=(0, 12),
        )

        info = ctk.CTkLabel(
            actions,
            text=(
                "Automatic backup is created when "
                "the application starts."
            ),
            text_color="#475569",
            font=ctk.CTkFont(
                size=13
            ),
        )

        info.pack(
            side="left",
            padx=18,
            pady=15,
        )

        refresh_button = ctk.CTkButton(
            actions,
            text="Refresh",
            width=100,
            height=40,
            command=self.load_data,
        )

        refresh_button.pack(
            side="right",
            padx=(5, 15),
            pady=10,
        )

        backup_button = ctk.CTkButton(
            actions,
            text="Create Manual Backup",
            width=170,
            height=40,
            command=self.create_manual_backup,
        )

        backup_button.pack(
            side="right",
            padx=5,
            pady=10,
        )

        # ----------------------------------------
        # BACKUP FILE TABLE
        # ----------------------------------------

        file_card = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12,
        )

        file_card.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 12),
        )

        file_title = ctk.CTkLabel(
            file_card,
            text="Available Backups",
            font=ctk.CTkFont(
                size=18,
                weight="bold",
            ),
            text_color="#111827",
        )

        file_title.pack(
            anchor="w",
            padx=18,
            pady=(15, 8),
        )

        file_container = ctk.CTkFrame(
            file_card,
            fg_color="transparent",
        )

        file_container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15),
        )

        columns = (
            "name",
            "type",
            "size",
            "modified",
        )

        self.backup_table = ttk.Treeview(
            file_container,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        self.backup_table.heading(
            "name",
            text="Backup File",
        )

        self.backup_table.heading(
            "type",
            text="Type",
        )

        self.backup_table.heading(
            "size",
            text="Size",
        )

        self.backup_table.heading(
            "modified",
            text="Created / Modified",
        )

        self.backup_table.column(
            "name",
            width=400,
        )

        self.backup_table.column(
            "type",
            width=110,
            anchor="center",
        )

        self.backup_table.column(
            "size",
            width=100,
            anchor="center",
        )

        self.backup_table.column(
            "modified",
            width=180,
            anchor="center",
        )

        vertical_scroll = ttk.Scrollbar(
            file_container,
            orient="vertical",
            command=self.backup_table.yview,
        )

        self.backup_table.configure(
            yscrollcommand=vertical_scroll.set,
        )

        self.backup_table.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        vertical_scroll.grid(
            row=0,
            column=1,
            sticky="ns",
        )

        file_container.grid_rowconfigure(
            0,
            weight=1,
        )

        file_container.grid_columnconfigure(
            0,
            weight=1,
        )

        self.backup_table.bind(
            "<<TreeviewSelect>>",
            self.backup_selected,
        )

        # ----------------------------------------
        # RESTORE AREA
        # ----------------------------------------

        restore_frame = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=12,
        )

        restore_frame.pack(
            fill="x",
            padx=25,
            pady=(0, 20),
        )

        self.selected_label = ctk.CTkLabel(
            restore_frame,
            text="No backup selected.",
            text_color="#64748B",
            font=ctk.CTkFont(
                size=12
            ),
        )

        self.selected_label.pack(
            side="left",
            padx=18,
            pady=15,
        )

        restore_button = ctk.CTkButton(
            restore_frame,
            text="Restore Selected Backup",
            width=190,
            height=40,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.restore_selected_backup,
        )

        restore_button.pack(
            side="right",
            padx=15,
            pady=10,
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

    def load_data(self):

        self.load_backups()
        self.refresh_statistics()

    def load_backups(self):

        for item in (
            self.backup_table.get_children()
        ):

            self.backup_table.delete(
                item
            )

        backups = get_available_backups()

        for backup in backups:

            size_kb = (
                backup["size"] / 1024
            )

            if size_kb < 1024:

                size_text = (
                    f"{size_kb:.1f} KB"
                )

            else:

                size_text = (
                    f"{size_kb / 1024:.2f} MB"
                )

            self.backup_table.insert(
                "",
                "end",
                values=(
                    backup["name"],
                    backup["type"],
                    size_text,
                    backup["modified"],
                ),
            )

    def backup_selected(
        self,
        event=None,
    ):

        selected = (
            self.backup_table.selection()
        )

        if not selected:

            self.selected_backup_path = None

            self.selected_label.configure(
                text="No backup selected."
            )

            return

        values = self.backup_table.item(
            selected[0],
            "values",
        )

        backup_name = values[0]

        backups = get_available_backups()

        for backup in backups:

            if backup["name"] == backup_name:

                self.selected_backup_path = (
                    backup["path"]
                )

                self.selected_label.configure(
                    text=(
                        f"Selected: "
                        f"{backup_name}"
                    ),
                    text_color="#2563EB",
                )

                return

    def create_manual_backup(self):

        success, message = (
            create_database_backup(
                backup_type="Manual",
                current_user=self.current_user,
            )
        )

        if success:

            messagebox.showinfo(
                "Backup Created",
                message,
            )

            self.load_data()

        else:

            messagebox.showerror(
                "Backup Failed",
                message,
            )

    def restore_selected_backup(self):

        if not self.selected_backup_path:

            messagebox.showwarning(
                "No Backup Selected",
                "Please select a backup first.",
            )

            return

        confirmation = messagebox.askyesno(
            "Confirm Database Restore",
            (
                "WARNING:\n\n"
                "Restoring this backup will replace "
                "the current database.\n\n"
                "A safety backup will be created "
                "before the restore.\n\n"
                "The application must be restarted "
                "after a successful restore.\n\n"
                "Do you want to continue?"
            ),
        )

        if not confirmation:
            return

        success, message = (
            restore_database(
                self.selected_backup_path,
                self.current_user,
            )
        )

        if success:

            messagebox.showinfo(
                "Restore Successful",
                message,
            )

            self.load_data()

        else:

            messagebox.showerror(
                "Restore Failed",
                message,
            )

    def refresh_statistics(self):

        statistics = (
            get_backup_statistics()
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