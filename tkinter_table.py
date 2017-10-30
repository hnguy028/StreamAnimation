import Tkinter as tk
import time

class App(tk.Tk):
  def __init__(self, *args, **kwargs):
    tk.Tk.__init__(self)
    table = Table(self, 46, 2, kwargs)
    table.pack(side="top", fill=None)
    table.update_table()

class Table(tk.Frame):
  def __init__(self, parent, rows=10, columns=2, **kwargs):
    # use black background so it "peeks through" to
    # form grid lines
    tk.Frame.__init__(self, parent, background="black")
    self._widgets = []

    # init table
    for row in range(rows):
      current_row = []
      for column in range(columns):
        label = tk.Label(self, text="%s/%s" % (row, column),
                         borderwidth=0, width=20)
        label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
        current_row.append(label)
      self._widgets.append(current_row)

    for column in range(columns):
      self.grid_columnconfigure(column, weight=1)

    self.cc = 0

  def update_cell(self, row, column, value):
    cell = self._widgets[row][column]
    cell.configure(text=value)

  def update_table(self):
    self.update_cell(0, 0, "test" + str(self.cc))
    self.cc+=1
    self.after(1000, self.update_table)

if __name__== "__main__":
    app = App()
    app.mainloop()