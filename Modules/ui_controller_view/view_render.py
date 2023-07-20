class ConsoleViewRender:
    """"""

    def display_title(self, display_string):
        print(f"\n----------{display_string.upper()}---------\n\n")

    def display_sub_title(self, display_string):
        print(f"{display_string}\n" +
              "-"* len(display_string))
        
    def display_formatted_string(self, display_string):
        print(display_string)