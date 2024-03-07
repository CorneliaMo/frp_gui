# coding=utf-8

import win32process
from win32api import CloseHandle, TerminateProcess


class frpcBooter:
    def __init__(self):
        self.hProcess = None

    def startup(self):
        if not self.status():
            result = win32process.CreateProcess("frpc.exe", 'frpc.exe -c frpc.toml', None, None, 0,
                                                win32process.CREATE_NEW_CONSOLE, None, None, win32process.STARTUPINFO())
            self.hProcess = result[0]
            print(self.hProcess)

    def shutup(self):
        if self.status():
            try:
                TerminateProcess(self.hProcess, 0)
            except:
                pass
            CloseHandle(self.hProcess)
            self.hProcess = None

    def status(self):
        if self.hProcess is None:
            return False
        else:
            return True
