# Health & Fitness Tracking Application

**A Python-based desktop application integrating nutrition tracking, workout logging, relational database management, and interactive data visualisation.**

**Technologies:** Python · SQLite · Tkinter · Matplotlib

---

## Project Overview

Developed a modular desktop application to help users monitor their nutritional intake, physical activity, and progress towards personal fitness goals.

The application combines automated health calculations, structured data storage, efficient searching algorithms, and graphical data visualisation within a user-friendly interface.

The project was developed through a complete iterative software development lifecycle, incorporating stakeholder research, system architecture, algorithm design, database development, implementation, testing, and evaluation.

### Key Project Highlights

- Developed an integrated Python application with five core functional modules.
- Designed a relational SQLite database with referential integrity and support for multiple users.
- Implemented a binary search algorithm with **O(log n)** time complexity for efficient food retrieval.
- Incorporated password hashing, automated health calculations, and interactive visualisations.
- Conducted stakeholder interviews, iterative testing, and usability evaluations.
- **Fully achieved 43 of 45 predefined success criteria**, with the remaining two partially achieved.

---

## Core Features

### 1. User Authentication & Account Management

- User registration and login functionality.
- Password hashing using SHA-256.
- Persistent storage of user account information using SQLite.
- User profile management and settings.
- Personalised health calculations based on user information and activity levels.

### 2. Nutrition & Calorie Tracking

- Search for food items within a structured nutritional database.
- Record daily food consumption and nutritional intake.
- Track calories and macronutrients, including protein, carbohydrates, and fats.
- Organise food consumption by meal.
- Automatically calculate daily nutritional totals.
- Compare recorded calorie intake against personalised daily targets.

### 3. Workout Tracking

- Record physical activities and workout sessions.
- Store exercise information within the relational database.
- Track workout duration and estimated calories burned.
- Review previously recorded fitness activities.

### 4. Statistics & Data Visualisation

- Generate visual representations of recorded nutritional and fitness data.
- Use Matplotlib to display trends and progress.
- Retrieve historical information from the database.
- Present health and fitness statistics through an integrated Tkinter interface.

### 5. User Settings

- Update personal information and fitness goals.
- Recalculate personalised calorie requirements.
- Manage account information.
- Maintain consistent user data across application modules.

---

## Technical Architecture

### Programming & Application Design

The application was developed using Python, with a modular, object-oriented architecture separating major functionality into distinct classes.

Key components include:

| Component | Responsibility |
|---|---|
| Authentication | Registration, login, and password handling |
| Food Logging | Nutritional database searching and meal tracking |
| Workout Logging | Recording and managing exercise data |
| Statistics | Retrieving, processing, and visualising data |
| Settings | Managing user information and health targets |

The architecture was designed to improve maintainability, reduce unnecessary code duplication, and support incremental development.

### Database Design — SQLite

Designed and implemented a relational database to manage user accounts, nutritional information, and workout records.

Key design considerations included:

- Database normalisation to Second Normal Form (2NF).
- Primary and foreign keys to establish relationships between tables.
- Referential integrity to maintain data consistency.
- Support for multiple user accounts.
- Persistent storage and retrieval of application data.

The database architecture was planned using entity-relationship diagrams and SQL table definitions.

### Algorithm Optimisation — Binary Search

Implemented a binary search algorithm for exact-match food retrieval from sorted data.

**Time Complexity: O(log n)**

For a dataset containing 100,000 sorted records:

| Search Method | Theoretical Worst-Case Comparisons |
|---|---:|
| Linear Search | 100,000 |
| Binary Search | Approximately 17 |

This demonstrates the use of algorithmic thinking to reduce the number of comparisons required for searching.

Binary search requires sorted input and exact matching. Partial-match searching was identified as an opportunity for future development.

### Data Structures

Implemented multiple data structures to support application functionality:

- **Stacks:** Used within the food-logging module.
- **Dictionaries:** Used in authentication, settings, and application management.
- **Lists:** Used to manage and process statistical information.

### Automated Health Calculations

Implemented mathematical calculations to generate personalised health metrics:

- **Basal Metabolic Rate (BMR):** Calculated using the Mifflin-St Jeor equation.
- **Total Daily Energy Expenditure (TDEE):** Estimated using activity-level multipliers.
- **Body Mass Index (BMI):** Calculated from user measurements.
- **Daily Calorie Targets:** Calculated and updated based on personal information and fitness goals.

---

## Software Development Lifecycle

The application was developed using a structured, iterative software development approach.

The complete development process is recorded in a 245-page technical report covering requirements analysis, system design, implementation, testing, and evaluation.

### Phase 1 — Requirements Analysis

Conducted research into existing health and fitness applications, including:

- MyFitnessPal
- Cronometer
- Lose It!
- Lifesum
- Cal AI

Evaluated existing solutions to identify strengths, limitations, and opportunities for improvement.

Identified four stakeholder groups:

1. General health-conscious users
2. Individuals managing diabetes
3. Fitness coaches and personal trainers
4. Elderly users

Conducted stakeholder interviews to identify user requirements, usability expectations, and desired functionality.

These findings informed the application's features and success criteria.

### Phase 2 — System Design

Produced technical designs and documentation before implementation, including:

- System decomposition diagrams
- Program flowcharts
- Class diagrams
- Entity-relationship diagrams
- Database table designs
- Algorithm specifications
- Truth tables
- GUI layouts and usability considerations
- Test plans and predefined success criteria

The design phase established the structure of the application and informed implementation decisions.

### Phase 3 — Iterative Implementation

Development was divided into five iterations.

| Iteration | Functionality Developed |
|---|---|
| 1 | Authentication system |
| 2 | Food logging and nutritional tracking |
| 3 | Workout logging |
| 4 | Statistics and data visualisation |
| 5 | User settings |

Each iteration involved implementation, testing, identification of issues, and refinement.

This approach allowed functionality to be developed and validated incrementally.

### Phase 4 — Software Testing

Conducted testing throughout development and after implementation.

Testing activities included:

- Functional testing of individual modules.
- Validation of expected and unexpected user inputs.
- Boundary and invalid-input testing.
- Database operations and data integrity testing.
- Graphical user interface testing.
- Post-development testing against predefined requirements.
- Usability evaluations involving representative users.

Test results were documented and used to identify improvements.

### Phase 5 — Evaluation

The completed application was evaluated against 45 predefined success criteria.

| Evaluation Result | Criteria |
|---|---:|
| Fully Met | 43 |
| Partially Met | 2 |
| Not Met | 0 |
| Total | 45 |

The evaluation confirmed successful implementation of the application's core computational requirements, including:

- Binary search
- Password hashing
- Relational database management
- Automated BMR, TDEE, and BMI calculations
- Nutrition and workout logging
- Statistical data processing and visualisation

The evaluation also identified usability limitations and potential improvements, demonstrating the importance of critically assessing software against its original requirements.

---

## Technical Documentation

A comprehensive technical report accompanies the source code and documents the complete development process.

The report includes:

| Section | Contents |
|---|---|
| Analysis | Problem identification, competitor research, stakeholder interviews, and requirements |
| Design | Algorithms, system architecture, database design, class diagrams, and interface design |
| Development | Implementation and testing across five iterations |
| Testing | Functional, GUI, database, post-development, and usability testing |
| Evaluation | Assessment against success criteria, limitations, and further development |

**[View Full Software Development Lifecycle Documentation (PDF)](documentation.pdf)**

---

## Limitations & Future Development

The final evaluation identified several opportunities for improvement:

**1. Enhanced Food Searching**

Extend the existing binary search implementation with partial-match searching to improve usability when users enter incomplete food names.

**2. Improved GUI Responsiveness**

Refine window sizing and layout management to provide a more consistent experience across different application screens.

**3. Enhanced Visual Feedback**

Introduce conditional colour indicators to highlight when users exceed their daily calorie targets.

**4. Further Usability Refinement**

Incorporate additional improvements identified through stakeholder feedback and usability evaluations.

---

## Technologies & Skills Demonstrated

| Technology / Concept | Application |
|---|---|
| Python | Core application development |
| SQLite | Relational database management |
| Tkinter | Graphical user interface |
| Matplotlib | Data visualisation |
| Binary Search | Algorithmic optimisation |
| Object-Oriented Programming | Modular software architecture |
| SQL & Database Normalisation | Structured data storage and integrity |
| SHA-256 | Password hashing implementation |
| Software Testing | Functional validation and quality assurance |
| Iterative Development | Incremental implementation and evaluation |

---

## Project Outcomes

This project provided practical experience in developing a complete software application, from identifying a real-world problem through to implementation and evaluation.

Key learning outcomes included:

- Translating stakeholder requirements into technical specifications.
- Designing and implementing a relational database.
- Applying algorithms and data structures to practical problems.
- Developing maintainable, modular Python software.
- Integrating data processing with graphical visualisation.
- Conducting structured testing and evaluating software against measurable requirements.
- Identifying technical limitations and proposing realistic improvements.

The project demonstrates a combination of **programming ability, analytical problem-solving, database design, independent project management, and systematic evaluation**.

---

## Documentation & Source Code

The repository contains the Python application source code and supporting technical documentation.

The source code demonstrates the implementation of the application's core functionality, while the development report provides a detailed explanation of the design decisions, implementation process, testing methodology, and evaluation.

**Full Technical Report:** [View Documentation](documentation.pdf)

---

*Developed as an independent software engineering project using Python, SQLite, Tkinter, and Matplotlib.*
