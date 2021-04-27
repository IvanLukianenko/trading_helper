import tkinter as tk
import threading
import time
from PIL import ImageTk, Image
import os 
import yaml_reader as yr
import NN
import shutil

def add_stock(stock = None):
    """ Функция добавления акции в список отслеживаемых акций """
    if stock is None:
        Input = inputAddStock.get("1.0", "end-1c")
    else:
        Input = stock
    if len(Input) > 0:
        lbox.insert(lbox.size(), Input)
        lblCountElems.config(text = f"Всего акций: {lbox.size()}")
        if stock is None:
            inputAddStock.delete("1.0", "end-1c")
    

def del_stock():
    """ Функция удаления выделенной акции из списка отслеживаемых акций """
    for i in reversed(lbox.curselection()):
        stock = lbox.get(i)
        os.remove(f"plots/{stock}_plot.png")
        shutil.rmtree(f"models/{stock}", ignore_errors=True)
        lbox.delete(i)
    lblCountElems.config(text = f"Всего акций: {lbox.size()}")
    plotTitle.config(text="График счастья наших клиентов:")
    img = ImageTk.PhotoImage(Image.open(f"img/PR_NN_s_2.png"))
    panelPlot.config(image=img)
    panelPlot.image = img
    list_box = lbox.get(0, tk.END)
    yr.writeYaml(list_box, "config.yaml")



def contact():
    """ Функция, которая создает окно 'Контакты' """
    a = tk.Toplevel()
    a.geometry('990x510')
    a.config(bg = 'grey')
    tk.Label(a, 
            text="Разработчик: Лукьяненко Иван\n"+
                "Должность: студент 2 курса МФТИ ФУПМ\n"+
                "Email: lukianenko.ia@phystech.edu\n"+
                "Telegram: lukianenko_ivan", ).pack(expand=1, side=tk.LEFT)
    

def about():
    """ Функция, которая создает окно 'О нас' """
    a = tk.Toplevel()
    a.geometry('990x510')
    a.config(bg = 'grey')
    tk.Label(a, text="Данное приложение не является первоисточником в купле/продаже акций.\n Данное приложение создано лишь для практики разработки программ с использованием моделей машинного обучения.\nВсем добра!", ).pack(expand=1)
    

def waitForNNS(threads):
    """ Поток, ожидающий конца обучения нейросетей """
    a = tk.Toplevel()
    a.geometry('990x510')
    a.config(bg = 'grey')
    label = tk.Label(a, text="Нейросети обучаются.")
    label.pack(expand=1)
    while(True):
        label.config(text = "Нейросети обучаются..")
        time.sleep(1)
        label.config(text = "Нейросети обучаются...")
        time.sleep(1)
        label.config(text = "Нейросети обучаются.")
        time.sleep(1)
        allIsEnd = True
        for thread in threads:
            if thread.is_alive() == True:
                allIsEnd = False
        if allIsEnd:
            label.config(text = "Нейросети готовы к использованию!!!")
            messageLbl.config(text="Нейросети готовы!")
            a.destroy()
            time.sleep(1)
            break

def follow():
    """ Функция запуска обучения нейронных сетей, вызывается по нажатию кнопки 'Следить' """
    threads = [] 
    list_box = lbox.get(0, tk.END)
    yr.writeYaml(list_box, "config.yaml")

    for stock in list_box:
        models[stock] = None
        threads.append(threading.Thread(target=NN.create_and_train_model, args=(stock, models, )))
        threads[-1].start()
    waitingThread = threading.Thread(target=waitForNNS, args=(threads, ))
    waitingThread.start()

def makePlotThread():
    list_box = lbox.get(0, tk.END)
    for stock in list_box:
        NN.make_plot(models, stock)
    messageLbl.config(text="Графики готовы!")

def makePlots():
    """ Функция построения графиков, вызывается по нажатию кнопки построить графики """
    thread = threading.Thread(target=makePlotThread, args=())
    thread.start()

def changePlot(event):
    """ Функция показа графика выделенной акции из списка отслеживаемых акций """
    stock = lbox.get(lbox.curselection()[0])
    plotTitle.config(text=f"График стоимости акций {stock}")
    img = ImageTk.PhotoImage(Image.open(f"plots/{stock}_plot.png"))
    panelPlot.config(image=img)
    panelPlot.image = img

models = {}

window = tk.Tk()
window.title("TradingApp")
window.geometry("1980x1020")
photo = ImageTk.PhotoImage(file="img/bg_image.jpeg")
w = tk.Label(window, image=photo)
w.pack()
ent = tk.Entry(window)
ent.focus_set()

mainmenu = tk.Menu(window)
window.config(menu = mainmenu)
mainmenu.add_command(label="O нас", command=about)
mainmenu.add_command(label="Контакты", command=contact)


lblTitle = tk.Label(
    text="Список отслеживаемых компаний:",
    font = ("Typofraphy", 12)
)
lblTitle.place(relx=0.085, rely=0.18)

addStockBtn = tk.Button(
    window, 
    text="Добавить акцию", 
    padx="14px", 
    pady="3px", 
    bg="#47525E", 
    fg="white", 
    font=("Typofraphy", 12),
    command=add_stock
)

addStockBtn.place(relx=0.083, rely=0.7881)

inputAddStock = tk.Text(
    window, height = 1,
    width=15,
    pady="3px",
    bg="light yellow",
    font=("Typofraphy", 12)
)
inputAddStock.place(relx=0.195, rely=0.7881)


delStockBtn = tk.Button(
    window, 
    text = "Удалить акцию", 
    padx="18px", 
    pady="3px", 
    bg="#47525E", 
    fg="white", 
    font=("Typofraphy", 12),
    command=del_stock
)
                        
delStockBtn.place(relx=0.083, rely=0.8281)


lbox = tk.Listbox(width=30, height=20, font=("Typofraphy", 12), selectbackground="#47525E")
lbox.place(relx=0.0826, rely=0.2109)

lblCountElems = tk.Label(text=f"Всего элементов {lbox.size()}", font = ("Typofraphy", 10))
lblCountElems.place(relx=0.083, rely = 0.7581)

messageLbl = tk.Label(text=f"Добро пожаловать!")
messageLbl.place(relx=0.5, rely=0.7)

img = ImageTk.PhotoImage(Image.open("img/PR_NN_s_2.png"))
panelPlot = tk.Label(window, image=img)
panelPlot.place(relx=0.3882, rely=0.2109)

followBtn = tk.Button(
    window,
    text="Следить",
    padx="25px", 
    pady="6px", 
    bg="#47525E", 
    fg="white", 
    font=("Typofraphy", 12),
    command=follow
)

lbox.bind(sequence="<<ListboxSelect>>" , func=changePlot)

followBtn.place(relx=0.5282, rely=0.5681)

makePlotBtn = tk.Button(
    window,
    text="Построить графики",
    padx="6px", 
    pady="6px", 
    bg="#47525E", 
    fg="white", 
    font=("Typofraphy", 12),
    command=makePlots
)
makePlotBtn.place(relx=0.42, rely=0.5681)

data = yr.readYaml("config.yaml")

stocks = data['stocks']
if len(stocks) > 0:
    for stock in stocks:
        add_stock(stock)
        models[stock] = NN.create_model()
        models[stock].load_weights(f"models/{stock}/checkpoint")

yahooLbl = tk.Label(window, text="Данные берутся с сайта finance.yahoo, точные названия акций уточняйте из источника.")
yahooLbl.place(relx=0.33, rely=0.9)
plotTitle = tk.Label(window, text="График счастья наших пользователей!", font=("Typofraphy", 12))
plotTitle.place(relx=0.39, rely=0.19)

window.mainloop()