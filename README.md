# 📰 HackerNews Desktop Notifier

A lightweight Python script that provides real-time desktop notifications for new posts from the Hacker News RSS feed, helping you stay up-to-date with the latest tech news.

## ✨ Features

* **Real-time Notifications:** Get instant desktop alerts for new Hacker News articles.
* **Customizable Rate Limit:** Set a maximum number of notifications per hour to prevent inundation.
* **Cross-Platform (Plyer):** Leverages `plyer` for native desktop notifications across different operating systems.
* **Simple & Efficient:** A compact script designed for minimal resource usage.

## ⚙️ How It Works

The script periodically fetches the Hacker News RSS feed (`https://news.ycombinator.com/rss`), checks for new entries, and sends desktop notifications for unseen posts. It maintains a list of seen links and enforces an hourly notification limit to ensure a smooth user experience.

## 🚀 Installation

### Prerequisites

* Python 3.x installed on your system.

### Steps

1.  **Clone the repository:**
    ```bash
    git clone [YOUR_GITHUB_REPO_LINK]
    cd hackernews-notifier # Or whatever your repository's directory name is
    ```

2.  **Install dependencies:**
    This project requires the `feedparser` and `plyer` libraries.
    ```bash
    pip install -r requirements.txt
    ```

## 💻 Usage

To start monitoring the Hacker News feed and receive notifications:

```bash
python src/main.py
```
*(Assuming your main script is named `main.py` inside the `src` folder. Adjust if your file name is different, e.g., `python src/notifier.py`)*

The script will run continuously in your terminal. You can stop it by pressing `Ctrl+C`.

### Configuration

You can customize the maximum number of notifications per hour by modifying the `MAX_POSTS_PER_HOUR` variable in `src/main.py` (or your script file):

```python
# Customizable max number of notifications per hour
MAX_POSTS_PER_HOUR = 3 # Change this value as needed
```

---

## 🔁 Running as a Systemd Background Service

For continuous, unattended operation on Linux systems, you can configure the HackerNews Notifier to run as a **systemd service**. This ensures the script starts automatically on boot and restarts if it crashes.

1.  **Create a systemd service file:**
    Create a file named `hackernews_rss.service` in `/etc/systemd/system/`. You'll need root privileges for this (e.g., `sudo nano /etc/systemd/system/hackernews_rss.service`).

2.  **Add the following content to the file:**

    ```ini
    [Unit]
    Description=HackerNews RSS Feed Notifier
    After=network.target

    [Service]
    Type=simple
    User=[YOUR_LINUX_USERNAME] # e.g., swiz13
    WorkingDirectory=[ABSOLUTE_PATH_TO_YOUR_PROJECT_SRC_DIRECTORY] # e.g., /home/swiz13/projects/hackernews-notifier/src
    ExecStart=[ABSOLUTE_PATH_TO_YOUR_PYTHON_EXECUTABLE] [YOUR_SCRIPT_NAME.py] # e.g., /home/swiz13/miniconda3/envs/check_hackernews_rss/bin/python main.py
    Restart=always
    RestartSec=10
    Environment=DISPLAY=:0
    Environment=XAUTHORITY=[ABSOLUTE_PATH_TO_YOUR_XAUTHORITY_FILE] # e.g., /home/swiz13/.Xauthority

    [Install]
    WantedBy=default.target
    ```

    **Remember to replace these placeholders:**
    * `[YOUR_LINUX_USERNAME]`: Your Linux user account name.
    * `[ABSOLUTE_PATH_TO_YOUR_PROJECT_SRC_DIRECTORY]`: The full path to the `src` directory within your cloned project.
    * `[ABSOLUTE_PATH_TO_YOUR_PYTHON_EXECUTABLE]`: The full path to the Python interpreter you want to use (e.g., from your conda environment or `/usr/bin/python3`).
    * `[YOUR_SCRIPT_NAME.py]`: The name of your main Python script (e.g., `main.py` or `notifier.py`).
    * `[ABSOLUTE_PATH_TO_YOUR_XAUTHORITY_FILE]`: The full path to your `.Xauthority` file, typically found in your home directory (e.g., `/home/your_username/.Xauthority`). This is vital for desktop notifications to work when run as a background service.

3.  **Reload systemd and manage the service:**

    After creating the file, reload systemd to recognize the new service, then enable and start it:

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable hackernews_rss.service
    sudo systemctl start hackernews_rss.service
    ```

4.  **Check the service status (optional):**

    You can verify if the service is running correctly:

    ```bash
    sudo systemctl status hackernews_rss.service
    ```

This setup allows your notifier to run reliably in the background, providing Hacker News updates without needing a terminal window open.

---

## ⚠️ Limitations

* This is a command-line script and does not have a graphical user interface (GUI).
* Notifications depend on your operating system's native notification system (handled by `plyer`).

## 📄 License

Distributed under the MIT License. See the `LICENSE` file for more information.

## ✉️ Contact

Salomon Metre - [kulosmetros088@gmail.ccom](mailto:kulosmetros088@gmail.com)