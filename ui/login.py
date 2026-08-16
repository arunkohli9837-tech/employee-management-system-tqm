import customtkinter as ctk

from services.auth_service import authenticate_user


class LoginFrame(ctk.CTkFrame):

    def __init__(self, master, login_callback):
        super().__init__(
            master,
            fg_color="#EEF2FF",
        )

        self.master = master
        self.login_callback = login_callback

        self.pack(
            fill="both",
            expand=True,
        )

        self.create_ui()

    def create_ui(self):

        container = ctk.CTkFrame(
            self,
            width=430,
            height=520,
            corner_radius=18,
            fg_color="white",
        )

        container.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
        )

        container.pack_propagate(False)

        title = ctk.CTkLabel(
            container,
            text="Employee Management System",
            font=ctk.CTkFont(
                size=25,
                weight="bold",
            ),
            text_color="#172554",
        )

        title.pack(
            pady=(55, 8),
        )

        subtitle = ctk.CTkLabel(
            container,
            text="Q01 • Improve Reliability",
            font=ctk.CTkFont(size=14),
            text_color="#64748B",
        )

        subtitle.pack(
            pady=(0, 35),
        )

        self.username_entry = ctk.CTkEntry(
            container,
            width=320,
            height=48,
            placeholder_text="Username",
        )

        self.username_entry.pack(
            pady=10,
        )

        self.password_entry = ctk.CTkEntry(
            container,
            width=320,
            height=48,
            placeholder_text="Password",
            show="*",
        )

        self.password_entry.pack(
            pady=10,
        )

        self.error_label = ctk.CTkLabel(
            container,
            text="",
            text_color="#DC2626",
            font=ctk.CTkFont(size=13),
        )

        self.error_label.pack(
            pady=(5, 5),
        )

        login_button = ctk.CTkButton(
            container,
            width=320,
            height=48,
            text="Login",
            font=ctk.CTkFont(
                size=15,
                weight="bold",
            ),
            fg_color="#1D4ED8",
            hover_color="#1E40AF",
            command=self.login,
        )

        login_button.pack(
            pady=(10, 20),
        )

        info = ctk.CTkLabel(
            container,
            text=(
                "Default Administrator\n"
                "Username: admin\n"
                "Password: Admin@123"
            ),
            font=ctk.CTkFont(size=12),
            text_color="#64748B",
        )

        info.pack(
            pady=10,
        )

        self.password_entry.bind(
            "<Return>",
            lambda event: self.login(),
        )

    def login(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username:
            self.error_label.configure(
                text="Username is required."
            )
            return

        if not password:
            self.error_label.configure(
                text="Password is required."
            )
            return

        user, error = authenticate_user(
            username,
            password,
        )

        if error:
            self.error_label.configure(
                text=error
            )
            return

        self.login_callback(user)