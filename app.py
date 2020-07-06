from tkinter import *
from tkinter import messagebox as msg
from tkinter.ttk import Treeview
import dbm

class GUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.store = dict()
        self.db = dbm.open("db/DB", "c")
        self.name = StringVar(value="admin")
        self.password = StringVar(value="admin")
        self.initUI()

    def initUI(self):
        self.pack(fill = BOTH, expand = True)

        frame1 = Frame(self)
        frame1.pack(fill = X)

        frame2 = Frame(self)
        frame2.pack(fill=X, pady = 30, padx = 20)

        self.frames = (frame1, frame2)

        mainLabel = Label(frame1, text = "Login", font = "ComicSans 16", bg = "#3b5998", fg = "white")
        mainLabel.pack(fill = X)

        nameLabel = Label(frame2, text = "Name: ", font = "ComicSans 12")
        nameLabel.grid(row = 0, column = 0, sticky = W)

        self.nameEntry = Entry(frame2, textvariable = self.name)
        self.nameEntry.grid(row = 0, column = 1)

        passwordLabel = Label(frame2, text = "Password: ", font = "ComicSans 12")
        passwordLabel.grid(row = 1, column = 0)

        self.passwordEntry = Entry(frame2, show = "*", textvariable = self.password)
        self.passwordEntry.grid(row = 1, column = 1)

        loginButton = Button(frame2, text = "Login", font = "ComicSans 12", command = self.eval)
        loginButton.grid(row = 0, column = 2, rowspan = 2)

        Grid.columnconfigure(frame2, 1, weight = 1)
        Grid.columnconfigure(frame2, 2, weight = 1)
        Grid.columnconfigure(frame2, 3, weight = 1)

    def eval(self):
        name = self.nameEntry.get()
        password = self.passwordEntry.get()

        if name == "":
            msg.showerror("Error", "Name can't be empty")

        elif password == "":
            msg.showerror("Error", "Password can't be empty")
        else:
            usn, pwd = self.db["Login"].decode().split(",")

            if name == usn and password == pwd:
                msg.showinfo("Welcome", f"Welcome mr.{name}")
                self.login()

            else:
                msg.showerror("Error", "Username or password is wrong")

    def login(self):
        global width, height
        width = 600
        height = 350
        root.geometry(f"{width}x{height}+{screenWidth//2 - width//2}+{screenHeight//2 - height//2}")

        for i in self.frames:
            i.destroy()

        frame1 = Frame(self)
        frame1.pack(fill = X)

        frame2 = Frame(self)
        frame2.pack(fill = X, padx = 20, pady = 30)

        mainLabel = Label(frame1, text = "Passwords", font = "ComicSans 16", bg = "#3b5998", fg = "white")
        mainLabel.pack(fill = X)

        self.tree = Treeview(frame2, selectmode = 'browse')
        self.tree.grid(row = 0, column = 0, rowspan = 3, sticky = "ns")

        vsb = Scrollbar(frame2, orient = "vertical", command = self.tree.yview)
        vsb.grid(row = 0, column = 1, rowspan = 3, sticky = "wens")
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree["columns"] = ("two", "three")
        self.tree.column("#0", width = 120, anchor = CENTER)
        self.tree.column("two", width = 120, anchor = CENTER)
        self.tree.column("three", width = 120, anchor = CENTER)

        self.tree.heading("#0", text="Site")
        self.tree.heading("two", text="Username")
        self.tree.heading("three", text="Password")

        self.show()

        addButton = Button(frame2, text = "Add", width = 7, command = self.add)
        addButton.grid(row = 0, column = 2)

        delButton = Button(frame2, text = "Delete", width = 7, command = self.delete)
        delButton.grid(row = 1, column = 2)

        updateButton = Button(frame2, text = "Update", width = 7, command = self.upt)
        updateButton.grid(row = 2, column = 2)

        Grid.columnconfigure(frame2, 2, weight = 1)

    def show(self):
        self.tree.delete(*self.tree.get_children())
        self.dic = {key.decode(): [value.decode().split(",")[0], value.decode().split(",")[1]] for key, value in self.db.items()}
        self.value = [(key, self.dic[key]) for key in sorted(self.dic)]

        for var in self.value:
            site = var[0]
            if site == "Login": continue
            username = var[1][0]
            password = var[1][1]
            self.tree.insert("", "end", text = f"{site}", values = (username, password))

    def add(self):
        global width, height
        width, height = 400, 100

        self.top = Toplevel()
        self.top.focus()
        self.top.title("Add Password")
        self.top.geometry(f"{width}x{height}+{screenWidth//2 - width//2}+{screenHeight//2 - height//2}")

        siteLabel = Label(self.top, text = "Site: ", font = "ComicSans 12")
        siteLabel.grid(row = 0, column = 0)

        self.siteEntry = Entry(self.top)
        self.siteEntry.grid(row = 0, column = 1)

        usernameLabel = Label(self.top, text="Username: ", font="ComicSans 12")
        usernameLabel.grid(row=1, column=0)

        self.usernameEntry = Entry(self.top)
        self.usernameEntry.grid(row=1, column=1)

        passwordLabel = Label(self.top, text="Password: ", font="ComicSans 12")
        passwordLabel.grid(row=2, column=0)

        self.passwordEntry = Entry(self.top)
        self.passwordEntry.grid(row=2, column=1)

        addButton = Button(self.top, text = "Add", font="ComicSans 12", width = 7, command = self.insert)
        addButton.grid(row = 1, column = 2)

        Grid.columnconfigure(self.top, 0, weight = 1)
        Grid.columnconfigure(self.top, 1, weight = 1)
        Grid.columnconfigure(self.top, 2, weight = 1)

        Grid.rowconfigure(self.top, 0, weight = 1)
        Grid.rowconfigure(self.top, 1, weight = 1)
        Grid.rowconfigure(self.top, 2, weight = 1)

    def insert(self):
        site = self.siteEntry.get()
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()

        if site != "" and username != "" and password != "":
            self.db[site] = f"{username},{password}"
            self.top.destroy()
            self.show()

        else:
            msg.showerror("Error", "Yo must fill all blank spaces")

    def delete(self):
        currItem = self.tree.focus()
        selected = self.tree.item(currItem)["text"]

        if selected == "":
            msg.showerror("Error", "You need to select an element to delete")
        else:
            del self.db[selected]
            self.show()

    def upt(self):
        currItem = self.tree.focus()
        selected = self.tree.item(currItem)["text"]

        if selected == "":
            msg.showerror("Error", "You need to select an element to update")
        else:
            self.new(selected)

    def new(self, selected):
        global width, height
        width, height = 400, 100
        username = self.db[selected].decode().split(",")[0]
        usn = StringVar(value=username)

        self.top = Toplevel()
        self.top.focus()
        self.top.title("Update Password")
        self.top.geometry(f"{width}x{height}+{screenWidth // 2 - width // 2}+{screenHeight // 2 - height // 2}")

        usernameLabel = Label(self.top, text="Username: ", font="ComicSans 12")
        usernameLabel.grid(row=0, column=0)

        self.usernameEntry = Entry(self.top, textvariable = usn)
        self.usernameEntry.grid(row=0, column=1)

        passwordLabel = Label(self.top, text="Password: ", font="ComicSans 12")
        passwordLabel.grid(row=1, column=0)

        self.passwordEntry = Entry(self.top)
        self.passwordEntry.grid(row=1, column=1)

        addButton = Button(self.top, text="Update", font="ComicSans 12", width=7)
        addButton.grid(row=0, column=2, rowspan = 2)
        addButton.bind("<ButtonRelease-1>", lambda event: self.db_update(selected))

        Grid.columnconfigure(self.top, 0, weight=1)
        Grid.columnconfigure(self.top, 1, weight=1)
        Grid.columnconfigure(self.top, 2, weight=1)

        Grid.rowconfigure(self.top, 0, weight=1)
        Grid.rowconfigure(self.top, 1, weight=1)
        Grid.rowconfigure(self.top, 2, weight=1)

    def db_update(self, selected):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()

        if username != "" and password != "":
            del self.db[selected]
            self.db[selected] = f"{username},{password}"
            self.top.destroy()
            self.show()

        else: msg.showerror("Error", "Yo must fill all blank spaces")

if __name__ == '__main__':
    root = Tk()
    app = GUI(root)
    root.title("Password Keeper")
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    width = 400
    height = 150
    root.geometry(f"{width}x{height}+{screenWidth//2 - width//2}+{screenHeight//2 - height//2}")
    root.mainloop()