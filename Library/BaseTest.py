# Pywinauto library for handling windows application

from robot.api.deco import keyword
from pywinauto import application as pwa
from pywinauto import keyboard
from robot.utils import asserts


class BaseTest:
    def _init_(self):
        self.app = None
        self.dlg = None

    @keyword("Connect UIA Window")
    def get_existing_windows_application(self, title_regex):

        self.app = pwa.Application(backend='uia').connect(title_re=title_regex)
        self.dlg = self.app[title_regex]

    @keyword("Start Application")
    def start_application(self, start_command):

        try:
            self.app = pwa.Application().start(start_command)
        except pwa.AppStartError:
            print("could not start the application \"" + start_command + '"')
            raise

    @keyword("Close Application")
    def close_application(self):
        try:
            self.app.kill()
        except pwa.AppNotConnected:
            print("could not close the application \"" + self.app + '"')
            raise

    @keyword("Get Dialog")
    def get_dialog(self, title):
        if self.app:
            try:
                self.dlg = self.app[title]
                self.dlg.draw_outline()
            except:
                print('could not find a dialog with the title "' + title + '" associated with the current application')
                raise
        else:
            print('No application currently selected. Searching for an application with the title "' + title + '"')
            try:
                self.app = pwa.Application().connect(title_re=title)
            except:
                print(
                    'Could not find application with the title "' + title + '" while searching for a dialog with that '
                                                                            'title. No application was previously '
                                                                            'selected.')
                raise
            print('Found an application with the title "' + title + '". Set this application to the current context.')
            print('Searching for a dialog with the same title. ("' + title + '")')
            try:
                self.dlg = self.app[title]
                self.dlg.draw_outline()
            except:
                print('dialog not found with the title "' + title + '"')
                raise

    @keyword("Click")
    def click(self, control):
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].click()

    @keyword("Double Click")
    def double_click(self, control):
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].doubleclick()

    @keyword("Type")
    def type_keys(self, control, keys):
        if self.app is None:
            raise UnboundLocalError("There is no application context currently set")
        if self.dlg is None:
            raise UnboundLocalError("There is no dialog context currently set")

        self.dlg[control].type_keys(keys, pause=0.05, with_spaces=True, with_tabs=True, with_newlines=True,
                                    turn_off_numlock=True)

    @keyword("Send Keys")
    def send_keyboard_keys(self, text):
        keyboard.SendKeys(text)

    @keyword("Print Control Identifiers")
    def print_control_identifiers(self):
        self.dlg.print_control_identifiers()

    @keyword("Click Child Window")
    def click_child_window(self, title, control_type):
        self.dlg.child_window(title=title, control_type=control_type).click_input()

    @keyword("Double Click Child Window")
    def double_click_child_window(self, title, control_type):
        self.dlg.child_window(title_re=title, control_type=control_type, found_index=0).double_click_input()

    @keyword("Click Tree Element")
    def click_tree_element(self, title, control_type, child_tree):
        self.dlg.child_window(title=title, control_type=control_type).child_window(title=child_tree).click_input()

    @keyword("Click AutoID")
    def click_auto_id(self, auto_id):
        self.dlg.child_window(auto_id=auto_id).click_input()

    @keyword("Send Keys AutoID")
    def send_keys_auto_id(self, auto_id, text):
        self.dlg.child_window(auto_id=auto_id).type_keys(text, with_spaces=True)

    @keyword("Get Text")
    def get_text(self, auto_id):
        child1 = self.dlg.child_window(auto_id=auto_id).children()
        return child1[0].children_texts()[0]

    @keyword("Verify Text")
    def verify_text(self, text_actual, text_expected):
        asserts.assert_equal(text_actual.strip(" "), text_expected,
                             "The text " + text_actual + "doesn't match " + text_expected)

    @keyword("Maximize Window")
    def maximize_window(self):
        self.dlg.maximize()

    @keyword("Verify Text Not Present")
    def verify_text_box_not_present(self, text_actual, text_expected):
        assert (text_actual != text_expected)

    @keyword("Double Click By AutoID")
    def double_click_auto_id(self, auto_id):
        self.dlg.child_window(auto_id=auto_id).double_click_input()

    @keyword("Check Exists")
    def check_name_exists(self, title, control_type):
        assert self.dlg.child_window(title=title, control_type=control_type).exists()

    @keyword("Close Current Window")
    def close_window(self):
        self.dlg.close()
