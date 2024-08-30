from src.utils.logger import LogManager


def handle_command(subscription_manager, update_fetcher, scheduler, report_generator, exporter):
    logger = LogManager.get_logger()
    while True:
        command = input("Enter command (add, remove, list, fetch, export, report, help, exit): ")

        if command == "add":
            repo = input("Enter repository to subscribe (username/repo): ")
            subscription_manager.add_subscription(repo)
            logger.info(f"Subscribed to {repo}.")
        elif command == "remove":
            repo = input("Enter repository to unsubscribe (username/repo): ")
            subscription_manager.remove_subscription(repo)
            logger.info(f"Unsubscribed from {repo}.")
        elif command == "list":
            subscriptions = subscription_manager.subscriptions
            if subscriptions:
                logger.info("Current Subscriptions:")
                for repo in subscriptions:
                    logger.info(f" - {repo}")
            else:
                logger.info("No subscriptions found.")
        elif command == "fetch":
            logger.info("Fetching updates for all subscribed repositories...")
            update_fetcher.fetch_all()
            logger.info("Updates fetched successfully.")
        elif command == "export":
            updates = update_fetcher.get_fetched_data()
            if updates:
                for repo, data in updates.items():
                    exporter.export_all(repo, data['issues'], data['pull_requests'])
                logger.info("Updates exported to Markdown files.")
            else:
                logger.info("No updates to export. Please fetch updates first.")
        elif command == "report":
            updates = update_fetcher.get_fetched_data()
            if updates:
                markdown_files = []
                for repo, data in updates.items():
                    markdown_files.extend(exporter.export_all(repo, data['issues'], data['pull_requests']))
                for file in markdown_files:
                    report_generator.generate_daily_report(file)
                logger.info("Reports generated successfully.")
            else:
                logger.info("No updates to report. Please fetch and export updates first.")
        elif command == "help":
            print_help()
        elif command == "exit":
            logger.info("Exiting GithubSentinel.")
            break
        else:
            logger.warning("Invalid command. Type 'help' to see available commands.")


def print_help():
    logger = LogManager.get_logger()
    help_text = """
GithubSentinel - Interactive Command Line Tool

Available Commands:
1. add:       Add a new repository to the subscription list.
              Usage: add
              Example: Enter 'username/repo' when prompted.

2. remove:    Remove a repository from the subscription list.
              Usage: remove
              Example: Enter 'username/repo' when prompted.

3. list:      List all currently subscribed repositories.
              Usage: list

4. fetch:     Fetch the latest updates for all subscribed repositories.
              Usage: fetch

5. export:    Export fetched updates to Markdown files.
              Usage: export

6. report:    Generate a summary report from exported Markdown files using LLM.
              Usage: report

7. help:      Display this help message.
              Usage: help

8. exit:      Exit the GithubSentinel tool.
              Usage: exit
"""
    logger.info(help_text)
