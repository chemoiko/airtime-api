from html2image import Html2Image
from datetime import datetime
import uuid,base64,os
from django.conf import settings
print(settings.BASE_DIR)
main_path = os.path.join(os.path.dirname(__file__),"receipts/deposit.html")
main_file = open(main_path,"r")
html_contents = main_file.read()


def makeReceipt(name, amount):
    file_name = str(uuid.uuid4()) + ".png"
    #os.path.join(os.path.dirname(__file__),str(uuid.uuid4()) + ".png")
    new_name = html_contents.replace('%name%',"Anywar").replace('%amount%',str(amount)).replace('%date%',str(datetime.now()))
    html_to_img  = Html2Image()
    html_to_img.screenshot(html_str=new_name, save_as=file_name)
    img_file = open(str(file_name),"rb")
    img_bytes = img_file.read()
    img_file.close()
    os.remove(file_name)
    return file_name,str(base64.b64encode(img_bytes).decode('utf-8'))

def makeReceiptHTML(name, amount):
    file_name = name+":"+str(uuid.uuid4()) + ".png"
    #os.path.join(os.path.dirname(__file__),str(uuid.uuid4()) + ".png")
    new_name = html_contents.replace('%name%',"Anywar").replace('%amount%',str(amount)).replace('%date%',str(datetime.now()))
    
    return file_name,str(base64.b64encode(bytes(new_name,'utf-8')).decode('utf-8'))


#base_64 = makeReceipt("Aivan","5000 ugx")
#print(base_64)