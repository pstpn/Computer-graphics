from algorithms import CAP_algorithm_with_ordered_list_of_edges, Point
import tkinter as tk
from tkinter import colorchooser, messagebox
from config import *
import time


is_ctrl_pressed = 0
ctrl_pos = set()
root = tk.Tk()
root.title("Лабораторная работа №5")
root["bg"] = MAIN_COLOUR

root.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
root.resizable(height=False, width=False)

def clearScreen():

    allFigures.clear()
    currentFigure.clear()
    listPoint_scroll.delete(0, tk.END)
    canvasField.delete("all")


def fill_all_figures():

    if not allFigures and not currentFigure:
        messagebox.showwarning("Ошибка!", "Фигура для закраски не введена!")
    elif not allFigures and  currentFigure:
        messagebox.showwarning("Ошибка!", "Фигура для закраски не замкнута!")
    else:
        delay = False
        if methodDraw.get() == 0:
            delay = True
        time_start = time.time()
        CAP_algorithm_with_ordered_list_of_edges(canvasField, allFigures, colour=LINE_COLOUR, delay=delay)
        time_end = time.time() - time_start
        if round(time_end * 1000, 2) < 1000:
            timeLabel["text"] = "Время закраски: " + str(round(time_end * 1000, 2)) + " mc."
        else:
            timeLabel["text"] = "Время закраски: " + str(round(time_end, 2)) + " c."


def get_point():

    x = xEntry.get()
    y = yEntry.get()
    if not x or not y:
        messagebox.showinfo("Ошибка!", "Координаты точек не введены!")
    else:
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            messagebox.showinfo("Ошибка!", "Координаты точек должны быть целыми!")
            return
        add_point(x, y)


def close_figure():

    global currentFigure, canvasField
    if len(currentFigure) > 2:
        canvasField.create_line(currentFigure[-1].x, currentFigure[-1].y, currentFigure[0].x, currentFigure[0].y)

        allFigures.append(currentFigure)
        currentFigure = []
    elif len(currentFigure) == 0:
        messagebox.showwarning("Ошибка!", "Точки фигуры не введены!")
    else:
        messagebox.showwarning("Ошибка!", "Не удалось замкнуть фигуру, так как введено меньше 3 точек")

    canvasField.delete("new")


def findIndexForListPointScroll(allArraysFigure, currentArray):

    index = 0

    for pointFigure in allArraysFigure:
         index += len(pointFigure) + 1
    index += len(currentArray)

    return index


def add_point(x, y):

    if Point(x, y) not in currentFigure:
        if currentFigure:
            canvasField.create_line(currentFigure[-1].x, currentFigure[-1].y, x, y)

        index = findIndexForListPointScroll(allFigures, currentFigure)
        listPoint_scroll.insert(index,  "{:3d}. ({:4d}, {:4d})".format(index + 1, x, y))
        currentFigure.append(Point(x, y))
    else:
        messagebox.showwarning("Ошибка!", "Данная точка уже существует!")


def press_key(event):

    global is_ctrl_pressed
    if event.keysym == "Control_L":
        if is_ctrl_pressed == 0:
            is_ctrl_pressed = 1

def release_key(event):

    global is_ctrl_pressed
    if event.keysym == "Control_L":
        if is_ctrl_pressed == 1:
            is_ctrl_pressed = 0


def moving_line(event):

    global ctrl_pos
    if len(currentFigure) != 0:
        if is_ctrl_pressed == 0:
            cur_pos = (event.x, event.y)
            canvasField.delete("new")
            canvasField.create_line(currentFigure[-1].x, currentFigure[-1].y, cur_pos[0], cur_pos[1], tag="new")
        else:
            x = event.x - currentFigure[-1].x
            y = event.y - currentFigure[-1].y

            if abs(y) >= abs(x):
                cur_pos = (currentFigure[-1].x, event.y)
            else:
                cur_pos = (event.x, currentFigure[-1].y)

            ctrl_pos = cur_pos

            canvasField.delete("new")
            canvasField.create_line(currentFigure[-1].x, currentFigure[-1].y, cur_pos[0], cur_pos[1], tag="new")


def add_point_figure_onClick(event):

    if is_ctrl_pressed != 0:
        x, y = ctrl_pos
    else:
        x, y = event.x,  event.y
    add_point(x, y)


def get_colour_line():

    color_code = colorchooser.askcolor(title="Choose colour line")
    set_linecolour(color_code[-1])


def set_linecolour(color):

    global LINE_COLOUR
    LINE_COLOUR = color
    lineCurColourLabel.configure(bg=LINE_COLOUR)


def show_info():

    messagebox.showinfo('Информация о программе',
                        'Программа реализует алгоритм закраски фигуры при помощи '
                        'упорядоченного списка активных ребер.\n\n'
                        'Выполнил: Постнов Степан, ИУ7-41Б.')


dataFrame = tk.Frame(root, width=DATA_FRAME_WIGHT, height=DATA_FRAME_HEIGHT)
dataFrame["bg"] = MAIN_FRAME_COLOR

dataFrame.pack(side=tk.LEFT, padx=BORDERS_SPACE, fill=tk.Y)

modeMakeLabel = tk.Label(dataFrame, bg=MAIN_COLOUR_LABEL_BG, text="Задержка",
                         font=("Ariel", 10),
                         fg=MAIN_COLOUR_LABEL_TEXT, relief=tk.SOLID)

yColourLine = 3
modeDraw = yColourLine + 3.1
makePoint = modeDraw + 2.1

infoBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Информация о программе", font=("Ariel", 10),
                    command=show_info)
infoBtn.place(x=0, y=10, width=DATA_FRAME_WIGHT - 50, height=DATA_FRAME_HEIGHT // COLUMNS)

chooseColourMainLabel = tk.Label(dataFrame, bg=MAIN_COLOUR_LABEL_BG, text="Цвет закраски",
                     font=("Ariel", 10), fg=MAIN_COLOUR_LABEL_TEXT, relief=tk.SOLID)

size = (DATA_FRAME_WIGHT // 1.6) // 8
chooseColourMainLabel.place(x=0, y=45, width=DATA_FRAME_WIGHT, height=DATA_FRAME_HEIGHT // COLUMNS)

lineColourLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Цвет:",
                     font=("Ariel", 10),
                     fg=MAIN_COLOUR_LABEL_TEXT)

lineCurColourTextLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Текущий цвет:",
                     font=("Ariel", 10),
                     fg=MAIN_COLOUR_LABEL_TEXT)

lineCurColourLabel = tk.Label(dataFrame, bg="blue")


whiteLine = tk.Button(dataFrame, bg="white", activebackground="white",
                    command=lambda: set_linecolour("white"))
yellowLine = tk.Button(dataFrame, bg="yellow", activebackground="yellow",
                     command=lambda: set_linecolour("yellow"))
orangeLine = tk.Button(dataFrame, bg="orange", activebackground="orange",
                     command=lambda: set_linecolour("orange"))
redLine = tk.Button(dataFrame, bg="red", activebackground="red",
                  command=lambda: set_linecolour("red"))
purpleLine = tk.Button(dataFrame, bg="purple", activebackground="purple",
                     command=lambda: set_linecolour("purple"))
greenLine = tk.Button(dataFrame, bg="green", activebackground="green",
                    command=lambda: set_linecolour("green"))
darkGreenLine = tk.Button(dataFrame, bg="darkgreen", activebackground="darkgreen",
                        command=lambda: set_linecolour("darkgreen"))
lightBlueLine = tk.Button(dataFrame, bg="lightblue", activebackground="lightblue",
                        command=lambda: set_linecolour("lightblue"))

lineColourBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text='Изменить цвет закраски', font=("Ariel", 10), command=get_colour_line)

lineColourLabel.place(x=0, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 3, height=DATA_FRAME_HEIGHT // COLUMNS)

whiteLine.pack(anchor=tk.NW, padx=BORDERS_SPACE)
whiteLine.place(x=DATA_FRAME_WIGHT // 3, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS - 10)
yellowLine.place(x=DATA_FRAME_WIGHT // 3 + size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS - 10)
orangeLine.place(x=DATA_FRAME_WIGHT // 3 + 2 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS - 10)
redLine.place(x=DATA_FRAME_WIGHT // 3 + 3 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS - 10)
purpleLine.place(x=DATA_FRAME_WIGHT // 3 + 4 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS - 10)
greenLine.place(x=DATA_FRAME_WIGHT // 3 + 5 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS - 10)
darkGreenLine.place(x=DATA_FRAME_WIGHT // 3 + 6 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS - 10)
lightBlueLine.place(x=DATA_FRAME_WIGHT // 3 + 7 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size, height=DATA_FRAME_HEIGHT // COLUMNS - 10)

lineColourBtn.place(x=0, y=(yColourLine + 1) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 1.5, height=DATA_FRAME_HEIGHT // COLUMNS)
lineCurColourTextLabel.place(x=0, y=(yColourLine + 2) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2, height=DATA_FRAME_HEIGHT // COLUMNS)
lineCurColourLabel.place(x=DATA_FRAME_WIGHT // 2, y=(yColourLine + 2) * DATA_FRAME_HEIGHT // COLUMNS + 5, width=DATA_FRAME_WIGHT // 8, height=DATA_FRAME_HEIGHT // COLUMNS - 10)

methodDraw = tk.IntVar()
methodDraw.set(1)
modeMakeLabel.place(x=0, y=modeDraw * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT, height=DATA_FRAME_HEIGHT // COLUMNS)
tk.Radiobutton(dataFrame, variable=methodDraw, text="Включить", value=0, bg=MAIN_FRAME_COLOR,
                font=("Ariel", 10), justify=tk.LEFT, fg=MAIN_COLOUR_LABEL_TEXT, selectcolor="black",
                activebackground=MAIN_FRAME_COLOR, activeforeground=MAIN_COLOUR_LABEL_TEXT,
               ).place(x=10, y=(modeDraw + 1) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2 - 2 * BORDERS_SPACE,
                       height=DATA_FRAME_HEIGHT // COLUMNS)
tk.Radiobutton(dataFrame, variable=methodDraw, text="Выключить", value=1, bg=MAIN_FRAME_COLOR,
                font=("Ariel", 10), justify=tk.LEFT, fg=MAIN_COLOUR_LABEL_TEXT, selectcolor="black",
                activebackground=MAIN_FRAME_COLOR, activeforeground=MAIN_COLOUR_LABEL_TEXT,
               ).place(x=DATA_FRAME_WIGHT // 2, y=(modeDraw + 1) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2 - 2 * BORDERS_SPACE,
                       height=DATA_FRAME_HEIGHT // COLUMNS)

pointMakeLabel = tk.Label(dataFrame, bg=MAIN_COLOUR_LABEL_BG, text="Координаты новой точки",
                          font=("Ariel", 10),
                          fg=MAIN_COLOUR_LABEL_TEXT, relief=tk.SOLID)

msgAboutPoint = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="X                          Y",
                         font=("Ariel", 10),
                         fg=MAIN_COLOUR_LABEL_TEXT)

xEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Ariel", 10), fg=MAIN_FRAME_COLOR, justify="center")
yEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Ariel", 10), fg=MAIN_FRAME_COLOR, justify="center")

drawPointBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Добавить точку", font=("Ariel", 10),
                         command=get_point)
drawCloseBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Замкнуть фигуру", font=("Ariel", 10),
                         command=close_figure)

pointMakeLabel.place(x=0, y=makePoint * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT, height=DATA_FRAME_HEIGHT // COLUMNS)
msgAboutPoint.place(x=0, y=(makePoint + 1) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT, height=DATA_FRAME_HEIGHT // COLUMNS)

xEntry.place(x=0, y=(makePoint + 2) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2, height=DATA_FRAME_HEIGHT // COLUMNS)
yEntry.place(x=2 * DATA_FRAME_WIGHT // 4, y=(makePoint + 2) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2, height=DATA_FRAME_HEIGHT // COLUMNS)

makePoint += 0.2
drawPointBtn.place(x=0, y=(makePoint + 3) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2, height=DATA_FRAME_HEIGHT // COLUMNS)
drawCloseBtn.place(x=DATA_FRAME_WIGHT // 2 + 10, y=(makePoint + 3) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2 - 10, height=DATA_FRAME_HEIGHT // COLUMNS)

listPoint_scroll = tk.Listbox(font=("Ariel", 10))
makePoint += 0.4
listPoint_scroll.place(x=40, y=(makePoint + 4) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT - 60, height=6 * DATA_FRAME_HEIGHT // COLUMNS)

currentFigure = []
allFigures = []

canvasField = tk.Canvas(root, bg=CANVAS_COLOUR)
canvasField.place(x=WINDOW_WIDTH * DATA_SITUATION + BORDERS_SPACE, y=BORDERS_SPACE, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)

root.bind("<KeyPress>", press_key)
root.bind("<KeyRelease>", release_key)

canvasField.bind("<Button-1>", add_point_figure_onClick)
canvasField.bind("<Button-3>", lambda event: close_figure())
canvasField.bind("<Motion>", moving_line)

timeLabel = tk.Label(root, bg="gray", text="Время закраски: ",
                             font=("Ariel", 10),
                             fg=MAIN_COLOUR_LABEL_TEXT)

fillingBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Выполнить закраску", font=("Ariel", 10), command=fill_all_figures)
clearCanvasBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Очистить экран", font=("Ariel", 10), command=clearScreen)

timeLabel.place(x=DATA_FRAME_WIGHT + 2 * BORDERS_SPACE, y=CANVAS_HEIGHT + BORDERS_SPACE - DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT - 60, height=DATA_FRAME_HEIGHT // COLUMNS)
fillingBtn.place(x=40, y=(makePoint + 11) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT - 80, height=DATA_FRAME_HEIGHT // COLUMNS)
clearCanvasBtn.place(x=40, y=(makePoint + 12) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT - 80, height=DATA_FRAME_HEIGHT // COLUMNS)

root.mainloop()
