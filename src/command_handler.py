from utils.logger import LogManager


def handle_command(subscription_manager, update_fetcher, report_generator, exporter):
    logger = LogManager().logger
    while True:
        command = input("Enter command (list, fetch, export, report, help, exit): ")
        if command == "list":
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
                    markdown_files.append(exporter.export_all(repo, data['issues'], data['pull_requests']))
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
    logger = LogManager().logger
    help_text = """
GithubSentinel - Interactive Command Line Tool

Available Commands:

 list:      List all currently subscribed repositories.
              Usage: list

 fetch:     Fetch the latest updates for all subscribed repositories.
              Usage: fetch

 export:    Export fetched updates to Markdown files.
              Usage: export

 report:    Generate a summary report from exported Markdown files using LLM.
              Usage: report

 help:      Display this help message.
              Usage: help

 exit:      Exit the GithubSentinel tool.
              Usage: exit
"""
    logger.info(help_text)
