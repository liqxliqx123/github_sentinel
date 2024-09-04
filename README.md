## Description

GithubSentinel is an open-source AI agent designed to streamline project management and team collaboration for
developers and project managers. By automatically tracking and summarizing updates from subscribed GitHub repositories,
GithubSentinel ensures that your projects are always up-to-date.

## Key Features:

Subscription Management: Easily manage and customize your list of subscribed repositories.
Automatic Update Retrieval: Regularly (daily/weekly) fetches the latest updates from your repositories.
Notification System: Sends notifications about new updates via email, Slack, or other communication channels.
Report Generation: Creates comprehensive daily or weekly reports summarizing all repository activities.
Task Scheduling: Automatically runs update checks and notifications at scheduled times.
GithubSentinel is designed to help you respond quickly to changes, track project progress efficiently, and ensure that
all team members are informed about the latest developments.


## Running the Project
* Using run.sh
To run the project in the background with scheduled tasks, execute the run.sh script.

* Using src/main.py
For command-line generation of reports, run the main.py file located in the src directory.

* Using Gradio
To generate and download reports visually, utilize the Gradio interface.


## Supported Models
* gpt-4o-mini
* glm-4-0520
* gemma2 (for private deployment)