# TrailMate
## A CITS5505 Agile Web Dev Group Project

## Table of Contents

- [Contributors](#contributors)
- [Purpose](#purpose)
- [Design](#design)
  - [Architecture](#architecture)
  - [Features](#features)
  - [User Experience Flow](#user-experience-flow)
  - [Testing](#testing)
- [How to Launch the Application](#how-to-launch-the-application)
- [How to Run the Tests](#how-to-run-the-tests)
- [Configuring Environment](#configuring-environment)


## Contributors

| Name                        | UWA ID   | GitHub User                    |
| --------------------------- | -------- | ------------------------------ |
| ChienAn Tu                  | 24367005 | https://github.com/ChienAnTu   |
| Calvin Siauw                | 24204443 | https://github.com/Wxvxl       |
| Dhanush Gowda               | 24245807 | https://github.com/kinggfisher |
| Swapnil Mangesh Kadam Kadam | 24497911 | https://github.com/swapnilkcr  |

## Purpose

**TrailMate** is a web application built to empower users to track, analyze, and share their physical activities—whether walking, cycling, swimming, or hiking. Our goal is to deliver a **fitness experience that’s not just functional, but motivating and delightful**.

We designed TrailMate based on three key principles:

- **Engaging** – The interface is visually appealing and emphasizes what matters most: your progress. From live charts to personalized nutrition suggestions, every element aims to draw the user in and make fitness fun.
- **Effective** – Users gain real value from TrailMate, with features like calorie tracking, trail exploration, leaderboard rankings, and nutrition/hydration suggestions. Whether you're looking for health insights or friendly competition, TrailMate delivers.
- **Intuitive** – All interactions—from uploading CSV files to selecting a trail on a map—are designed to be simple and seamless. Users can navigate, log, and share activities with minimal effort.

To support flexible data entry, TrailMate allows users to:

- Manually log an activity
- Select a real-world trail with pre-filled data
- Upload multiple entries at once via CSV

In return, users get visual insights through interactive **dashboards**, **weekly goal tracking**, and comparisons with peers via a calorie-based **leaderboard**. They can also explore detailed progress charts and selectively **share activities** with other users. 

Our team focused on keeping the core interface intuitive while layering in just enough analytics to keep users informed and motivated — without feeling overwhelmed.

## Design

### Architecture

We followed a modular and scalable architecture throughout our Flask application. All database logic is abstracted into a dedicated `models.py` and `database.py` layer. Application configuration is separated using `config.py`, supporting different environments (e.g., development vs. testing).

To improve maintainability, we **refactored route logic** into `register_routes(app)` and centralized **visual and analytical processing** in the `activity_service.py`. We also split UI layout into Jinja templates (`base.html`, `_sidebar.html`) for reusability and clarity.

Static files are organized by type (`script/`, `images/`, `styles/`), and key JS modules handle different responsibilities (e.g., `dashboard_charts.js`, `shared_with_me.js`, `calories.js`) in line with component separation principles.

> [!NOTE]
>
> We adopted a **3-Tier Architecture**, which separates the application into:
>
> - A **Presentation Layer** (Jinja templates + Tailwind + JavaScript) for the frontend UI and interaction,
> - An **Application Layer** (Flask route handlers and services) for handling logic such as calorie calculations, data filtering, and visualization preparation,
> - And a **Data Layer** (SQLAlchemy models and database) for managing persistent data.



------

### Features

**Introductory View**

- **Trail Explorer**
  Browse beautiful local trails on an interactive map, complete with distance, difficulty, and duration. One click to log your adventure.

**Visualise Data**

- **Interactive Dashboard**
  Instantly see how many calories you’ve burned and how active you’ve been lately via easy-to-read charts.
- **Weekly Goals**
  Calorie-burning goals can be set and tracked with donut and line charts.

**Upload Data**

- **Manual Entry**
  Prefer entering details yourself? Just pick an activity, duration, and weight.
- **Trail-based Entry**
  Select a trail you completed, and we'll fill in the details for you.
- **CSV Upload**
  Got lots of data? Upload a CSV and let us handle it—all with helpful feedback.

**Share Data**

- **Activity Sharing**
  Select one or more activities and share them with another user.
- **View shared activity**
  See what others have shared with you and get a breakdown of how everyone’s doing.
- **Pagination & Filtering**
  Both sharing interfaces support per-page limits and navigation for large datasets.

**Interactivity & Motivation**

- **Calories Leaderboard**
  Stay motivated by seeing how you rank in the community—friendly competition makes it fun!
- **Personal Nutrition Suggestions API**
  Burned some calories? Your TrailMate will use an **AJAX Request** to scour the internet suggest food and hydration ideas to help you recover smartly.

**Security**

- **User Registration & Login**
- **Form Protection with CSRF Tokens**

------

### User Experience Flow

1. **Landing Page**
    Users are greeted with a clean homepage describing the app and can sign up or log in via modals. 
    Once logged in, they’re automatically redirected to their personal **dashboard**, and TrailMate remembers their login status when they return.
2. **Activity Management**
   Accessible via the sidebar, users can:
   - Manually log a new activity
   - Select from real-world trails with pre-filled information
   - Upload `.csv` files for quick batch entry
   - Users can also view all their past activities, select multiple entries, and delete them if needed.
3. **Dashboard**
   The dashboard gives a quick overview of:
   - The **most recent activity**, including type, calories, and duration
   - A personalized **nutrition suggestion** based on calories burned
   - Progress toward the user’s **weekly calorie goal**, shown in donut and line charts
   - Flexible date views (daily / weekly / monthly)
4. **Sharing**
   Users can select any number of activities and **share** them with another registered user via email.
    In the **Shared With Me** view, users can:
   - Browse received activities
   - See a **leaderboard** ranked by calories burned
   - View a **breakdown of shared activity types** (shown in a pie chart)
   - Use pagination and filters for easier browsing
5. **Progress**
    Provides further interactive pie charts and bar graphs showing activity breakdown by time spent and calories.
6. **Challenges**
    Users can explore new locations using our interactive **Trail Explorer**.
    Each trail comes with map routes, details, and suggested duration—users can add the trail to their log with just one click.

------

### Testing
We included a `tests/` folder that contains sample `.csv` files to help test the **batch upload** feature with realistic data.
We also implemented both **unit tests** and **Selenium (UI) tests** using:

- `unittest` for database model and backend functionality (in `Tests.py`)
- `Selenium` for testing login/signup flows, element interaction, and DOM behaviour
- A full test-runner (`Tests.py`) that:
  - Sets up a clean test database
  - Adds random users and activities
  - Validates key features like auto-increment IDs, password hashing, shared activity correctness

More Details : [**How to Run the Tests**](#how-to-run-the-tests)

All test scripts are designed to run with:

```bash
python3 Tests.py
```

## How to Launch the Application

1. **Clone the repository**

   ```bash
   git clone https://github.com/YourTeam/StrideTrack.git
   cd StrideTrack
   ```

2. **Create a virtual environment**

   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**

   - macOS / Linux:

     ```bash
     source venv/bin/activate
     ```

   - Windows:

     ```bash
     .\venv\Scripts\activate
     ```

4. **Install dependencies**
   *(Optional: upgrade pip first with `pip install --upgrade pip`)*

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Flask application**

   ```bash
   flask run
   ```

6. **Visit the app in your browser**
   Go to [http://127.0.0.1:5000](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000/).
   Flask runs on port **5000** by default.

   For more detailed environment setup instructions, please refer to the [**Configuring Environment**](#configuring-environment) section below.

## How to Run the Tests

To execute our backend and UI tests, simply run the following command from the root directory:

```bash
python3 Tests.py
```

This script will:

- Set up a temporary testing database
- Add random users and activities
- Run core functionality tests (user creation, activity sharing, calorie calculation)
- Execute Selenium-based UI tests for signup/login

If all tests pass, you will see success messages like:

```
Back End Test Results:
  test_database_creation: PASSED
  test_db_user_addition: PASSED
  test_password_hashing: PASSED
  test_user_ID: PASSED
  test_db_activity_addition: PASSED
  test_db_shared_activity_addition: PASSED
Selenium Test Results:
  test_signup_functionality: PASSED
  test_signin_wrong_password: PASSED
  test_signin_correct_password: PASSED
  test_logout_functionality: PASSED
  test_signin_random_user: PASSED
  test_dashboard_header_link: PASSED
  test_site_navigation: PASSED
```

## Configuring Environment

This project utilizes a Flask server to be set up and deployed. Here are the steps required to set up the Flask 
### 1. Set up the Python Virtual Environment
You can set up the Python Virtual Env by running the following command in the root folder of the project (`/StrideTrack`).

```shell
python3 -m venv venv
```

Note that the second `venv` will be the name of directory created, you can modified this to `application-env` or anything else:

```shell
python3 -m venv <directory name you want>
```

But since we need to write it to `.gitignore` to ignore this directory when pushing to Github, I recommend we use the same name `venv`.

### 2. Getting into the Virtual Environment
An `venv` (or any other name you gave it like `application-env`) folder should be created within the root folder containing the Python Virtual Environment.

How to activate the VE depends on which system do you use:

| System                 | Virtual Environment Directory | Command to Activate           |
| ---------------------- | ----------------------------- | ----------------------------- |
| **macOS / Linux**      | `venv/bin/activate`           | `source venv/bin/activate`    |
| **Windows** (CMD)      | `venv\Scripts\activate.bat`   | `venv\Scripts\activate`       |
| **Windows PowerShell** | `venv\Scripts\Activate.ps1`   | `.\venv\Scripts\Activate.ps1` |

**For example, if you use Windows in your VScode terminal:**

Navigate the terminal into the `venv/Scripts` and run the command `./activate` 

**If you use `Linux` or `WSL` extension in your VScode terminal:**

Run `source venv/bin/activate` command under `/StrideTrack`

**Check if it's activated:**

To check if your virtual environment is activated, look at your terminal window. If it is 
activated, the terminal prompt will look something like this:
`(venv) something@something:/mnt/c/path/to/my/folder$`
If there is a `(venv)` in brackets at the start of the line, that means the virtual environment is 
activated.

### 3. Installing Requirements
Once you have activated the VE, in the root folder, run the command `pip install -r requirements.txt` and install all of the required dependencies.
### 4. Running Flask

#### Using `flask run` to run the server

Using `flask run` command under project root directory like`YourPath/StrideTrack`  you can run the Flask server, it should say `Running on http://127.0.0.1:5000`, which means the local server has successfully been deployed. Open the link in a web browser to visit the homepage.

To close and stop the server, Key in `Ctrl+C` at the terminal.

> [!NOTE]
>
> **Use Debug Mode**
>
> You can use `debug mode` to get the instance response upon every changes in your script so that you don't have to stop the server and re-run it to render changes.
>
> **The command for this is:**`flask --debug run`
>
> (You may have to refresh the browser to render changes)

#### Using `python3 run.py` to run the server

You can also run the `python3 run.py` command under the same directory of your terminal to run the Flask server.

