from tkinter import *
from PIL import  Image ,  ImageTk
root=Tk()
root.title("Greenviz LoginPage")
root.geometry("12000x700")

bg_img=ImageTk.PhotoImage(Image.open("C:/Users/Anil Kumar/PycharmProject/loginpage/resized one.jpg"))
bg_label=Label(root , image=bg_img)
bg_label.image=bg_img
bg_label.grid()

login_frame=Frame(root , bg="white")
login_frame.place(x=300 , y=50 , height=625, width=475)

title=Label(login_frame , text="Greenviz" , font=("times new roman" ,32, "bold") , fg="#d77337" , bg="white")
title.place(x=90 ,y=20)

des=Label(login_frame , text="Admin Registration Page" , font=("Goudy old style" ,16 , "bold") , fg="#d25d17" , bg="white")
des.place(x=90 ,y=80)

name_label=Label(login_frame , text="Name :-" , font=("Goudy old style" ,13 , "bold") , fg="gray" , bg="white")
name_label.place(x=90 ,y=120)
name_entry=Entry(login_frame , font=("times new roman" , 13), bg="lightgray")
name_entry.insert(0 , "Enter your name here")
name_entry.place(x=90 , y=150 , height=30 , width=300)

mail_label=Label(login_frame , text="E-Mail :-" , font=("Goudy old style" ,13 , "bold") , fg="gray" , bg="white")
mail_label.place(x=90 ,y=260)
mail_entry=Entry(login_frame , font=("times new roman" , 13), bg="lightgray")
mail_entry.insert(0 , "Enter your mail-id here")
mail_entry.place(x=90 , y=290 , height=30 , width=300)

reg_label=Label(login_frame , text="College ID  ::" , font=("Goudy old style" ,13 , "bold") , fg="gray" , bg="white")
reg_label.place(x=90 ,y=190)
reg_entry=Entry(login_frame , font=("times new roman" , 13), bg="lightgray")
reg_entry.insert(0 , "Enter your ID")
reg_entry.place(x=90 , y=220 , height=30 , width=300)

branch_label=Label(login_frame , text="Department ::" , font=("Goudy old style" ,13 , "bold") , fg="gray" , bg="white")
branch_label.place(x=90 ,y=330)
branch_entry=Entry(login_frame , font=("times new roman" , 13), bg="lightgray")
branch_entry.insert(0 , "Enter your Department Here")
branch_entry.place(x=90 , y=360 , height=30 , width=300)

pass_label=Label(login_frame , text="Password :-" , font=("Goudy old style" ,13 , "bold") , fg="gray" , bg="white")
pass_label.place(x=90 ,y=400)
pass_entry=Entry(login_frame , font=("times new roman" , 13), bg="lightgray")
pass_entry.insert(0 , "DDMMYYYY")
pass_entry.place(x=90 , y=430 , height=30 , width=300)

reg_button=Button(root , text="Register" , fg="white" , bg="#d77337",font=("times new roman",18))
reg_button.place(x=340, y=610, height=30 , width=130)
reg1_button=Button(root , text=" Back to Home" , fg="white" , bg="#d77337",font=("times new roman",15))
reg1_button.place(x=560, y=610, height=30 , width=150)


root.mainloop()