# TrailMate
## A CITS5505 Agile Web Dev Group Project

[TOC]

## Contributors

| Name                        | UWA ID   | GitHub User                    |
| --------------------------- | -------- | ------------------------------ |
| ChienAn Tu                  | 24367005 | https://github.com/ChienAnTu   |
| Calvin Siauw                | 24204443 | https://github.com/Wxvxl       |
| Dhanush Gowda               | 24245807 | https://github.com/kinggfisher |
| Swapnil Mangesh Kadam Kadam | 24497911 | https://github.com/swapnilkcr  |

## Purpose

The goal of this project was to develop **TrailMate**, a fitness-tracking web application inspired by the simplicity and motivation of platforms like Strava.

We designed TrailMate based on three key principles:

- **Effortless Tracking**: Logging workouts should be simple and not feel like a chore.
- **Visual Motivation**: Users should see their progress clearly and feel encouraged.
- **Social Sharing**: Fitness becomes more engaging when shared with friends.

While apps like Strava exist, we found a gap in platforms that balance **lightweight user interaction**, **trail exploration**, and **data-driven visual feedback** — especially for casual exercisers. TrailMate aims to fill this gap.

TrailMate allows users to log activities manually, by selecting real-world trails, or via CSV upload. They can set weekly calorie goals, monitor their daily progress with donut and line charts, and receive nutrition suggestions based on calories burned. What makes TrailMate fun is the **gamified dashboard**, **leaderboards**, and the ability to **share selected activities** with others, turning solo exercise into a friendly competition.

Our team focused on keeping the core interface intuitive while layering in just enough analytics to keep users informed and motivated — without feeling overwhelmed.

## Design

### Architecture

We followed a modular and scalable architecture throughout our Flask application. All database logic is abstracted into a dedicated `models.py` and `database.py` layer. Application configuration is separated using `config.py`, supporting different environments (e.g., development vs. testing).

To improve maintainability, we **refactored route logic** into `register_routes(app)` and centralized visual and analytical processing in the `activity_service.py`. We also split UI layout into Jinja templates (`base.html`, `_sidebar.html`) for reusability and clarity.

Static files are organized by type (`script/`, `images/`, `styles/`), and key JS modules handle different responsibilities (e.g., `dashboard_charts.js`, `shared_with_me.js`, `calories.js`) in line with component separation principles.

------

### Features

- **User Login & Registration** with Flask-Login and hashed password storage
- **Dashboard** for calorie summary, activity overview, and donut/line charts
- **Weekly Goals** and progress indicators
- **Trail Explorer** with real-world map integration and auto-fill data input
- **CSV Upload** with batch processing and validation feedback
- **Share Activities** with other users and view shared data
- **Leaderboard** ranked by calories burned
- **Nutrition Suggestions API** dynamically recommends post-workout meals
- **Pagination & Filtering** for user control in large datasets

------

### User Experience Flow

1. **Landing Page**
    Users are greeted with a clean homepage describing the app and can sign up or log in via modals.
2. **Upload Activities**
    Accessible via the sidebar, users can:
   - Manually enter activity data
   - Select from curated real-world trails
   - Upload `.csv` files for batch uploading
3. **Dashboard**
    Displays:
   - Activity summaries
   - Weekly goal progress (donut + line charts)
   - View switching: daily, weekly, or monthly
4. **Sharing**
    Users can:
   - Select activities
   - Share with another registered email
   - View activities shared with them (with sort and pagination)
5. **Progress**
    Provides further interactive pie charts and bar graphs showing activity breakdown by time spent and calories.
6. **Challenges**
    Trail-based UI allows users to visually explore new locations and add to their activity logs.

------

### Testing

We implemented both **unit tests** and **Selenium (UI) tests** using:

- `unittest` for database model and backend functionality (in `Tests.py`)
- `Selenium` for testing login/signup flows, element interaction, and DOM behaviour
- A full test-runner (`Tests.py`) that:
  - Sets up a clean test database
  - Adds random users and activities
  - Validates key features like auto-increment IDs, password hashing, shared activity correctness

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

   For more detailed environment setup instructions, please refer to the **Configuring Environment** section below.

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
App Setup Test passed
Database Randomized Addition Test passed with 10 random users.
Password Hashing Testing passed
User ID auto-increment testing passed
Random activity addition test passed: 5 activities per user.
Random shared activity addition test passed: 10 shared activities per user.
Selenium Testing Finished
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



