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

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Gowtham@246",
    database="savoursearch"
)
cursor = conn.cursor()

# Set modern theme and appearance
customtkinter.set_default_color_theme("green")  # or try "blue", "dark-blue"
customtkinter.set_appearance_mode("System")  # "Light" or "Dark"


class SavourSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SavourSearch")
        self.root.geometry("1100x700")
        self.root.minsize(1000, 650)

        # Center the window
        self.center_window()

        # Load NLP model
        self.nlp = spacy.load("en_core_web_sm")

        # Load images (add error handling in production)
        try:
            self.logo_img = ImageTk.PhotoImage(
                Image.open("logo.png").resize((150, 150)))
        except:
            self.logo_img = None

        self.show_login()

    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def show_login(self):
        """Show login screen with modern design"""
        self.login_frame = customtkinter.CTkFrame(self.root, corner_radius=15)
        self.login_frame.pack(expand=True, fill="both", padx=50, pady=50)

        # Add logo if available
        if self.logo_img:
            logo_label = customtkinter.CTkLabel(
                self.login_frame, image=self.logo_img, text="")
            logo_label.pack(pady=(20, 10))

        title = customtkinter.CTkLabel(
            self.login_frame,
            text="Welcome to SavourSearch",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=(10, 20))

        # Form fields with better styling
        form_frame = customtkinter.CTkFrame(
            self.login_frame, fg_color="transparent")
        form_frame.pack(pady=10, padx=20)

        self.username_entry = customtkinter.CTkEntry(
            form_frame,
            placeholder_text="Username",
            width=300,
            height=40,
            corner_radius=10,
            font=("Arial", 14)
        )
        self.username_entry.pack(pady=10)

        self.password_entry = customtkinter.CTkEntry(
            form_frame,
            placeholder_text="Password",
            show="*",
            width=300,
            height=40,
            corner_radius=10,
            font=("Arial", 14)
        )
        self.password_entry.pack(pady=10)

        login_button = customtkinter.CTkButton(
            form_frame,
            text="Login",
            command=self.check_login,
            width=300,
            height=40,
            corner_radius=10,
            font=("Arial", 14, "bold"),
            fg_color="#2CC985",
            hover_color="#207A4A"
        )
        login_button.pack(pady=20)

        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.check_login())

    def check_login(self):
        """Check login credentials"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "pass":
            self.login_frame.pack_forget()
            self.show_main_app()
        else:
            # Show error with animation
            error_label = customtkinter.CTkLabel(
                self.login_frame,
                text="⚠ Invalid credentials",
                text_color="red",
                font=("Arial", 12)
            )
            error_label.pack(pady=5)
            # Remove error after 3 seconds
            self.root.after(3000, error_label.destroy)

    def show_main_app(self):
        """Show main application with tabs"""
        # Configure root grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Create tab view with modern styling
        self.tabView = customtkinter.CTkTabview(
            self.root,
            width=1000,
            height=700,
            corner_radius=15,
            segmented_button_selected_color="#2CC985",
            segmented_button_selected_hover_color="#207A4A",
            segmented_button_unselected_hover_color="#D3D3D3"
        )
        self.tabView.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Add tabs
        self.tabView.add("Recipes")
        self.tabView.add("Ingredients")
        self.tabView.add("Chatbot")
        self.tabView.set("Recipes")  # Default tab

        # Create sections for each tab
        self.create_search_section(
            "Recipes", self.search_recipes, self.clear_results1, self.recommend_recipes)
        self.create_search_section(
            "Ingredients", self.search_ingredients, self.clear_results2, self.recommend_ingredients)
        self.create_chatbot_tab()

        # Add status bar
        self.status_bar = customtkinter.CTkLabel(
            self.root,
            text="Ready",
            anchor="w",
            font=("Arial", 10),
            text_color="gray"
        )
        self.status_bar.grid(row=1, column=0, sticky="ew",
                             padx=10, pady=(0, 5))

    def create_search_section(self, tab_name, search_command, clear_command, recommend_command):
        """Create a consistent search section for each tab"""
        tab = self.tabView.tab(tab_name)

        # Configure tab grid
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        # Search container with modern styling
        search_container = customtkinter.CTkFrame(
            tab,
            fg_color="transparent",
            corner_radius=10
        )
        search_container.grid(row=0, column=0, pady=20, padx=20, sticky="ew")

        # Search bar with icon
        search_bar = customtkinter.CTkEntry(
            search_container,
            width=500,
            height=40,
            placeholder_text=f"Search {tab_name.lower()}...",
            corner_radius=10,
            font=("Arial", 14)
        )
        search_bar.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        # Search button with icon
        search_button = customtkinter.CTkButton(
            search_container,
            text="Search",
            command=search_command,
            width=100,
            height=40,
            corner_radius=10,
            font=("Arial", 14),
            fg_color="#2CC985",
            hover_color="#207A4A"
        )
        search_button.grid(row=0, column=1, padx=(0, 10))

        # Clear button
        clear_button = customtkinter.CTkButton(
            search_container,
            text="Clear",
            command=clear_command,
            width=80,
            height=40,
            corner_radius=10,
            font=("Arial", 14),
            fg_color="#6C757D",
            hover_color="#495057"
        )
        clear_button.grid(row=0, column=2, padx=(0, 10))

        # Recommend button
        recommend_button = customtkinter.CTkButton(
            search_container,
            text="Similar",
            command=lambda: recommend_command(search_bar.get()),
            width=100,
            height=40,
            corner_radius=10,
            font=("Arial", 14),
            fg_color="#007BFF",
            hover_color="#0056B3"
        )
        recommend_button.grid(row=0, column=3)

        # Make search bar expandable
        search_container.grid_columnconfigure(0, weight=1)

        # Results frame with scrollbar
        results_frame = customtkinter.CTkScrollableFrame(
            tab,
            width=900,
            height=500,
            corner_radius=10
        )
        results_frame.grid(row=1, column=0, padx=20,
                           pady=(0, 20), sticky="nsew")

        # Store references
        if tab_name == "Recipes":
            self.searchBar1 = search_bar
            self.results_frame1 = results_frame
        else:
            self.searchBar2 = search_bar
            self.results_frame2 = results_frame

    def create_chatbot_tab(self):
        """Create the chatbot interface with modern design"""
        chatbot_tab = self.tabView.tab("Chatbot")

        # Configure grid
        chatbot_tab.grid_rowconfigure(1, weight=1)
        chatbot_tab.grid_columnconfigure(0, weight=1)

        # Chat output area with better styling
        self.chat_output = customtkinter.CTkTextbox(
            chatbot_tab,
            height=400,
            width=800,
            corner_radius=10,
            font=("Arial", 14),
            wrap="word",
            fg_color="#F8F9FA",
            text_color="#212529"
        )
        self.chat_output.grid(row=1, column=0, pady=(
            20, 10), padx=20, sticky="nsew")
        self.chat_output.insert(
            "end", "Bot: Hello! I'm your food assistant. Ask me anything about recipes or ingredients.\n\n")
        self.chat_output.configure(state="disabled")

        # Input frame
        input_frame = customtkinter.CTkFrame(
            chatbot_tab,
            fg_color="transparent",
            height=50
        )
        input_frame.grid(row=2, column=0, pady=(0, 20), padx=20, sticky="ew")

        # Chat entry with placeholder
        self.chat_entry = customtkinter.CTkEntry(
            input_frame,
            width=600,
            height=50,
            placeholder_text="Ask something about food...",
            corner_radius=10,
            font=("Arial", 14)
        )
        self.chat_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        # Send button with icon
        send_button = customtkinter.CTkButton(
            input_frame,
            text="Send",
            command=self.handle_chatbot,
            width=100,
            height=50,
            corner_radius=10,
            font=("Arial", 14, "bold"),
            fg_color="#2CC985",
            hover_color="#207A4A"
        )
        send_button.grid(row=0, column=1, padx=(0, 10))

        # Voice input button
        voice_input_button = customtkinter.CTkButton(
            input_frame,
            text="🎤",
            command=self.start_voice_input,
            width=60,
            height=50,
            corner_radius=10,
            font=("Arial", 18),
            fg_color="#6C757D",
            hover_color="#495057"
        )
        voice_input_button.grid(row=0, column=2)

        # Make entry expandable
        input_frame.grid_columnconfigure(0, weight=1)

        # Bind Enter key to send message
        self.chat_entry.bind('<Return>', lambda event: self.handle_chatbot())

    def start_voice_input(self):
        """Start voice input in a separate thread"""
        threading.Thread(target=self.voice_input_thread, daemon=True).start()

    def voice_input_thread(self):
        """Handle voice recognition"""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.update_chat_output(
                "Listening for your question...\n", is_user=False)
            try:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=5)
                user_message = recognizer.recognize_google(audio)
                self.chat_entry.delete(0, "end")
                self.chat_entry.insert(0, user_message)
                self.update_chat_output(
                    f"You said: {user_message}\n", is_user=True)
            except sr.UnknownValueError:
                self.update_chat_output(
                    "Sorry, I didn't catch that.\n", is_user=False)
            except sr.RequestError:
                self.update_chat_output(
                    "Sorry, there was an issue with the speech service.\n", is_user=False)
            except Exception as e:
                self.update_chat_output(f"Error: {str(e)}\n", is_user=False)

    def update_chat_output(self, message, is_user=False):
        """Update chat output with formatted message"""
        self.chat_output.configure(state="normal")
        tag = "user" if is_user else "bot"
        self.chat_output.insert("end", message, tag)
        self.chat_output.tag_config("user", foreground="#007BFF")
        self.chat_output.tag_config("bot", foreground="#28A745")
        self.chat_output.configure(state="disabled")
        self.chat_output.see("end")

    def handle_chatbot(self):
        """Process chatbot input"""
        user_message = self.chat_entry.get().strip()
        if not user_message:
            return

        self.update_chat_output(f"You: {user_message}\n", is_user=True)
        self.chat_entry.delete(0, "end")

        # Process in a separate thread to prevent UI freeze
        threading.Thread(target=self.process_chatbot_message,
                         args=(user_message,), daemon=True).start()

    def process_chatbot_message(self, user_message):
        """Process the user message and generate response"""
        try:
            response = self.process_nlp(user_message)
            self.root.after(0, self.update_chat_output,
                            f"Bot: {response}\n\n", False)
        except Exception as e:
            self.root.after(0, self.update_chat_output,
                            f"Bot: Sorry, an error occurred: {str(e)}\n\n", False)

    def process_nlp(self, user_message):
        """Process natural language query"""
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
        """Display results in a table format with better styling"""
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

        # Create header row
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

        # Create data rows with alternating colors
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
        """Search for recipes"""
        query = self.searchBar1.get()
        self.status_bar.configure(text="Searching recipes...")

        try:
            cursor.execute('''SELECT Recipe_name, Main_Ingredients, 
                                     Calories_per_serving, Protein_g, Fat_g, Carbohydrates_g 
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
        """Search for ingredients"""
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
        """Recommend similar recipes"""
        self.status_bar.configure(text="Finding similar recipes...")

        try:
            cursor.execute(
                "SELECT Recipe_name, Calories_per_serving FROM recipes_nutrition")
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
                query = f'''SELECT Recipe_name, Main_Ingredients, Calories_per_serving, Protein_g, Fat_g, Carbohydrates_g 
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
        """Recommend similar ingredients"""
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
        """Clear recipe results"""
        for widget in self.results_frame1.winfo_children():
            widget.destroy()
        self.status_bar.configure(text="Ready")

    def clear_results2(self):
        """Clear ingredient results"""
        for widget in self.results_frame2.winfo_children():
            widget.destroy()
        self.status_bar.configure(text="Ready")


# Run the app
if __name__ == "__main__":
    root = customtkinter.CTk()
    app = SavourSearchApp(root)
    root.mainloop()
