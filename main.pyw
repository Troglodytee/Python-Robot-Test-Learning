from tkinter import Tk, Frame, Canvas, Label, Button, Scale, Listbox, Spinbox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from random import random


MIN_MAP_SIZE = 10
MAX_MAP_SIZE = 100
MIN_NB_STEPS = 1
MAX_NB_STEPS = 100
MIN_NB_ROBOTS = 4
MAX_NB_ROBOTS = 100
PROB_NEW_CHARACTER = 0.5

class Window:
    def __init__(self):
        self.__font = "Consolas 10"
        self.__map_size = 50
        self.__map = [[0 for x in range(self.__map_size)] for y in range(self.__map_size)]
        self.__spawn = self.__map_size//2-(self.__map_size%2 == 0)
        self.__canvas_size = 500
        self.__ide = 0
        self.__nb_robots = 20
        self.__robots = {}
        self.__nb_steps = self.__map_size//2
        self.__window = Tk()
        self.__window.title("Project GalacticShoqapik")
        self.__window.resizable(width=False, height=False)

        self.__canvas = Canvas(self.__window, width=self.__canvas_size, height=self.__canvas_size, bg="white")
        self.__canvas.grid(row=0, column=0, rowspan=8, sticky="nw")
        self.__canvas.bind("<Button-1>", self.__add_tile)
        self.__canvas.bind("<B1-Motion>", self.__add_tile)

        self.__listbox = Listbox(self.__window, width=33, height=21, font=self.__font)
        self.__listbox.grid(row=0, column=1, sticky="nw")
        self.__listbox.bind("<Button-1>", self.__display_parameters)
        self.__listbox.bind("<B1-Motion>", self.__display_parameters)
        self.__listbox.bind("<Key>", self.__display_parameters)
        self.__frame_3 = Frame(self.__window)
        self.__frame_3.grid(row=1, column=1, sticky="nw")
        self.__label_restart = Label(self.__frame_3, text="Restart with ", font=self.__font)
        self.__label_restart.grid(row=0, column=0, sticky="w")
        self.__spinbox_restart = Spinbox(self.__frame_3, from_=MIN_NB_ROBOTS, to=MAX_NB_ROBOTS, increment=1, width=4, font=self.__font)
        self.__spinbox_restart.grid(row=0, column=1, sticky="w")
        self.__spinbox_restart.delete(0, "end")
        self.__spinbox_restart.insert(0, str(self.__nb_robots))
        self.__label_robots = Label(self.__frame_3, text=" robots", font=self.__font)
        self.__label_robots.grid(row=0, column=2, sticky="w")
        self.__button_restart = Button(self.__frame_3, text="►", font=self.__font, command=self.__start)
        self.__button_restart.grid(row=0, column=3, sticky="nw")
        self.__label_dontmove = Label(self.__window, text="Don't move : ?", font=self.__font)
        self.__label_dontmove.grid(row=2, column=1, sticky="nw")
        self.__label_up = Label(self.__window, text="Up         : ?", font=self.__font)
        self.__label_up.grid(row=3, column=1, sticky="nw")
        self.__label_down = Label(self.__window, text="Down       : ?", font=self.__font)
        self.__label_down.grid(row=4, column=1, sticky="nw")
        self.__label_left = Label(self.__window, text="Left       : ?", font=self.__font)
        self.__label_left.grid(row=5, column=1, sticky="nw")
        self.__label_right = Label(self.__window, text="Right      : ?", font=self.__font)
        self.__label_right.grid(row=6, column=1, sticky="nw")
        self.__frame_4 = Frame(self.__window)
        self.__frame_4.grid(row=7, column=1, sticky="nw")
        self.__button_add1 = Button(self.__frame_4, text="+1", font=self.__font, command=lambda x=1:self.__evolve(x))
        self.__button_add1.grid(row=0, column=0, sticky="nw")
        self.__button_add10 = Button(self.__frame_4, text="+10", font=self.__font, command=lambda x=10:self.__evolve(x))
        self.__button_add10.grid(row=0, column=1, sticky="nw")
        self.__button_add50 = Button(self.__frame_4, text="+50", font=self.__font, command=lambda x=50:self.__evolve(x))
        self.__button_add50.grid(row=0, column=2, sticky="nw")
        self.__button_add100 = Button(self.__frame_4, text="+100", font=self.__font, command=lambda x=100:self.__evolve(x))
        self.__button_add100.grid(row=0, column=3, sticky="nw")
        self.__label_generation = Label(self.__frame_4, text=" Generation(s)", font=self.__font)
        self.__label_generation.grid(row=0, column=4, sticky="w")

        self.__frame_1 = Frame(self.__window)
        self.__frame_1.grid(row=8, column=0, sticky="nw")
        self.__button_open = Button(self.__frame_1, text="Open map", font=self.__font, command=self.__open_map)
        self.__button_open.grid(row=0, column=0, sticky="nw")
        self.__button_save = Button(self.__frame_1, text="Save map", font=self.__font, command=self.__save_map)
        self.__button_save.grid(row=0, column=1, sticky="nw")
        self.__scale = Scale(self.__frame_1, orient="horizontal", from_=-10, to=10, resolution=1, length=335, showvalue=0, font=self.__font, command=self.__change_value)
        self.__scale.grid(row=0, column=2, sticky="nw")
        self.__label_value = Label(self.__frame_1, text="0", font=self.__font)
        self.__label_value.grid(row=0, column=3, sticky="nw")

        self.__frame_2 = Frame(self.__window)
        self.__frame_2.grid(row=9, column=0, sticky="nw")
        self.__label_size = Label(self.__frame_2, text="Size of the map : ", font=self.__font)
        self.__label_size.grid(row=0, column=0, sticky="w")
        self.__spinbox_size = Spinbox(self.__frame_2, from_=MIN_MAP_SIZE, to=MAX_MAP_SIZE, increment=1, width=4, font=self.__font)
        self.__spinbox_size.grid(row=0, column=1, sticky="w")
        self.__spinbox_size.delete(0, "end")
        self.__spinbox_size.insert(0, str(self.__map_size))
        self.__label_size = Label(self.__frame_2, text="   Number of steps : ", font=self.__font)
        self.__label_size.grid(row=0, column=2, sticky="w")
        self.__spinbox_nbsteps = Spinbox(self.__frame_2, from_=MIN_NB_STEPS, to=MAX_NB_STEPS, increment=1, width=4, font=self.__font)
        self.__spinbox_nbsteps.grid(row=0, column=3, sticky="w")
        self.__spinbox_nbsteps.delete(0, "end")
        self.__spinbox_nbsteps.insert(0, str(self.__nb_steps))
        self.__button_validate = Button(self.__frame_2, text="►", font=self.__font, command=self.__validate)
        self.__button_validate.grid(row=0, column=4, sticky="nw")

        self.__display()

        self.__window.mainloop()

    def __del_map(self):
        for y in range(self.__map_size):
            del self.__map[0][:]
            del self.__map[0]
        del self.__map

    def __open_map(self):
        resp = askopenfilename(title="Open map...", filetypes=[("map files",".map")])
        if resp != "":
            file = open(resp, "r")
            lines = file.read().split("\n")
            file.close()
            self.__map_size = int(lines[0])
            self.__map = [[0 for x in range(self.__map_size)] for y in range(self.__map_size)]
            for y in range(self.__map_size):
                lines[y+1] = lines[y+1].split(",")
                for x in range(self.__map_size):
                    self.__map[y][x]= int(lines[y+1][x])
            self.__spawn = self.__map_size//2-(self.__map_size%2 == 0)
            self.__display()

    def __save_map(self):
        resp = asksaveasfilename(title="Save map...", filetypes=[("map files",".map")], defaultextension=".map")
        if resp != "":
            file = open(resp, "w")
            file.write(str(self.__map_size))
            for y in range(self.__map_size):
                file.write("\n")
                file.write(str(self.__map[y][0]))
                for x in range(1, self.__map_size):
                    file.write(","+str(self.__map[y][x]))
            file.close()

    def __add_tile(self, event):
        if 0 <= event.x < self.__canvas_size and 0 <= event.y < self.__canvas_size:
            self.__map[event.y//(self.__canvas_size//self.__map_size)][event.x//(self.__canvas_size//self.__map_size)] = self.__scale.get()
            self.__display()

    def __validate(self):
        try:
            previous_map_size = self.__map_size
            self.__map_size = int(self.__spinbox_size.get())
            self.__nb_steps = int(self.__spinbox_nbsteps.get())
            if self.__map_size < MIN_MAP_SIZE:
                self.__map_size = MIN_MAP_SIZE
            elif self.__map_size > MAX_MAP_SIZE:
                self.__map_size = MAX_MAP_SIZE
            if self.__nb_steps < MIN_NB_STEPS:
                self.__nb_steps = MIN_NB_STEPS
            elif self.__nb_steps > MAX_NB_STEPS:
                self.__nb_steps = MAX_NB_STEPS
            if previous_map_size < self.__map_size:
                for y in range(self.__map_size):
                    if y >= previous_map_size:
                        self.__map += [[0 for x in range(self.__map_size)]]
                    else:
                        for x in range(self.__map_size-previous_map_size):
                            self.__map[y] += [0]
            elif previous_map_size > self.__map_size:
                for y in range(self.__map_size):
                    for x in range(self.__map_size, previous_map_size):
                        del self.__map[y][self.__map_size]
                for y in range(self.__map_size, previous_map_size):
                    del self.__map[self.__map_size]
            self.__spawn = self.__map_size//2-(self.__map_size%2 == 0)
            self.__display()
        except: 0

    def __change_value(self, event=None):
        self.__label_value["text"] = str(self.__scale.get())
        self.__display_parameters()

    def __start(self):
        try:
            self.__nb_robots = int(self.__spinbox_restart.get())
            if self.__nb_robots < MIN_NB_ROBOTS:
                self.__nb_robots = MIN_NB_ROBOTS
            elif self.__nb_robots > MAX_NB_ROBOTS:
                self.__nb_robots = MAX_NB_ROBOTS
            self.__listbox.delete(0, "end")
            self.__ide = 0
            for i in range(self.__nb_robots):
                self.__robots[self.__ide] = Robot()
                self.__ide += 1
            self.__evolve(1)
        except: 0

    def __sort_robots(self):
        results = []
        for i in self.__robots:
            j = 0
            while j < len(results) and (self.__robots[i].score == None or results[j][1] > self.__robots[i].score):
                j += 1
            results = results[:j]+[(i, self.__robots[i].score)]+results[j:]
        return results

    def __reproduction(self):
        l = self.__sort_robots()
        del l[len(l)//2:]
        results = {}
        for i in range(len(l)):
            for j in range(1, 3):
                if i+j >= len(l):
                    parent = self.__robots[l[i+j-len(l)][0]]
                else:
                    parent = self.__robots[l[i+j][0]]
                results[self.__ide] = Robot(self.__robots[l[i][0]], parent)
                results[self.__ide].new_character()
                self.__ide += 1
        del l[:]
        keys = []
        for i in self.__robots:
            keys += [i]
        for i in keys:
            del self.__robots[i]
        self.__robots = results

    def __evolve(self, n):
        if len(self.__robots) > 0:
            self.__listbox.delete(0, "end")
            for i in range(n):
                self.__reproduction()
                for j in self.__robots:
                    self.__robots[j].compute(self.__map, self.__nb_steps, self.__spawn)
            l = self.__sort_robots()
            for i in l:
                self.__listbox.insert("end", str(i[0])+" Score : "+str(i[1]))
            self.__display()

    def __display_parameters(self, event=None):
        if self.__listbox.get("active") == "":
            self.__label_dontmove["text"] = "Don't move : ?"
            self.__label_up["text"] = "Up         : ?"
            self.__label_down["text"] = "Down       : ?"
            self.__label_left["text"] = "Left       : ?"
            self.__label_right["text"] = "Right      : ?"
        else:
            parameters = self.__robots[int(self.__listbox.get("active").split()[0])].get_parameters(self.__scale.get())
            self.__label_dontmove["text"] = "Don't move : "+str(parameters[0])
            self.__label_up["text"] = "Up         : "+str(parameters[1])
            self.__label_down["text"] = "Down       : "+str(parameters[2])
            self.__label_left["text"] = "Left       : "+str(parameters[3])
            self.__label_right["text"] = "Right      : "+str(parameters[4])
        self.__display()

    def __display(self):
        self.__canvas.delete("all")
        tile_size = self.__canvas_size/self.__map_size
        for y in range(self.__map_size):
            for x in range(self.__map_size):
                if self.__map[y][x] != 0:
                    color = str(hex(int(255-25.5*abs(self.__map[y][x]))))[2:]
                    if len(color) == 1:
                        color = "0"+color
                    if self.__map[y][x] > 0:
                        color = "#ff"+color*2
                    else:
                        color = "#"+color*2+"ff"
                    self.__canvas.create_rectangle(x*tile_size+2, y*tile_size+2, (x+1)*tile_size+2, (y+1)*tile_size+2, fill=color, outline=color)
        if self.__listbox.get("active") != "":
            act = int(self.__listbox.get("active").split()[0])
            for i in self.__robots:
                if i != act:
                    for j in range(len(self.__robots[i].path)-1):
                        x1 = (self.__robots[i].path[j][0]+0.5)*tile_size+2
                        y1 = (self.__robots[i].path[j][1]+0.5)*tile_size+2
                        x2 = (self.__robots[i].path[j+1][0]+0.5)*tile_size+2
                        y2 = (self.__robots[i].path[j+1][1]+0.5)*tile_size+2
                        self.__canvas.create_line(x1, y1, x2, y2, width=1, fill="#f0f")
            for i in range(len(self.__robots[act].path)-1):
                x1 = (self.__robots[act].path[i][0]+0.5)*tile_size+2
                y1 = (self.__robots[act].path[i][1]+0.5)*tile_size+2
                x2 = (self.__robots[act].path[i+1][0]+0.5)*tile_size+2
                y2 = (self.__robots[act].path[i+1][1]+0.5)*tile_size+2
                self.__canvas.create_line(x1, y1, x2, y2, width=1, fill="#0f0")
        self.__canvas.create_rectangle(self.__spawn*tile_size+2, self.__spawn*tile_size+2, (self.__spawn+1)*tile_size+2, (self.__spawn+1)*tile_size+2, fill="#080", outline="#080")
        for i in range(1, self.__map_size):
            self.__canvas.create_line(2, i*tile_size+2, self.__canvas_size+2, i*tile_size+2, width=1, fill="#000")
            self.__canvas.create_line(i*tile_size+2, 2, i*tile_size+2, self.__canvas_size+2, width=1, fill="#000")

class Robot:
    def __init__(self, first_parent=None, second_parent=None):
        self.score = None
        self.__parameters = [[] for i in range(21)]
        self.path = []
        if first_parent == None or second_parent == None:
            for i in range(21):
                for j in range(5):
                    self.__parameters[i] += [random()]
                s = sum(self.__parameters[i])
                for j in range(5):
                    self.__parameters[i][j] *= 1/s
        else:
            for i in range(21):
                parameters_1 = first_parent.get_parameters(i-10)
                parameters_2 = second_parent.get_parameters(i-10)
                for j in range(5):
                    self.__parameters[i] += [(parameters_1[j]+parameters_2[j])/2]

    def get_parameters(self, value):
        return self.__parameters[value+10]

    def compute(self, map_, nb_steps, spawn):
        x = spawn
        y = spawn
        self.score = 0
        del self.path[:]
        self.path = [(x, y)]
        for i in range(nb_steps):
            action = random()
            i = 0
            s = self.__parameters[map_[y][x]][i]
            while s < action:
                i += 1
                s += self.__parameters[map_[y][x]][i]
            if i == 1 and y > 0:
                y -= 1
            elif i == 2 and y < len(map_)-1:
                y += 1
            elif i == 3 and x > 0:
                x -= 1
            elif i == 4 and x < len(map_[0])-1:
                x += 1
            self.score += map_[y][x]
            self.path += [(x, y)]

    def new_character(self):
        for i in range(21):
            if random() < PROB_NEW_CHARACTER:
                action = int(random()*5)
                s = 0
                for j in range(5):
                    if j != action:
                        a = self.__parameters[i][j]*0.2
                        s += a
                        self.__parameters[i][j] -= a
                self.__parameters[i][action] += s


window = Window()
