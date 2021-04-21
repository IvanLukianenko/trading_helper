import tkinter as tk
import threading
import time

def add_stock():
    Input = inputAddStock.get("1.0", "end-1c")
    if len(Input) > 0:
        lbox.insert(lbox.size(), inputAddStock.get("1.0", "end-1c"))
        lblCountElems.config(text = f"Всего акций: {lbox.size()}")
        inputAddStock.delete("1.0", "end-1c")

def del_stock():
    for i in reversed(lbox.curselection()):
        lbox.delete(i)
    lblCountElems.config(text = f"Всего акций: {lbox.size()}")

def change_test_label(k):
    testLbl.config(text=f"{k}")


def thread1():
    for i in range(1000):
        time.sleep(2)
        change_test_label(i)


window = tk.Tk()
window.title("TradingApp")
window.geometry("1980x1020")

lblTitle = tk.Label(text="Список отслеживаемых компаний:",
                    font = ("Typofraphy", 12))
lblTitle.place(relx=0.085, rely=0.18)

addStockBtn = tk.Button(window, 
                        text="Добавить акцию", 
                        padx="14px", 
                        pady="3px", 
                        bg="#47525E", 
                        fg="white", 
                        font=("Typofraphy", 12),
                        command=add_stock)

addStockBtn.place(relx=0.083, rely=0.7881)

inputAddStock = tk.Text(window, height = 1,
                width=15,
                pady="3px",
                bg="light yellow",
                font=("Typofraphy", 12))
inputAddStock.place(relx=0.195, rely=0.7881)


delStockBtn = tk.Button(window, 
                        text = "Удалить акцию", 
                        padx="18px", 
                        pady="3px", 
                        bg="#47525E", 
                        fg="white", 
                        font=("Typofraphy", 12),
                        command=del_stock)
                        
delStockBtn.place(relx=0.083, rely=0.8281)


lbox = tk.Listbox(width=30, height=20, font=("Typofraphy", 12), selectbackground="#47525E")
lbox.place(relx=0.0826, rely=0.2109)

lblCountElems = tk.Label(text=f"Всего элементов {lbox.size()}", font = ("Typofraphy", 10))
lblCountElems.place(relx=0.083, rely = 0.7581)

testLbl = tk.Label(text=f"-1")
testLbl.place(relx=0.5, rely=0.5)

thread = threading.Thread(target=thread1)
thread.start()
window.mainloop()