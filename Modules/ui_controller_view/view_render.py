from tabulate import tabulate

class ConsoleViewRender:
    """"""

    def display_title(self, display_string):
        print(f"\n----------{display_string.upper()}---------\n")


    def display_sub_title(self, display_string):
        print(f"\n{display_string}\n" +
              "-"* len(display_string))
        

    def display_formatted_string(self, display_string):
        print(display_string)


    def input_request(self, input_message):
        return input(f"{input_message}")
    
    
    def display_table_with_header(self, data_list):
        print(tabulate(data_list, headers = "firstrow", tablefmt = "grid"))