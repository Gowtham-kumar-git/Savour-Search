import tkinter
import customtkinter
import mysql.connector
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np
import spacy
import speech_recognition as sr
import threading
from PIL import Image, ImageTk
from random import choice

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Gowtham@246",
    database="savoursearch"
)
cursor = conn.cursor()

customtkinter.set_default_color_theme("dark-blue")
customtkinter.set_appearance_mode("System")

COLORS = {
    "primary": "#FF6B6B",
    "secondary": "#4ECDC4",
    "accent": "#FFE66D",
    "background": "#292F36",
    "text": "#F7FFF7",
    "highlight": "#FF9F1C"
}


class SavourSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SavourSearch 🍔")
        self.root.geometry("1200x750")
        self.root.minsize(1100, 700)
        self.center_window()
        self.nlp = spacy.load("en_core_web_sm")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        try:
            self.logo_img = ImageTk.PhotoImage(
                Image.open("logo.png").resize((180, 180)))
        except:
            self.logo_img = None

        self.set_custom_styles()
        self.show_login()

    def set_custom_styles(self):
        customtkinter.CTkLabel.appearance = {
            "font": ("Arial Rounded MT Bold", 12),
            "text_color": COLORS["text"]
        }

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def show_login(self):
        self.login_frame = customtkinter.CTkFrame(self.root, corner_radius=20, fg_color=COLORS["background"],
                                                  border_color=COLORS["accent"], border_width=3)
        self.login_frame.pack(expand=True, fill="both", padx=100, pady=80)

        if self.logo_img:
            logo_label = customtkinter.CTkLabel(
                self.login_frame, image=self.logo_img, text="")
            logo_label.pack(pady=(30, 10))
        else:
            logo_label = customtkinter.CTkLabel(self.login_frame, text="🍕 SavourSearch 🍔",
                                                font=("Arial Rounded MT Bold", 28), text_color=COLORS["primary"])
            logo_label.pack(pady=(30, 10))

        title = customtkinter.CTkLabel(self.login_frame, text="Welcome Food Explorer!",
                                       font=("Arial Rounded MT Bold", 24), text_color=COLORS["secondary"])
        title.pack(pady=(10, 30))

        form_frame = customtkinter.CTkFrame(
            self.login_frame, fg_color="transparent")
        form_frame.pack(pady=10, padx=20)

        self.username_entry = customtkinter.CTkEntry(form_frame, placeholder_text="👤 Username",
                                                     width=350, height=50, corner_radius=12,
                                                     font=("Arial", 16), fg_color="#2B2B2B",
                                                     border_color=COLORS["primary"], border_width=2)
        self.username_entry.pack(pady=15)

        self.password_entry = customtkinter.CTkEntry(form_frame, placeholder_text="🔒 Password", show="•",
                                                     width=350, height=50, corner_radius=12,
                                                     font=("Arial", 16), fg_color="#2B2B2B",
                                                     border_color=COLORS["primary"], border_width=2)
        self.password_entry.pack(pady=15)

        login_button = customtkinter.CTkButton(form_frame, text="Let's Cook! 🚀", command=self.check_login,
                                               width=350, height=50, corner_radius=12,
                                               font=("Arial Rounded MT Bold", 18), fg_color=COLORS["primary"],
                                               hover_color=COLORS["highlight"],
                                               border_color=COLORS["accent"], border_width=2)
        login_button.pack(pady=30)

        self.root.bind('<Return>', lambda event: self.check_login())
        self.add_decorative_elements()

    def add_decorative_elements(self):
        food_icons = ["🍕", "🍔", "🍟", "🌮", "🍣", "🍦", "🍩"]
        for i in range(5):
            label = customtkinter.CTkLabel(self.login_frame, text=choice(food_icons),
                                           font=("Arial", 24),
                                           text_color=choice([COLORS["primary"], COLORS["secondary"], COLORS["accent"]]))
            label.place(x=choice(range(50, 400)), y=choice(
                range(50, 500)), anchor="center")

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "admin" and password == "pass":
            self.login_frame.pack_forget()
            self.show_main_app()
        else:
            error_label = customtkinter.CTkLabel(self.login_frame,
                                                 text="⚠ Oops! Wrong credentials. Try again!",
                                                 text_color="#FF6B6B",
                                                 font=("Arial Rounded MT Bold", 14))
            error_label.pack(pady=5)
            self.root.after(3000, error_label.destroy)
            self.shake_window()

    def shake_window(self):
        x = self.root.winfo_x()
        for i in range(0, 3):
            for offset in [10, -10, 8, -8, 5, -5, 0]:
                self.root.geometry(f"+{x + offset}+{self.root.winfo_y()}")
                self.root.update()
                self.root.after(50)

    def show_main_app(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.tabView = customtkinter.CTkTabview(self.root, width=1100, height=700, corner_radius=20,
                                                segmented_button_selected_color=COLORS["primary"],
                                                segmented_button_selected_hover_color=COLORS["highlight"],
                                                segmented_button_unselected_hover_color="#3A3A3A",
                                                segmented_button_fg_color=COLORS["background"],
                                                text_color=COLORS["text"],
                                                border_width=2, border_color=COLORS["accent"])
        self.tabView.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.tabView.add("🍳 Recipes")
        self.tabView.add("🥦 Ingredients")
        self.tabView.add("🤖 Foodie Bot")
        self.tabView.set("🍳 Recipes")

        self.create_search_section(
            "🍳 Recipes", self.search_recipes, self.clear_results1, self.recommend_recipes)
        self.create_search_section(
            "🥦 Ingredients", self.search_ingredients, self.clear_results2, self.recommend_ingredients)
        self.create_chatbot_tab()

        self.status_bar = customtkinter.CTkLabel(self.root,
                                                 text="🌟 Ready to explore delicious recipes! 🌟",
                                                 anchor="w",
                                                 font=(
                                                     "Arial Rounded MT Bold", 12),
                                                 text_color=COLORS["accent"])
        self.status_bar.grid(row=1, column=0, sticky="ew",
                             padx=20, pady=(0, 10))
        self.animate_status_bar()

    def animate_status_bar(self):
        messages = [
            "🌟 Finding the tastiest recipes for you...",
            "🍕 Pizza time! What are you craving?",
            "👨‍🍳 Your personal chef is ready!",
            "🔍 Searching the culinary universe..."
        ]
        current_msg = self.status_bar.cget("text")
        new_msg = choice([m for m in messages if m != current_msg])
        self.status_bar.configure(text=new_msg)
        self.root.after(5000, self.animate_status_bar)

    def create_search_section(self, tab_name, search_command, clear_command, recommend_command):
        tab = self.tabView.tab(tab_name)
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        search_container = customtkinter.CTkFrame(tab, fg_color=COLORS["background"],
                                                  corner_radius=15, border_width=2,
                                                  border_color=COLORS["secondary"])
        search_container.grid(row=0, column=0, pady=20, padx=20, sticky="ew")

        search_icon = "🔍" if "Recipes" in tab_name else "🥗"
        search_bar = customtkinter.CTkEntry(search_container, width=600, height=50,
                                            placeholder_text=f"{search_icon} Search {tab_name.strip()}...",
                                            corner_radius=12, font=("Arial", 16),
                                            fg_color="#2B2B2B", border_color=COLORS["primary"], border_width=2)
        search_bar.grid(row=0, column=0, padx=(15, 10), pady=15, sticky="ew")

        button_config = {
            "width": 100, "height": 50, "corner_radius": 12,
            "font": ("Arial Rounded MT Bold", 14), "border_width": 2
        }

        search_button = customtkinter.CTkButton(search_container, text="Search 🔎", command=search_command,
                                                fg_color=COLORS["primary"], hover_color=COLORS["highlight"],
                                                border_color=COLORS["accent"], **button_config)
        search_button.grid(row=0, column=1, padx=(0, 10), pady=15)

        clear_button = customtkinter.CTkButton(search_container, text="Clear 🧹", command=clear_command,
                                               fg_color="#6C757D", hover_color="#495057",
                                               border_color="#ADB5BD", **button_config)
        clear_button.grid(row=0, column=2, padx=(0, 10), pady=15)

        recommend_button = customtkinter.CTkButton(search_container, text="Similar 💫",
                                                   command=lambda: recommend_command(
                                                       search_bar.get()),
                                                   fg_color=COLORS["secondary"], hover_color="#3AA8A1",
                                                   border_color="#4ECDC4", **button_config)
        recommend_button.grid(row=0, column=3, padx=(0, 15), pady=15)

        search_container.grid_columnconfigure(0, weight=1)

        results_frame = customtkinter.CTkScrollableFrame(tab, width=1000, height=550,
                                                         corner_radius=15, fg_color="#2B2B2B",
                                                         border_width=2, border_color=COLORS["primary"])
        results_frame.grid(row=1, column=0, padx=20,
                           pady=(0, 20), sticky="nsew")

        if "Recipes" in tab_name:
            self.searchBar1 = search_bar
            self.results_frame1 = results_frame
        else:
            self.searchBar2 = search_bar
            self.results_frame2 = results_frame

    def create_chatbot_tab(self):
        chatbot_tab = self.tabView.tab("🤖 Foodie Bot")
        chatbot_tab.grid_rowconfigure(1, weight=1)
        chatbot_tab.grid_columnconfigure(0, weight=1)

        self.chat_output = customtkinter.CTkTextbox(chatbot_tab, height=450, width=900,
                                                    corner_radius=15, font=("Arial", 14), wrap="word",
                                                    fg_color="#2B2B2B", text_color=COLORS["text"],
                                                    border_width=2, border_color=COLORS["secondary"],
                                                    scrollbar_button_color=COLORS["primary"],
                                                    scrollbar_button_hover_color=COLORS["highlight"])
        self.chat_output.grid(row=1, column=0, pady=(
            20, 10), padx=20, sticky="nsew")
        self.chat_output.insert(
            "end", "🤖 Foodie Bot: Hello! I'm your culinary assistant! 🍽️\n\n")
        self.chat_output.configure(state="disabled")

        input_frame = customtkinter.CTkFrame(
            chatbot_tab, fg_color="transparent", height=60)
        input_frame.grid(row=2, column=0, pady=(0, 20), padx=20, sticky="ew")

        self.chat_entry = customtkinter.CTkEntry(input_frame, width=700, height=60,
                                                 placeholder_text="🍴 Ask something about food...",
                                                 corner_radius=12, font=("Arial", 16),
                                                 fg_color="#2B2B2B", border_color=COLORS["primary"],
                                                 border_width=2)
        self.chat_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        send_button = customtkinter.CTkButton(input_frame, text="Send ✈️", command=self.handle_chatbot,
                                              width=120, height=60, corner_radius=12,
                                              font=("Arial Rounded MT Bold", 16), fg_color=COLORS["primary"],
                                              hover_color=COLORS["highlight"], border_color=COLORS["accent"],
                                              border_width=2)
        send_button.grid(row=0, column=1, padx=(0, 10))

        voice_input_button = customtkinter.CTkButton(input_frame, text="🎤 Speak", command=self.start_voice_input,
                                                     width=100, height=60, corner_radius=12,
                                                     font=("Arial Rounded MT Bold", 16), fg_color=COLORS["secondary"],
                                                     hover_color="#3AA8A1", border_color="#4ECDC4", border_width=2)
        voice_input_button.grid(row=0, column=2)

        input_frame.grid_columnconfigure(0, weight=1)
        self.chat_entry.bind('<Return>', lambda event: self.handle_chatbot())

    def start_voice_input(self):
        threading.Thread(target=self.voice_input_thread, daemon=True).start()

    def voice_input_thread(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.update_chat_output(
                "Listening for your question...\n", is_user=False)
            try:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=5)
                user_message = recognizer.recognize_google(audio)
                self.root.after(0, self.chat_entry.delete, 0, "end")
                self.root.after(0, self.chat_entry.insert, 0, user_message)
                # Automatically send the message after inserting it
                self.root.after(0, self.handle_chatbot)
            except sr.UnknownValueError:
                self.update_chat_output(
                    "Sorry, I didn't catch that.\n", is_user=False)
            except sr.RequestError:
                self.update_chat_output(
                    "Sorry, there was an issue with the speech service.\n", is_user=False)
            except Exception as e:
                self.update_chat_output(f"Error: {str(e)}\n", is_user=False)

    def update_chat_output(self, message, is_user=False):
        self.chat_output.configure(state="normal")
        tag = "user" if is_user else "bot"
        self.chat_output.insert("end", message, tag)
        self.chat_output.tag_config("user", foreground="#007BFF")
        self.chat_output.tag_config("bot", foreground="#28A745")
        self.chat_output.configure(state="disabled")
        self.chat_output.see("end")

    def handle_chatbot(self):
        user_message = self.chat_entry.get().strip()
        if not user_message:
            return
        self.update_chat_output(f"You: {user_message}\n", is_user=True)
        self.chat_entry.delete(0, "end")
        threading.Thread(target=self.process_chatbot_message,
                         args=(user_message,), daemon=True).start()

    def process_chatbot_message(self, user_message):
        try:
            response = self.process_nlp(user_message)
            self.root.after(0, self.update_chat_output,
                            f"Bot: {response}\n\n", False)
        except Exception as e:
            self.root.after(0, self.update_chat_output,
                            f"Bot: Sorry, an error occurred: {str(e)}\n\n", False)

    def process_nlp(self, user_message):
        doc = self.nlp(user_message.lower())
        keywords = [
            token.text for token in doc if token.pos_ in ["NOUN", "ADJ"]]
        nutrient_map = {
            "protein": "Protein_g",
            "fat": "Fat_g",
            "fats": "Fat_g",
            "carb": "Carbohydrates_g",
            "carbs": "Carbohydrates_g",
            "calorie": "Calories_kcal",
            "calories": "Calories_kcal",
        }
        high_keywords = {"high", "more", "rich",
                         "maximum", "above", "increase"}
        low_keywords = {"low", "less", "minimum", "below", "reduce"}
        target_table = "ingredients_nutrition" if "ingredient" in user_message else "recipes_nutrition"
        nutrient_column = None
        threshold = 10
        is_high = True
        for kw in keywords:
            for word, col in nutrient_map.items():
                if word in kw:
                    nutrient_column = col
                    break
        for kw in keywords:
            if kw in low_keywords:
                is_high = False
            elif kw in high_keywords:
                is_high = True
        if not nutrient_column:
            return "I'm not sure what nutrient you're referring to. Try asking about protein, fat, carbs, or calories."
        operator = ">" if is_high else "<"
        query = f"SELECT * FROM {target_table} WHERE {nutrient_column} {operator} %s LIMIT 10"
        try:
            cursor.execute(query, (threshold,))
            results = cursor.fetchall()
            if not results:
                return "No matching results found."
            response_lines = []
            for row in results:
                response_lines.append(", ".join(str(val) for val in row[:2]))
            return "\n".join(response_lines)
        except Exception as e:
            return f"Error: {e}"

    def display_results(self, frame, columns, results):
        for widget in frame.winfo_children():
            widget.destroy()
        if not results:
            no_data = customtkinter.CTkLabel(
                frame,
                text="No matching results found.",
                font=("Arial", 14),
                text_color="gray"
            )
            no_data.pack(pady=20)
            return
        header_frame = customtkinter.CTkFrame(frame, fg_color="#E9ECEF")
        header_frame.pack(fill="x", pady=(0, 5))
        for col_index, col_name in enumerate(columns):
            label = customtkinter.CTkLabel(
                header_frame,
                text=col_name,
                font=("Arial", 12, "bold"),
                text_color="#212529",
                anchor="w"
            )
            label.grid(row=0, column=col_index, padx=10, pady=5, sticky="ew")
            header_frame.grid_columnconfigure(col_index, weight=1)
        for row_index, row_data in enumerate(results):
            row_frame = customtkinter.CTkFrame(
                frame,
                fg_color="#F8F9FA" if row_index % 2 == 0 else "#E9ECEF"
            )
            row_frame.pack(fill="x", pady=1)
            for col_index, value in enumerate(row_data):
                label = customtkinter.CTkLabel(
                    row_frame,
                    text=value,
                    font=("Arial", 12),
                    text_color="#212529",
                    anchor="w"
                )
                label.grid(row=0, column=col_index,
                           padx=10, pady=5, sticky="ew")
                row_frame.grid_columnconfigure(col_index, weight=1)

    def search_recipes(self):
        query = self.searchBar1.get()
        self.status_bar.configure(text="Searching recipes...")
        try:
            cursor.execute('''SELECT Recipe_name, Main_Ingredients, 
                                         Calories_kcal, Protein_g, Fat_g, Carbohydrates_g 
                                  FROM recipes_nutrition 
                                  WHERE Recipe_name LIKE %s''', ('%' + query + '%',))
            results = cursor.fetchall()
            columns = ["Recipe Name", "Main Ingredients",
                       "Calories", "Proteins", "Fats", "Carbs"]
            self.display_results(self.results_frame1, columns, results)
            self.status_bar.configure(text=f"Found {len(results)} recipes")
        except Exception as e:
            self.status_bar.configure(text=f"Error: {str(e)}")

    def search_ingredients(self):
        query = self.searchBar2.get()
        self.status_bar.configure(text="Searching ingredients...")
        try:
            cursor.execute('''SELECT Ingredient, Calories_kcal, Protein_g, Fat_g, Carbohydrates_g 
                                  FROM ingredients_nutrition 
                                  WHERE Ingredient LIKE %s''', ('%' + query + '%',))
            results = cursor.fetchall()
            columns = ["Ingredient", "Calories", "Proteins", "Fats", "Carbs"]
            self.display_results(self.results_frame2, columns, results)
            self.status_bar.configure(text=f"Found {len(results)} ingredients")
        except Exception as e:
            self.status_bar.configure(text=f"Error: {str(e)}")

    def recommend_recipes(self, keyword):
        self.status_bar.configure(text="Finding similar recipes...")
        try:
            cursor.execute(
                "SELECT Recipe_name, Calories_kcal FROM recipes_nutrition")
            data = cursor.fetchall()
            if not data:
                self.status_bar.configure(text="No recipe data available")
                return
            names, calories = zip(*data)
            calories_array = np.array(calories).reshape(-1, 1)
            scaler = StandardScaler()
            scaled_calories = scaler.fit_transform(calories_array)
            kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
            labels = kmeans.fit_predict(scaled_calories)
            name_to_label = dict(zip(names, labels))
            cursor.execute(
                "SELECT Recipe_name FROM recipes_nutrition WHERE Recipe_name LIKE %s", ('%' + keyword + '%',))
            matches = cursor.fetchall()
            if not matches:
                self.status_bar.configure(text="No matches found")
                return
            target_label = name_to_label.get(matches[0][0], None)
            if target_label is None:
                self.status_bar.configure(text="No similar recipes found")
                return
            similar_names = [name for name in names if name_to_label.get(
                name) == target_label and name != matches[0][0]]
            if similar_names:
                format_strings = ','.join(['%s'] * len(similar_names))
                query = f'''SELECT Recipe_name, Main_Ingredients, Calories_kcal, Protein_g, Fat_g, Carbohydrates_g 
                                FROM recipes_nutrition 
                                WHERE Recipe_name IN ({format_strings})'''
                cursor.execute(query, tuple(similar_names))
                results = cursor.fetchall()
                columns = ["Recipe Name", "Main Ingredients",
                           "Calories", "Proteins", "Fats", "Carbs"]
                self.display_results(self.results_frame1, columns, results)
                self.status_bar.configure(
                    text=f"Found {len(results)} similar recipes")
            else:
                self.status_bar.configure(text="No similar recipes found")
        except Exception as e:
            self.status_bar.configure(text=f"Error: {str(e)}")

    def recommend_ingredients(self, keyword):
        self.status_bar.configure(text="Finding similar ingredients...")
        try:
            cursor.execute(
                "SELECT Ingredient, Calories_kcal FROM ingredients_nutrition")
            data = cursor.fetchall()
            if not data:
                self.status_bar.configure(text="No ingredient data available")
                return
            names, calories = zip(*data)
            calories_array = np.array(calories).reshape(-1, 1)
            scaler = StandardScaler()
            scaled_calories = scaler.fit_transform(calories_array)
            kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
            labels = kmeans.fit_predict(scaled_calories)
            name_to_label = dict(zip(names, labels))
            cursor.execute(
                "SELECT Ingredient FROM ingredients_nutrition WHERE Ingredient LIKE %s", ('%' + keyword + '%',))
            matches = cursor.fetchall()
            if not matches:
                self.status_bar.configure(text="No matches found")
                return
            target_label = name_to_label.get(matches[0][0], None)
            if target_label is None:
                self.status_bar.configure(text="No similar ingredients found")
                return
            similar_names = [name for name in names if name_to_label.get(
                name) == target_label and name != matches[0][0]]
            if similar_names:
                format_strings = ','.join(['%s'] * len(similar_names))
                query = f'''SELECT Ingredient, Calories_kcal, Protein_g, Fat_g, Carbohydrates_g 
                                FROM ingredients_nutrition 
                                WHERE Ingredient IN ({format_strings})'''
                cursor.execute(query, tuple(similar_names))
                results = cursor.fetchall()
                columns = ["Ingredient", "Calories",
                           "Proteins", "Fats", "Carbs"]
                self.display_results(self.results_frame2, columns, results)
                self.status_bar.configure(
                    text=f"Found {len(results)} similar ingredients")
            else:
                self.status_bar.configure(text="No similar ingredients found")
        except Exception as e:
            self.status_bar.configure(text=f"Error: {str(e)}")

    def clear_results1(self):
        for widget in self.results_frame1.winfo_children():
            widget.destroy()
        self.status_bar.configure(text="Ready")

    def clear_results2(self):
        for widget in self.results_frame2.winfo_children():
            widget.destroy()
        self.status_bar.configure(text="Ready")

    def display_results(self, frame, columns, results):
        for widget in frame.winfo_children():
            widget.destroy()
        if not results:
            no_data = customtkinter.CTkLabel(
                frame,
                text="No matching results found.",
                font=("Arial", 14),
                text_color="gray"
            )
            no_data.pack(pady=20)
            return
        header_frame = customtkinter.CTkFrame(frame, fg_color="#E9ECEF")
        header_frame.pack(fill="x", pady=(0, 5))
        for col_index, col_name in enumerate(columns):
            label = customtkinter.CTkLabel(
                header_frame,
                text=col_name,
                font=("Arial", 12, "bold"),
                text_color="#212529",
                anchor="w"
            )
            label.grid(row=0, column=col_index, padx=10, pady=5, sticky="ew")
            header_frame.grid_columnconfigure(col_index, weight=1)
        for row_index, row_data in enumerate(results):
            row_frame = customtkinter.CTkFrame(
                frame,
                fg_color="#F8F9FA" if row_index % 2 == 0 else "#E9ECEF"
            )
            row_frame.pack(fill="x", pady=1)
            for col_index, value in enumerate(row_data):
                label = customtkinter.CTkLabel(
                    row_frame,
                    text=value,
                    font=("Arial", 12),
                    text_color="#212529",
                    anchor="w"
                )
                label.grid(row=0, column=col_index,
                           padx=10, pady=5, sticky="ew")
                row_frame.grid_columnconfigure(col_index, weight=1)

    def handle_chatbot(self):
        user_message = self.chat_entry.get().strip()
        if not user_message:
            return
        self.update_chat_output(f"You: {user_message}\n", is_user=True)
        self.chat_entry.delete(0, "end")
        threading.Thread(target=self.process_chatbot_message,
                         args=(user_message,), daemon=True).start()

    def process_chatbot_message(self, user_message):
        try:
            response = self.process_nlp(user_message)
            self.root.after(0, self.update_chat_output,
                            f"Bot: {response}\n\n", False)
        except Exception as e:
            self.root.after(0, self.update_chat_output,
                            f"Bot: Sorry, an error occurred: {str(e)}\n\n", False)

    def process_nlp(self, user_message):
        doc = self.nlp(user_message.lower())
        keywords = [
            token.text for token in doc if token.pos_ in ["NOUN", "ADJ"]]
        nutrient_map = {
            "protein": "Protein_g",
            "fat": "Fat_g",
            "fats": "Fat_g",
            "carb": "Carbohydrates_g",
            "carbs": "Carbohydrates_g",
            "calorie": "Calories_kcal",
            "calories": "Calories_kcal",
        }
        high_keywords = {"high", "more", "rich",
                         "maximum", "above", "increase"}
        low_keywords = {"low", "less", "minimum", "below", "reduce"}
        target_table = "ingredients_nutrition" if "ingredient" in user_message else "recipes_nutrition"
        nutrient_column = None
        threshold = 10
        is_high = True
        for kw in keywords:
            for word, col in nutrient_map.items():
                if word in kw:
                    nutrient_column = col
                    break
        for kw in keywords:
            if kw in low_keywords:
                is_high = False
            elif kw in high_keywords:
                is_high = True
        if not nutrient_column:
            return "I'm not sure what nutrient you're referring to. Try asking about protein, fat, carbs, or calories."
        operator = ">" if is_high else "<"
        query = f"SELECT * FROM {target_table} WHERE {nutrient_column} {operator} %s LIMIT 10"
        try:
            cursor.execute(query, (threshold,))
            results = cursor.fetchall()
            if not results:
                return "No matching results found."
            response_lines = []
            for row in results:
                response_lines.append(", ".join(str(val) for val in row[:2]))
            return "\n".join(response_lines)
        except Exception as e:
            return f"Error: {e}"

    def update_chat_output(self, message, is_user=False):
        self.chat_output.configure(state="normal")
        tag = "user" if is_user else "bot"
        self.chat_output.insert("end", message, tag)
        self.chat_output.tag_config("user", foreground="#007BFF")
        self.chat_output.tag_config("bot", foreground="#28A745")
        self.chat_output.configure(state="disabled")
        self.chat_output.see("end")

    def start_voice_input(self):
        threading.Thread(target=self.voice_input_thread, daemon=True).start()

    def voice_input_thread(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.update_chat_output(
                "Listening for your question...\n", is_user=False)
            try:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=5)
                user_message = recognizer.recognize_google(audio)
                self.root.after(0, self.chat_entry.delete, 0, "end")
                self.root.after(0, self.chat_entry.insert, 0, user_message)
                self.root.after(0, self.handle_chatbot)
            except sr.UnknownValueError:
                self.update_chat_output(
                    "Sorry, I didn't catch that.\n", is_user=False)
            except sr.RequestError:
                self.update_chat_output(
                    "Sorry, there was an issue with the speech service.\n", is_user=False)
            except Exception as e:
                self.update_chat_output(f"Error: {str(e)}\n", is_user=False)


if __name__ == "__main__":
    root = customtkinter.CTk()
    app = SavourSearchApp(root)
    root.mainloop()
