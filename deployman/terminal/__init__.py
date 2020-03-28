import sys
from wasabi import Printer, color
from terminal import errors

SCRIPT_NAME = "deployman"

class ExitCodes:
    OK              = 0
    GeneralError    = 1

class Terminal:
    def __init__(self):
        self.printer = Printer()

        self._pending_ecode = False

    @property
    def pending_ecode(self):
        """Whether a console task is awaiting exit code."""
        return self._pending_ecode

    @pending_ecode.setter
    def pending_ecode(self, value):
        """Set whether a console task is awaiting exit code."""
        self._pending_ecode = value

    def cmd_head(self, task_name: str, task_text: str):
        script_name = color(SCRIPT_NAME, bold=True)
        self.printer.text(f"{script_name} {task_name}: {task_text}")

    # @classmethod
    def echo(self, title: str, details: str = None, spaced: bool = True):
        if details != None:
            self.printer.text(title=title, text=details, spaced=spaced)
        else:
            self.printer.text(title=title, spaced=spaced)

    # @classmethod
    def task(self, task_name: str, task_details: str = None, wait: bool = True):
        msg_title = f"{task_name}"

        if self.pending_ecode:
            raise Exception("Task already running")
        
        if wait:
            if task_details != None:
                self.echo(title=msg_title, details=task_details, spaced=False)
            else:
                self.echo(title=msg_title, details=None, spaced=False)
            self.pending_ecode = True
        else:
            if task_details != None:
                self.echo(title=msg_title, details=task_details, spaced=True)
            else:
                self.echo(title=msg_title, details=None, spaced=True)

    # @classmethod
    def ok(self, exit: int = None):
        if self.pending_ecode != True:
            raise errors.NoPendingStatusError()

        self.printer.good("OK")
        self.pending_ecode = False

        if exit != None:
            sys.exit(exit)

    # @classmethod
    def fail(self, exit: int = None):
        if not self.pending_ecode:
            raise errors.NoPendingStatusError()

        self.printer.fail("FAIL")
        self.pending_ecode = False

        if exit != None:
            sys.exit(exit)

    # @classmethod
    def exit(self, code: int = 0, message: str = None):
        if self.pending_ecode:
            self.fail()

        if message != None:
            self.echo(message)

def print_ok(self, exit: int = None):
    if not self.pending_ecode:
        raise errors.NoPendingStatusError()

    self.printer.good("OK")
    self.pending_ecode = False

    if exit != None:
        sys.exit(exit)

def err(exit: int, msg: str):
    printer = Printer()
    printer.fail(msg)
    del printer

    sys.exit(exit)