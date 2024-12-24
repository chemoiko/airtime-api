from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
class MasterObject:
    def __init__(self,name,password):
        self.APIUsername = name
        self.APIPassword = password

class YoDepositMoney:
    """
    Class representing the Yo API Deposit money request structure
    """
    def __init__(self, api_username, api_password,telno,amount):
        """
        Initialize the YOAPI object used to deposit money  from a client telephone number with the provided API credentials.

        Args:
        api_username (str, required): The YO API username
        api_password (str, required): The YO API password
        account (str, required): The telephone number to which to deposit money from e.g 256700000000 where 256 is the area code
        amount (float, required): amount of money to deposit
        """
        #, non_blocking, amount, account, account_provider_code, narrative, narrative_file_name, narrative_file_base64, internal_reference, external_reference, provider_reference_text, instant_notification_url, failure_notification_url, authentication_signature_base64):
        self.APIUsername = api_username
        self.APIPassword = api_password
        #self.Method = "acrequestfundspush"
        self.Method = "acdepositfunds"
        self.NonBlocking = "FALSE"
        self.Amount = amount
        self.Account = telno
        #self.AccountProviderCode = account_provider_code
        self.Narrative = "Edoctor Deposit"
        #self.NarrativeFileName = narrative_file_name
        #self.NarrativeFileBase64 = narrative_file_base64
        #self.InternalReference = internal_reference
        #self.ExternalReference = external_reference
        #self.ProviderReferenceText = provider_reference_text
        #self.InstantNotificationUrl = instant_notification_url
        #self.FailureNotificationUrl = failure_notification_url
        #self.AuthenticationSignatureBase64 = authentication_signature_base64

class YoWithdrawMoney:
    """
    Class representing the Yo API Withdraw money request structure
    """
    def __init__(self, api_username, api_password,account,amount):
        #, account_provider_code, transaction_limit_account_identifier, narrative, narrative_file_name, narrative_file_base64, internal_reference, external_reference, provider_reference_text, public_key_authentication_nonce, public_key_authentication_signature_base64):
        """
        Initialize the YOAPI object used to withdraw money with the provided API credentials, telephone number and amount.

        Args:
        api_username (str, required): The YO API username
        api_password (str, required): The YO API password
        account (str, required): The telephone number to which to withdraw money to e.g 256700000000 where 256 is the area code
        amount (float, required): amount of money to withdraw
        """
        self.APIUsername = api_username
        self.APIPassword = api_password
        self.Method = "acwithdrawfunds"
        self.NonBlocking = "FALSE"
        self.Amount = amount
        self.Account = account
        #self.AccountProviderCode = account_provider_code
        #self.TransactionLimitAccountIdentifier = transaction_limit_account_identifier
        self.Narrative = "withdraw money"
        #self.NarrativeFileName = narrative_file_name
        #self.NarrativeFileBase64 = narrative_file_base64
        #self.InternalReference = internal_reference
        #self.ExternalReference = external_reference
        #self.ProviderReferenceText = provider_reference_text
        #self.PublicKeyAuthenticationNonce = public_key_authentication_nonce
        #self.PublicKeyAuthenticationSignatureBase64 = public_key_authentication_signature_base64


class YoSendAirtime:
    """
    Class representing the Yo API Send Airtime request structure
    """
    def __init__(self,name,password,amount,account):
        """
        Initialize the YOAPI object to send artime with the provided API credentials, amount and telephone number to which to send airtime to.


        Args:
        name (str, required): The YO API username
        password (str, required): The YO API password
        amount (float, required): amount of airtime to buy
        Account (str, required): The telephone number to which to send airtime to e.g 256700000000 where 256 is the area code

        """
        self.APIUsername = name
        self.APIPassword = password
        self.Amount = amount
        self.Account = account
        self.Method = "acsendairtimemobile"
        self.InternetBundle =  ""
        self.AccountProviderCode = ""
        self.Narrative = "Airtime Gift"
        #self.NarrativeFileName = ""
        #self.InternalReference = ""
        #self.ExternalReference = ""
        self.ProviderReferenceText = ""

class YoSendInternalAirtime:
    """
    Class representing the Yo API Send Airtime to an internal yo account request structure
    """
    def __init__(self,name,password,amount,receiver_account,receiver_email):
        """
        Initialize the YOAPI object to send artime with the provided API credentials, amount and yo account to which to send airtime to.


        Args:
        name (str, required): The YO API username
        password (str, required): The YO API password
        receiver_amount (float, required): amount of airtime to buy
        Account (str, required): The telephone number to which to send airtime to e.g 256700000000 where 256 is the area code

        """
        self.APIUsername = name
        self.APIPassword = password
        self.Amount = amount
        self.BeneficiaryAccount = receiver_account
        self.BeneficiaryEmail = receiver_email
        self.Method = "acsendairtimeinternal"
        self.InternetBundle =  ""
        self.AccountProviderCode = ""
        self.Narrative = "Airtime Gift"
        #self.NarrativeFileName = ""
        #self.InternalReference = ""
        #self.ExternalReference = ""
        self.ProviderReferenceText = ""
 
class YoBuyAirtime:
    """
    Class representing the Yo API Buy Airtime request structure
    """
    def __init__(self, APIUsername, APIPassword,AirtimeCurrencyCode, Amount, TransactionReference=""):
        """
        Initialize the YOAPI object to BuyAirtime with the provided API credentials, currency code, amount and transaction reference.

        Args:
        APIUsername (str, required): The YO API username
        APIPassword (str, required): The YO API password
        AirtimeCurrencyCode (str, required): a code representing the currency being used to buy airtime and the service provide from which the airtime is being bought from
        Amount (float, required): amount of airtime to buy
        TransactionReference (str, optional): a transaction refernce to a previous transaction
        """
        self.APIUsername = APIUsername
        self.APIPassword = APIPassword
        self.Method = "acuserpurchaseairtimestock"
        self.AirtimeCurrencyCode = AirtimeCurrencyCode
        self.Amount = Amount
        self.TransactionReference = TransactionReference

class YoCheckMsisdn:
    """
    Class representing the Yo API request structure to get information about a telephone number (msisdn)
    """
    def __init__(self, APIUsername, APIPassword, Msisdn):
        """
        Initialize the YOAPI object with the provided API credentials and MSISDN.

        This method initializes the YOAPI object with the provided API credentials and MSISDN.
        Args:
        APIUsername (str, required): The YO API username
        APIPassword (str, required): The YO API password
        Msisdn (str, required): The MSISDN associated with the account you whose information you would like to get e.g 256700000000 where 256 is the area code
        """
        self.APIUsername = APIUsername #yo api username
        self.APIPassword = APIPassword #yo api password
        self.Method = "acgetmsisdnkycinfo" #method to use
        self.Msisdn = Msisdn #telephone number to check in the format 256700000000 where 256 is the area code
class YoMsisdnMoneyBalance:
    def __init__(self, APIUsername, APIPassword,Account):
        self.APIUsername = APIUsername
        self.APIPassword = APIPassword
        self.Method = "acgetmsisdnmmbalance"
        self.Account = Account
        self.AccountProviderCode = AccountProviderCode

class YoMoneyBalance:
    def __init__(self, APIUsername, APIPassword):
        self.APIUsername = APIUsername
        self.APIPassword = APIPassword
        self.Method = "acacctbalance"

class YoBankDepositStatus:
    def __init__(self, APIUsername, APIPassword,RequestTrackingId=None, BankDepositRequestReference=None):
        self.APIUsername = APIUsername
        self.APIPassword = APIPassword
        self.Method = "acbankdepositcheckstatus"
        if(RequestTrackingId != None):
            self.RequestTrackingId = RequestTrackingId
        elif(BankDepositRequestReference != None):
            self.BankDepositRequestReference = BankDepositRequestReference
        elif((RequestTrackingId != None)and(BankDepositRequestReference != None)):
            self.RequestTrackingId = RequestTrackingId
            self.BankDepositRequestReference = BankDepositRequestReference

class YoAccountValidity:
    def __init__(self, APIUsername, APIPassword, Account):
        self.APIUsername = APIUsername
        self.APIPassword = APIPassword
        self.Method = "acverifyaccountvalidity"
        self.Account = Account
        self.AccountProviderCode = AccountProviderCode

class YoBankDepositRequest:
    def __init__(self, APIUsername, APIPassword, RequestTrackingId=None, TotalDepositAmount=None, Narrative=None, BankTransferFileName=None, BankTransferFileContentBase64=None, CurrencyAllocations=None):
        self.APIUsername = APIUsername
        self.APIPassword = APIPassword
        self.Method = "acsubmitbankdeposit"
        if(RequestTrackingId!=None):
            self.RequestTrackingId = RequestTrackingId
        self.TotalDepositAmount = TotalDepositAmount
        self.Narrative = Narrative
        self.BankTransferFileName = BankTransferFileName
        self.BankTransferFileContentBase64 = BankTransferFileContentBase64
        self.AmountBreakDown = CurrencyAllocations


class YoCheckTransactionStatus:
    """
    Class representing the AutoCreate Transaction Check Status request structure
    """
    def __init__(self, api_username, api_password, transaction_reference = None, private_transaction_reference = None, deposit_transaction_type = "PULL"):
        """
        Initialize the AutoCreateTransactionCheckStatus object used to create a new transaction check status request with the provided API credentials and transaction details.

        Args:
        api_username (str, required): The API username
        api_password (str, required): The API password
        transaction_reference (str, required): The transaction reference for the request
        private_transaction_reference (str, required): The private transaction reference for the request
        deposit_transaction_type (str, required): The deposit transaction type for the request
        """
        self.APIUsername = api_username
        self.APIPassword = api_password
        self.Method = "actransactioncheckstatus"
        if(transaction_reference!=None):
            self.TransactionReference = transaction_reference
        elif(private_transaction_reference!=None):
            self.PrivateTransactionReference = private_transaction_reference
        self.DepositTransactionType = deposit_transaction_type

class YoBankWithdrawFunds:
    """
    Class representing the Withdraw Funds to Bank request structure
    """
    def __init__(self, api_username, api_password, amount, currency_code, bank_account_name, bank_account_number, bank_account_identifier, private_transaction_reference = None):
        """
        Initialize the AutoCreateWithdrawFundsToBank object used to create a new withdraw funds to bank request with the provided API credentials and transaction details.

        Args:
        api_username (str, required): The API username
        api_password (str, required): The API password
        amount (float, required): The amount to withdraw
        currency_code (str, required): The currency code for the withdrawal
        bank_account_name (str, required): The name of the bank account
        bank_account_number (str, required): The number of the bank account
        bank_account_identifier (str, required): The identifier of the bank account
        private_transaction_reference (str, optional): The private transaction reference for the request
        """
        self.APIUsername = api_username
        self.APIPassword = api_password
        self.Method = "acwithdrawfundstobank"
        self.Amount = amount
        self.CurrencyCode = currency_code
        self.BankAccountName = bank_account_name
        self.BankAccountNumber = bank_account_number
        self.BankAccountIdentifier = bank_account_identifier
        if (private_transaction_reference!=None):
            self.PrivateTransactionReference = private_transaction_reference


class YoBankWithdrawStatus:
    """
    Class representing the check Bank withdraw Status request structure
    """
    def __init__(self, api_username, api_password, settlement_transaction_identifier = None, private_transaction_reference = None):
        """
        Initialize the AutoCreateCheckBankSettlementStatus object used to create a new check bank settlement status request with the provided API credentials and transaction identifiers.

        Args:
        api_username (str, required): The API username
        api_password (str, required): The API password
        settlement_transaction_identifier (str, required): The settlement transaction identifier for the request, received from bank withdraw transaction response
        private_transaction_reference (str, required): The private transaction reference for the request
        """
        self.APIUsername = api_username
        self.APIPassword = api_password
        self.Method = "accheckbanksettlementstatus"
        if(settlement_transaction_identifier!=None):
            self.SettlementTransactionIdentifier = settlement_transaction_identifier
        elif(private_transaction_reference!=None):
            self.PrivateTransactionReference = private_transaction_reference


class YoBalanceCheck:
    """
    Class representing the Account Balance request structure
    """
    def __init__(self, api_username, api_password):
        """
        Initialize the AutoCreateAccountBalance object used to create a new account balance request with the provided API credentials.

        Args:
        api_username (str, required): The API username
        api_password (str, required): The API password
        """
        self.APIUsername = api_username
        self.APIPassword = api_password
        self.Method = "acacctbalance"


class YoMiniStatementRequest:
    """
    Class representing the AutoCreate XML request structure
    """
    def __init__(self, api_username, api_password, start_date=None, end_date=None, transaction_status=None, currency_code=None, result_set_limit=None, transaction_entry_designation=None, external_reference=None):
        """
        Initialize the MiniStatementRequest object used to create a new request with the provided API credentials and optional parameters.

        Args:
        api_username (str, required): The API username
        api_password (str, required): The API password
        start_date (str, optional): The start date of the statement range in YYYY-MM-DD format
        end_date (str, optional): The end date of the statement range in YYYY-MM-DD format
        transaction_status (str, optional): The transaction status to filter by
        currency_code (str, optional): The currency code to filter by
        result_set_limit (int, optional): The maximum number of results to return
        transaction_entry_designation (str, optional): The transaction entry designation to filter by
        external_reference (str, optional): The external reference to filter by
        """
        self.APIUsername = api_username
        self.APIPassword = api_password
        self.Method = "acgetministatement"
        if(start_date!=None):
            self.StartDate = start_date
        if(end_date!=None):
            self.EndDate = end_date
        if(transaction_status!=None):
            self.TransactionStatus = transaction_status
        if(currency_code!=None):
            self.CurrencyCode = currency_code
        if(result_set_limit!=None):
            self.ResultSetLimit = result_set_limit
        if(transaction_entry_designation!=None):
            self.TransactionEntryDesignation = transaction_entry_designation
        if(external_reference!=None):
            self.ExternalReference = external_reference


class YoInternalTransferRequest:
    """
    Class representing the AutoCreate Internal Transfer request structure
    """
    def __init__(self, api_username, api_password, currency_code, amount, beneficiary_account, beneficiary_email, narrative, narrative_file_name=None, narrative_file_base64=None, internal_reference=None, external_reference=None):
        """
        Initialize the InternalTransfer object used to create a new internal transfer of funds rwith the provided API credentials and optional parameters.

        Args:
        api_username (str, required): The API username
        api_password (str, required): The API password
        currency_code (str, required): The currency code for the transfer
        amount (float, required): The amount to transfer
        beneficiary_account (str, required): The beneficiary account number
        beneficiary_email (str, required): The beneficiary email address
        narrative (str, optional): The narrative for the transfer
        narrative_file_name (str, optional): The name of the narrative file
        narrative_file_base64 (str, optional): The base64 encoded narrative file
        internal_reference (str, optional): The internal reference for the transfer
        external_reference (str, optional): The external reference for the transfer
        """
        self.APIUsername = api_username
        self.APIPassword = api_password
        self.Method = "acinternaltransfer"
        self.CurrencyCode = currency_code
        self.Amount = amount
        self.BeneficiaryAccount = beneficiary_account
        self.BeneficiaryEmail = beneficiary_email
        self.Narrative = narrative
        if(narrative_file_name!=None):
            self.NarrativeFileName = narrative_file_name
        if(narrative_file_base64!=None):
            self.NarrativeFileBase64 = narrative_file_base64
        if(internal_reference!=None):
            self.InternalReference = internal_reference
        if(external_reference!=None):
            self.ExternalReference = external_reference

class YoRequest:
    """
    Class representing a yo xml request 
    """
    def __init__(self,internal_request):
        """
        Initialize the YOAPIRequest object with the internal request.

        This method initializes the YOAPIRequest object with the internal request, which should contain the necessary information in the request.

        Args:
        internal_request (dict): A dictionary containing the necessary information to in the request.
        """
        self.Request = internal_request.__dict__ #turn the requect object into a dictionary
        
    def to_xml(self,item_name_func = None):
        """
        Generate an XML styled format for the yo api request.

        Returns:
        str: The YO API request in XML format.
        """
        
        xml_str = dicttoxml(self.__dict__,attr_type=False,custom_root="AutoCreate",return_bytes=False,item_func=item_name_func) if item_name_func!= None else dicttoxml(self.__dict__,attr_type=False,custom_root="AutoCreate",return_bytes=False)
        xml_dom = parseString(xml_str)
        return xml_dom.toprettyxml()