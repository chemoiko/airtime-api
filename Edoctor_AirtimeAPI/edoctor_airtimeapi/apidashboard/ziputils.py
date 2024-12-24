import zipfile36 as zipfile
import os
from edoctor_airtimeapi import settings
import time
def makeZip(uploaded_files,user_name):
    time_stamp = int(time.time())
    media_root = settings.MEDIA_ROOT
    
    tmp_name = f"{user_name}_{time_stamp}"
    file_path = os.path.join(settings.MEDIA_ROOT, tmp_name)
    tmp_zip = f"{tmp_name}.zip"
    print("\n\tcreating zip archieve at: ", file_path)
    with zipfile.ZipFile(tmp_zip, 'w') as zip_file:
        for uploaded_file in uploaded_files:
            #file_path = os.path.join(settings.MEDIA_ROOT, )
            zip_file.write(uploaded_file)
        zip_file.close
        return zip_file.filename