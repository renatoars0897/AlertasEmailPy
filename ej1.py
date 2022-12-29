import smtplib,ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import consultas
import extras
from datetime import datetime
from tkinter import *

master = Tk()
master.config(bg='Red')
master.geometry('500x140')
master.resizable(0,0)
master.title('Envio de Alertas SSED')
p = Entry(master, width = 70,show='*')
Label(master, text="Contraseña").pack()
p.pack()

p.focus_set()
Label(master, text="Destinatario").pack()
d = Entry(master, width = 70)
d.pack()

d.focus_set()

b = Button(master, text = "OK", width = 10, command = master.quit)
b.pack()

mainloop()

now = datetime.now()
resultado=extras.current_date_format(now)


cuenta=consultas.cuenta_exp()
values = ','.join(str(v) for v in cuenta)
expedient=consultas.obtenerExp()
fecha=consultas.fecha()
espe=consultas.especialista()
     

fc='<BR>'.join(map(str,fecha))

username="rariasbe@pj.gob.pe"
password=p.get()

destinatario=d.get()
asunto=(f"""Ingresos al {resultado}""")

mensaje = MIMEMultipart("alternative")
mensaje["Subject"]=asunto
mensaje["From"]=username
mensaje["To"]=destinatario

html= f"""
<html>
<body>
<p><font size=6> Dr(a). {espe} Usted posee <b>{values}</b> escritos en estado pendiente de proveer.</font><br>
 Los Expedientes son los siguiente:<br>
 <table>
    <tr>
        <td><b>Expediente</b></td>
        <td>          </td>
        <td><b>Fecha de Ingreso</b></td>
    </tr>
  <tr>

    <td>{expedient}</td>
    <td>======></td>
    <td>{fc}</td>

  </tr>
 
 </table>
 
</body>
</html>"""

parte_html = MIMEText(html,"html")
mensaje.attach(parte_html)
context= ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context) as server:
    server.login(username,password)
    server.sendmail(username,destinatario,mensaje.as_string())