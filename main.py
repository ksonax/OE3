from output.generateoutput import generate_csv, generate_plot
from algo import algo
from ui.UserInterface import UserInterface
import os
import sys

'''
gen_b_rows, gen_avg_rows, gen_std_dev_rows = algo.deap()
generate_csv(gen_b_rows, gen_avg_rows, gen_std_dev_rows)
generate_plot()
'''

if __name__ == "__main__":
    app = UserInterface()
    app.mainloop()
