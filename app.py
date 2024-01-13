import tkinter
import customtkinter

from _TopLevWin import _ToplevelWindow

from requests_html import HTMLSession


month = {
    'январь': 'january',
    'февраль': 'february',
    'март': 'march',
    'апрель': 'april',
    'май': 'may',
    'июнь': 'june',
    'июль': 'july',
    'август': 'august',
    'сентябрь': 'september',
    'октябрь': 'october',
    'ноябрь': 'november',
    'декабрь': 'december',
}


class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("350x200")
        self.title("test")

        self.day_lab = customtkinter.CTkLabel(self, text="Введи число")
        self.day_lab.pack(anchor=tkinter.CENTER)
        self.day = customtkinter.CTkEntry(self)
        self.day.pack()

        self.font = ("Arial", 12)
        self.month_lab = customtkinter.CTkLabel(self, text="Введи месяц (в именительном падеже)", font=self.font)
        self.month_lab.pack(anchor=tkinter.CENTER)
        self.month_inp = customtkinter.CTkEntry(self)
        self.month_inp.pack()

        self.toplevel_window = None

        self.button = customtkinter.CTkButton(self, text='input', command=self.open_toplevel)
        self.button.pack(pady=3)


    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():

            session = HTMLSession()
            self.day_input = self.day.get().lower()
            self.month_input = self.month_inp.get().lower()

            if self.month_input in month:
                self.response = session.get(
                    f"https://kalendar-365.ru/garden/2024/{month[self.month_input]}/{self.day_input}")
                print(self.response)
                self.elements = self.response.html.find('blockquote.moon_influence_neutral p')
                for self.element in self.elements:
                    self.text = self.element.text
                session.close()
            else:
                self.text = f"Проверьте написание месяца.\n <-Такого месяца --{self.month_input}-- не существует!->"
            print(self.text)
            with open("log.txt", "w") as file:
                file.write(f"{self.text}")
            self.toplevel_window = _ToplevelWindow(self)

        else:
            self.toplevel_window.focus()


app = App()
app.mainloop()