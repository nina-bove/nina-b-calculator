import tkinter as tk  # self-explanatory, just imports the tkinter module, a built-in Graphic User Interface library,
# when used in the code, it'll be shortened to tk

# These are constants (kinda like variables but not really cuz they are assigned a value that does not change later
# on and are written in all caps) which just change the design a bit because the default arial and grey is boring
FONT_STYLE = ("Times", 30)
LARGER_FONT_STYLE = ("Times", 60)
BUTTON_FONT_STYLE = ("Times", 36)
BLACK = "#000000"  # note to self: unnecessary, remove later and just write black directly
FONT_COLOR = "#189EAA"


class Calculator:  # creates a class and everything within it is its objects
    def __init__(self):  # def defines functions, __init__ is used whenever objects of a class is created, hence why
        # it's at the top before all the following code. self is needed to access any of the objects within the class
        # following part just initializes the main window
        self.window = tk.Tk()
        self.window.geometry("375x667")  # size
        self.window.resizable(0, 0)  # the tkinter-window has a fixed size, so it doesn't mess up the layout
        self.window.title("Calculator")
        self.window.configure(bg=BLACK)  # spent half an hour just trying to change the background color of the whole
        # tkinter window before I had to give up in order to not lose my sanity
        # Initial expressions for calculations v
        self.total_expression = ""
        self.current_expression = ""
        self.display_frame = self.create_display_frame()

        self.total_label, self.label = self.create_display_labels()

        self.numbers = {  # dictionary for numeric buttons & their placement by grid layout, 1st number=row, 2nd=column
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            '.': (4, 1), 0: (4, 2)  # note to self: maybe switch the order of the decimal point and 0 ?
        }

        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}  # a dictionary for operations
        self.buttons_frame = self.create_buttons_frame()  # creates a frame for the numeric and operator buttons above
        # Arranges rows and column weights for the layout v
        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()  # bind buttons to keyboard keys

    def create_special_buttons(self):
        self.create_clear_button()  # clear everythigm
        self.create_result_button()  # answer
        self.create_squared_button()  # x squared
        self.create_squareroot_button()  # square root of x

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())  # binds "Return"-key to calculate results
        for key in self.numbers:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:  # binds numeric keys and operators for input
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_display_labels(self):  # creates and packs labels for displaying total and current expressions
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=BLACK,
                               fg=FONT_COLOR, padx=24, font=FONT_STYLE)  # text will be everything you type in yourself,
        # anchor=tk.E just means numbers will appear from and stick to the right, bg and fg is just more design,
        # padx is padding (amount of space surrounding object) and font is just font...
        total_label.pack(expand=True, fill='both')  # clarifies that the object will take up all space available

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=BLACK, fg=FONT_COLOR,
                         padx=24, font=LARGER_FONT_STYLE)
        label.pack(expand=True, fill='both')

        return total_label, label

    def create_display_frame(self):  # creates a frame for the display where expressions and answer will appear
        frame = tk.Frame(self.window, height=221, bg=BLACK)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):  # updates current expression with whatever value was selected
        self.current_expression += str(value)
        self.update_label()

    def create_digit_buttons(self):  # creates numeric buttons and binds them to their corresponding functions
        for digit, grid_value in self.numbers.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=BLACK, fg=FONT_COLOR, font=BUTTON_FONT_STYLE,
                               borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)  # the button's position is determined
            # by the number's that were assigned on line 34-38. first number decides which row and the second which
            # column, sticky=tk.NSEW means the object sticks to its surroundings on all sides (north, south, east, west)

    def append_operator(self, operator):  # attach operator to current expression and update a bunch of labels
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self):  # exact same thing as the numeric buttons except the i variable for row number
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=BLACK, fg=FONT_COLOR, font=BUTTON_FONT_STYLE,
                               borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self):  # clears both total and current expressions
        self.current_expression = ""  # turns into an empty string
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):  # creates "Clear"-button and bind it to the clear function
        button = tk.Button(self.buttons_frame, text="C", bg=BLACK, fg=FONT_COLOR, font=BUTTON_FONT_STYLE,
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def squared(self):  # calculates the square of the current expression and updates label accordingly
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_squared_button(self):  # creates "squared"-button and binds it to the squared function
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=BLACK, fg=FONT_COLOR, font=BUTTON_FONT_STYLE,
                           borderwidth=0, command=self.squared)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def squareroot(self):  # calculates the square-root of the current expression and updates label accordingly
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_squareroot_button(self):  # creates "square-root"-button and binds it to the square-root function
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=BLACK, fg=FONT_COLOR, font=BUTTON_FONT_STYLE,
                           borderwidth=0, command=self.squareroot)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def evaluate(self):  # evaluates the totla expressions, update labels and checks for exceptions so that if a problem
        # does not have an answer it will type out "error" instead
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ""
        except Exception as random_words_cause_it_doesnt_matter_and_will_not_be_used_for_anything:
            self.current_expression = "Error"
        finally:
            self.update_label()  # this part will go through at the end regardless which of the above 2 conditions
            # were fulfilled

    def create_result_button(self):  # creatse a "Result"-button and binds it to the evaluate function
        button = tk.Button(self.buttons_frame, text="=", bg=BLACK, fg=FONT_COLOR, font=BUTTON_FONT_STYLE,
                           borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def create_buttons_frame(self):  # creates a frame for the buttons and makes sure it takes up all space availble
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):  # replaces symbols of the operator buttons from those in python code to regular math
        # signs. multiplication sign which is '*' in python code will be shown in the display as the regular 'x'
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:10])  # limits the amount of numbers displayed at the same
        # time to the first 10 digits of the string

    def run(self):  # starts the main event loop
        self.window.mainloop()


if __name__ == "__main__":  # apparently I'm supposed to do this, don't know why, but mrCoding on Youtube said so
    # creates an instance of the calculator and "starts" the whole code, without this part the whole file does nothing v
    calculator_4 = Calculator()
    calculator_4.run()


# fix later:
# Change color to purple? or green idk
# cut down the code, its unneccessary long and messy code, example code on classroom was like half the amount of lines
