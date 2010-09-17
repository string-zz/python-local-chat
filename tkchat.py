# -*- coding: utf-8 -*-
import socket, threading, cPickle, re
from Tkinter import *
cst_port = 6400
server = client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', cst_port))
mch_address = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
var_connstatus = False

class trd_server(threading.Thread):
 def run(self):
  while True:
   server.listen(1)
   channel, details = server.accept()
   buffer = self.channel.recv(1024)
   if buffer == 'exit':
    txt_area.insert(END, self.details[0] + ' вышел.\n')
   buffer = cPickle.loads(buffer)
   if buffer:
    txt_area.insert(END, self.details[0] + ': ' + buffer + '\n')

trd_server().start()

def act_connect(event):
 global var_connstatus
 if var_connstatus:
  client.close()
 if mch_address.match(edt_address.get()):
  try:
   client.connect((edt_address.get(), cst_port))
  except:
   var_label.set('Соединение невозможно')
  var_label.set('Вы соединены с ' + edt_address.get())
  var_connstatus = True
 else:
  var_label.set('Введён кривой IP')

def act_send(event):
 global var_connstatus
 if var_connstatus:
  buffer = cPickle.dumps(edt_message.get(), 2)
  try:
   client.send(buffer)
  except:
   var_label.set('Ошибка отправки')
  client.close()
  var_label.set('Сообщение отослано')
 else:
  var_label.set('Сначала подключитесь')


frm_root = Tk()
frm_area = Frame(frm_root)
frm_message = Frame(frm_root)
var_label = StringVar()
var_label.set('Введите ниже адрес')
btn_send = Button(frm_message, text = 'Послать сообщение')
btn_connect = Button(frm_message, text = 'Соединиться')
lbl_status = Label(frm_message, text = 'Введите адрес', textvariable = var_label)
txt_area = Text(frm_area)
edt_address = Entry(frm_message)
edt_message = Entry(frm_message)
scr_area = Scrollbar(frm_area)

frm_area["height"] = 700
frm_area["width"] = 300
frm_area["borderwidth"] = 1
frm_area["relief"] = FLAT
txt_area['height'] = 8
txt_area['width'] = 70
scr_area['width'] = 40
frm_message["height"] = 300
frm_message["width"] = 300
frm_message["borderwidth"] = 1
frm_message["relief"] = FLAT
frm_message['height'] = 5
frm_message['width'] = 80
btn_send.bind('<Button-1>', act_send)
frm_root.bind('<Key-Return>', act_send)
btn_connect.bind('<Button-1>', act_connect)
scr_area.config(command = txt_area.yview)
txt_area.focus_set()
txt_area.config(yscrollcommand = scr_area.set)
frm_message['bg'] = lbl_status['bg'] = btn_send['bg'] = btn_connect['bg'] = scr_area['bg'] = '#efebe7'
frm_area.pack(fill = BOTH)
frm_message.pack(fill = BOTH)
txt_area.pack(side = LEFT, fill = BOTH)
scr_area.pack(side = RIGHT, fill = Y)
lbl_status.pack(ipadx = 3, ipady = 3, padx = 8, pady = 8)
edt_address.pack(padx = 8, pady = 8)
btn_connect.pack(ipadx = 3, ipady = 3, padx = 8, pady = 8)
edt_message.pack(padx = 8, pady = 8)
btn_send.pack(ipadx = 3, ipady = 3, padx = 8, pady = 8)
frm_root.title('ケータイあつめタ')
frm_root.mainloop()
if var_connstatus:
 client.send('exit')
