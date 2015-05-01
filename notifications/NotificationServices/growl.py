import gntp.notifier
import remote_notify

def sendNotification(notificationId, to, body):
    growl = gntp.notifier.GrowlNotifier(
        applicationName="homework-notify",
        notifications=["Router Notification"],
        defaultNotifications=["Router Notifications"],
        hostname=to
    )

    growl.register()
    res = growl.notify(
        noteType="Router Notification",
        title="Router Notification",
        description=body,
        sticky=False,
        priority=1
    )

    if res is True:
        nr = remote_notify.sendNotification("growl", to, body)
        return True
    return False
