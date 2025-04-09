import tkinter
import customtkinter
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Gowtham@246", #sakthi #sid use your db name and password
    database="savoursearch"
)
cursor = conn.cursor()

customtkinter.set_default_color_theme("green")


class SavourSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SavourSearch")
        self.root.geometry("1000x1000")
        self.show_login()

    def show_login(self):
        self.login_frame = customtkinter.CTkFrame(
            self.root, width=700, height=700)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        title = customtkinter.CTkLabel(
            self.login_frame, text="Login", font=("Arial", 20))
        title.pack(pady=20)

        self.username_entry = customtkinter.CTkEntry(
            self.login_frame, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.password_entry = customtkinter.CTkEntry(
            self.login_frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        login_button = customtkinter.CTkButton(
            self.login_frame, text="Login", command=self.check_login)
        login_button.pack(pady=20)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "pass":
            self.login_frame.destroy()
            self.show_main_app()
        else:
            error_label = customtkinter.CTkLabel(
                self.login_frame, text="Invalid credentials", text_color="red")
            error_label.pack()

    def show_main_app(self):
        self.tabView = customtkinter.CTkTabview(
            self.root, width=1000, height=1000)
        self.tabView.pack(padx=1, pady=1)

        self.tabView.add("Recipes")
        self.tabView.add("Ingredients")
        self.tabView.set("Recipes")

        self.create_search_section(
            "Recipes", self.search_recipes, self.clear_results1)
        self.create_search_section(
            "Ingredients", self.search_ingredients, self.clear_results2)

    def create_search_section(self, tab_name, search_command, clear_command):
        tab = self.tabView.tab(tab_name)

        search_bar = customtkinter.CTkEntry(tab, width=400)
        search_bar.place(relx=0.4, rely=0.05, anchor=tkinter.CENTER)

        search_button = customtkinter.CTkButton(
            tab, text="Search", command=search_command)
        search_button.place(relx=0.7, rely=0.05, anchor=tkinter.CENTER)

        clear_button = customtkinter.CTkButton(
            tab, text="Clear Results", command=clear_command)
        clear_button.place(relx=0.85, rely=0.05, anchor=tkinter.CENTER)

        results_frame = customtkinter.CTkFrame(tab)
        results_frame.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

        if tab_name == "Recipes":
            self.searchBar1, self.results_frame1 = search_bar, results_frame
        else:
            self.searchBar2, self.results_frame2 = search_bar, results_frame

    def display_results(self, frame, columns, results):
        for widget in frame.winfo_children():
            widget.destroy()

        col_widths = [20, 30, 10, 10, 10, 10]

        for col_index, col_name in enumerate(columns):
            label = customtkinter.CTkLabel(
                frame, text=col_name, font=("Arial", 12, "bold"))
            label.grid(row=0, column=col_index, padx=10, pady=5, sticky="w")

        for row_index, row_data in enumerate(results, start=1):
            for col_index, value in enumerate(row_data):
                label = customtkinter.CTkLabel(
                    frame, text=value, font=("Arial", 10))
                label.grid(row=row_index, column=col_index,
                           padx=10, pady=5, sticky="w")

    def search_recipes(self):
        query = self.searchBar1.get()
        cursor.execute('''SELECT Recipe_name, Main_Ingredients, 
                                 Calories_per_serving, Protein_g, Fat_g, Carbohydrates_g 
                          FROM recipes_nutrition 
                          WHERE Recipe_name LIKE %s''', ('%' + query + '%',))
        results = cursor.fetchall()
        columns = ["Recipe Name", "Main Ingredients",
                   "Calories", "Proteins", "Fats", "Carbs"]
        self.display_results(self.results_frame1, columns, results)

    def search_ingredients(self):
        query = self.searchBar2.get()
        cursor.execute('''SELECT Ingredient, Calories_kcal, Protein_g, Fat_g, Carbohydrates_g 
                          FROM ingredients_nutrition 
                          WHERE Ingredient LIKE %s''', ('%' + query + '%',))
        results = cursor.fetchall()
        columns = ["Ingredient", "Calories", "Proteins", "Fats", "Carbs"]
        self.display_results(self.results_frame2, columns, results)

    def clear_results1(self):
        for widget in self.results_frame1.winfo_children():
            widget.destroy()

    def clear_results2(self):
        for widget in self.results_frame2.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = customtkinter.CTk()
    SavourSearchApp(app)
    app.mainloop()
    conn.close()
