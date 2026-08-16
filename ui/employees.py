import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import date

from services.employee_service import (
    create_employee,
    get_all_employees,
    get_employee_by_id,
    update_employee,
    deactivate_employee,
)


class EmployeesFrame(ctk.CTkFrame):

    def __init__(self, master, current_user):
        super().__init__(
            master,
            fg_color="#F4F6F8",
        )

        self.current_user = current_user
        self.selected_employee_id = None

        self.pack(
            fill="both",
            expand=True,
        )

        self.create_ui()
        self.load_employees()

    def create_ui(self):

        # --------------------------------------------
        # HEADER
        # --------------------------------------------

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
            text="Employee Management",
            font=ctk.CTkFont(
                size=26,
                weight="bold",
            ),
            text_color="#111827",
        )

        title.pack(
            side="left",
        )

        # --------------------------------------------
        # MAIN AREA
        # --------------------------------------------

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

        # --------------------------------------------
        # FORM
        # --------------------------------------------

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
            text="Employee Details",
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

        self.employee_code_entry = self.create_entry(
            form_frame,
            "Employee Code"
        )

        self.full_name_entry = self.create_entry(
            form_frame,
            "Full Name"
        )

        self.email_entry = self.create_entry(
            form_frame,
            "Email"
        )

        self.phone_entry = self.create_entry(
            form_frame,
            "Phone"
        )

        self.department_entry = self.create_entry(
            form_frame,
            "Department"
        )

        self.designation_entry = self.create_entry(
            form_frame,
            "Designation"
        )

        self.salary_entry = self.create_entry(
            form_frame,
            "Salary"
        )

        self.joining_date_entry = self.create_entry(
            form_frame,
            "Joining Date (YYYY-MM-DD)"
        )

        self.joining_date_entry.insert(
            0,
            date.today().isoformat()
        )

        self.message_label = ctk.CTkLabel(
            form_frame,
            text="",
            wraplength=280,
            font=ctk.CTkFont(size=12),
        )

        self.message_label.pack(
            pady=(7, 4),
        )

        buttons = ctk.CTkFrame(
            form_frame,
            fg_color="transparent",
        )

        buttons.pack(
            fill="x",
            padx=20,
            pady=(5, 20),
        )

        self.save_button = ctk.CTkButton(
            buttons,
            text="Add Employee",
            height=40,
            command=self.save_employee,
        )

        self.save_button.pack(
            fill="x",
            pady=4,
        )

        clear_button = ctk.CTkButton(
            buttons,
            text="Clear Form",
            height=38,
            fg_color="#64748B",
            hover_color="#475569",
            command=self.clear_form,
        )

        clear_button.pack(
            fill="x",
            pady=4,
        )

        self.deactivate_button = ctk.CTkButton(
            buttons,
            text="Deactivate Employee",
            height=38,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.deactivate_selected_employee,
        )

        self.deactivate_button.pack(
            fill="x",
            pady=4,
        )

        # --------------------------------------------
        # LIST SECTION
        # --------------------------------------------

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
                "Search by name, code, email, "
                "department or designation"
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
            lambda event: self.load_employees()
        )

        refresh_button = ctk.CTkButton(
            search_frame,
            text="Refresh",
            width=100,
            height=40,
            command=self.load_employees,
        )

        refresh_button.pack(
            side="right",
        )

        # --------------------------------------------
        # TABLE
        # --------------------------------------------

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
            "code",
            "name",
            "email",
            "department",
            "designation",
            "salary",
            "status",
        )

        self.employee_table = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        self.employee_table.heading(
            "id",
            text="ID",
        )

        self.employee_table.heading(
            "code",
            text="Code",
        )

        self.employee_table.heading(
            "name",
            text="Name",
        )

        self.employee_table.heading(
            "email",
            text="Email",
        )

        self.employee_table.heading(
            "department",
            text="Department",
        )

        self.employee_table.heading(
            "designation",
            text="Designation",
        )

        self.employee_table.heading(
            "salary",
            text="Salary",
        )

        self.employee_table.heading(
            "status",
            text="Status",
        )

        self.employee_table.column(
            "id",
            width=45,
            anchor="center",
        )

        self.employee_table.column(
            "code",
            width=90,
        )

        self.employee_table.column(
            "name",
            width=150,
        )

        self.employee_table.column(
            "email",
            width=180,
        )

        self.employee_table.column(
            "department",
            width=110,
        )

        self.employee_table.column(
            "designation",
            width=120,
        )

        self.employee_table.column(
            "salary",
            width=90,
        )

        self.employee_table.column(
            "status",
            width=80,
            anchor="center",
        )

        vertical_scroll = ttk.Scrollbar(
            table_container,
            orient="vertical",
            command=self.employee_table.yview,
        )

        horizontal_scroll = ttk.Scrollbar(
            table_container,
            orient="horizontal",
            command=self.employee_table.xview,
        )

        self.employee_table.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set,
        )

        self.employee_table.grid(
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

        self.employee_table.bind(
            "<<TreeviewSelect>>",
            self.employee_selected,
        )

    def create_entry(self, parent, placeholder):

        entry = ctk.CTkEntry(
            parent,
            width=300,
            height=38,
            placeholder_text=placeholder,
        )

        entry.pack(
            padx=20,
            pady=5,
        )

        return entry

    def collect_form_data(self):

        return {
            "employee_code":
                self.employee_code_entry.get(),

            "full_name":
                self.full_name_entry.get(),

            "email":
                self.email_entry.get(),

            "phone":
                self.phone_entry.get(),

            "department":
                self.department_entry.get(),

            "designation":
                self.designation_entry.get(),

            "salary":
                self.salary_entry.get(),

            "joining_date":
                self.joining_date_entry.get(),
        }

    def save_employee(self):

        data = self.collect_form_data()

        if self.selected_employee_id is None:

            success, message = create_employee(
                data,
                self.current_user,
            )

        else:

            success, message = update_employee(
                self.selected_employee_id,
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

            self.load_employees()

        else:

            self.message_label.configure(
                text=message,
                text_color="#DC2626",
            )

    def load_employees(self):

        search_text = ""

        if hasattr(self, "search_entry"):
            search_text = self.search_entry.get()

        employees = get_all_employees(
            search_text
        )

        for item in self.employee_table.get_children():
            self.employee_table.delete(item)

        for employee in employees:

            self.employee_table.insert(
                "",
                "end",
                values=(
                    employee["id"],
                    employee["employee_code"],
                    employee["full_name"],
                    employee["email"],
                    employee["department"],
                    employee["designation"],
                    f"{employee['salary']:.2f}",
                    employee["status"],
                ),
            )

    def employee_selected(self, event=None):

        selected = self.employee_table.selection()

        if not selected:
            return

        values = self.employee_table.item(
            selected[0],
            "values",
        )

        employee_id = int(values[0])

        employee = get_employee_by_id(
            employee_id
        )

        if not employee:
            return

        self.selected_employee_id = employee_id

        self.set_entry(
            self.employee_code_entry,
            employee["employee_code"],
        )

        self.set_entry(
            self.full_name_entry,
            employee["full_name"],
        )

        self.set_entry(
            self.email_entry,
            employee["email"],
        )

        self.set_entry(
            self.phone_entry,
            employee["phone"] or "",
        )

        self.set_entry(
            self.department_entry,
            employee["department"] or "",
        )

        self.set_entry(
            self.designation_entry,
            employee["designation"] or "",
        )

        self.set_entry(
            self.salary_entry,
            str(employee["salary"]),
        )

        self.set_entry(
            self.joining_date_entry,
            employee["joining_date"] or "",
        )

        self.save_button.configure(
            text="Update Employee"
        )

        self.message_label.configure(
            text=(
                f"Editing employee "
                f"{employee['employee_code']}"
            ),
            text_color="#2563EB",
        )

    def set_entry(self, entry, value):

        entry.delete(0, "end")

        entry.insert(
            0,
            value
        )

    def clear_form(
        self,
        keep_message=False,
    ):

        self.selected_employee_id = None

        entries = [
            self.employee_code_entry,
            self.full_name_entry,
            self.email_entry,
            self.phone_entry,
            self.department_entry,
            self.designation_entry,
            self.salary_entry,
            self.joining_date_entry,
        ]

        for entry in entries:
            entry.delete(0, "end")

        self.joining_date_entry.insert(
            0,
            date.today().isoformat()
        )

        self.save_button.configure(
            text="Add Employee"
        )

        if not keep_message:

            self.message_label.configure(
                text=""
            )

        for selection in self.employee_table.selection():

            self.employee_table.selection_remove(
                selection
            )

    def deactivate_selected_employee(self):

        if self.selected_employee_id is None:

            messagebox.showwarning(
                "No Employee Selected",
                "Please select an employee first.",
            )

            return

        confirm = messagebox.askyesno(
            "Confirm Deactivation",
            (
                "Are you sure you want to deactivate "
                "this employee?\n\n"
                "The record will not be permanently deleted."
            ),
        )

        if not confirm:
            return

        success, message = deactivate_employee(
            self.selected_employee_id,
            self.current_user,
        )

        if success:

            messagebox.showinfo(
                "Employee Updated",
                message,
            )

            self.clear_form()
            self.load_employees()

        else:

            messagebox.showerror(
                "Operation Failed",
                message,
            )