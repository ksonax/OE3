import customtkinter
from ui.plot_function import plot_function

from algo import algo
from ui.UserInputs import UserInputs
from time import time
from tkinter import messagebox
from output.generateoutput import generate_csv, generate_plot
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class UserInterface(customtkinter.CTk):
    WIDTH = 780
    HEIGHT = 720

    def __init__(self):
        super().__init__()
        self.timer = 0
        self.title("Genetic Algorithm for finding MIN/MAX in Beale Function")
        self.geometry(f"{UserInterface.WIDTH}x{UserInterface.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Beale Function")  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Plot Function",
                                                command=self.plot_button_event)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0, pady=25, padx=20, sticky="w")

        # ============ frame_right ============

        # configure grid layout (3x11)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=2)
        self.frame_right.rowconfigure(10, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        # ============ frame_info ============

        # ============ frame_right ============

        self.label_radio_group = customtkinter.CTkLabel(master=self.frame_right,
                                                        text="Choose Method:")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, pady=15, padx=15, sticky="")

        self.combobox_selection_method = customtkinter.CTkComboBox(master=self.frame_right,
                                                                   values=["Tournament", "Best",
                                                                           "Roulette", "Random",
                                                                           "Worst", "Double Tournament"])
        self.combobox_selection_method.grid(row=1, column=2, columnspan=1, pady=15, padx=15, sticky="we")

        self.combobox_cross_method = customtkinter.CTkComboBox(master=self.frame_right,
                                                               values=["One Point Cross", "Two Point Cross",
                                                                       "Uniform Cross", "Blend Alpha-R"])
        self.combobox_cross_method.grid(row=2, column=2, columnspan=1, pady=15, padx=15, sticky="we")

        self.combobox_mutation_method = customtkinter.CTkComboBox(master=self.frame_right,
                                                                  values=["Flip Bit", "Shuffle Indexes", "Gaussian-R"])
        self.combobox_mutation_method.grid(row=3, column=2, columnspan=1, pady=15, padx=15, sticky="we")

        self.check_box_maximum = customtkinter.CTkCheckBox(master=self.frame_right,
                                                           text="Maximum")
        self.check_box_maximum.grid(row=4, column=2, pady=15, padx=15, sticky="w")

        self.check_box_elite_strategy = customtkinter.CTkCheckBox(master=self.frame_right,
                                                           text="Elite Strategy")
        self.check_box_elite_strategy.grid(row=5, column=2, pady=15, padx=15, sticky="w")

        self.check_box_real_representation = customtkinter.CTkCheckBox(master=self.frame_right,
                                                                  text="Real Representation*")
        self.check_box_real_representation.grid(row=6, column=2, pady=15, padx=15, sticky="w")

        self.label_radio_group = customtkinter.CTkLabel(master=self.frame_right,
                                                        text="*If Real Representation selected => Only Methods with 'R' will work.")
        self.label_radio_group.grid(row=10, column=1, columnspan=2, pady=15, padx=15, sticky="")

        self.entry_population_amount = customtkinter.CTkEntry(master=self.frame_right,
                                                              width=120,
                                                              placeholder_text="Population amount")
        self.entry_population_amount.grid(row=0, column=0, columnspan=2, pady=15, padx=15, sticky="we")


        self.entry_epochs_amount = customtkinter.CTkEntry(master=self.frame_right,
                                                          width=120,
                                                          placeholder_text="Epochs amount")
        self.entry_epochs_amount.grid(row=1, column=0, columnspan=2, pady=15, padx=15, sticky="we")


        self.entry_cross_probability_amount = customtkinter.CTkEntry(master=self.frame_right,
                                                                     width=120,
                                                                     placeholder_text="Cross probability")
        self.entry_cross_probability_amount.grid(row=2, column=0, columnspan=2, pady=15, padx=15, sticky="we")

        self.entry_mutation_probability = customtkinter.CTkEntry(master=self.frame_right,
                                                                 width=120,
                                                                 placeholder_text="Mutation probability")
        self.entry_mutation_probability.grid(row=3, column=0, columnspan=2, pady=15, padx=15, sticky="we")

        self.button_start = customtkinter.CTkButton(master=self.frame_right,
                                                    text="Start",
                                                    border_width=2,  # <- custom border_width
                                                    fg_color="grey",  # <- no fg_color
                                                    command=self.button_start)
        self.button_start.grid(row=10, column=0, columnspan=3, pady=15, padx=15, sticky="swe")

        # set default values
        self.combobox_selection_method.set("Selection Method")
        self.combobox_cross_method.set("Cross Method")
        self.combobox_mutation_method.set("Mutation Method")
        self.check_box_maximum.select()
        self.check_box_elite_strategy.select()
        self.check_box_real_representation.select()

    def button_start(self):
        x = self.get_user_inputs()
        time_start = time()
        gen_b_rows, gen_avg_rows, gen_std_dev_rows, best_ind, value = algo.deap(x)
        time_end = time()
        generate_csv(gen_b_rows, gen_avg_rows, gen_std_dev_rows)
        generate_plot()
        time_diff = time_end - time_start
        result = "Execution in sec: " + str(round(time_diff, 5)) + "s" + "\n [" + str(best_ind) + "] =" + str(value)
        messagebox.showinfo("output",  result)



    @staticmethod
    def change_appearance_mode(new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()

    @staticmethod
    def plot_button_event():
        plot_function()

    def get_user_inputs(self):
        return UserInputs(
            int(self.entry_population_amount.get()),
            int(self.entry_epochs_amount.get()),
            float(self.entry_cross_probability_amount.get()),
            float(self.entry_mutation_probability.get()),
            self.combobox_selection_method.get(),
            self.combobox_cross_method.get(),
            self.combobox_mutation_method.get(),
            bool(self.check_box_maximum.get()),
            bool(self.check_box_elite_strategy.get()),
            bool(self.check_box_real_representation.get()),
        )