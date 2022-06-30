import os
import zipfile
import requests
import pyemailbot.utils
from pyemailbot.client import EmailBot,EmailMessage
from pydownloader.downloader import Downloader

BASE_ROOT_PATH = 'root/'

def send_root(message):
    listdir = os.listdir(BASE_ROOT_PATH)
    reply = '📄 Root 📄\n\n'
    i=-1
    for item in listdir:
            i+=1
            fname = item
            fsize = pyemailbot.utils.get_file_size(BASE_ROOT_PATH + item)
            prettyfsize = pyemailbot.utils.sizeof_fmt(fsize)
            reply += str(i) + ' - ' + fname + ' ' + prettyfsize + '\n'
    message.reply_file(file='folderlogo.png',text=reply,subject='')

def onenteremail(bot:EmailBot=None,message:EmailMessage=None):
    text = message.mail_content

    reply_subject_text = ''
    reply_subject_file = ''

    if '/start' in text:
        reply = '👋 DeltaFile2Mail 👋\n\n'
        reply+= 'Bot Para Descargar Archivos Desde Internet Directo A Tu Email,'
        reply+= 'Los Archivos Con Mas De 15mb Se Enviaran En Partes\n\n'
        reply+= 'Como Usar?\n'
        reply+= 'Enviar Cualquier 🔗Link De Descarga🔗'
        message.reply_file(file='logo.png',text=reply,subject=reply_subject_text)
        pass

    if '/ls' in text:send_root(message)

    if '/rm' in text:
        index = None
        range = None
        try:
            index = int(str(text).split(' ')[1])
            range = int(str(text).split(' ')[2])
        except:pass
        if index!=None:
           listdir = os.listdir(BASE_ROOT_PATH)
           if range==None:
               rmfile = BASE_ROOT_PATH + listdir[index]
               os.unlink(rmfile)
           else:
               while index<=range:
                   rmfile = BASE_ROOT_PATH + listdir[index]
                   os.unlink(rmfile)
                   index+=1
        send_root(message)

    if '/upload' in text:
        index = None
        range = None
        try:
            index = int(str(text).split(' ')[1])
            range = int(str(text).split(' ')[2])
        except:pass
        if index!=None:
           listdir = os.listdir(BASE_ROOT_PATH)
           if range==None:
               message.reply_text(text=f'📤Subiendo {listdir[index]}...',subject=reply_subject_text)
               file = BASE_ROOT_PATH + listdir[index]
               message.reply_file(file,text=file,subject='')
           else:
               message.reply_text(text=f'📤Subiendo Archivos...',subject=reply_subject_text)
               while index<=range:
                   file = BASE_ROOT_PATH + listdir[index]
                   fname = listdir[index]
                   message.reply_file(file,text=fname,subject='')
                   index+=1
        send_root(message)

    if 'zip' in text:
       index = None
       try:
          index = int(str(text).split(' ')[1])
       except:pass
       if index!=None:
          listdir = os.listdir(BASE_ROOT_PATH)
          ffullpath = BASE_ROOT_PATH + listdir[index]
          message.reply_text(text=f'📚Comprimiendo {listdir[index]}...',subject=reply_subject_text)
          zipname = str(ffullpath).split('.')[0]
          multifile = zipfile.MultiFile(zipname,1024*1024*15)
          zip = zipfile.ZipFile(multifile,  mode='w', compression=zipfile.ZIP_DEFLATED)
          zip.write(ffullpath)
          zip.close()
          multifile.close()
          send_root(message)

    if 'http' in text:
        resp = requests.get(text,allow_redirects=True,stream=True)
        if resp.status_code == 200:
            filename = pyemailbot.utils.get_url_file_name(text,resp)
            filesize = pyemailbot.utils.req_file_size(resp)
            prettyfilesize = pyemailbot.utils.sizeof_fmt(filesize)
            reply = '📡 Descargando...\n'
            reply+= '📄Nombre: '+ filename + '\n' 
            reply+= '🗳Tamaño: '+ prettyfilesize + '\n' 
            message.reply_text(text=reply,subject=reply_subject_text)
        down = Downloader(BASE_ROOT_PATH)
        file = down.download_url(text)
        reply = '💚Archivo Descargado💚\n'
        reply+= '📄Nombre: '+ filename + '\n' 
        reply+= '🗳Tamaño: '+ prettyfilesize + '\n'
        message.reply_text(text=reply,subject=reply_subject_text)
        pass
    print('Finished Procesed Message!')


def main():
    natcli = EmailBot(email='deltafile2mail@gmail.com',email_password='Obysoft2001@',type='gmail')
    loged = natcli.login()
    if loged:
        print('DeltaFile2Mail Runing!')
        natcli.dispatch_receiv_emails(onenteremail=onenteremail)
if __name__ == '__main__':main()
