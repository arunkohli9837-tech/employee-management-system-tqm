import customtkinter as ctk
from tkinter import ttk, messagebox

from services.user_service import (
    create_user,
    get_all_users,
    get_user_by_id,
    update_user,
    toggle_user_status,
)


class UsersFrame(ctk.CTkFrame):

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
        self.selected_user_id = None

        self.pack(
            fill="both",
            expand=True,
        )

        self.create_ui()
        self.load_users()

    def create_ui(self):

        # ----------------------------------------
        # PAGE HEADER
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
            text="User Roles & Access Control",
            font=ctk.CTkFont(
                size=26,
                weight="bold",
            ),
            text_color="#111827",
        )

        title.pack(
            side="left",
        )

        # ----------------------------------------
        # MAIN AREA
        # ----------------------------------------

        main = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        main.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(5, 20),
        )

        # ----------------------------------------
        # USER FORM
        # ----------------------------------------

        form_frame = ctk.CTkScrollableFrame(
            main,
            width=340,
            fg_color="white",
            corner_radius=12,
        )

        form_frame.pack(
            side="left",
            fill="y",
            padx=(0, 15),
        )

        form_title = ctk.CTkLabel(
            form_frame,
            text="User Account",
            font=ctk.CTkFont(
                size=19,
                weight="bold",
            ),
            text_color="#111827",
        )

        form_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 15),
        )

        self.username_entry = self.create_entry(
            form_frame,
            "Username",
        )

        self.full_name_entry = self.create_entry(
            form_frame,
            "Full Name",
        )

        self.password_entry = ctk.CTkEntry(
            form_frame,
            width=300,
            height=40,
            placeholder_text="Password",
            show="*",
        )

        self.password_entry.pack(
            padx=20,
            pady=7,
        )

        password_info = ctk.CTkLabel(
            form_frame,
            text=(
                "For updates, leave password blank\n"
                "to keep the existing password."
            ),
            text_color="#64748B",
            font=ctk.CTkFont(size=11),
        )

        password_info.pack(
            padx=20,
            pady=(0, 8),
        )

        role_label = ctk.CTkLabel(
            form_frame,
            text="User Role",
            font=ctk.CTkFont(
                size=13,
                weight="bold",
            ),
            text_color="#374151",
        )

        role_label.pack(
            anchor="w",
            padx=20,
            pady=(8, 4),
        )

        self.role_menu = ctk.CTkOptionMenu(
            form_frame,
            width=300,
            height=40,
            values=[
                "Admin",
                "HR",
                "Employee",
            ],
        )

        self.role_menu.set("Employee")

        self.role_menu.pack(
            padx=20,
            pady=(0, 10),
        )

        self.message_label = ctk.CTkLabel(
            form_frame,
            text="",
            wraplength=290,
            font=ctk.CTkFont(size=12),
        )

        self.message_label.pack(
            padx=20,
            pady=8,
        )

        self.save_button = ctk.CTkButton(
            form_frame,
            text="Create User",
            width=300,
            height=42,
            command=self.save_user,
        )

        self.save_button.pack(
            padx=20,
            pady=5,
        )

        clear_button = ctk.CTkButton(
            form_frame,
            text="Clear Form",
            width=300,
            height=40,
            fg_color="#64748B",
            hover_color="#475569",
            command=self.clear_form,
        )

        clear_button.pack(
            padx=20,
            pady=5,
        )

        self.status_button = ctk.CTkButton(
            form_frame,
            text="Activate / Deactivate",
            width=300,
            height=40,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.change_status,
        )

        self.status_button.pack(
            padx=20,
            pady=(5, 20),
        )

        # ----------------------------------------
        # TABLE AREA
        # ----------------------------------------

        list_frame = ctk.CTkFrame(
            main,
            fg_color="white",
            corner_radius=12,
        )

        list_frame.pack(
            side="left",
            fill="both",
            expand=True,
        )

        search_frame = ctk.CTkFrame(
            list_frame,
            fg_color="transparent",
        )

        search_frame.pack(
            fill="x",
            padx=18,
            pady=(18, 10),
        )

        self.search_entry = ctk.CTkEntry(
            search_frame,
            height=40,
            placeholder_text=(
                "Search by username, name, role or status"
            ),
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10),
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.load_users(),
        )

        refresh_button = ctk.CTkButton(
            search_frame,
            text="Refresh",
            width=100,
            height=40,
            command=self.load_users,
        )

        refresh_button.pack(
            side="right",
        )

        table_container = ctk.CTkFrame(
            list_frame,
            fg_color="transparent",
        )

        table_container.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=(5, 18),
        )

        columns = (
            "id",
            "username",
            "name",
            "role",
            "status",
            "created",
        )

        self.user_table = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        self.user_table.heading(
            "id",
            text="ID",
        )

        self.user_table.heading(
            "username",
            text="Username",
        )

        self.user_table.heading(
            "name",
            text="Full Name",
        )

        self.user_table.heading(
            "role",
            text="Role",
        )

        self.user_table.heading(
            "status",
            text="Status",
        )

        self.user_table.heading(
            "created",
            text="Created At",
        )

        self.user_table.column(
            "id",
            width=45,
            anchor="center",
        )

        self.user_table.column(
            "username",
            width=130,
        )

        self.user_table.column(
            "name",
            width=180,
        )

        self.user_table.column(
            "role",
            width=90,
            anchor="center",
        )

        self.user_table.column(
            "status",
            width=90,
            anchor="center",
        )

        self.user_table.column(
            "created",
            width=160,
        )

        vertical_scroll = ttk.Scrollbar(
            table_container,
            orient="vertical",
            command=self.user_table.yview,
        )

        horizontal_scroll = ttk.Scrollbar(
            table_container,
            orient="horizontal",
            command=self.user_table.xview,
        )

        self.user_table.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set,
        )

        self.user_table.grid(
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

        self.user_table.bind(
            "<<TreeviewSelect>>",
            self.user_selected,
        )

    def create_entry(
        self,
        parent,
        placeholder,
    ):

        entry = ctk.CTkEntry(
            parent,
            width=300,
            height=40,
            placeholder_text=placeholder,
        )

        entry.pack(
            padx=20,
            pady=7,
        )

        return entry

    def collect_form_data(self):

        return {
            "username":
                self.username_entry.get(),

            "full_name":
                self.full_name_entry.get(),

            "password":
                self.password_entry.get(),

            "role":
                self.role_menu.get(),
        }

    def save_user(self):

        data = self.collect_form_data()

        if self.selected_user_id is None:

            success, message = create_user(
                data,
                self.current_user,
            )

        else:

            success, message = update_user(
                self.selected_user_id,
                data,
                self.current_user,
            )

        if success:

            self.message_label.configure(
                text=message,
                text_color="#15803D",
            )

            self.clear_form(
                keep_message=True
            )

            self.load_users()

        else:

            self.message_label.configure(
                text=message,
                text_color="#DC2626",
            )

    def load_users(self):

        search_text = ""

        if hasattr(
            self,
            "search_entry",
        ):
            search_text = (
                self.search_entry.get()
            )

        users = get_all_users(
            search_text
        )

        for item in self.user_table.get_children():

            self.user_table.delete(
                item
            )

        for user in users:

            self.user_table.insert(
                "",
                "end",
                values=(
                    user["id"],
                    user["username"],
                    user["full_name"],
                    user["role"],
                    user["status"],
                    user["created_at"],
                ),
            )

    def user_selected(
        self,
        event=None,
    ):

        selected = self.user_table.selection()

        if not selected:
            return

        values = self.user_table.item(
            selected[0],
            "values",
        )

        user_id = int(
            values[0]
        )

        user = get_user_by_id(
            user_id
        )

        if not user:
            return

        self.selected_user_id = user_id

        self.set_entry(
            self.username_entry,
            user["username"],
        )

        self.set_entry(
            self.full_name_entry,
            user["full_name"],
        )

        self.password_entry.delete(
            0,
            "end",
        )

        self.role_menu.set(
            user["role"]
        )

        self.save_button.configure(
            text="Update User"
        )

        if user["status"] == "Active":

            self.status_button.configure(
                text="Deactivate User",
                fg_color="#DC2626",
                hover_color="#B91C1C",
            )

        else:

            self.status_button.configure(
                text="Activate User",
                fg_color="#15803D",
                hover_color="#166534",
            )

        self.message_label.configure(
            text=(
                f"Editing user "
                f"{user['username']}"
            ),
            text_color="#2563EB",
        )

    def set_entry(
        self,
        entry,
        value,
    ):

        entry.delete(
            0,
            "end",
        )

        entry.insert(
            0,
            value,
        )

    def clear_form(
        self,
        keep_message=False,
    ):

        self.selected_user_id = None

        self.username_entry.delete(
            0,
            "end",
        )

        self.full_name_entry.delete(
            0,
            "end",
        )

        self.password_entry.delete(
            0,
            "end",
        )

        self.role_menu.set(
            "Employee"
        )

        self.save_button.configure(
            text="Create User"
        )

        self.status_button.configure(
            text="Activate / Deactivate",
            fg_color="#DC2626",
            hover_color="#B91C1C",
        )

        if not keep_message:

            self.message_label.configure(
                text=""
            )

        for selection in self.user_table.selection():

            self.user_table.selection_remove(
                selection
            )

    def change_status(self):

        if self.selected_user_id is None:

            messagebox.showwarning(
                "No User Selected",
                "Please select a user account first.",
            )

            return

        selected_user = get_user_by_id(
            self.selected_user_id
        )

        if not selected_user:

            messagebox.showerror(
                "Error",
                "Selected user no longer exists.",
            )

            return

        new_action = (
            "deactivate"
            if selected_user["status"] == "Active"
            else "activate"
        )

        confirmation = messagebox.askyesno(
            "Confirm User Status",
            (
                f"Are you sure you want to "
                f"{new_action} "
                f"{selected_user['username']}?"
            ),
        )

        if not confirmation:
            return

        success, message = toggle_user_status(
            self.selected_user_id,
            self.current_user,
        )

        if success:

            messagebox.showinfo(
                "User Status Updated",
                message,
            )

            self.clear_form()
            self.load_users()

        else:

            messagebox.showerror(
                "Operation Blocked",
                message,
            )