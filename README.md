# StrideTrack
## A CITS5505 Agile Web Dev Group Project
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
