import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
from datetime import datetime, timedelta
import matplotlib.pyplot as plt




# Password hashing using SHA-256
class Passwordhasher():
    # Hash password for secure storage
    def hash(self, password):
        return hashlib.sha256(password.encode("utf8")).hexdigest()

    # Verify password matches stored hash
    def verify(self, password, storedHash):
        if self.hash(password) == storedHash:
            return True
        return False

# Connect to SQLite database
def connectDatabase():
    return sqlite3.connect("/Users/aadamanwar/Desktop/coursework/fitness tracker database (1).db")

# Create Users table in database if it doesn't exist
def createUserTable():
    conn = connectDatabase()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            passwordHash TEXT NOT NULL,
            name TEXT,
            age INTEGER,
            gender TEXT,
            heightCm REAL,
            initialWeight REAL,
            activityLevel TEXT,
            goal TEXT
        )
    """)
    conn.commit()
    conn.close()

# Main application window
class HealthTrackerApp(tk.Tk):
    def __init__(self, hasher):
        super().__init__()
        self.title("Health & Fitness Tracker")
        self.geometry("600x500")
        self.configure(bg="#e6f2ff")

        self.hasher = hasher
        self.currentUserId = -1  # Store logged-in user's ID

        # Create all pages/screens
        self.pages = {}
        self.pages["AuthMenu"] = AuthMenu(self)
        self.pages["SignUp"] = SignUp(self)
        self.pages["Login"] = Login(self)
        self.pages["MainMenu"] = MainMenu(self)
        self.pages["LogFood"] = LogFood(self)
        self.pages["LogWorkout"] = LogWorkout(self)
        self.pages["ViewStats"] = ViewStats(self)
        self.pages["Settings"] = Settings(self)

        # Grid all pages in same position
        self.pages["AuthMenu"].grid(column=0, row=0, sticky="nesw")
        self.pages["SignUp"].grid(column=0, row=0, sticky="nesw")
        self.pages["Login"].grid(column=0, row=0, sticky="nesw")
        self.pages["MainMenu"].grid(column=0, row=0, sticky="nesw")
        self.pages["LogFood"].grid(column=0, row=0, sticky="nesw")
        self.pages["LogWorkout"].grid(column=0, row=0, sticky="nesw")
        self.pages["ViewStats"].grid(column=0, row=0, sticky="nesw")
        self.pages["Settings"].grid(column=0, row=0, sticky="nesw")
        self.showPage("AuthMenu")

    # Bring specified page to front
    def showPage(self, pageName):
        pageToShow = self.pages[pageName]
        pageToShow.tkraise()

# Initial login/signup screen
class AuthMenu(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        tk.Label(self, text="Welcome to Fitness Tracker", font=("Helvetica", 20, "bold")).pack(pady=30)
        tk.Button(self, text="Login", width=25, height=2, command=lambda: container.showPage("Login")).pack(pady=10)
        tk.Button(self, text="Sign Up", width=25, height=2, command=lambda: container.showPage("SignUp")).pack(pady=10)

# User registration screen
class SignUp(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.container = container

        # Create input fields for user details
        self.usernameLabel = tk.Label(self, text="Username")
        self.usernameLabel.pack()
        self.usernameEntry = tk.Entry(self)
        self.usernameEntry.pack()
        self.passwordLabel = tk.Label(self, text="Password")
        self.passwordLabel.pack()
        self.passwordEntry = tk.Entry(self)
        self.passwordEntry.pack()
        self.passwordEntry.config(show="*")  # Hide password text
        self.nameLabel = tk.Label(self, text="Name")
        self.nameLabel.pack()
        self.nameEntry = tk.Entry(self)
        self.nameEntry.pack()
        self.ageLabel = tk.Label(self, text="Age")
        self.ageLabel.pack()
        self.ageEntry = tk.Entry(self)
        self.ageEntry.pack()
        self.genderLabel = tk.Label(self, text="Gender")
        self.genderLabel.pack()
        self.genderEntry = tk.Entry(self)
        self.genderEntry.pack()
        self.heightLabel = tk.Label(self, text="Height (cm)")
        self.heightLabel.pack()
        self.heightEntry = tk.Entry(self)
        self.heightEntry.pack()
        self.weightLabel = tk.Label(self, text="Weight (kg)")
        self.weightLabel.pack()
        self.weightEntry = tk.Entry(self)
        self.weightEntry.pack()
        self.activityLabel = tk.Label(self, text="Activity Level (Sedentary, Light, Moderate, Active, Very Active)")
        self.activityLabel.pack()
        self.activityEntry = tk.Entry(self)
        self.activityEntry.pack()
        self.goalweightLabel = tk.Label(self, text="Goal weight (kg)")
        self.goalweightLabel.pack()
        self.goalweightEntry = tk.Entry(self)
        self.goalweightEntry.pack()
        self.weeksLabel = tk.Label(self, text="the number of weeks you want to take to reach your goal weight within")
        self.weeksLabel.pack()
        self.weeksEntry = tk.Entry(self)
        self.weeksEntry.pack()
        self.submitButton = tk.Button(self, text="Sign Up", command=lambda: self.register()).pack(pady=10)

    # Create new user account in database
    def register(self):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        hashed = self.container.hasher.hash(password)  # Hash password for security

        name = self.nameEntry.get()
        
        # Validate numeric inputs
        ageStr = self.ageEntry.get()
        heightStr = self.heightEntry.get()
        weightStr = self.weightEntry.get()
        goalweightStr = self.goalweightEntry.get()
        weeksStr = self.weeksEntry.get()
        
        if ageStr.isdigit():
            age = int(ageStr)
        else:
            messagebox.showerror("Error", "Please enter valid age.")
            return
            
        if self.isValidFloat(heightStr):
            height = float(heightStr)
        else:
            messagebox.showerror("Error", "Please enter valid height.")
            return
            
        if self.isValidFloat(weightStr):
            weight = float(weightStr)
        else:
            messagebox.showerror("Error", "Please enter valid weight.")
            return
            
        if self.isValidFloat(goalweightStr):
            goalweight = float(goalweightStr)
        else:
            messagebox.showerror("Error", "Please enter valid goal weight.")
            return
            
        if weeksStr.isdigit():
            weeks = int(weeksStr)
        else:
            messagebox.showerror("Error", "Please enter valid weeks.")
            return

        gender = self.genderEntry.get().upper()
        activity = self.activityEntry.get().upper()

        # Calculate BMI and daily calorie target
        userbmi = weight / ((height / 100) ** 2)
        dailycalories = self.calculatedailycalories(weight, goalweight, height, age, gender, activity, weeks)

        # Check if username already exists in database
        conn = connectDatabase()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM Users WHERE username = ?", (username,))
        existing = cursor.fetchone()

        if existing:
            conn.close()
            messagebox.showerror("Error", "Username already exists.")
            return
        
        # Insert new user into database
        cursor.execute("""
            INSERT INTO Users (
                username, passwordHash, name, age, gender, heightCm, initialWeight,
                activityLevel, bmi, dailycalories, goalweight
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            username, hashed, name, age, gender, height, weight,
            activity, userbmi, dailycalories, goalweight
        ))
        conn.commit()
        conn.close()
        self.container.showPage("MainMenu")
    
    # Check if string is valid decimal number
    def isValidFloat(self, value):
        dotCount = 0
        for char in value:
            if char == '.':
                dotCount = dotCount + 1
            elif char.isdigit():
                continue
            else:
                return False
        if dotCount > 1:
            return False
        return True

    # Calculate daily calorie target based on TDEE and weight goal
    def calculatedailycalories(self, weight, goalweight, height, age, gender, activity, weeks):
        # Calculate BMR using Mifflin-St Jeor equation
        if gender.upper() == 'MALE':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161

        # Multiply BMR by activity level to get TDEE
        activity_levels = {
            'SEDENTARY': 1.2,
            'LIGHT': 1.375,
            'MODERATE': 1.55,
            'ACTIVE': 1.725,
            'VERY ACTIVE': 1.9
        }
        tdee = bmr * activity_levels.get(activity.upper(), 1.2)

        # Calculate daily calorie adjustment to reach goal
        weight_change = goalweight - weight
        kcal_change = weight_change * 7700  # 7700 kcal per kg
        daily_adjustment = kcal_change / (weeks * 7)

        dailycalories = tdee + daily_adjustment

        # Minimum 1200 calories for health
        if dailycalories < 1200:
            return 1200
        return dailycalories

# Login screen
class Login(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.container = container

        self.usernameLabel = tk.Label(self, text="Username")
        self.usernameLabel.pack()
        self.usernameEntry = tk.Entry(self)
        self.usernameEntry.pack()
        self.passwordLabel = tk.Label(self, text="Password")
        self.passwordLabel.pack()
        self.passwordEntry = tk.Entry(self)
        self.passwordEntry.pack()
        self.passwordEntry.config(show="*")
        self.submitButton = tk.Button(self, text="Login", command=lambda: self.login()).pack(pady=10)

    # Verify credentials and log user in
    def login(self):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        
        # Fetch user from database
        conn = connectDatabase()
        cursor = conn.cursor()
        cursor.execute("SELECT id, passwordHash FROM Users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result:
            # Verify password hash matches
            if self.container.hasher.verify(password, result[1]):
                self.container.currentUserId = result[0]
                self.container.showPage("MainMenu")
                return
        
        messagebox.showerror("Error", "Invalid credentials")

# Main navigation menu
class MainMenu(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.container = container

        self.title = tk.Label(self, text="Main Menu", font=("Helvetica", 20, "bold"))
        self.title.pack(pady=30)

        self.foodButton = tk.Button(self, text="Log Food", width=25, height=2, command=lambda: self.container.showPage("LogFood"))
        self.foodButton.pack(pady=30)
        self.workoutButton = tk.Button(self, text="Log Workout", width=25, height=2, command=lambda: self.container.showPage("LogWorkout"))
        self.workoutButton.pack(pady=30)
        self.statsButton = tk.Button(self, text="View Stats", width=25, height=2, command=lambda: self.showStats())
        self.statsButton.pack(pady=30)
        self.settingsButton = tk.Button(self, text="Settings", width=25, height=2, command=lambda: self.container.showPage("Settings"))
        self.settingsButton.pack(pady=30)
        self.exitButton = tk.Button(self, text="Exit", width=25, height=2, command=lambda: self.container.destroy())
        self.exitButton.pack(pady=30)

    # Load stats before showing stats page
    def showStats(self):
        self.container.pages["ViewStats"].getStats()
        self.container.showPage("ViewStats")

# Stack data structure for undo functionality
class Stack:
    def __init__(self):
        self.items = []
    
    # Add item to top of stack
    def push(self, item):
        self.items.append(item)
    
    # Remove and return top item
    def pop(self):
        if len(self.items) == 0:
            return None
        return self.items.pop()
    
    # View top item without removing
    def peek(self):
        if len(self.items) == 0:
            return None
        return self.items[-1]
    
    # Check if stack is empty
    def isEmpty(self):
        if len(self.items) == 0:
            return True
        return False
    
    # Get number of items in stack
    def size(self):
        return len(self.items)


# Food logging screen
class LogFood(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.container = container
        self.mealStack = Stack()  # Track meal entries for undo

        # Daily summary display
        self.dailymacrosHeader = tk.Label(self, text="Calories & Macronutrients")
        self.dailymacrosHeader.pack(pady=(20, 5))
        self.dailymacroslistbox = tk.Listbox(self, width=40, height=6)
        self.dailymacroslistbox.pack(padx=80, pady=(0, 30))

        # Food search input
        self.searchfoodLabel = tk.Label(self, text="Search Food:")
        self.searchfoodLabel.pack(pady=(0, 5))
        self.searchfoodEntry = tk.Entry(self)
        self.searchfoodEntry.pack()
        self.submitfoodButton = tk.Button(self, text="search", command=lambda: self.searchfood())
        self.submitfoodButton.pack(pady=(10, 30))

        # Search results display
        self.foodsearchHeader = tk.Label(self, text="Food Search Results")
        self.foodsearchHeader.pack(pady=(0, 5))
        self.foodsearchlistbox = tk.Listbox(self, width=40, height=5)
        self.foodsearchlistbox.pack(padx=80, pady=(0, 20))

        # Buttons to log food to different meals
        self.logfoodBreakfastButton = tk.Button(self, text="Log Food for Breakfast", command=lambda: self.logselectedfood("Breakfast"))
        self.logfoodBreakfastButton.pack(padx=40, pady=(0, 10))
        self.logfoodLunchButton = tk.Button(self, text="Log Food for Lunch", command=lambda: self.logselectedfood("Lunch"))
        self.logfoodLunchButton.pack(padx=40, pady=(0, 10))
        self.logfoodDinnerButton = tk.Button(self, text="Log Food for Dinner", command=lambda: self.logselectedfood("Dinner"))
        self.logfoodDinnerButton.pack(padx=40, pady=(0, 10))
        
        # Undo last logged meal
        self.undoButton = tk.Button(self, text="Undo Last Entry", command=lambda: self.undolastmealentry())
        self.undoButton.pack(padx=40, pady=(10, 20))

        # Display logged meals
        self.breakfastHeader = tk.Label(self, text="Breakfast")
        self.breakfastHeader.pack(pady=(0, 5))
        self.breakfastlistbox = tk.Listbox(self, width=40, height=5)
        self.breakfastlistbox.pack(padx=40, pady=(0, 25))

        self.lunchHeader = tk.Label(self, text="Lunch")
        self.lunchHeader.pack(pady=(0, 5))
        self.lunchlistbox = tk.Listbox(self, width=40, height=5)
        self.lunchlistbox.pack(padx=40, pady=(0, 25))

        self.dinnerHeader = tk.Label(self, text="Dinner")
        self.dinnerHeader.pack(pady=(0, 5))
        self.dinnerlistbox = tk.Listbox(self, width=40, height=5)
        self.dinnerlistbox.pack(padx=40, pady=(0, 30))

        self.backButton = tk.Button(self, text="Back to Main Menu", command=lambda: self.container.showPage("MainMenu"))
        self.backButton.pack(padx=40, pady=(0, 20))

    # Refresh meals when page is shown
    def tkraise(self):
        super().tkraise()
        self.loadTodaysMeals()
        self.updateDailyMacros()
    
    # Binary search to find food in sorted list
    def binarySearch(self, foodList, searchTerm):
        left = 0
        right = len(foodList) - 1
        results = []
        
        while left <= right:
            mid = (left + right) // 2
            midFood = foodList[mid][0]
            
            if searchTerm == midFood:
                results.append(foodList[mid])
                return results
            elif searchTerm < midFood:
                right = mid - 1
            else:
                left = mid + 1
        
        return results

    # Search for food in database using binary search
    def searchfood(self):
        searchedfood = self.searchfoodEntry.get().upper()
        
        # Fetch all foods sorted by name from database
        conn = connectDatabase()
        cursor = conn.cursor()
        cursor.execute("SELECT name, calories, protein, carbs, fat FROM Food ORDER BY name")
        allFoods = cursor.fetchall()
        conn.close()
        
        # Binary search through sorted food list
        results = self.binarySearch(allFoods, searchedfood)
        
        # Display search results
        self.foodsearchlistbox.delete(0, tk.END)

        if len(results) == 0:
            self.foodsearchlistbox.insert(tk.END, "No foods found. Try a different search.")
            return
            
        for food in results:
            displayText = "NAME: " + str(food[0]) + "  CALORIES: " + str(food[1]) + "  P: " + str(food[2]) + "g  C: " + str(food[3]) + "g  F: " + str(food[4]) + "g"
            self.foodsearchlistbox.insert(tk.END, displayText)

    # Log selected food to specified meal in database
    def logselectedfood(self, meal):
        selection = self.foodsearchlistbox.curselection()
        if len(selection) == 0:
            return

        index = selection[0]
        selectedfood = self.foodsearchlistbox.get(index)

        if "NAME: " in selectedfood:
            foodName = selectedfood.split("  ")[0].replace("NAME: ", "").strip()

            # Get food details from database
            conn = connectDatabase()
            cursor = conn.cursor()
            cursor.execute("SELECT foodId, calories, protein, carbs, fat FROM Food WHERE name = ?", (foodName,))
            foodData = cursor.fetchone()

            if foodData:
                foodId = foodData[0]
                calories = foodData[1]
                protein = foodData[2]
                carbs = foodData[3]
                fat = foodData[4]
                
                todayDate = datetime.now().strftime("%Y-%m-%d")
                quantity = 1.0
                totalCal = calories * quantity
                totalProtein = protein * quantity
                totalCarbs = carbs * quantity
                totalFat = fat * quantity
                mealType = meal.lower()

                # Insert meal log into database
                cursor.execute("""
                    INSERT INTO MealLogs (userId, date, mealType, foodId, quantity, totalCal, totalProtein, totalCarbs, totalFat)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    self.container.currentUserId,
                    todayDate,
                    mealType,
                    foodId,
                    quantity,
                    totalCal,
                    totalProtein,
                    totalCarbs,
                    totalFat
                ))
                conn.commit()
                
                # Add to undo stack
                self.mealStack.push(cursor.lastrowid)
                
                conn.close()

                self.loadTodaysMeals()
                self.updateDailyMacros()
                return
                
            conn.close()
    
    # Undo last meal entry using stack
    def undolastmealentry(self):
        if self.mealStack.isEmpty() == False:
            lastMealId = self.mealStack.pop()
            
            # Delete meal from database
            conn = connectDatabase()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM MealLogs WHERE logId = ?", (lastMealId,))
            conn.commit()
            conn.close()
            
            self.loadTodaysMeals()
            self.updateDailyMacros()

    # Load today's logged meals from database
    def loadTodaysMeals(self):
        todayDate = datetime.now().strftime("%Y-%m-%d")

        # Clear existing displays
        self.breakfastlistbox.delete(0, tk.END)
        self.lunchlistbox.delete(0, tk.END)
        self.dinnerlistbox.delete(0, tk.END)

        # Fetch today's meals from database
        conn = connectDatabase()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT m.mealType, f.name, m.totalCal, m.totalProtein, m.totalCarbs, m.totalFat
            FROM MealLogs m
            JOIN Food f ON m.foodId = f.foodId
            WHERE m.userId = ? AND m.date = ?
            ORDER BY m.logId
        """, (self.container.currentUserId, todayDate))

        meals = cursor.fetchall()
        conn.close()

        # Display meals in appropriate listbox
        for meal in meals:
            mealType = meal[0]
            foodName = meal[1]
            totalCal = meal[2]
            totalProtein = meal[3]
            totalCarbs = meal[4]
            totalFat = meal[5]
            
            displayText = str(foodName) + "  " + str(round(totalCal, 0)) + " cal  P: " + str(round(totalProtein, 1)) + "g  C: " + str(round(totalCarbs, 1)) + "g  F: " + str(round(totalFat, 1)) + "g"

            if mealType == "breakfast":
                self.breakfastlistbox.insert(tk.END, displayText)
            if mealType == "lunch":
                self.lunchlistbox.insert(tk.END, displayText)
            if mealType == "dinner":
                self.dinnerlistbox.insert(tk.END, displayText)

    # Update daily calorie and macro totals display
    def updateDailyMacros(self):
        todayDate = datetime.now().strftime("%Y-%m-%d")

        # Get user's daily calorie target from database
        conn = connectDatabase()
        cursor = conn.cursor()

        cursor.execute("SELECT dailycalories FROM Users WHERE id = ?", (self.container.currentUserId,))
        userResult = cursor.fetchone()
        if userResult:
            if userResult[0]:
                dailycalories = userResult[0]
            else:
                dailycalories = 2000
        else:
            dailycalories = 2000

        # Sum today's totals from database
        cursor.execute("""
            SELECT
                SUM(totalCal) as totalCalories,
                SUM(totalProtein) as totalProtein,
                SUM(totalCarbs) as totalCarbs,
                SUM(totalFat) as totalFat
            FROM MealLogs
            WHERE userId = ? AND date = ?
        """, (self.container.currentUserId, todayDate))

        totals = cursor.fetchone()
        conn.close()

        if totals[0] is None:
            totalCalories = 0
            totalProtein = 0
            totalCarbs = 0
            totalFat = 0
        else:
            totalCalories = int(totals[0])
            totalProtein = int(totals[1])
            totalCarbs = int(totals[2])
            totalFat = int(totals[3])

        caloriesRemaining = int(dailycalories - totalCalories)

        # Display summary
        self.dailymacroslistbox.delete(0, tk.END)
        self.dailymacroslistbox.insert(tk.END, "Date: " + todayDate)
        self.dailymacroslistbox.insert(tk.END, "Total Calories: " + str(totalCalories) + " cal")
        self.dailymacroslistbox.insert(tk.END, "Calories Remaining: " + str(caloriesRemaining) + " cal")
        self.dailymacroslistbox.insert(tk.END, "Protein: " + str(totalProtein) + "g")
        self.dailymacroslistbox.insert(tk.END, "Carbs: " + str(totalCarbs) + "g")
        self.dailymacroslistbox.insert(tk.END, "Fat: " + str(totalFat) + "g")

# Workout logging screen
class LogWorkout(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.container = container

        self.titleLabel = tk.Label(self, text="Log Workout")
        self.titleLabel.pack(pady=10)

        # Today's workout summary
        self.workoutSummaryHeader = tk.Label(self, text="Today's Workout Summary")
        self.workoutSummaryHeader.pack()
        self.workoutSummaryListbox = tk.Listbox(self, width=40, height=5)
        self.workoutSummaryListbox.pack(padx=80, pady=10)

        # Input fields for new workout
        self.workoutTypeLabel = tk.Label(self, text="Workout Type (e.g., Running, Cycling, Gym):")
        self.workoutTypeLabel.pack()
        self.workoutTypeEntry = tk.Entry(self, width=30)
        self.workoutTypeEntry.pack(pady=5)

        self.durationLabel = tk.Label(self, text="Duration (minutes):")
        self.durationLabel.pack()
        self.durationEntry = tk.Entry(self, width=30)
        self.durationEntry.pack(pady=5)

        self.caloriesLabel = tk.Label(self, text="Calories Burned:")
        self.caloriesLabel.pack()
        self.caloriesEntry = tk.Entry(self, width=30)
        self.caloriesEntry.pack(pady=5)

        self.logButton = tk.Button(self, text="Log Workout", command=lambda: self.logWorkout())
        self.logButton.pack(pady=10)

        # Today's logged workouts
        self.todaysWorkoutsHeader = tk.Label(self, text="Today's Workouts")
        self.todaysWorkoutsHeader.pack(pady=10)
        self.todaysWorkoutsListbox = tk.Listbox(self, width=60, height=8)
        self.todaysWorkoutsListbox.pack(padx=40, pady=10)

        self.deleteButton = tk.Button(self, text="Delete Selected Workout", command=lambda: self.deleteWorkout())
        self.deleteButton.pack(pady=5)

        self.backButton = tk.Button(self, text="Back to Main Menu", command=lambda: self.container.showPage("MainMenu"))
        self.backButton.pack(padx=40, pady=10)

    # Refresh workouts when page is shown
    def tkraise(self):
        super().tkraise()
        self.loadTodaysWorkouts()
        self.updateWorkoutSummary()

    # Save workout to database
    def logWorkout(self):
        workoutType = self.workoutTypeEntry.get().strip()
        durationStr = self.durationEntry.get().strip()
        caloriesStr = self.caloriesEntry.get().strip()

        # Validate inputs
        if len(workoutType) == 0:
            return
        if len(durationStr) == 0:
            return
        if len(caloriesStr) == 0:
            return
       
        if durationStr.isdigit():
            duration = int(durationStr)
        else:
            messagebox.showerror("Error", "Please enter valid numeric values for duration")
            return

        # Validate calories is a digit
        if caloriesStr.isdigit():
           caloriesBurned = int(caloriesStr)
        else:
            messagebox.showerror("Error", "Please enter valid numeric values for calories")
            return

        # Validate positive values
        if duration <= 0:
            messagebox.showerror("Error", "Duration must be a positive number")
            return
            
        if caloriesBurned <= 0:
            messagebox.showerror("Error", "Calories must be a positive number")
            return
        todayDate = datetime.now().strftime("%Y-%m-%d")

        # Insert workout into database
        conn = connectDatabase()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO WorkoutLogs (userId, date, workoutType, durationMin, caloriesBurned)
            VALUES (?, ?, ?, ?, ?)
        """, (
            self.container.currentUserId,
            todayDate,
            workoutType,
            duration,
            caloriesBurned
        ))
        conn.commit()
        conn.close()

        # Clear input fields
        self.workoutTypeEntry.delete(0, tk.END)
        self.durationEntry.delete(0, tk.END)
        self.caloriesEntry.delete(0, tk.END)

        self.loadTodaysWorkouts()
        self.updateWorkoutSummary()

    # Load today's workouts from database
    def loadTodaysWorkouts(self):
        todayDate = datetime.now().strftime("%Y-%m-%d")

        self.todaysWorkoutsListbox.delete(0, tk.END)

        # Fetch workouts from database
        conn = connectDatabase()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT logId, workoutType, durationMin, caloriesBurned
            FROM WorkoutLogs
            WHERE userId = ? AND date = ?
            ORDER BY logId
        """, (self.container.currentUserId, todayDate))

        workouts = cursor.fetchall()
        conn.close()

        if len(workouts) == 0:
            self.todaysWorkoutsListbox.insert(tk.END, "No workouts logged today")
            return
        
        # Display workouts
        for workout in workouts:
            logId = workout[0]
            workoutType = workout[1]
            duration = workout[2]
            calories = workout[3]
            displayText = str(workoutType) + "  " + str(duration) + " min   " + str(calories) + " cal burned [ID: " + str(logId) + "]"
            self.todaysWorkoutsListbox.insert(tk.END, displayText)

    # Calculate and display workout summary
    def updateWorkoutSummary(self):
        todayDate = datetime.now().strftime("%Y-%m-%d")

        # Sum workout totals from database
        conn = connectDatabase()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                SUM(durationMin) as totalDuration,
                SUM(caloriesBurned) as totalCalories,
                COUNT(*) as workoutCount
            FROM WorkoutLogs
            WHERE userId = ? AND date = ?
        """, (self.container.currentUserId, todayDate))

        totals = cursor.fetchone()
        conn.close()

        if totals[0] is None:
            totalDuration = 0
            totalCalories = 0
            workoutCount = 0
        else:
            totalDuration = int(totals[0])
            totalCalories = int(totals[1])
            workoutCount = int(totals[2])

        # Display summary
        self.workoutSummaryListbox.delete(0, tk.END)
        self.workoutSummaryListbox.insert(tk.END, "Date: " + str(todayDate))
        self.workoutSummaryListbox.insert(tk.END, "Total Workouts: " + str(workoutCount))
        self.workoutSummaryListbox.insert(tk.END, "Total Duration: " + str(totalDuration) + " min")
        self.workoutSummaryListbox.insert(tk.END, "Total Calories Burned: " + str(totalCalories) + " cal")

    # Delete selected workout from database
    def deleteWorkout(self):
        selection = self.todaysWorkoutsListbox.curselection()

        if len(selection) == 0:
            return

        index = selection[0]
        selectedItem = self.todaysWorkoutsListbox.get(index)

        # Extract workout ID from display text
        if "[ID: " in selectedItem:
            logIdStr = selectedItem.split("[ID: ")[1].split("]")[0]
            logId = int(logIdStr)

            # Delete from database
            conn = connectDatabase()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM WorkoutLogs WHERE logId = ? AND userId = ?", (logId, self.container.currentUserId))
            conn.commit()
            conn.close()

            self.loadTodaysWorkouts()
            self.updateWorkoutSummary()

# Statistics and graphs screen
class ViewStats(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.container = container

    # Load and display user stats
    def getStats(self):
        # Fetch user stats from database
        conn = connectDatabase()
        cursor = conn.cursor()
        cursor.execute("SELECT name, initialWeight, heightCm, bmi FROM users WHERE id = ?", [str(self.container.currentUserId)])

        stats = cursor.fetchall()
        conn.close()

        # Display basic stats
        todolist = tk.Listbox(self, width=70, height=20, font=("Arial", 12))
        todolist.grid(row=0, column=0, padx=20, pady=20)

        for stat in stats:
            todolist.insert(tk.END, "Name: " + str(stat[0]) + " | Weight: " + str(stat[1]) + "kg | Height: " + str(stat[2]) + "m | BMI: " + str(stat[3]))
        
        # Buttons to show different graphs
        graphButton1 = tk.Button(self, text="Calorie Intake (Last 7 Days)", width=30, command=lambda: self.showCalorieGraph())
        graphButton1.grid(row=1, column=0, pady=5)
        
        graphButton2 = tk.Button(self, text="Workout Minutes (Last 7 Days)", width=30, command=lambda: self.showWorkoutGraph())
        graphButton2.grid(row=2, column=0, pady=5)
        
        graphButton3 = tk.Button(self, text="Macronutrient Breakdown (Today)", width=30, command=lambda: self.showMacroGraph())
        graphButton3.grid(row=3, column=0, pady=5)
        
        backButton = tk.Button(self, text="Back to Main Menu", command=lambda: self.container.showPage("MainMenu"))
        backButton.grid(row=4, column=0, pady=10)

    # Display bar chart of last 7 days calorie intake
    def showCalorieGraph(self):
        conn = connectDatabase()
        cursor = conn.cursor()
        
        dates = []
        calories = []
        
        # Get data for each of last 7 days
        for i in range(7):
            date = (datetime.now() - timedelta(days=6 - i)).strftime("%Y-%m-%d")
            dates.append(date[-5:])  # Format as MM-DD
            
            # Sum calories from database for each day
            cursor.execute("""
                SELECT SUM(totalCal) FROM MealLogs 
                WHERE userId = ? AND date = ?
            """, (self.container.currentUserId, date))
            
            result = cursor.fetchone()
            if result[0]:
                calories.append(result[0])
            else:
                calories.append(0)
        
        conn.close()
        
        # Create bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(dates, calories, color='#4CAF50')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Calories', fontsize=12)
        plt.title('Calorie Intake over the last 7 Days', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    # Display bar chart of last 7 days workout minutes
    def showWorkoutGraph(self):
        conn = connectDatabase()
        cursor = conn.cursor()
        
        dates = []
        minutes = []
        
        # Get data for each of last 7 days
        for i in range(7):
            date = (datetime.now() - timedelta(days=6 - i)).strftime("%Y-%m-%d")
            dates.append(date[-5:])
       
            # Sum workout duration from database for each day
            cursor.execute("""
                SELECT SUM(durationMin) FROM WorkoutLogs 
                WHERE userId = ? AND date = ?
            """, (self.container.currentUserId, date))
            
            result = cursor.fetchone()
            if result[0]:
                minutes.append(result[0])
            else:
                minutes.append(0)
        
        conn.close()
        
        # Create bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(dates, minutes, color='#2196F3')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Minutes', fontsize=12)
        plt.title('Workout Duration over the Last 7 Days', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    # Display pie chart of today's macronutrient breakdown
    def showMacroGraph(self):
        conn = connectDatabase()
        cursor = conn.cursor()
        
        todayDate = datetime.now().strftime("%Y-%m-%d")
        
        # Get today's macro totals from database
        cursor.execute("""
            SELECT SUM(totalProtein), SUM(totalCarbs), SUM(totalFat)
            FROM MealLogs
            WHERE userId = ? AND date = ?
        """, (self.container.currentUserId, todayDate))
        
        result = cursor.fetchone()
        conn.close()
        
        # Don't show graph if no data
        if result[0] is None:
            return
        if result[0] == 0 and result[1] == 0 and result[2] == 0:
            return
        
        if result[0]:
            protein = result[0]
        else:
            protein = 0
            
        if result[1]:
            carbs = result[1]
        else:
            carbs = 0
            
        if result[2]:
            fat = result[2]
        else:
            fat = 0
        
        # Create pie chart
        labels = ['Protein', 'Carbs', 'Fat']
        sizes = [protein, carbs, fat]
        colors = ['#FF6B6B', '#4ECDC4', '#FFE66D']
        explode = (0.05, 0.05, 0.05)
        
        plt.figure(figsize=(8, 8))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', 
                shadow=True, startangle=90, textprops={'fontsize': 12})
        plt.title('Macronutrient Breakdown - ' + str(todayDate), fontsize=14, fontweight='bold')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()


# Settings screen for updating user data
class Settings(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.container = container

        tk.Label(self, text="Settings", font=("Helvetica", 18, "bold")).pack(pady=20)

        # Input fields for updating weight goals
        tk.Label(self, text="Update Current Weight (kg):").pack(pady=5)
        self.weightEntry = tk.Entry(self, width=30)
        self.weightEntry.pack(pady=5)

        tk.Label(self, text="Update Goal Weight (kg):").pack(pady=5)
        self.goalWeightEntry = tk.Entry(self, width=30)
        self.goalWeightEntry.pack(pady=5)

        tk.Button(self, text="Save Changes", width=20, command=self.updateSettings).pack(pady=20)

        # Password change section
        tk.Label(self, text="Change Password", font=("Helvetica", 12, "bold")).pack(pady=15)

        tk.Label(self, text="New Password:").pack(pady=5)
        self.newPasswordEntry = tk.Entry(self, width=30, show="*")
        self.newPasswordEntry.pack(pady=5)

        tk.Button(self, text="Update Password", width=20, command=self.changePassword).pack(pady=15)

        tk.Button(self, text="Back to Main Menu", command=lambda: self.container.showPage("MainMenu")).pack(pady=10)

    # Update user weight and recalculate BMI and daily calories
    def updateSettings(self):
        weightStr = self.weightEntry.get().strip()
        goalWeightStr = self.goalWeightEntry.get().strip()

        if len(weightStr) == 0 and len(goalWeightStr) == 0:
            return

        # Get current user data from database
        conn = connectDatabase()
        cursor = conn.cursor()

        cursor.execute("SELECT initialWeight, goalweight, heightCm, age, gender, activityLevel FROM Users WHERE id = ?", (self.container.currentUserId,))
        userData = cursor.fetchone()
        
        currentWeight = userData[0]
        currentGoalWeight = userData[1]
        height = userData[2]
        age = userData[3]
        gender = userData[4]
        activity = userData[5]

        # Update weight if provided
        if len(weightStr) > 0:
            if self.isValidFloat(weightStr):
                currentWeight = float(weightStr)
                cursor.execute("UPDATE Users SET initialWeight = ? WHERE id = ?", (currentWeight, self.container.currentUserId))
            else:
                conn.close()
                messagebox.showerror("Error", "Please enter valid weight")
                return

        # Update goal weight if provided
        if len(goalWeightStr) > 0:
            if self.isValidFloat(goalWeightStr):
                currentGoalWeight = float(goalWeightStr)
                cursor.execute("UPDATE Users SET goalweight = ? WHERE id = ?", (currentGoalWeight, self.container.currentUserId))
            else:
                conn.close()
                messagebox.showerror("Error", "Please enter valid goal weight")
                return

        # Recalculate BMI with new weight
        newBMI = currentWeight / ((height / 100) ** 2)
        cursor.execute("UPDATE Users SET bmi = ? WHERE id = ?", (newBMI, self.container.currentUserId))

        # Recalculate daily calorie target
        if gender.upper() == 'MALE':
            bmr = 10 * currentWeight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * currentWeight + 6.25 * height - 5 * age - 161

        activity_levels = {
            'SEDENTARY': 1.2,
            'LIGHT': 1.375,
            'MODERATE': 1.55,
            'ACTIVE': 1.725,
            'VERY ACTIVE': 1.9
        }
        tdee = bmr * activity_levels.get(activity.upper(), 1.2)

        weight_change = currentGoalWeight - currentWeight
        kcal_change = weight_change * 7700
        weeks = 12
        daily_adjustment = kcal_change / (weeks * 7)

        dailycalories = tdee + daily_adjustment

        if dailycalories < 1200:
            dailycalories = 1200

        # Update daily calories in database
        cursor.execute("UPDATE Users SET dailycalories = ? WHERE id = ?", (dailycalories, self.container.currentUserId))

        conn.commit()
        conn.close()

        # Clear input fields
        self.weightEntry.delete(0, tk.END)
        self.goalWeightEntry.delete(0, tk.END)
    
    # Check if string is valid decimal number
    def isValidFloat(self, value):
        dotCount = 0
        for char in value:
            if char == '.':
                dotCount = dotCount + 1
            elif char.isdigit():
                continue
            else:
                return False
        if dotCount > 1:
            return False
        return True
    
    # Update password in database
    def changePassword(self):
        newpassword = self.newPasswordEntry.get()
        hashed = self.container.hasher.hash(newpassword)  # Hash new password

        # Update password hash in database
        conn = connectDatabase()
        cursor = conn.cursor()
        cursor.execute("UPDATE Users SET passwordHash = ? WHERE id = ?", (hashed, self.container.currentUserId))
        conn.commit()
        conn.close()

        self.newPasswordEntry.delete(0, tk.END)

        self.newPasswordEntry.delete(0, tk.END)

# Run the application
if __name__ == "__main__":
    hasher = Passwordhasher()
    app = HealthTrackerApp(hasher)
    app.mainloop()