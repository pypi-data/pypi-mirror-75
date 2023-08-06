from selenium import webdriver
from thonny import get_workbench
from selenium.common import exceptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from tkinter.simpledialog import askstring
from threading import Thread
import time
import uuid
import ast
import _ast
import json
import os
from pathlib import Path


class Singleton:
    """This Singleton class is needed so you do not spawn more selenium contexts when
    opening a new link or working on a past context.

    __instance: The current instance of this class.
    closed: A variable that indicates if the current browser window has been closed by
    the user.
    sleeptime: The seconds to wait after every check if an HTML element has changed.
    observed_ids: The HTML element ids which are observed by the observe method.
        """

    __instance = None
    closed = False
    sleeptime = 0.1
    observed_ids = []

    @staticmethod
    def getInstance():
        """This is a modified Singleton.getInstance() method. It will create a new
        instance if the variable closed is set to true.

        Returns:
            Nested Singleton object with an initialized webdriver using a selenium
            context
        """
        if Singleton.__instance == None or Singleton.closed:
            Singleton()
        return Singleton.__instance

    def __init__(self):
        """This is a modified Singleton constructor. Just like Singleton.getInstance()
        it will create a new instance if the variable closed is set to true. Before
        creating the new context, security settings will also be set for Firefox. Other
        browsers only support the W3C compliant capabilities (
        https://www.w3.org/TR/webdriver/#capabilities).
        """
        if Singleton.__instance != None and Singleton.closed == False:
            raise Exception("This class is a singleton!")
        else:
            try:
                firefox_capabilities = DesiredCapabilities.FIREFOX
                # Only communicate over HTTPS and do not accept insecure Certificates
                firefox_capabilities["handleAlerts"] = False
                firefox_capabilities["acceptSslCerts"] = False
                firefox_capabilities["acceptInsecureCerts"] = False
                profile = webdriver.FirefoxProfile()
                profile.accept_untrusted_certs = False
                profile.set_preference("network.http.use-cache", False)
                profile.set_preference("dom.security.https_only_mode", True)
                # Disable unsafe cipher
                profile.set_preference("security.ssl3.rsa_des_ede3_sha", False)
                # Disable ciphers with no forward secrecy
                profile.set_preference("security.ssl3.dhe_rsa_aes_128_sha", False)
                profile.set_preference("security.ssl3.dhe_rsa_aes_256_sha", False)
                profile.set_preference("security.ssl3.rsa_aes_128_sha", False)
                profile.set_preference("security.ssl3.rsa_aes_256_sha", False)
                profile.set_preference("security.ssl3.ecdhe_ecdsa_aes_128_sha", False)
                profile.set_preference("security.ssl3.ecdhe_ecdsa_aes_256_sha", False)
                profile.set_preference("security.ssl3.ecdhe_rsa_aes_128_sha", False)
                profile.set_preference("security.ssl3.ecdhe_rsa_aes_256_sha", False)
                self.driver = webdriver.Firefox(
                    capabilities=firefox_capabilities, firefox_profile=profile
                )
            except BaseException:
                try:
                    self.driver = webdriver.Chrome()
                except BaseException:
                    try:
                        self.driver = webdriver.Safari()
                    except BaseException:
                        try:
                            self.driver = webdriver.Edge()
                        except BaseException:
                            try:
                                self.driver = webdriver.Opera()
                            except BaseException:
                                try:
                                    self.driver = webdriver.Ie()
                                except Exception as e:
                                    print(str(e))
                                    print(
                                        "You seem to be using a browser and webdriver "
                                        + "which are not supported by selenium. You can "
                                        + "find the list of supported browsers here: "
                                        + "https://www.selenium.dev/documentation/en/"
                                        + "getting_started_with_webdriver/browsers/"
                                    )
            Singleton.closed = False
            Singleton.__instance = self

    def toggle_closed(self):
        """This method toggles the closed variable.

        Returns:
            None
        """
        Singleton.closed = not Singleton.closed

    def get_sleeptime(self):
        """This method gets the current sleep time. The time to wait after every check
        if an HTML element has changed.

        Returns:
            float in seconds
        """
        return Singleton.sleeptime

    def set_sleeptime(self, sleeptime):
        """This method sets the sleep time. The time to wait after every check if an
        HTML element has changed.

        :param sleeptime: Seconds to sleep represented as float

        Returns:
            None
        """
        Singleton.sleeptime = sleeptime

    def get_observed_ids(self):
        """Get the list of HTML element ids which are currently observed.

        Returns:
            list of HTML element ids
        """
        return Singleton.observed_ids

    def add_observed_id(self, html_id):
        """This method adds one HTML element id to the list of currently observed ids.

        :param html_id: HTML element id that you wish to add

        Returns:
            None
        """
        Singleton.observed_ids.append(html_id)

    def remove_observed_id(self, html_id):
        """This method removes one HTML element id to the list of currently observed
        ids.

        :param html_id: HTML element id that you wish to remove

        Returns:
            None
        """
        Singleton.observed_ids.remove(html_id)


def open_website():
    """This method gets called if the "Open Website" command is clicked in the "tools"
    menu. It will get the Singleton instance and then tries to open the desired
    website. Insecure Certificates will be shown as an error page to the user. If the
    browser window has been closed by the user, a new selenium context will be created.

        Returns:
            None
        """
    singleton = Singleton.getInstance()
    # This is the URL for struktog development server
    address = "https://dditools.inf.tu-dresden.de/dev/struktog/"
    try:
        singleton.driver.get(address)
    except exceptions.InsecureCertificateException:
        return
    except exceptions.WebDriverException:
        singleton.toggle_closed()
        singleton = Singleton.getInstance()
        singleton.driver.get(address)
    # This simulates a click on the ToggleSourcecode element, to show the select element to choose a programming language
    singleton.driver.execute_script(
        'document.getElementsByClassName("ToggleSourcecode")[0].click()'
    )
    # This also simulates a click on the correct option but the code is different as the .click() function does not work for this: https://stackoverflow.com/questions/49886729/simulate-a-human-click-and-select-on-dropdown-menu
    singleton.driver.execute_script(
        'var optionToClick = document.getElementById("SourcecodeSelect").childNodes[1]; optionToClick.selected = true; optionToClick.dispatchEvent(new PointerEvent("pointerdown", {bubbles: true})); optionToClick.dispatchEvent(new MouseEvent("mousedown", {bubbles: true})); optionToClick.dispatchEvent(new PointerEvent("pointerup", {bubbles: true})); optionToClick.dispatchEvent(new MouseEvent("mouseup", {bubbles: true})); optionToClick.dispatchEvent(new MouseEvent("mouseout", {bubbles: true})); optionToClick.dispatchEvent(new MouseEvent("click", {bubbles: true})); optionToClick.dispatchEvent(new Event("change", {bubbles: true}));'
    )


def observe_element_in_background():
    """This method gets called by the start_observing_element_by_id method. If the text
    of the HTML element changes, the info will be printed to stdout.

        Returns:
            None
        """
    singleton = Singleton.getInstance()
    driver = singleton.driver
    url = driver.current_url
    observed_ids = singleton.get_observed_ids()
    list_id = len(observed_ids) - 1
    html_id = observed_ids[list_id]
    observed_text = driver.find_element_by_id(html_id).text
    # Get the current opened code view
    code_view = (
        get_workbench().get_editor_notebook().get_current_editor().get_code_view()
    )
    # Change the content to the observed text
    code_view.set_content(observed_text)
    print("Start observing on the following URL: " + url)
    print("And the following ID: " + html_id)
    while html_id in singleton.get_observed_ids():
        try:
            element = driver.find_element_by_id(html_id)
            if element.text != observed_text:
                # Uncomment the following line to get more DEBUG insights
                # print("Text of " + html_id + " changed to: " + element.text)
                observed_text = element.text
                # Change the content to the observed text every time a change is detected
                code_view.set_content(observed_text)
        except exceptions.NoSuchElementException as e:
            print(e)
            print("Observing this element is not possible as it does not exist.")
            return
        except exceptions.WebDriverException as e:
            print(
                "The Browser window was closed. Observing this element is not possible"
                + " anymore"
            )
            print(e)
            return
        time.sleep(singleton.get_sleeptime())
    print("Observing was stopped as requested.")


def start_observing_element_by_id():
    """This method gets called if the "Start observing element by id" command is
    clicked in the "tools" menu. It will prompt the user to provide an HTML ID which
    will be added to the list of observed elements. After that, a new thread will be
    created to observe this HTML ID.

        Returns:
            None
        """
    observe_id = "Sourcecode"
    singleton = Singleton.getInstance()
    singleton.add_observed_id(observe_id)
    t = Thread(target=observe_element_in_background)
    t.daemon = True
    t.start()


def stop_observing_element_by_id():
    """This method gets called if the "Stop observing element by id" command is clicked
    in the "tools" menu. It will prompt the user to provide an HTML ID which will be removed
    from the list of observed elements.

        Returns:
            None
        """
    observe_id = "Sourcecode"
    singleton = Singleton.getInstance()
    singleton.remove_observed_id(observe_id)


def transform_ast(ast_list, data, python_lines):
    """This method gets called by the method transform_code_view. It will transform a
    list of Abstract Syntax Tree (_ast.*) objects to a dictionary. It uses a recursive
    approach for _ast.For, _ast.While and _ast.If objects. For all other objects only a
    subtree has to be modified.

        Returns:
            None
        """
    subtree = data
    for body_obj in ast_list:
        while True and subtree != {}:
            if subtree.get("followElement") is None:
                break
            else:
                subtree = subtree.get("followElement")
        if isinstance(body_obj, _ast.Assign):
            try:
                if body_obj.value.func.id == "input":
                    # This is always an InputNode (e.g. x = input("Eingabe"))
                    subtree.update(
                        {
                            "followElement": {
                                "id": str(uuid.uuid4()),
                                "type": "InputNode",
                                "text": body_obj.targets[0].id,
                                "followElement": {
                                    "id": str(uuid.uuid4()),
                                    "type": "InsertNode",
                                    "followElement": None,
                                },
                            }
                        }
                    )
                else:
                    # This is called if there is another method call
                    # (e.g. y = x.isalpha())
                    subtree.update(
                        {
                            "followElement": {
                                "id": str(uuid.uuid4()),
                                "type": "TaskNode",
                                "text": python_lines[body_obj.value.lineno - 1],
                                "followElement": {
                                    "id": str(uuid.uuid4()),
                                    "type": "InsertNode",
                                    "followElement": None,
                                },
                            }
                        }
                    )
            except:
                # This is called if there is no method call (e.g. x = x +1)
                subtree.update(
                    {
                        "followElement": {
                            "id": str(uuid.uuid4()),
                            "type": "TaskNode",
                            "text": python_lines[body_obj.value.lineno - 1],
                            "followElement": {
                                "id": str(uuid.uuid4()),
                                "type": "InsertNode",
                                "followElement": None,
                            },
                        }
                    }
                )
        if isinstance(body_obj, _ast.Expr):
            try:
                if body_obj.value.func.id == "print":
                    # This is always an OutputNode. The text value can either be a
                    # variable or a string.
                    value = ""
                    try:
                        # This is called if a variable is given.
                        value = body_obj.value.args[0].id
                    except:
                        # This is called if a string is given. That is why we add
                        # double quotes.
                        value = '"' + body_obj.value.args[0].value + '"'
                    subtree.update(
                        {
                            "followElement": {
                                "id": str(uuid.uuid4()),
                                "type": "OutputNode",
                                "text": value,
                                "followElement": {
                                    "id": str(uuid.uuid4()),
                                    "type": "InsertNode",
                                    "followElement": None,
                                },
                            }
                        }
                    )
                else:
                    # This is always a TaskNode.
                    subtree.update(
                        {
                            "followElement": {
                                "id": str(uuid.uuid4()),
                                "type": "TaskNode",
                                "text": python_lines[body_obj.value.lineno - 1],
                                "followElement": {
                                    "id": str(uuid.uuid4()),
                                    "type": "InsertNode",
                                    "followElement": None,
                                },
                            }
                        }
                    )
            except:
                # This is always a TaskNode.
                subtree.update(
                    {
                        "followElement": {
                            "id": str(uuid.uuid4()),
                            "type": "TaskNode",
                            "text": python_lines[body_obj.value.lineno - 1],
                            "followElement": {
                                "id": str(uuid.uuid4()),
                                "type": "InsertNode",
                                "followElement": None,
                            },
                        }
                    }
                )
        if isinstance(body_obj, _ast.For):
            # If a CountLoopNode is discovered we need to do recursion as the child element
            # has to be populated with data.
            start = {
                "id": str(uuid.uuid4()),
                "type": "InsertNode",
                "followElement": None,
            }
            subtree.update(
                {
                    "followElement": {
                        "id": str(uuid.uuid4()),
                        "type": "CountLoopNode",
                        "text": python_lines[body_obj.lineno - 1]
                        .replace("for ", "")
                        .replace(":", ""),
                        "followElement": {
                            "id": str(uuid.uuid4()),
                            "type": "InsertNode",
                            "followElement": None,
                        },
                        "child": transform_ast(body_obj.body, start, python_lines),
                    }
                }
            )
        if isinstance(body_obj, _ast.While):
            # If a HeadLoopNode is discovered we need to do recursion as the child
            # element has to be populated with data.
            start = {
                "id": str(uuid.uuid4()),
                "type": "InsertNode",
                "followElement": None,
            }
            subtree.update(
                {
                    "followElement": {
                        "id": str(uuid.uuid4()),
                        "type": "HeadLoopNode",
                        "text": python_lines[body_obj.lineno - 1]
                        .replace("while ", "")
                        .replace(":", ""),
                        "followElement": {
                            "id": str(uuid.uuid4()),
                            "type": "InsertNode",
                            "followElement": None,
                        },
                        "child": transform_ast(body_obj.body, start, python_lines),
                    }
                }
            )
        if isinstance(body_obj, _ast.If):
            # The Python Abstract Syntax Tree implementation sees no difference between
            # a CaseNode and a BranchNode. Both are of type _ast.If . We can only find
            # out the difference by checking if the orelse attribute contains another
            # _ast.If object. We need to do recursion wherever other elements than
            # followElement need to be populated.
            try:
                if isinstance(body_obj.orelse[0], _ast.If):
                    # This is always a CaseNode.
                    defaultNode = {}
                    start_cases_first = {
                        "id": str(uuid.uuid4()),
                        "type": "InsertNode",
                        "followElement": None,
                    }
                    # The cases object is populated with data from the first case before adding other cases.
                    cases = [
                        {
                            "id": str(uuid.uuid4()),
                            "type": "InsertCase",
                            "text": python_lines[body_obj.lineno - 1]
                            .split(" == ")[1]
                            .replace(":", ""),
                            "followElement": transform_ast(
                                body_obj.body, start_cases_first, python_lines
                            ),
                        }
                    ]
                    defaultOn = False
                    case_obj = body_obj
                    while True:
                        try:
                            if isinstance(case_obj.orelse[0], _ast.If):
                                # Another case has been discovered and will be added to the
                                # list of cases.
                                case_obj = case_obj.orelse[0]
                                start_cases = {
                                    "id": str(uuid.uuid4()),
                                    "type": "InsertNode",
                                    "followElement": None,
                                }
                                cases.append(
                                    {
                                        "id": str(uuid.uuid4()),
                                        "type": "InsertCase",
                                        "text": python_lines[case_obj.lineno - 1]
                                        .split(" == ")[1]
                                        .replace(":", ""),
                                        "followElement": transform_ast(
                                            case_obj.body, start_cases, python_lines
                                        ),
                                    }
                                )
                            else:
                                # case_obj.orelse list does not contain a _ast.If statement
                                # but another one, we know it has to be the default case
                                # now.
                                start_cases = {
                                    "id": str(uuid.uuid4()),
                                    "type": "InsertNode",
                                    "followElement": None,
                                }
                                defaultOn = True
                                defaultNode = {
                                    "id": str(uuid.uuid4()),
                                    "type": "InsertCase",
                                    "text": "Sonst",
                                    "followElement": transform_ast(
                                        case_obj.orelse, start_cases, python_lines
                                    ),
                                }
                                break
                        except:
                            # If calling case_obj.orelse[0] throws an error, we know that
                            # the default case does not exist, so we set it to a
                            # Placeholder. Struktog also acts like this.
                            defaultOn = False
                            defaultNode = {
                                "id": str(uuid.uuid4()),
                                "type": "InsertCase",
                                "text": "Sonst",
                                "followElement": {
                                    "id": str(uuid.uuid4()),
                                    "type": "InsertNode",
                                    "followElement": {"type": "Placeholder"},
                                },
                            }
                            break
                    subtree.update(
                        {
                            "followElement": {
                                "id": str(uuid.uuid4()),
                                "type": "CaseNode",
                                "text": python_lines[body_obj.lineno - 1]
                                .replace("if ", "")
                                .replace(":", "")
                                .split(" == ")[0],
                                "cases": cases,
                                "defaultOn": defaultOn,
                                "defaultNode": defaultNode,
                                "followElement": {
                                    "id": str(uuid.uuid4()),
                                    "type": "InsertNode",
                                    "followElement": None,
                                },
                            }
                        }
                    )
                else:
                    # This is always a BranchNode. We need to do recursion on the
                    # trueChild and falseChild element.
                    start_true = {
                        "id": str(uuid.uuid4()),
                        "type": "InsertNode",
                        "followElement": None,
                    }
                    start_false = {
                        "id": str(uuid.uuid4()),
                        "type": "InsertNode",
                        "followElement": None,
                    }
                    subtree.update(
                        {
                            "followElement": {
                                "id": str(uuid.uuid4()),
                                "type": "BranchNode",
                                "text": python_lines[body_obj.lineno - 1]
                                .replace("if ", "")
                                .replace(":", ""),
                                "trueChild": transform_ast(
                                    body_obj.body, start_true, python_lines
                                ),
                                "falseChild": transform_ast(
                                    body_obj.orelse, start_false, python_lines
                                ),
                                "followElement": {
                                    "id": str(uuid.uuid4()),
                                    "type": "InsertNode",
                                    "followElement": None,
                                },
                            }
                        }
                    )
            except:
                # This is always a BranchNode. We need to do recursion on the trueChild
                # element.
                start_true = {
                    "id": str(uuid.uuid4()),
                    "type": "InsertNode",
                    "followElement": None,
                }
                subtree.update(
                    {
                        "followElement": {
                            "id": str(uuid.uuid4()),
                            "type": "BranchNode",
                            "text": python_lines[body_obj.lineno - 1]
                            .replace("if ", "")
                            .replace(":", ""),
                            "trueChild": transform_ast(
                                body_obj.body, start_true, python_lines
                            ),
                            "falseChild": {
                                "id": str(uuid.uuid4()),
                                "type": "InsertNode",
                                "followElement": {"type": "Placeholder"},
                            },
                            "followElement": {
                                "id": str(uuid.uuid4()),
                                "type": "InsertNode",
                                "followElement": None,
                            },
                        }
                    }
                )
    return data


def transform_code_view():
    """This method gets called if the "Transform code view to JSON" command is clicked
    in the "tools" menu. It will get the content of the current editor and transform it
    in a JSON representation that is readable by struktog. It does this by converting
    the source code in an Abstract Syntax Tree first. Then, it will dump the JSON
    representation in a file. After that, the file will be sent to the webapplication
    using a HTML input element.

        Returns:
            None
        """
    data = {"id": str(uuid.uuid4()), "type": "InsertNode", "followElement": None}
    python_code = get_workbench().get_editor_notebook().get_current_editor_content()
    python_lines = python_code.splitlines()
    ast_obj = ast.parse(python_code)
    data.update(transform_ast(ast_obj.body, data, python_lines))
    path_to_file = str((Path.home() / "output.json").resolve())
    with open(path_to_file, "w") as json_file:
        json.dump(data, json_file)
    singleton = Singleton.getInstance()
    upload = singleton.driver.find_element_by_class_name("webdriver-input")
    upload.send_keys(path_to_file)


def load_plugin():
    """This method gets called if this plugin is in the PYTHONPATH environment variable
       upon starting thonny. This code is executed before TK windows are drawn. That is
       why you should use add a command to the thonny GUI before running anything.

        Returns:
            None
        """
    get_workbench().add_command(
        command_id="webview_open_website",
        menu_name="tools",
        command_label="Open website",
        handler=open_website,
    )
    get_workbench().add_command(
        command_id="webview_observing_add",
        menu_name="tools",
        command_label="Start observing element by id",
        handler=start_observing_element_by_id,
    )
    get_workbench().add_command(
        command_id="webview_observing_delete",
        menu_name="tools",
        command_label="Stop observing element by id",
        handler=stop_observing_element_by_id,
    )
    get_workbench().add_command(
        command_id="transform_code_view",
        menu_name="tools",
        command_label="Transform code view to JSON",
        handler=transform_code_view,
    )
