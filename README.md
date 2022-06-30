# deltafile2mailbot
Bot de gmail para manejar descargas de archivos x correo electronico 
# API pyemailbot
   ``` 
   from pyemailbot.client import EmailBot,EmailMessage
   def onenteremail(bot,message):
       pass
   def main():
    cli = EmailBot(email='xxx@gmail.com',email_password='xxx',type='gmail')
    loged = cli.login()
    if loged:
        print('DeltaFile2Mail Runing!')
        cli.dispatch_receiv_emails(onenteremail=onenteremail)
   if __name__ == '__main__':main()
