from win10toast import ToastNotifier
import time
def notify(subject, body, duration1=10):
    toaster = ToastNotifier()
    toaster.show_toast(subject,
                       body,
                       icon_path=None,
                       duration=duration1)
    while toaster.notification_active(): time.sleep(0.1)
