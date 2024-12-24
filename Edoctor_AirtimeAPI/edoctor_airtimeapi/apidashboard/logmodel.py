from .models import APIcredentials, DashboardUsers, Companies
#from .ExtralLogmodel import getExternalLog
from airtimeapi.logmodel import LogModel
class Logs:

    def __init__(self):
        pass
    def allLogs(self, dashboard_user, log_type,log_params=None):
        api_keys = self.getExtraLogs(dashboard_user,"*", log_params)
    def getLog(self, dashboard_user, log_type,log_params=None):
        if log_type == "apikeys":
            return self.getAPIKeys(dashboard_user)
        elif log_type == "all_admins":
            return self.getAdmins()
        elif log_type == "all_users":
            return self.getUsers()
        elif log_type == "all_companies":
            return self.getCompanies(dashboard_user)
        elif log_type == "user_keys":
            return self.getProductionKeys(dashboard_user)
        elif log_type == "verify_requests":
            print("verify requests list")
            return self.getUnverifiedCompanies(dashboard_user)
        else:
            return self.getExtraLogs(dashboard_user,log_type,log_params)
    def getAPIKeys(self, for_user):
        user_credentials = APIcredentials.objects.filter(owner=for_user)

        all_keys = []

        for user_credential in user_credentials:
            token_username = user_credential.token_user.username
            is_pdt_key = user_credential.is_production_key
            is_validated = user_credential.is_validated
        
            user_token= user_credential.token
            token_key = user_token.key
            token_datetime = user_token.created

            token_date = token_datetime.strftime("%d/%B/%Y")
            token_time = token_datetime.strftime("%H:%M:%S")

            log = [
                    token_username, token_key, "production" if is_pdt_key else "sandbox" , is_validated , token_date, token_time
                ]
            print("using log: ",log)
            all_keys.append(log)
        return all_keys
    
    def getAdmins(self):
        dashboard_users = DashboardUsers.objects.filter(user_role = "admin")

        all_keys = []

        for dashbord_user in dashboard_users:
            dashboard_username = dashbord_user.user.username
            dashboard_useremail = dashbord_user.user.email
            dashbord_usertelno = ""
            db_tmp_creator = dashbord_user.created_by
            dashbord_usercreator = "self" if  db_tmp_creator== None else db_tmp_creator.username
            
            created_datetime = dashbord_user.created_on

            created_date = created_datetime.strftime("%d/%B/%Y")
            created_time = created_datetime.strftime("%H:%M:%S")

            log = [
                    dashboard_username, dashboard_useremail , dashbord_usertelno, dashbord_usercreator , created_date, created_time
                ]
            print("using log: ",log)
            all_keys.append(log)
        return all_keys
    
    def getUsers(self):
        dashboard_users = DashboardUsers.objects.filter(user_role = "developer")

        all_keys = []

        for dashbord_user in dashboard_users:
            dashboard_usernames = dashbord_user.user.get_full_name()
            dashboard_useremail = dashbord_user.user.email
            dashbord_user_verified = dashbord_user.user.is_active
            #db_tmp_creator = dashbord_user.created_by
            dashbord_username = dashbord_user.user.get_username()
            #"self" if  db_tmp_creator== None else db_tmp_creator.username
            
            created_datetime = dashbord_user.created_on

            created_date = created_datetime.strftime("%d/%B/%Y")
            created_time = created_datetime.strftime("%H:%M:%S")

            log = [
                    dashboard_usernames, dashboard_useremail , dashbord_user_verified, dashbord_username , created_date, created_time
                ]
            print("using all_user log: ",log)
            all_keys.append(log)
        return all_keys
    
    def getCompanies(self, dashboard_user):
        current_user_companies = Companies.objects.filter(user =dashboard_user)

        all_keys = []

        for current_user_company in current_user_companies:
            co_name = current_user_company.company_name
            co_email = current_user_company.company_email
            co_telno = current_user_company.company_telno
            co_verification_status = current_user_company.verification_status
            
            co_created_at = current_user_company.created_on

            created_date = co_created_at.strftime("%d/%B/%Y")
            created_time = co_created_at.strftime("%H:%M:%S")

            log = [
                    co_name, co_email , co_telno, co_verification_status , f"{created_date} {created_time}",""
                ]
            print("using log: ",log)
            all_keys.append(log)
        return all_keys
    
    def getUnverifiedCompanies(self, dashboard_user):
        current_user_companies = Companies.objects.all()

        all_keys = []

        for current_user_company in current_user_companies:
            co_name = current_user_company.company_name
            co_email = current_user_company.company_email
            co_telno = current_user_company.company_telno
            co_documents = current_user_company.company_docs.all()
            co_uuid = current_user_company.company_uuid
            co_created_at = current_user_company.created_on

            root_div = '''<div class="container-fluid">
                            <div class="row">
                                <div class="col-sm-6">
                                    1 of three columns
                                </div>
                                <div class="col-sm-6">
                                    2 of three columns
                                </div>
                                <div class="col-sm-6">
                                    3 of three columns
                                </div>
                            </div>
                        </div>'''
            head_div = '<div class="container-fluid"><div class="row">'
            row_div  =  '<div class="row">'
            tail_div = "</div>"
            
            main_div = head_div
            div_count = 0
            doc_count = 0
            for co_document in co_documents:
                doc_name = co_document.uploaded_file.name.split('/')[1]

                tmp_div = ""
                #if (div_count == 2) or (div_count == 0):
                #    tmp_div = f"{row_div}"
                formx = f'''<form action="/dashboard/getDoc" target="_blank" method="post">
                                <input name =co_uuid value={doc_count} hidden>
                                <input name =co_uuid value={co_uuid} hidden>
                                <button name="getdoc" type="submit" class="btn btn-primary">
                                    <i class="fa fa-file-pdf-o"></i>Download {doc_name}
                                </button>
                            </form>'''
                #tmp_div = tmp_div+'<div class="col-sm">'+doc_name+'</div>'
                main_div = main_div+f'<div class="col-sm-6">{formx}</div>'
                print("\n\tdocuments available: ", co_document.uploaded_file)
                div_count = div_count+1
                doc_count = doc_count+1
                #main_div = main_div+tmp_div+tail_div
            main_div = main_div+tail_div
            created_date = co_created_at.strftime("%d/%B/%Y")
            created_time = co_created_at.strftime("%H:%M:%S")

            print("\n\t all data: ", main_div)
            verification_action = f'<button name="verify_co" value="{co_uuid}" onclick="verify(this)" class="btn btn-success"> <i class="fa fa-check"></i> VERIFY </button>'
            
            previous_data = f'''<form action="/dashboard/getDoc" target="_blank" method="post">
                                    <input name =co_uuid value={co_uuid} hidden>
                                    
                                    <button name="getdoc" type="submit" class="btn btn-primary">
                                        <i class="fa fa-file-pdf-o"></i> GET DOCS
                                    </button>
                                </form>'''

            dropper = '''<div class="btn-group dropup">
                                <button type="button" class="btn btn-secondary" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        Dropup
                                </button>
                                <div class="dropdown-menu">
                                    welcome home man
                                </div>
                        </div>'''
            
            modeler = '''<div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
                            <div class="modal-dialog" role="document">
                                <div class="modal-content">
                                        <div class="modal-header">
                                                <h5 class="modal-title" id="exampleModalLabel">Modal title</h5>
                                                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                                    <span aria-hidden="true">&times;</span>
                                                </button>
                                        </div>
                                        <div class="modal-body">
                                            <div class="container-fluid">
                            <div class="row">
                                <div class="col-sm-6">
                                    1 of three columns
                                </div>
                                <div class="col-sm-6">
                                    2 of three columns
                                </div>
                                <div class="col-sm-6">
                                    3 of three columns
                                </div>
                            </div>
                        </div>
                                        </div>
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                                            <button type="button" class="btn btn-primary">Save changes</button>
                                        </div>
                                </div>
                            </div>
                        </div>'''
            
            xmodal_btn = '''<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#coDocsModal">
                                <i class="fa fa-file-pdf-o"></i>Show Company Docs
                            </button>'''
            modal_btn = f'''<button type="button" class="btn btn-primary" onclick="getDocs(this)" value={co_uuid}>
                                <i class="fa fa-file-pdf-o"></i>Show Company Docs
                            </button>'''
            modal_div = f"{modal_btn}"
            get_downloads = f'<button name="getdoc" onclick="getDocs(this)" value={co_uuid} class="btn btn-primary"> <i class="fa fa-file-pdf-o"></i> GET DOCS</button>'
            if current_user_company.verification_status == True:
               verification_action = f'<i class="fa fa-check"></i>ALLREADY VERIFIED </button>'
            log = [
                    co_name, 
                    co_email , 
                    co_telno, 
                    modal_div, 
                    f"{created_date} {created_time}", 
                    verification_action
                ]
            print("using log: ",log)
            all_keys.append(log)
        return all_keys
    
    def getCompanyDocs(self, co_uuid):
            current_user_company = Companies.objects.get(company_uuid = co_uuid)

            all_keys = []

        
            co_name = current_user_company.company_name
            co_email = current_user_company.company_email
            co_telno = current_user_company.company_telno
            co_documents = current_user_company.company_docs.all()
            co_uuid = current_user_company.company_uuid
            co_created_at = current_user_company.created_on

            root_div = '''<div class="container-fluid">
                            <div class="row">
                                <div class="col-sm-6">
                                    1 of three columns
                                </div>
                                <div class="col-sm-6">
                                    2 of three columns
                                </div>
                                <div class="col-sm-6">
                                    3 of three columns
                                </div>
                            </div>
                        </div>'''
            root_div_2 = f'''<div class="container-fluid">
                            
                                <div class="col-md-4">
                                    <form action="/dashboard/getDoc" target="_blank" method="post"><input name =co_uuid value={co_uuid} hidden><button name="getdoc" type="submit" class="btn btn-primary">
                                    <i class="fa fa-file-pdf-o"></i>tmp_Bank_Withdraw_Logs_m8iBUUz.pdf</button></form>
                                </div>
                                <div class="col-md-4">
                                    <form action="/dashboard/getDoc" target="_blank" method="post"><input name =co_uuid value={co_uuid} hidden><button name="getdoc" type="submit" class="btn btn-primary">
                                    <i class="fa fa-file-pdf-o"></i>tmp_Bank_Withdraw_Logs_m8iBUUz.pdf</button></form>
                                </div>
                                <div class="col-md-4">
                                    <form action="/dashboard/getDoc" target="_blank" method="post"><input name =co_uuid value={co_uuid} hidden><button name="getdoc" type="submit" class="btn btn-primary">
                                    <i class="fa fa-file-pdf-o"></i>tmp_Bank_Withdraw_Logs_m8iBUUz.pdf</button></form>
                                </div>
                            
                        </div>'''
            head_div = '\n<div class="container-fluid">'#\n\t<div class="row">'
            row_div  =  '<div class="row">'
            tail_div = "</div>"
            
            main_div = head_div
            div_count = 0
            doc_count = 0
            for co_document in co_documents:
                doc_name = co_document.uploaded_file.name.split('/')[1]

                tmp_div = ""
                #if (div_count == 2) or (div_count == 0):
                #    tmp_div = f"{row_div}"
                formx = f'''<form action="/dashboard/getDoc" target="_blank" method="post">\n
                    \t<input name ="doc_index" value="{doc_count}" hidden>\n
                    \t<input name ="co_uuid" value="{co_uuid}" hidden>\n
                    \t<button name="getdoc" type="submit" class="btn btn-primary">\n
                    <i class="fa fa-file-pdf-o"></i>{doc_name}\n
                    \t</button>
                </form><br/><br/>'''
                #tmp_div = tmp_div+'<div class="col-sm">'+doc_name+'</div>'
                main_div = main_div+f'<div class="col-sm-6">{formx}</div>'
                print("\n\tdocuments available: ", co_document.uploaded_file)
                div_count = div_count+1
                doc_count = doc_count+1
                #main_div = main_div+tmp_div+tail_div
            main_div = main_div+'\n'+'\n'+tail_div#+'\n'+tail_div
            created_date = co_created_at.strftime("%d/%B/%Y")
            created_time = co_created_at.strftime("%H:%M:%S")

            previous_data = f'<form action="/dashboard/getDoc" target="_blank" method="post"><input name =co_uuid value={co_uuid} hidden><button name="getdoc" type="submit" class="btn btn-primary"> <i class="fa fa-file-pdf-o"></i> GET DOCS</button></form>'

            xmodal_btn = '''<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#coDocsModal">
                                <i class="fa fa-file-pdf-o"></i>Show Company Docs
                            </button>'''
            modal_btn = f'''<button type="button" class="btn btn-primary" onclick="getDocs(this)" value={co_uuid}>
                                <i class="fa fa-file-pdf-o"></i>Show Company Docs
                            </button>'''
            modal_div = f"{modal_btn}"
            get_downloads = f'<button name="getdoc" onclick="getDocs(this)" value={co_uuid} class="btn btn-primary"> <i class="fa fa-file-pdf-o"></i> GET DOCS</button>'
            if current_user_company.verification_status == True:
               verification_action = f'<i class="fa fa-check"></i>ALLREADY VERIFIED </button>'
            
            return main_div
    
    def getProductionKeys(self, dashboard_user):
        verification_filter = False
        all_pdt_keys = APIcredentials.objects.filter(is_production_key =True)

        all_keys = []

        for pdt_keys in all_pdt_keys:
            print("\n\tusing user")
            key_owner = pdt_keys.owner
            token_user =  pdt_keys.token_user

            print("\n\tusing pdt key user: ", key_owner.username)
            key_role = "api test"
            try:
                dashboard_owner = DashboardUsers.objects.get(user = key_owner)
                key_role = dashboard_owner.user_role
            except:
                dashboard_owner = None

            key_owner_username = key_owner.username
            key_owner_fullnames = key_owner.get_full_name()
            key_owner_email = key_owner.email
            key_owner_telno = ""
            
            token_uuid = pdt_keys.token_uuid
            actions = f'<button name="verify_co" value="{token_uuid}" onclick="verifyKey(this)" class="btn btn-primary"> <i class="fa fa-check"></i> VERIFY </button><br/><button name="verify_co" value="{token_uuid}" onclick="disableKey(this)" class="btn btn-danger"> <i class="fa fa-times"></i> DISABLE </button>'

            if pdt_keys.is_validated == True:
                    actions = f'<i class="fa fa-check"></i>VERIFIED </button><br/><button name="disable_co" value="{token_uuid}" onclick="disableKey(this)" class="btn btn-danger"> <i class="fa fa-times"></i> DISABLE </button>'
            
            token_created_at = token_user.date_joined
            created_date = token_created_at.strftime("%d/%B/%Y")
            created_time = token_created_at.strftime("%H:%M:%S")

            log = [
                    key_owner_username, 
                    key_owner_email, 
                    key_owner_telno,
                    key_owner_fullnames,
                    actions, 
                    f"{created_date} {created_time}", 
                    key_role
                ]
            print("using log: ",log)
            all_keys.append(log)
        return all_keys
    
    def getExtraLogs(self,request_user,log_type,log_params):
        print("getting external logs")
        dashboard_user = DashboardUsers.objects.get(user = request_user)
        user_token = dashboard_user.internal_token.token.key
        return LogModel(request_user, log_params).getLog(log_type)