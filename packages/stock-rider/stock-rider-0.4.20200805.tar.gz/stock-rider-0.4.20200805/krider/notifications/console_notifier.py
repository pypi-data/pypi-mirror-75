import logging


class ConsoleNotifier:
    def send_notification(self, content):
        logging.info(content.get("body"))


console_notifier = ConsoleNotifier()
