from .models import *
from datetime import datetime
class LogModel:

    log_types = [
        "mmAirtime_Transaction",
        "msisdn",
        "airtime_purchase",
        "mmdeposit",
        "mmwithdraw",
        "bank_deposit",
        "internal_transfer",
        "bank_withdraw",
        "transaction_status",
        "bank_withdraw_status",
        "balance",
        "ministatement",
    ]
    def __init__(self, user_man = None, log_params= {}):
        self.user_man = user_man
        self.logData = [
                             ['+25670000000', '50000', '200 Ok', '{"amount":5000,"note":"deposit cash", "usage":[{"provider":"mtn","amount":1000},{"provider":"airtel","amount":4000}  ]}', '#{"Status": "OK","StatusCode": "0","BankDepositRequestReference": "0777d5c17d4066b82ab86dff8a46af6f"} ', '102.100.5.1'],
                       
                   ]
        self.logColumns = [
                            { "title": 'Name' },
                            { "title": 'Position' },
                            { "title": 'Office' },
                            { "title": 'Extn.' },
                            { "title": 'Start date' },
                            { "title": 'Salary' }
                          ]
        
        self.log_params = log_params
    def getTable(self):
        return self.logColumns,self.logData
    
    def logSummary(self):
        api_count = 0
        for log_cmd in self.log_types:
            log_data = self.getLog(log_cmd)
            api_count = api_count+len(log_data)
        return api_count
             
    
    def getLog(self,log_type):
        print("gotten log: ",log_type)
        if (log_type=="mmAirtime_Transaction"):
            return self.mmAirtimeTransactionLog()
        elif (log_type=="msisdn"):
            return self.msisdnLog()
        elif (log_type=="airtime_purchase"):
            return self.airtimePurchaseLog()
        elif (log_type=="mmdeposit"):
            return self.mmDepositLog()
        elif (log_type=="mmwithdraw"):
            return self.mmWithdrawLog()
        elif (log_type=="bank_deposit"):
            return self.bankDepositLog()
        elif (log_type=="internal_transfer"):
            return self.internalTransferLog()
        elif (log_type=="bank_withdraw"):
            return self.bankWithdrawLog()
        elif (log_type=="transaction_status"):
            return self.transactionStatusLog()
        elif (log_type=="bank_withdraw_status"):
            return self.bankWithdrawStatusLog()
        elif (log_type=="balance"):
            return self.balanceLog()
        elif (log_type=="ministatement"):
            return self.ministatementLog()
        elif (log_type=="all_companies"):
            return ""
        elif (log_type=="apikeys"):
            return ""
        elif (log_type=="all_admins"):
            return ""
        elif (log_type=="verify_requests"):
            return ""
        elif (log_type=="user_keys"):
            return ""


    
    def mmAirtimeTransactionLog(self) :
        self.logData = [
                        ['+25670000000', '50000', 'SEND', '200 Ok', '{"amount":5000,"note":"deposit cash", "usage":[{"provider":"mtn","amount":1000},{"provider":"airtel","amount":4000}  ]}', '{"Status": "OK","StatusCode": "0","BankDepositRequestReference": "0777d5c17d4066b82ab86dff8a46af6f"} ', '102.100.5.1','4/11/2024','5:35 pm'],
                       
                   ]
        
        filter_type = self.log_params.get("filter_type","all")
        print(f"\n\tusing filter: {filter_type}")

        airtime_transactions = AirtimeTransaction.objects.filter(owner = self.user_man)
        log_data =  []
        filter_data_number = airtime_transactions.count()
        print("\n response number: ",filter_data_number)
        log_data =  []
        if filter_data_number==0:
            return log_data
        for airtime_transaction in airtime_transactions:
            record_date = airtime_transaction.date

            if filter_type == "date_filter":
                str_start_date = self.log_params.get("start_datepicker",datetime.now())
                str_end_date = self.log_params.get("end_datepicker",datetime.now())

                start_date = datetime.strptime(str_start_date,"%Y-%m-%d").date()
                end_date = datetime.strptime(str_end_date,"%Y-%m-%d").date()

                print(f"using filter: {start_date} to {end_date}")
                if (record_date>=start_date) and (record_date<=end_date):

                    at_log = [
                        airtime_transaction.status,
                        airtime_transaction.telno,
                        airtime_transaction.amount,
                        airtime_transaction.method,
                        airtime_transaction.request,
                        airtime_transaction.response,
                        airtime_transaction.ip,
                        f"{airtime_transaction.date} {airtime_transaction.time}",
                        airtime_transaction.user.username
                    ]
                    log_data.append(at_log)

            elif filter_type == "today_filter":
                start_date = datetime.now()
                
                print(f"using filter: {start_date}")
                if (record_date==start_date):

                    at_log = [
                        airtime_transaction.status,
                        airtime_transaction.telno,
                        airtime_transaction.amount,
                        airtime_transaction.method,
                        airtime_transaction.request,
                        airtime_transaction.response,
                        airtime_transaction.ip,
                        f"{airtime_transaction.date} {airtime_transaction.time}",
                        airtime_transaction.user.username
                    ]
                    log_data.append(at_log)

            else:
                print("displaying all logs")
                at_log = [
                        airtime_transaction.status,
                        airtime_transaction.telno,
                        airtime_transaction.amount,
                        airtime_transaction.method,
                        airtime_transaction.request,
                        airtime_transaction.response,
                        airtime_transaction.ip,
                        f"{airtime_transaction.date} {airtime_transaction.time}",
                        airtime_transaction.user.username
                    ]
                log_data.append(at_log)
        return log_data
    
    def msisdnLog(self):
        self.logData = [
                        ['200 Ok','{"amount":5000,"note":"deposit cash", "usage":[{"provider":"mtn","amount":1000},{"provider":"airtel","amount":4000}  ]}','{"Status": "OK","StatusCode": "0","BankDepositRequestReference": "0777d5c17d4066b82ab86dff8a46af6f"} ', '102.100.5.1','4/11/2024','5:35 pm']
                       ]
        
        filter_type = self.log_params.get("filter_type","all")
        print(f"\n\tusing filter: {filter_type}")

        filter_data = MSISDNInfo.objects.filter(owner = self.user_man)
        filter_data_number = filter_data.count()
        print("\n response number: ",filter_data_number)
        log_data =  []
        if filter_data_number==0:
            return log_data
        for filter_datum in filter_data:
            record_date = filter_datum.date
            if filter_type == "date_filter":
                str_start_date = self.log_params.get("start_datepicker",datetime.now())
                str_end_date = self.log_params.get("end_datepicker",datetime.now())

                start_date = datetime.strptime(str_start_date,"%Y-%m-%d").date()
                end_date = datetime.strptime(str_end_date,"%Y-%m-%d").date()

                print(f"using filter: {start_date} to {end_date}")
                if (record_date>=start_date) and (record_date<=end_date):

                    datum_log = [                       
                        filter_datum.status,
                        filter_datum.response,
                        filter_datum.request,
                        filter_datum.ip,
                        f"{filter_datum.date} {filter_datum.time}",
                        filter_datum.user.username
                    ]
                    log_data.append(datum_log)
            elif filter_type == "today_filter":
                start_date = datetime.now()
                
                print(f"using filter: {start_date}")
                if (record_date==start_date):

                    datum_log = [                       
                        filter_datum.status,
                        filter_datum.response,
                        filter_datum.request,
                        filter_datum.ip,
                        f"{filter_datum.date} {filter_datum.time}",
                        filter_datum.user.username
                    ]
                    log_data.append(datum_log)

            else:
                print("displaying all logs")
                datum_log = [                       
                        filter_datum.status,
                        filter_datum.response,
                        filter_datum.request,
                        filter_datum.ip,
                        f"{filter_datum.date} {filter_datum.time}",
                        filter_datum.user.username
                    ]
                log_data.append(datum_log)
        return log_data
    
    def airtimePurchaseLog(self):
        self.logData = [
                        ['200 Ok','MTN','5000','{"amount":5000,"note":"deposit cash", "usage":[{"provider":"mtn","amount":1000},{"provider":"airtel","amount":4000}  ]}','{"Status": "OK","StatusCode": "0","BankDepositRequestReference": "0777d5c17d4066b82ab86dff8a46af6f"} ', '102.100.5.1','4/11/2024','5:35 pm']
                       ]
        
        filter_type = self.log_params.get("filter_type","all")
        print(f"\n\tusing filter: {filter_type}")

        filter_data = AirtimePurchase.objects.filter(owner = self.user_man)
        log_data =  []
        filter_data_number = filter_data.count()
        print("\n response number: ",filter_data_number)
        log_data =  []
        if filter_data_number==0:
            return log_data
        for filter_datum in filter_data:
            record_date = filter_datum.date

            if filter_type == "date_filter":
                str_start_date = self.log_params.get("start_datepicker",datetime.now())
                str_end_date = self.log_params.get("end_datepicker",datetime.now())

                start_date = datetime.strptime(str_start_date,"%Y-%m-%d").date()
                end_date = datetime.strptime(str_end_date,"%Y-%m-%d").date()

                print(f"using filter: {start_date} to {end_date}")

                if (record_date>=start_date) and (record_date<=end_date):
                        datum_log = [
                            filter_datum.status,
                            filter_datum.netwrk,
                            filter_datum.amount,             
                            filter_datum.response,
                            filter_datum.request,
                            filter_datum.ip,
                            f"{filter_datum.date} {filter_datum.time}",
                            filter_datum.user.username
                        ]
                        log_data.append(datum_log)
            elif filter_type == "today_filter":
                start_date = datetime.now()
                
                print(f"using filter: {start_date}")
                if (record_date==start_date):

                    datum_log = [                       
                        filter_datum.status,
                        filter_datum.netwrk,
                        filter_datum.amount,
                        filter_datum.response,
                        filter_datum.request,
                        filter_datum.ip,
                        f"{filter_datum.date} {filter_datum.time}",
                        filter_datum.user.username
                    ]
                    log_data.append(datum_log)

            else:
                print("displaying all logs")
                datum_log = [                       
                        filter_datum.status,
                        filter_datum.netwrk,
                        filter_datum.amount,
                        filter_datum.response,
                        filter_datum.request,
                        filter_datum.ip,
                        f"{filter_datum.date} {filter_datum.time}",
                        filter_datum.user.username
                    ]
                log_data.append(datum_log)
        return log_data
    
    def mmDepositLog(self):
        self.logData = [
                             [ '200 Ok','+25670000000', '50000', '{"amount":5000,"note":"deposit cash", "usage":[{"provider":"mtn","amount":1000},{"provider":"airtel","amount":4000}  ]}', '{"Status": "OK","StatusCode": "0","BankDepositRequestReference": "0777d5c17d4066b82ab86dff8a46af6f"} ', '102.100.5.1','4/11/2024','6:12 pm'],
                       
                   ]
        
        filter_type = self.log_params.get("filter_type","all")
        print(f"\n\tusing filter: {filter_type}")

        filter_data = MMFundsDeposit.objects.filter(owner = self.user_man)
        log_data =  []
        filter_data_number = filter_data.count()
        print("\n response number: ",filter_data_number)
        log_data =  []
        if filter_data_number==0:
            return log_data
        for filter_datum in filter_data:
            record_date = filter_datum.date
            if filter_type == "date_filter":
                str_start_date = self.log_params.get("start_datepicker",datetime.now())
                str_end_date = self.log_params.get("end_datepicker",datetime.now())

                start_date = datetime.strptime(str_start_date,"%Y-%m-%d").date()
                end_date = datetime.strptime(str_end_date,"%Y-%m-%d").date()

                print(f"using filter: {start_date} to {end_date}")
                if (record_date>=start_date) and (record_date<=end_date):

                    datum_log = [
                        filter_datum.status,
                        filter_datum.telno,
                       # filter_datum.amount,
                        filter_datum.response,
                        filter_datum.request,
                        filter_datum.ip,
                        f"{filter_datum.date} {filter_datum.time}",
                        filter_datum.user.username
                        
                    ]
                    log_data.append(datum_log)
            elif filter_type == "today_filter":
                start_date = datetime.now()
                
                print(f"using filter: {start_date}")
                if (record_date==start_date):
                    datum_log = [
                        filter_datum.status,
                        filter_datum.telno,
                       # filter_datum.amount,
                        filter_datum.response,
                        filter_datum.request,
                        filter_datum.ip,
                        f"{filter_datum.date} {filter_datum.time}",
                        filter_datum.user.username
                        
                    ]
                    log_data.append(datum_log)
            else:
                print("displaying all logs")
                datum_log = [                       
                        filter_datum.status,
                        filter_datum.telno,
                       # filter_datum.amount,
                        filter_datum.response,
                        filter_datum.request,
                        filter_datum.ip,
                        f"{filter_datum.date} {filter_datum.time}",
                        filter_datum.user.username
                    ]
                log_data.append(datum_log)
        return log_data
    
    def mmWithdrawLog(self):
        self.logData = [
                             ['200 Ok', '+25670000000', '50000',  '{"amount":50000,"note":"deposit cash", "usage":[{"provider":"mtn","amount":1000},{"provider":"airtel","amount":4000}  ]}', '{"Status": "OK","StatusCode": "0","BankDepositRequestReference": "0777d5c17d4066b82ab86dff8a46af6f"} ', '102.100.5.1','4/11/2024','6:12 pm'],
                       
                   ]
        filter_type = self.log_params.get("filter_type","all")
        print(f"\n\tusing filter: {filter_type}")
        filter_data = MMFundsWithdraw.objects.filter(owner = self.user_man)
        log_data =  []
        filter_data_number = filter_data.count()
        print("\n response number: ",filter_data_number)
        log_data =  []
        if filter_data_number==0:
            return log_data
        for filter_datum in filter_data:
            record_date = filter_datum.date
            if filter_type == "date_filter":
                str_start_date = self.log_params.get("start_datepicker",datetime.now())
                str_end_date = self.log_params.get("end_datepicker",datetime.now())

                start_date = datetime.strptime(str_start_date,"%Y-%m-%d").date()
                end_date = datetime.strptime(str_end_date,"%Y-%m-%d").date()

                print(f"using filter: {start_date} to {end_date}")
                if (record_date>=start_date) and (record_date<=end_date):
                    datum_log = [
                        filter_datum.status,
                        filter_datum.telno,
                        filter_datum.amount,
                        filter_datum.response,
                        filter_datum.request,
                        filter_datum.ip,
                        f"{filter_datum.date} : {filter_datum.time}",
                        filter_datum.user.username
                    ]
                    log_data.append(datum_log)
                elif filter_type == "today_filter":
                    start_date = datetime.now()
                
                    print(f"using filter: {start_date}")
                    if (record_date==start_date):
                        datum_log = [
                                filter_datum.status,
                                filter_datum.telno,
                                filter_datum.amount,
                                filter_datum.response,
                                filter_datum.request,
                                filter_datum.ip,
                                f"{filter_datum.date} : {filter_datum.time}",
                                filter_datum.user.username
                            ]
                        log_data.append(datum_log)
                else:
                    print("displaying all logs")
                    datum_log = [
                                filter_datum.status,
                                filter_datum.telno,
                                filter_datum.amount,
                                filter_datum.response,
                                filter_datum.request,
                                filter_datum.ip,
                                f"{filter_datum.date} : {filter_datum.time}",
                                filter_datum.user.username
                            ]
                    log_data.append(datum_log)
                
        return log_data
    
    def bankDepositLog(self):
        self.logData = [
                             ['200 Ok', '123536738383', '50000',  '{"amount":50000,"note":"deposit cash", "usage":[{"provider":"mtn","amount":1000},{"provider":"airtel","amount":4000}  ]}', '{"Status": "OK","StatusCode": "0","BankDepositRequestReference": "0777d5c17d4066b82ab86dff8a46af6f"} ', '102.100.5.1','4/11/2024','6:12 pm'],
                       
                   ]
        
        filter_type = self.log_params.get("filter_type","all")
        print(f"\n\tusing filter: {filter_type}")
        filter_data = BankDeposit.objects.filter(owner = self.user_man)
        log_data =  []
        filter_data_number = filter_data.count()
        print("\n response number: ",filter_data_number)
        log_data =  []
        if filter_data_number==0:
            return log_data
        #for filter_datum in filter_data:
        #    datum_log = [
        #                filter_datum.status,
        #                filter_datum.accno,
        #                filter_datum.amount,             
        #                filter_datum.response,
        #                filter_datum.request,
        #                filter_datum.ip,
        #                f"{filter_datum.date}:{filter_datum.time}",
        #                filter_datum.user.username
        #    ]
        #    log_data.append(datum_log)
        
        for filter_datum in filter_data:
            record_date = filter_datum.date

            if filter_type == "date_filter":
                str_start_date = self.log_params.get("start_datepicker",datetime.now())
                str_end_date = self.log_params.get("end_datepicker",datetime.now())

                start_date = datetime.strptime(str_start_date,"%Y-%m-%d").date()
                end_date = datetime.strptime(str_end_date,"%Y-%m-%d").date()

                print(f"using filter: {start_date} to {end_date}")

                if (record_date>=start_date) and (record_date<=end_date):
                        datum_log = [
                            filter_datum.status,
                            filter_datum.accno,
                            filter_datum.amount,             
                            filter_datum.response,
                            filter_datum.request,
                            filter_datum.ip,
                            f"{filter_datum.date}:{filter_datum.time}",
                            filter_datum.user.username
                        ]
                        log_data.append(datum_log)
            elif filter_type == "today_filter":
                start_date = datetime.now()
                
                print(f"using filter: {start_date}")
                if (record_date==start_date):

                    datum_log = [
                            filter_datum.status,
                            filter_datum.accno,
                            filter_datum.amount,             
                            filter_datum.response,
                            filter_datum.request,
                            filter_datum.ip,
                            f"{filter_datum.date}:{filter_datum.time}",
                            filter_datum.user.username
                        ]
                    log_data.append(datum_log)

            else:
                print("displaying all logs")
                datum_log = [
                            filter_datum.status,
                            filter_datum.accno,
                            filter_datum.amount,             
                            filter_datum.response,
                            filter_datum.request,
                            filter_datum.ip,
                            f"{filter_datum.date}:{filter_datum.time}",
                            filter_datum.user.username
                        ]
                log_data.append(datum_log)
        return log_data
    
    def internalTransferLog(self):
        self.logData = [
                             ['200 Ok', '123536738383', '1981282882221', 50000,  '{"amount":50000,"note":"deposit cash", "usage":[{"provider":"mtn","amount":1000},{"provider":"airtel","amount":4000}  ]}', '{"Status": "OK","StatusCode": "0","BankDepositRequestReference": "0777d5c17d4066b82ab86dff8a46af6f"} ', '102.100.5.1','4/11/2024','6:12 pm'],
                       
                   ]
        filter_type = self.log_params.get("filter_type","all")
        print(f"\n\tusing filter: {filter_type}")
        filter_data = InternalTransfer.objects.filter(owner = self.user_man)
        log_data =  []
        filter_data_number = filter_data.count()
        print("\n response number: ",filter_data_number)
        log_data =  []
        if filter_data_number==0:
            return log_data
        #for filter_datum in filter_data:
        #    datum_log = [
        #                filter_datum.status,
        #                filter_datum.sender_acc,             
        #                filter_datum.recv_acc,
        #                filter_datum.amount,
        #                filter_datum.response,
        #                filter_datum.request,
        #                filter_datum.ip,
        #                f"{filter_datum.date} {filter_datum.time}",
        #                filter_datum.user.username
        #    ]
        #   log_data.append(datum_log)
        for filter_datum in filter_data:
            record_date = filter_datum.date
            if filter_type == "date_filter":
                str_start_date = self.log_params.get("start_datepicker",datetime.now())
                str_end_date = self.log_params.get("end_datepicker",datetime.now())

                start_date = datetime.strptime(str_start_date,"%Y-%m-%d").date()
                end_date = datetime.strptime(str_end_date,"%Y-%m-%d").date()

                print(f"using filter: {start_date} to {end_date}")
                if (record_date>=start_date) and (record_date<=end_date):

                    datum_log = [
                        filter_datum.status,
                        filter_datum.sender_acc,             
                        filter_datum.recv_acc,
                        filter_datum.amount,
                        filter_datum.response,
                        filter_datum.request,
                        filter_datum.ip,
                        f"{filter_datum.date} {filter_datum.time}",
                        filter_datum.user.username
                        
                    ]
                    log_data.append(datum_log)
            elif filter_type == "today_filter":
                start_date = datetime.now()
                
                print(f"using filter: {start_date}")
                if (record_date==start_date):
                    datum_log = [
                        filter_datum.status,
                        filter_datum.sender_acc,             
                        filter_datum.recv_acc,
                        filter_datum.amount,
                        filter_datum.response,
                        filter_datum.request,
                        filter_datum.ip,
                        f"{filter_datum.date} {filter_datum.time}",
                        filter_datum.user.username
                        
                    ]
                    log_data.append(datum_log)
            else:
                print("displaying all logs")
                datum_log = [                       
                        filter_datum.status,
                        filter_datum.sender_acc,             
                        filter_datum.recv_acc,
                        filter_datum.amount,
                        filter_datum.response,
                        filter_datum.request,
                        filter_datum.ip,
                        f"{filter_datum.date} {filter_datum.time}",
                        filter_datum.user.username
                    ]
                log_data.append(datum_log)
        return log_data
    
    
    def bankWithdrawLog(self):
        self.logData = [
                             ['200 Ok', '123536738383', 50000,  '{"amount":50000,"note":"deposit cash", "usage":[{"provider":"mtn","amount":1000},{"provider":"airtel","amount":4000}  ]}', '{"Status": "OK","StatusCode": "0","BankDepositRequestReference": "0777d5c17d4066b82ab86dff8a46af6f"} ', '102.100.5.1','4/11/2024','6:12 pm'],
                       
                   ]
        
        filter_type = self.log_params.get("filter_type","all")
        print(f"\n\tusing filter: {filter_type}")
        filter_data = WithdrawMoneyToBank.objects.filter(owner = self.user_man)
        
        filter_data_number = filter_data.count()
        print("\n response number: ",filter_data_number)
        log_data =  []
        if filter_data_number==0:
            return log_data
        #for filter_datum in filter_data:
        #    datum_log = [
        #                filter_datum.status,
        #                filter_datum.accno,
        #                filter_datum.amount,             
        #                filter_datum.response,
        #                filter_datum.request,
        #                filter_datum.ip,
        #                f"{filter_datum.date}:{filter_datum.time}",
        #                filter_datum.user.username
        #               
        #    ]
        #    log_data.append(datum_log)
        
        for filter_datum in filter_data:
            record_date = filter_datum.date
            if filter_type == "date_filter":
                str_start_date = self.log_params.get("start_datepicker",datetime.now())
                str_end_date = self.log_params.get("end_datepicker",datetime.now())

                start_date = datetime.strptime(str_start_date,"%Y-%m-%d").date()
                end_date = datetime.strptime(str_end_date,"%Y-%m-%d").date()

                print(f"using filter: {start_date} to {end_date}")
                if (record_date>=start_date) and (record_date<=end_date):

                    datum_log = [
                        filter_datum.status,
                        filter_datum.accno,
                        filter_datum.amount,
                        filter_datum.response,
                        filter_datum.request,
                        filter_datum.ip,
                        f"{filter_datum.date} {filter_datum.time}",
                        filter_datum.user.username
                        
                    ]
                    log_data.append(datum_log)
            elif filter_type == "today_filter":
                start_date = datetime.now()
                
                print(f"using filter: {start_date}")
                if (record_date==start_date):
                    datum_log = [
                        filter_datum.status,
                        filter_datum.accno,
                        filter_datum.amount,
                        filter_datum.response,
                        filter_datum.request,
                        filter_datum.ip,
                        f"{filter_datum.date} {filter_datum.time}",
                        filter_datum.user.username
                        
                    ]
                    log_data.append(datum_log)
            else:
                print("displaying all logs")
                datum_log = [                       
                        filter_datum.status,
                        filter_datum.accno,
                        filter_datum.amount,
                        filter_datum.response,
                        filter_datum.request,
                        filter_datum.ip,
                        f"{filter_datum.date} {filter_datum.time}",
                        filter_datum.user.username
                    ]
                log_data.append(datum_log)
        return log_data
    
    def transactionStatusLog(self):
        self.logData = [
                             ['200 Ok', '123536738383', 'DEPOSIT','{"amount":50000,"note":"deposit cash", "usage":[{"provider":"mtn","amount":1000},{"provider":"airtel","amount":4000}  ]}', '{"Status": "OK","StatusCode": "0","BankDepositRequestReference": "0777d5c17d4066b82ab86dff8a46af6f"} ', '102.100.5.1','4/11/2024','6:12 pm'],
                       
                   ]
        filter_type = self.log_params.get("filter_type","all")
        print(f"\n\tusing filter: {filter_type}")
        filter_data = TransactionStatus.objects.filter(owner = self.user_man)
        log_data =  []
        filter_data_number = filter_data.count()
        print("\n response number: ",filter_data_number)
        log_data =  []
        if filter_data_number==0:
            return log_data
        #for filter_datum in filter_data:
        #    datum_log = [
        #                filter_datum.status,
        #                filter_datum.transaction_id,
        #                filter_datum.transaction_type,             
        #                str(filter_datum.response),
        #                str(filter_datum.request),
        #                filter_datum.ip,
        #                f"{filter_datum.date} {filter_datum.time}",
        #                filter_datum.user.username
        #    ]
        #    log_data.append(datum_log)
        for filter_datum in filter_data:
            record_date = filter_datum.date
            if filter_type == "date_filter":
                str_start_date = self.log_params.get("start_datepicker",datetime.now())
                str_end_date = self.log_params.get("end_datepicker",datetime.now())

                start_date = datetime.strptime(str_start_date,"%Y-%m-%d").date()
                end_date = datetime.strptime(str_end_date,"%Y-%m-%d").date()

                print(f"using filter: {start_date} to {end_date}")
                if (record_date>=start_date) and (record_date<=end_date):

                    datum_log = [
                        filter_datum.status,
                        filter_datum.transaction_id,
                        filter_datum.transaction_type,             
                        str(filter_datum.response),
                        str(filter_datum.request),
                        filter_datum.ip,
                        f"{filter_datum.date} {filter_datum.time}",
                        filter_datum.user.username
                        
                    ]
                    log_data.append(datum_log)
            elif filter_type == "today_filter":
                start_date = datetime.now()
                
                print(f"using filter: {start_date}")
                if (record_date==start_date):
                    datum_log = [
                        filter_datum.status,
                        filter_datum.transaction_id,
                        filter_datum.transaction_type,             
                        str(filter_datum.response),
                        str(filter_datum.request),
                        filter_datum.ip,
                        f"{filter_datum.date} {filter_datum.time}",
                        filter_datum.user.username
                        
                    ]
                    log_data.append(datum_log)
            else:
                print("displaying all logs")
                datum_log = [                       
                        filter_datum.status,
                        filter_datum.transaction_id,
                        filter_datum.transaction_type,             
                        str(filter_datum.response),
                        str(filter_datum.request),
                        filter_datum.ip,
                        f"{filter_datum.date} {filter_datum.time}",
                        filter_datum.user.username
                    ]
                log_data.append(datum_log)
        return log_data
    
    def bankWithdrawStatusLog(self):
        self.logData = [
                             ['200 Ok', '123536738383',50000,'{"amount":50000,"note":"deposit cash", "usage":[{"provider":"mtn","amount":1000},{"provider":"airtel","amount":4000}  ]}', '{"Status": "OK","StatusCode": "0","BankDepositRequestReference": "0777d5c17d4066b82ab86dff8a46af6f"} ', '102.100.5.1','4/11/2024','6:12 pm'],
                       
                   ]
        filter_type = self.log_params.get("filter_type","all")
        print(f"\n\tusing filter: {filter_type}")
        filter_data = BankWithdrawStatus.objects.filter(owner = self.user_man)
        log_data =  []
        filter_data_number = filter_data.count()
        print("\n response number: ",filter_data_number)
        log_data =  []
        if filter_data_number==0:
            return log_data
        #for filter_datum in filter_data:
        #    datum_log = [
        #                filter_datum.status,
        #                filter_datum.transaction_id,
        #                filter_datum.amount,             
        #                str(filter_datum.response),
        #                str(filter_datum.request),
        #                filter_datum.ip,
        #                f"{filter_datum.date} {filter_datum.time}",
        #                filter_datum.user.username
        #    ]
        #    log_data.append(datum_log)
        
        for filter_datum in filter_data:
            record_date = filter_datum.date
            if filter_type == "date_filter":
                str_start_date = self.log_params.get("start_datepicker",datetime.now())
                str_end_date = self.log_params.get("end_datepicker",datetime.now())

                start_date = datetime.strptime(str_start_date,"%Y-%m-%d").date()
                end_date = datetime.strptime(str_end_date,"%Y-%m-%d").date()

                print(f"using filter: {start_date} to {end_date}")
                if (record_date>=start_date) and (record_date<=end_date):

                    datum_log = [
                        filter_datum.status,
                        filter_datum.transaction_id,
                        filter_datum.amount,            
                        str(filter_datum.response),
                        str(filter_datum.request),
                        filter_datum.ip,
                        f"{filter_datum.date} {filter_datum.time}",
                        filter_datum.user.username
                        
                    ]
                    log_data.append(datum_log)
            elif filter_type == "today_filter":
                start_date = datetime.now()
                
                print(f"using filter: {start_date}")
                if (record_date==start_date):
                    datum_log = [
                        filter_datum.status,
                        filter_datum.transaction_id,
                        filter_datum.amount,              
                        str(filter_datum.response),
                        str(filter_datum.request),
                        filter_datum.ip,
                        f"{filter_datum.date} {filter_datum.time}",
                        filter_datum.user.username
                        
                    ]
                    log_data.append(datum_log)
            else:
                print("displaying all logs")
                datum_log = [                       
                        filter_datum.status,
                        filter_datum.transaction_id,
                        filter_datum.amount,            
                        str(filter_datum.response),
                        str(filter_datum.request),
                        filter_datum.ip,
                        f"{filter_datum.date} {filter_datum.time}",
                        filter_datum.user.username
                    ]
                log_data.append(datum_log)
        return log_data
    
    def balanceLog(self):
        self.logData = [
                             ['200 Ok', '50000','{"amount":50000,"note":"deposit cash", "usage":[{"provider":"mtn","amount":1000},{"provider":"airtel","amount":4000}  ]}', '{"Status": "OK","StatusCode": "0","BankDepositRequestReference": "0777d5c17d4066b82ab86dff8a46af6f"} ', '102.100.5.1','4/11/2024','6:12 pm'],
                       
                   ]
        
        filter_type = self.log_params.get("filter_type","all")
        print(f"\n\tusing filter: {filter_type}")
        filter_data = Balance.objects.filter(owner = self.user_man)
        log_data =  []
        filter_data_number = filter_data.count()
        print("\n response number: ",filter_data_number)
        log_data =  []
        if filter_data_number==0:
            return log_data
        #for filter_datum in filter_data:
        #    datum_log = [
        #                filter_datum.status,
        #                str(filter_datum.balance),         
        #                str(filter_datum.response),
        #                str(filter_datum.request),
        #                filter_datum.ip,
        #                f"{filter_datum.date} {filter_datum.time}",
        #                filter_datum.user.username
        #    ]
        #    log_data.append(datum_log)
        
        for filter_datum in filter_data:
            record_date = filter_datum.date
            if filter_type == "date_filter":
                str_start_date = self.log_params.get("start_datepicker",datetime.now())
                str_end_date = self.log_params.get("end_datepicker",datetime.now())

                start_date = datetime.strptime(str_start_date,"%Y-%m-%d").date()
                end_date = datetime.strptime(str_end_date,"%Y-%m-%d").date()

                print(f"using filter: {start_date} to {end_date}")
                if (record_date>=start_date) and (record_date<=end_date):

                    datum_log = [
                        filter_datum.status,
                        str(filter_datum.balance),           
                        str(filter_datum.response),
                        str(filter_datum.request),
                        filter_datum.ip,
                        f"{filter_datum.date} {filter_datum.time}",
                        filter_datum.user.username
                        
                    ]
                    log_data.append(datum_log)
            elif filter_type == "today_filter":
                start_date = datetime.now()
                
                print(f"using filter: {start_date}")
                if (record_date==start_date):
                    datum_log = [
                        filter_datum.status,
                        str(filter_datum.balance),             
                        str(filter_datum.response),
                        str(filter_datum.request),
                        filter_datum.ip,
                        f"{filter_datum.date} {filter_datum.time}",
                        filter_datum.user.username
                        
                    ]
                    log_data.append(datum_log)
            else:
                print("displaying all logs")
                datum_log = [                       
                        filter_datum.status,
                        str(filter_datum.balance),           
                        str(filter_datum.response),
                        str(filter_datum.request),
                        filter_datum.ip,
                        f"{filter_datum.date} {filter_datum.time}",
                        filter_datum.user.username
                    ]
                log_data.append(datum_log)
        return log_data
    
    def ministatementLog(self):
        self.logData = [
                             ['200 Ok','14566egfdtd6e77e7', '50000','{"amount":50000,"note":"deposit cash", "usage":[{"provider":"mtn","amount":1000},{"provider":"airtel","amount":4000}  ]}', '{"Status": "OK","StatusCode": "0","BankDepositRequestReference": "0777d5c17d4066b82ab86dff8a46af6f"} ', '102.100.5.1','4/11/2024','6:12 pm'],
                       
                   ]
        
        filter_type = self.log_params.get("filter_type","all")
        print(f"\n\tusing filter: {filter_type}")
        filter_data = MiniStatement.objects.filter(owner = self.user_man)
        log_data =  []
        filter_data_number = filter_data.count()
        print("\n response number: ",filter_data_number)
        log_data =  []
        if filter_data_number==0:
            return log_data
        #for filter_datum in filter_data:
        #    datum_log = [
        #                filter_datum.status,
        #                filter_datum.total_transactions,  
        #                filter_datum.response,
        #                filter_datum.request,
        #                filter_datum.ip,
        #                filter_datum.date,
        #                filter_datum.time
        #    ]
        #    log_data.append(datum_log)
        for filter_datum in filter_data:
            record_date = filter_datum.date
            if filter_type == "date_filter":
                str_start_date = self.log_params.get("start_datepicker",datetime.now())
                str_end_date = self.log_params.get("end_datepicker",datetime.now())

                start_date = datetime.strptime(str_start_date,"%Y-%m-%d").date()
                end_date = datetime.strptime(str_end_date,"%Y-%m-%d").date()

                print(f"using filter: {start_date} to {end_date}")
                if (record_date>=start_date) and (record_date<=end_date):

                    datum_log = [
                        filter_datum.status,
                        filter_datum.total_transactions,
                        filter_datum.response,
                        filter_datum.request,
                        filter_datum.ip,
                        f"{filter_datum.date} {filter_datum.time}",
                        filter_datum.user.username
                        
                    ]
                    log_data.append(datum_log)
            elif filter_type == "today_filter":
                start_date = datetime.now()
                
                print(f"using filter: {start_date}")
                if (record_date==start_date):
                    datum_log = [
                        filter_datum.status,
                        filter_datum.total_transactions,
                        filter_datum.response,
                        filter_datum.request,
                        filter_datum.ip,
                        f"{filter_datum.date} {filter_datum.time}",
                        filter_datum.user.username
                        
                    ]
                    log_data.append(datum_log)
            else:
                print("displaying all logs")
                datum_log = [                       
                        filter_datum.status,
                        filter_datum.total_transactions,
                        filter_datum.response,
                        filter_datum.request,
                        filter_datum.ip,
                        f"{filter_datum.date} {filter_datum.time}",
                        filter_datum.user.username
                    ]
                log_data.append(datum_log)
        return log_data
   
    #def apiKeys(self):
    #    return ""
       
    #def allCompanies(self):
    #     return ""
        
    #def allAdmins(self):
    #    return ""
    
       
   