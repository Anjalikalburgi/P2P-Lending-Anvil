# from ._anvil_designer import borrower_notificationsTemplate
# from anvil import *
# import anvil.server

# class borrower_notifications(borrower_notificationsTemplate):
#     def __init__(self, user_Id, **properties):
#         self.init_components(**properties)
#         self.user_Id = user_Id
#         self.read_notifications = set()  # Initialize the read notifications set
#         self.load_notifications()

#     def load_notifications(self):
#         self.notifications = anvil.server.call('get_notifications', self.user_Id)
#         for notification in self.notifications:
#             notification['read'] = (notification['date'], notification['message']) in self.read_notifications
#         self.repeating_panel_1.items = self.notifications
#         self.update_notification_count()

#     def update_notification_count(self):
#         unread_count = len([n for n in self.notifications if not n['read']])
#         get_open_form().update_notification_count(unread_count)

#     def mark_notification_as_read(self, loan_id):
#         anvil.server.call('mark_notification_as_read', loan_id)
#         self.load_notifications()

#     def button_refresh_click(self, **event_args):
#         self.load_notifications()

#     def back_button_click(self, **event_args):
#         open_form('borrower.dashboard')

#     def button_2_click(self, **event_args):
#         open_form('borrower.dashboard')


from ._anvil_designer import borrower_notificationsTemplate
from anvil import *
import anvil.server

class borrower_notifications(borrower_notificationsTemplate):
    def __init__(self, user_Id, **properties):
        self.init_components(**properties)
        self.user_Id = user_Id
        self.read_notifications = set()  # Initialize the read notifications set
        self.load_notifications()

    def load_notifications(self):
        self.notifications = anvil.server.call('get_notifications', self.user_Id)
        for notification in self.notifications:
            if notification['read']:
                self.read_notifications.add((notification['date'], notification['message']))
            notification['read'] = (notification['date'], notification['message']) in self.read_notifications
        self.repeating_panel_1.items = self.notifications
        self.update_notification_count()

    def update_notification_count(self):
        unread_count = len([n for n in self.notifications if not n['read']])
        if hasattr(get_open_form(), 'update_notification_count'):
            get_open_form().update_notification_count(unread_count)

    def mark_notification_as_read(self, loan_id):
        anvil.server.call('mark_notification_as_read', loan_id)
        self.load_notifications()

    def button_refresh_click(self, **event_args):
        self.load_notifications()

    def back_button_click(self, **event_args):
        open_form('borrower.dashboard')  # Ensure it opens the correct main form

    def button_2_click(self, **event_args):
        open_form('borrower.dashboard')  # Ensure it opens the correct main form
