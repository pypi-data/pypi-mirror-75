from cryptomodel.cryptostore import user_notification, user_channel, user_settings
from cryptomodel.operations import OPERATIONS

from cryptodataaccess.Memory import Memory
from cryptodataaccess.Repository import Repository

DATE_FORMAT = "%Y-%m-%d"


class UsersRepository(Repository):

    def __init__(self, users_store):
        self.users_store = users_store
        super(UsersRepository, self).__init__()

        self.notifications = []
        notification_memory = Memory(on_add=self.users_store.insert_notification,
                                     on_edit=self.users_store.update_notification,
                                     on_remove=self.users_store.delete_notification,
                                     items=self.notifications
                                     )
        self.memories.append(notification_memory)

        self.user_settings = []
        user_settings_memory = Memory(on_add=self.users_store.insert_user_settings,
                                      on_edit=self.users_store.update_user_settings,
                                      on_remove=self.users_store.delete_user_settings,
                                      items=self.user_settings
                                      )
        self.memories.append(user_settings_memory)

        self.user_channels = []
        user_channels_memory = Memory(on_add=self.users_store.insert_user_channel,
                                      on_edit=None,
                                      on_remove=None,
                                      items=self.user_channels
                                      )
        self.memories.append(user_channels_memory)

    def get_user_channels(self, user_id):
        return self.users_store.get_user_channels(user_id)

    def get_user_settings(self, user_id):
        return self.users_store.fetch_user_settings(user_id)

    def get_notifications(self, items_count):
        return self.users_store.fetch_notifications(items_count)

    def add_notification(self, user_id, user_name, user_email, expression_to_evaluate, check_every_seconds,
                         check_times, is_active, channel_type, fields_to_send, source_id):
        n =  user_notification(
            user_id=user_id, user_name=user_name, user_email=user_email, expression_to_evaluate=expression_to_evaluate,
            check_every_seconds=check_every_seconds, check_times=check_times, is_active=is_active,
            channel_type=channel_type, fields_to_send=fields_to_send, source_id=source_id,
            operation=OPERATIONS.ADDED.name)
        self.notifications.append(n)
        return n

    def edit_notification(self, in_id, user_id, user_name, user_email, expression_to_evaluate, check_every_seconds,
                          check_times, is_active, channel_type, fields_to_send, source_id):

        n = user_notification(
            id=in_id,
            user_id=user_id, user_name=user_name, user_email=user_email, expression_to_evaluate=expression_to_evaluate,
            check_every_seconds=check_every_seconds, check_times=check_times, is_active=is_active,
            channel_type=channel_type, fields_to_send=fields_to_send, source_id=source_id,
            operation=OPERATIONS.MODIFIED.name)

        self.notifications.append(n)
        return n

    def add_user_settings(self, user_id, preferred_currency, source_id):
        uc = user_settings( userId=user_id,preferred_currency=preferred_currency, source_id = source_id,
                            operation=OPERATIONS.ADDED.name)
        self.user_settings.append(uc)
        return uc

    def edit_user_settings(self, user_id, preferred_currency, source_id):
        uc = user_settings(user_id=user_id,
                           preferred_currency=preferred_currency, source_id = source_id,

                           operation=OPERATIONS.MODIFIED.name)
        self.user_settings.append(uc)
        return uc

    def add_user_channel(self, user_id, channel_type, chat_id, source_id):
        uc = user_channel(
                user_id=user_id,
                channel_type=channel_type,
                chat_id=chat_id,
                operation=OPERATIONS.ADDED.name,
                source_id = source_id)

        self.user_channels.append(
                uc
        )
        return uc

    def remove_notification(self, in_id):
        notification = next((x for x in self.notifications if x.id == in_id), None)
        self.mark_user_notifications_deleted(notification)

    def remove_user_setting(self, in_id):
        us = next((x for x in self.user_settings if x.id == in_id), None)
        self.mark_user_settings_deleted(us)

    def mark_user_settings_deleted(self, us):
        if us is None:
            us = self.fetch_user_settings(id)
            us.operation = OPERATIONS.REMOVED.name
            self.transactions.append(us)
        else:
            us.operation = OPERATIONS.REMOVED.name

    def mark_user_notifications_deleted(self, un):
        if un is None:
            un = self.fetch_user_settings(id)
            un.operation = OPERATIONS.REMOVED.name
            self.transactions.append(un)
        else:
            un.operation = OPERATIONS.REMOVED.name

    def mark_user_channels_deleted(self, uc):
        if uc is None:
            uc = self.fetch_user_channels(id)
            uc.operation = OPERATIONS.REMOVED.name
            self.transactions.append(uc)
        else:
            uc.operation = OPERATIONS.REMOVED.name
