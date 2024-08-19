import threading
from config import Config
from subscription_manager import SubscriptionManager
from update_fetcher import UpdateFetcher
from notifier import Notifier
from report_generator import ReportGenerator
from scheduler import Scheduler


def print_help():
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

4. fetch:     Fetch the latest updates for all subscribed repositories immediately.
              Usage: fetch

5. help:      Display this help message.
              Usage: help

6. exit:      Exit the GithubSentinel tool.
              Usage: exit
"""
    print(help_text)


def run_scheduler(scheduler):
    scheduler.start()


def command_loop(subscription_manager, update_fetcher, scheduler):
    while True:
        command = input("Enter command (add, remove, list, fetch, help, exit): ")

        if command == "add":
            repo = input("Enter repository to subscribe (username/repo): ")
            subscription_manager.add_subscription(repo)
            print(f"Subscribed to {repo}.")
        elif command == "remove":
            repo = input("Enter repository to unsubscribe (username/repo): ")
            subscription_manager.remove_subscription(repo)
            print(f"Unsubscribed from {repo}.")
        elif command == "list":
            subscriptions = subscription_manager.subscriptions
            if subscriptions:
                print("Current Subscriptions:")
                for repo in subscriptions:
                    print(f" - {repo}")
            else:
                print("No subscriptions found.")
        elif command == "fetch":
            updates = update_fetcher.fetch_updates()
            for repo, events in updates.items():
                print(f"\nRepository: {repo}")
                for event in events:
                    print(f" - {event['type']}: {event['created_at']}")
        elif command == "help":
            print_help()
        elif command == "exit":
            print("Exiting GithubSentinel.")
            break
        else:
            print("Invalid command. Type 'help' to see available commands.")


def main():
    config = Config.load()

    subscription_manager = SubscriptionManager(config)
    update_fetcher = UpdateFetcher(config)
    notifier = Notifier(config)
    report_generator = ReportGenerator(config)
    scheduler = Scheduler(config, update_fetcher, notifier, report_generator)

    # Print help message on startup
    print_help()

    # Run Scheduler in background
    threading.Thread(target=run_scheduler, args=(scheduler,)).start()

    # Start command loop for interactive input
    command_loop(subscription_manager, update_fetcher, scheduler)


if __name__ == "__main__":
    main()
