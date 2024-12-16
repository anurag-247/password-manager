from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    for char in range(nr_letters):
        password_list.append(random.choice(letters))

    for char in range(nr_symbols):
        password_list += random.choice(symbols)

    for char in range(nr_numbers):
        password_list += random.choice(numbers)

    random.shuffle(password_list)

    password = ""
    for char in password_list:
        password += char

    # print(f"Your password is: {password}")
    pyperclip.copy(password)
    password_input.insert(0, password)


# ---------------------------- SEARCH WEBSITE ------------------------------- #


def on_search():
    website = website_input.get()
    try:
        with open("data.json", "r") as data_file:
            # Reading and updating data
            data = json.load(data_file)
            email = data[website]["email"]
            password = data[website]["password"]
    except KeyError:
        messagebox.showerror(title="Error", message="Website not found")
    else:
        messagebox.showinfo(title=f"Details of {website} account", message=f"Email: {email}\nPassword: {password}")


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    if len(website) < 1:
        messagebox.showerror(title="Error", message="Please provide a website")
    elif len(email) < 1:
        messagebox.showerror(title="Error", message="Please provide an email")
    elif len(password) < 1:
        messagebox.showerror(title="Error", message="Please provide a password")
    else:
        try:
            with open("data.json", "r+") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # data.update(new_data)
            with open("data.json", "r+") as data_file:
                data[website]= new_data[website]
                # data_file.seek(0)
                json.dump(data, data_file, indent=4)

        finally:
            messagebox.showinfo(title="INFO", message="password saved")
            website_input.delete(0, END)
            password_input.delete(0, END)
            website_input.focus()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

website_input = Entry(width=35)
website_input.grid(row=1, column=1, columnspan=2)
website_input.focus()

email_input = Entry(width=35)
email_input.grid(row=2, column=1, columnspan=2)
email_input.insert(0, "xyz@example.com")

password_input = Entry(width=21)
password_input.grid(row=3, column=1)

submit = Button(text="Add", width=36, command=save)
submit.grid(row=4, column=1, columnspan=2)

generate = Button(text="Generate password", command=generate_password)
generate.grid(row=3, column=2)

search_button = Button(text="Search", command=on_search)
search_button.grid(row=1, column=3)

window.mainloop()
