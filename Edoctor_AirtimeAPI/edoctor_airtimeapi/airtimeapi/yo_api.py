from .pyxml import *
import requests
import xmltodict
from xml.dom.minidom import parseString
import uuid,json
from .pyreceipt import makeReceipt,makeReceiptHTML
from .models import *
from ipware import get_client_ip
class YO_API:
    
    def __init__(self, name,password):
        """
        Initializes the YO_API object with the given name and password.

        :param name: The name of the YO API user.
        :type name: str
        :param password: The password of the YO API user.
        :type password: str
        """
        self.yo_name = name
        self.yo_password = password
        #self.end_point = "https://paymentsdev1.yo.co.ug/yopaytest/task.php"
        self.end_point = "https://sandbox.yo.co.ug/services/yopaymentsdev/task.php"
        #self.end_point = "https://sandbox.yo.co.ug/services/yopaymentsdev/task.php"
        self.headers = { "Content-Type": "application/xml",} 
        
    def getMSISDNInfo(self,request):
       """
        Fetches information related to the MSISDN (Mobile Station International Subscriber Directory Number).

        :param msisdn: The MSISDN for which information is to be fetched.
        :type msisdn: str
        :return: The information in XML format as a string.
        :rtype: str
        :raises requests.exceptions.RequestException: If there is an error in making the request to the YO API.
        :raises xmltodict.
       """
       json_request = json.loads(request.body)
       msisdn = json_request["telno"]
       msisdn = json_request["telno"]
       msisdn_info  = YoCheckMsisdn(self.yo_name,self.yo_password,msisdn)
       msisdn_request  = YoRequest(msisdn_info)
       #msisdn_xml_dom = parseString(msisdn_request.to_xml())
       msisdn_xml = msisdn_request.to_xml()
       #print(msisdn_xml)
       response = requests.post(self.end_point, headers=self.headers, data = msisdn_xml)
       xml_response = xmltodict.parse(response.text)
       #print(xml_response)

       clear_xml_response = xml_response["AutoCreate"]["Response"]
       status_code = clear_xml_response["StatusCode"]
       status_msg = clear_xml_response["Status"]
       response_msg = clear_xml_response

       client_ip = get_client_ip(request)
       msisdninfo = MSISDNInfo(user=request.user,
                               msisdn=msisdn,
                               status=f"{status_msg}:{status_code}",
                               endpoint="/airtime/api/msisdninfo",
                               response=str(response_msg),
                               request=str(json_request),
                               ip=client_ip[0])

       msisdninfo.save()

       
       return xml_response["AutoCreate"]["Response"]


    def sendAirtime(self,request):
       """
        Sends airtime to the specified MSISDN.

        :param msisdn: The MSISDN to which airtime is to be sent.
        :type msisdn: str
        :param amount: The amount of airtime to be sent.
        :type amount: float
        :return: The information in XML format as a string.
        :rtype: str
        :raises requests.exceptions.RequestException: If there is an error in making the request to the YO API.
        :raises xmltodict.expat.ExpatError: If there is an error in parsing the XML response.
       """
       json_request = json.loads(request.body)
       msisdn = json_request["telno"]
       amount = json_request["amount"]
       send_airtime_object  = YoSendAirtime(
                            self.yo_name,
                            self.yo_password,
                            amount, 
                            msisdn)
       send_airtime_request = YoRequest(send_airtime_object)
       send_airtime_xml = send_airtime_request.to_xml()
       #print(send_airtime_xml)
       response = requests.post(self.end_point, headers=self.headers, data = send_airtime_xml)
       
       xml_response = xmltodict.parse(response.text)
       #print(xml_response)
       client_ip = get_client_ip(request)
       client_user = request.user

       clear_xml_response = xml_response["AutoCreate"]["Response"]
       status_code = clear_xml_response["StatusCode"]
       status_msg = clear_xml_response["Status"]
       response_msg = clear_xml_response

       print("Using client user: ", client_user)
       airtime_transaction = AirtimeTransaction(
            user = client_user,
            ip= client_ip[0],
            response=str(response_msg),
            request=str(send_airtime_request),      
            status=f"{status_msg}:{status_code}",
            amount = amount,
            telno= msisdn,
            method = "SEND"
        )
       
       airtime_transaction.save()

       return xml_response["AutoCreate"]["Response"]

    def buyAirtime(self,request):
        """
            Buys airtime for the specified network.

            :param netwrk: The network for which airtime is to be bought.
            :type netwrk: str
            :param amount: The amount of airtime to be bought.
            :type amount: float
            :return: The information in XML format as a string.
            :rtype: str
            :raises requests.exceptions.RequestException: If there is an error in making the request to the YO API.
            :raises xmltodict.expat.ExpatError: If there is an error in parsing the XML response.
        """
        yo_obj = None
        json_request = json.loads(request.body)
        netwrk = json_request["provider"]
        amount = json_request["amount"]
        if (netwrk == "airtel") or (netwrk == "AIRTEL"):
            yo_obj = YoBuyAirtime(self.yo_name,self.yo_password,"UGX-AIRAT", amount)
        elif (netwrk == "mtn") or (netwrk == "MTN"):
            yo_obj = YoBuyAirtime(self.yo_name,self.yo_password,"UGX-MTNAT", amount)
        elif (netwrk == "utl") or (netwrk == "UTL"):
            yo_obj = YoBuyAirtime(self.yo_name,self.yo_password,"UGX-UTLAT", amount)
        
        yo_request = YoRequest(yo_obj)
        yo_xml = yo_request.to_xml()
        #print(yo_xml)
        response = requests.post(self.end_point, headers=self.headers, data = yo_xml)
        xml_response = xmltodict.parse(response.text)
        client_ip = get_client_ip(request)
        client_user = request.user

        clear_xml_response = xml_response["AutoCreate"]["Response"]
        status_code = clear_xml_response["StatusCode"]
        status_msg = clear_xml_response["Status"]
        response_msg = clear_xml_response
        print("Using client user: ", client_user)
        log_entry = AirtimePurchase(
            user = client_user,
            ip= client_ip[0],
            response=str(response_msg),
            request=str(json_request),      
            status=f"{status_msg}:{status_code}",
            amount = amount,
            netwrk= netwrk,
        )

        log_entry.save()
        #print(xml_response)
        return clear_xml_response
        #xml_response["AutoCreate"]["Response"]
    
    def depositMoney(self,request):
        """
        Deposit a specified amount of money into the user's account associated with the given phone number.

        This method deposits the given amount of money into the user's account associated with the given phone number.

        Args:
        telno (str): The phone number associated with the user's account.
        amount (float): The amount of money to deposit.

        Returns:
        dict: A dictionary containing the result of the funds deposit.
        """
        json_request = json.loads(request.body)
        telno = json_request["telno"]
        amount = json_request["amount"]
        money_deposit = YoDepositMoney(self.yo_name,self.yo_password,telno,amount)

        json_response, xstatus_code= self.execRequest(money_deposit)

        print("\t\n\t", json_response)
        clear_json_response = json_response
        status_code = json_response["StatusCode"]
        status_msg = json_response["Status"]
        response_msg = ""
        if status_code!=0:
            response_msg = json_response
        else:
            response_msg = json_response
        client_ip = get_client_ip(request)
        client_user = request.user

        print("Using client user: ", client_user)
        log_entry = MMFundsDeposit(
            user = client_user,
            ip= client_ip[0],
            response=str(response_msg),
            request=str(json_request),      
            status=f"{status_msg}:{status_code}",
            amount = amount,
            telno= telno,
        )

        log_entry.save()
        return clear_json_response
    
    
    def withdrawMoney(self,request):
        """
        Withdraw a specified amount of money from the user's account associated with the given phone number.

        This method withdraws the given amount of money from the user's account associated with the given phone number.

        Args:
        telno (str): The phone number associated with the user's account.
        amount (float): The amount of money to withdraw.

        Returns:
        dict: A dictionary containing the result of the funds withdrawal.
        """
        json_request = json.loads(request.body)
        telno = json_request["telno"]
        amount = json_request["amount"]
        money_withdraw = YoWithdrawMoney(self.yo_name,self.yo_password,telno,amount)
        json_response, status_code = self.execRequest(money_withdraw)
        client_ip = get_client_ip(request)

        client_user = request.user

        print("\t\n\t", json_response)
        clear_json_response = json_response
        status_code = json_response["StatusCode"]
        status_msg = json_response["Status"]
        response_msg = json_response


        print("Using client user: ", client_user)
        log_entry = MMFundsWithdraw(
            user = client_user,
            ip= client_ip[0],
            response=str(response_msg),
            request=str(json_request),      
            status=f"{status_msg}:{status_code}",
            amount = amount,
            telno= telno,
        )

        log_entry.save()
        return json_response
  
  
    def recvAirtime(self,msisdn,amount):
        pass

    def checkTransactionStatus(self,request):
        json_request = json.loads(request.body)
        transaction_id = json_request["transaction_id"]
        transaction_status = YoCheckTransactionStatus(self.yo_name,self.yo_password,transaction_id)
        json_response, status_code = self.execRequest(transaction_status)
        client_ip = get_client_ip(request)
        client_user = request.user
        print("Using client user: ", client_user)
        print("json response: ", str(json_response))
        clear_json_response = json_response
        status_code = json_response["StatusCode"]
        status_msg = json_response["Status"]
        response_msg = json_response

        log_entry = TransactionStatus(
            user = client_user,
            ip= client_ip[0],
            response=(json_response),
            request=(json_request),      
            status=f"{status_msg}:{status_code}",
            transaction_id = transaction_id,
            transaction_type = json_response
 
        )

        log_entry.save()
        return json_response

    def withdrawMoneyToBank(self,request):
        json_request = json.loads(request.body)
        amount = json_request["amount"]
        mm_provider = json_request["mmprovider"].upper()
        mm_holder = "UGX-MTNMM" if  mm_provider == 'MTN' else ("UGX-AIRMM" if mm_provider == "AIRTEL" else "")

        user_acc_no = json_request["account_no"]
        user_acc_name = json_request["account_name"]
        user_acc_id = json_request["account_id"]

        money_withdraw = YoBankWithdrawFunds(self.yo_name,self.yo_password,amount,mm_holder,user_acc_name,user_acc_no,user_acc_id)
        json_response, status_code = self.execRequest(money_withdraw)
        client_ip = get_client_ip(request)

        client_user = request.user

        clear_json_response = json_response
        status_code = json_response["StatusCode"]
        status_msg = json_response["Status"]
        response_msg = json_response

        print("Using client user: ", client_user)
        log_entry = WithdrawMoneyToBank(
            user = client_user,
            ip= client_ip[0],
            response=str(response_msg),
            request=str(json_request),      
            status=f"{status_msg}:{status_code}",
            accno = user_acc_no,
            amount = amount, 
 
        )

        log_entry.save()
        return json_response



    def getBankWithdrawStatus(self,request):
        json_request = json.loads(request.body)
        transaction_id = json_request["transaction_id"]
        yo_withdraw_status = YoBankWithdrawStatus(self.yo_name,self.yo_password,settlement_transaction_identifier=transaction_id)
        json_response, status_code = self.execRequest(yo_withdraw_status)
        
        client_ip = get_client_ip(request)
        client_user = request.user
        print("Using client user: ", client_user)

        status_code = json_response["StatusCode"]
        status_msg = json_response["Status"]
        response_msg = json_response
        amount = 0 if status_code!="0" else json_response["Amount"]
        

        print("Bank withdraw status response: ", json_response)
        log_entry = BankWithdrawStatus(
            user = client_user,
            ip= client_ip[0],
            response=json_response,
            request=json_request,      
            status=f"{status_msg}:{status_code}",
            transaction_id = transaction_id,
            amount = amount
 
        )

        log_entry.save()
        return json_response


    def checkBalance(self,request):
        """## get the balance in the user's account

        ### Args:
            - `json_request (json)`: check the account balance

        ### Returns:
            dict: A dictionary containing the result of the balance check.
        """
        balance_check = YoBalanceCheck(self.yo_name,self.yo_password)
        json_response, status_code = self.execRequest(balance_check)
        client_ip = get_client_ip(request)
        client_user = request.user
        print("Using client user: ", client_user)

        status_code = json_response["StatusCode"]
        status_msg = json_response["Status"]
        response_msg = json_response
        balance = 0 if status_code!="0" else json_response["Balance"]

        log_entry = Balance(
            user = client_user,
            ip= client_ip[0],
            response=json_response,
            request=json_response,      
            status=status_code,
            balance = balance
            
 
        )

        log_entry.save()
        return json_response


    def makeInternalTransfer(self,request):
        json_request = json.loads(request.body)
        receiver_acc =  json_request['receiver_account_no']
        receiver_email = json_request["receiver_email"]
        amount = json_request["amount"]
        mm_provider = json_request["mmprovider"].upper()
        mm_holder = "UGX-MTNMM" if  mm_provider == 'MTN-MM' else ("UGX-WTLMM" if mm_provider == "AIRTEL-MM" else ("UGX-MTNAT" if mm_provider == "MTN-AT" else ("UGX-AIRAT" if mm_provider == "AIRTEL-AT" else "UGX-AIRAT")))
        description_txt = json_request["description"]

        yo_internal_transfer_struct = YoInternalTransferRequest(self.yo_name,self.yo_password,mm_provider,amount,receiver_acc,receiver_email,description_txt)
        json_response, status_code = self.execRequest(yo_internal_transfer_struct)
        client_ip = get_client_ip(request)
        client_user = request.user
        print("Using client user: ", client_user)

        status_code = json_response["StatusCode"]
        status_msg = json_response["Status"]
        response_msg = json_response

        log_entry = InternalTransfer(
            user = client_user,
            ip= client_ip[0],
            response=str(json_response),
            request=str(json_request),      
            status=f"{status_msg}:{status_code}",
            sender_acc= "recv" ,
            recv_acc = receiver_acc, 
            amount = amount
 
        )

        log_entry.save() 
        return json_response


    def getMiniStatement(self,request):
        """## get ministatement of all the transactions

        ### Args:
            - `json_request (json)`: json request with the mini statement filters
        """
        json_request = ""#json.loads(request.body)
        yo_mini_statement = YoMiniStatementRequest(self.yo_name,self.yo_password)
        json_response, status_code = self.execRequest(yo_mini_statement)
        client_ip = get_client_ip(request)
        client_user = request.user
        print("Using client user: ", client_user)
        print("Using client response: ", str(json_response))
        total_transactions = 0 if json_response['StatusCode']=='0' else json_response["TotalTransactions"]
        log_entry = MiniStatement(
            user = client_user,
            ip= client_ip[0],
            response=str(json_response),
            request=str(json_request),      
            status=status_code,
            total_transactions =  total_transactions,
 
        )

        log_entry.save()
        return json_response

    def submitBankDeposit(self,user_name,request):
        """## Submit a bank deposit request

        ### Args:
            - `user_name (string)`: user name of the user to be written in the deposit slip
            - `json_request (json)`: json request with the bank deposit details

        ### Returns:
            dict: A dictionary containing the result of the funds withdrawal.
        """
        json_request = json.loads(request.body)
        amount_to_deposit = json_request["amount"]
        funds_usage = json_request["usage"]
        description = json_request["note"]

        

        amount_breakdown = []
        for usage in funds_usage:
            mm_provider = usage["provider"].upper()
            mm_holder = "UGX-MTNMM" if  mm_provider == 'MTN' else ("UGX-AIRTELMM" if mm_provider == "AIRTEL" else "")
            
            mm_amount = usage["amount"]
            mm_usage = {
                "CurrencyCode":mm_holder,
                "Amount":mm_amount
            }
            amount_breakdown.append(mm_usage)
        bank_file_name, bank_file_data = makeReceiptHTML(user_name,amount_to_deposit)
        bank_deposit = YoBankDepositRequest(self.yo_name,self.yo_password,TotalDepositAmount=amount_to_deposit,Narrative=description,BankTransferFileName=bank_file_name,BankTransferFileContentBase64=bank_file_data,CurrencyAllocations=amount_breakdown)
        my_item_func = lambda x: 'CurrencyAllocation'

        json_response, status_code = self.execRequest(bank_deposit,my_item_func)
        client_ip = get_client_ip(request)
        client_user = request.user

        clear_json_response = json_response
        status_code = json_response["StatusCode"]
        status_msg = json_response["Status"]
        response_msg = json_response
        print("Using client user: ", client_user)
        log_entry = BankDeposit(
            user = client_user,
            ip= client_ip[0],
            response=str(json_response),
            request=str(json_request),      
            status=f"{status_msg}:{status_code}",
            accno = json_response["BankDepositRequestReference"] ,
            amount = amount_to_deposit
 
        )

        log_entry.save()
        return json_response
        

    def execRequest(self,yo_obj,item_name_func=None):
        """
        Execute a request using the provided YO object.

        This method processes and executes a request using the provided YO object, which should contain the necessary information to perform the request.

        Args:
        yo_obj (dict): A dictionary containing the necessary information to perform the request.

        Returns:
        dict: A dictionary containing the result of the request execution.
        """
        yo_request = YoRequest(yo_obj)
        yo_xml = yo_request.to_xml(item_name_func)
        print(yo_xml)
        response = requests.post(self.end_point, headers=self.headers, data = yo_xml)
        if response == None:
            return {}
        xml_response = xmltodict.parse(response.text)
        return xml_response["AutoCreate"]["Response"],response.status_code
    
    def execPullRequest(self,yo_obj):
        yo_request = YoRequest(yo_obj)
        yo_xml = yo_request.to_xml()
        #print(yo_xml)
        response = requests.post(self.end_point, headers=self.headers, data = yo_xml)
        xml_response = xmltodict.parse(response.text)
        return xml_response["AutoCreate"]["Response"],response.status_code
        