"""Application View Renderer module to render desired view format for application.

Classes:
--------
ConsoleViewRender:
    Uses functions to print program data to terminal console or request user input

    Exported Functions:
    -------------------
    display_title(self, display_string) -> None
        display message in All Caps with additional hyphen format

    display_sub_title(self, display_string) -> None
        display message as received with underline

    display_formatted_string(self, display_string) -> None
        display message as received

    input_request(self, input_message) -> str
        request user_input displaying 'input_message'

    display_table_with_header(self, data_list ) -> None
        use 'tabulate' module to display data_list in tabular form
"""

from tabulate import tabulate

class ConsoleViewRender:
    """Create functionality to display desired view types to terminal console.
    
    Methods:
    --------
    display_title(self, display_string) -> None
        display message in All Caps with additional hyphen format

    display_sub_title(self, display_string) -> None
        display message as received with underline

    display_formatted_string(self, display_string) -> None
        display message as received

    input_request(self, input_message) -> str
        request user_input displaying 'input_message'

    display_table_with_header(self, data_list ) -> None
        use 'tabulate' module to display data_list in tabular form

    Module Requirements:
    --------------------
    tabulate - printing program data in tabular form
    """

    def display_title(self, display_string):
        """print message in All Caps with additional hyphen format"""
        print(f"\n----------{display_string.upper()}---------\n")


    def display_sub_title(self, display_string):
        """print message as received with underline"""
        print(f"\n{display_string}\n" +
              "-"* len(display_string))


    def display_formatted_string(self, display_string):
        """print message as received"""
        print(display_string)


    def input_request(self, input_message):
        """Request user input and return as string"""
        return input(f"{input_message}")


    def display_table_with_header(self, data_list):
        """print data-list in tabular form"""
        print(tabulate(data_list, headers = "firstrow", tablefmt = "grid"))
