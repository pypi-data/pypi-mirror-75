import os
import threading
import time
from nx_work_log.change_time_dialog import ChangeTimeDialog
from nx_work_log.sys_tray_icon import SysTrayIcon

paused = True
icons = {'running': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'SysTrayRunning.ico'),
         'paused': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'SysTrayPaused.ico')}
minute_timer = None
my_sys_tray_icon = None


class MinuteTimer():
    def __init__(self, callback_function):
        self.callback_function = callback_function
        self.next_call = time.time()
        self.__timer()

    def cancel(self):
        self.thread.cancel()

    def __timer(self):
        self.next_call = self.next_call + 60
        self.thread = threading.Timer(self.next_call - time.time(), self.__timer)
        self.thread.start()
        self.callback_function()


def show_change_time_dialog(sys_tray_icon):
    ChangeTimeDialog().show_window()


def pause_clicked(sys_tray_icon):
    global paused
    paused = not paused
    sys_tray_icon.icon = icons['paused'] if paused else icons['running']
    sys_tray_icon.refresh_icon()


def is_paused():
    return paused


def minute_timer_callback():
    if not paused:
        dialog_time = ChangeTimeDialog().get_time()
        dialog_time += 1
        ChangeTimeDialog().set_time(dialog_time)
        my_sys_tray_icon.set_hover_text('{:02d}:{:02d}'.format(int(dialog_time / 60), dialog_time % 60))


def on_startup(sys_tray_icon):
    global my_sys_tray_icon
    my_sys_tray_icon = sys_tray_icon


def on_exit(sys_tray_icon):
    minute_timer.cancel()


def exit():
    SysTrayIcon().exit()


def main():
    global minute_timer

    menu_options = [
        ('Change Time', None, show_change_time_dialog),
        ('Pause', is_paused, pause_clicked),
    ]

    minute_timer = MinuteTimer(minute_timer_callback)
    SysTrayIcon(icons['paused'], '00:00', menu_options, call_on_startup=on_startup, on_exit=on_exit, default_menu_index=1)


if __name__ == '__main__':
    main()
