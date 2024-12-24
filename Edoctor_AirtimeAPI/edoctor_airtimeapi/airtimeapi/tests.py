from django.test import TestCase
from .yo_api import YO_API
# Create your tests here.
class AirtimeAPITestCase(TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.yo_test = YO_API("90005702859","MsUl-Ei4O-BmJo-apHP-npHY-wsYT-c8nc-skny")
        print("\t\ttesting has begun")
    def test_getMSISDNInfo(self):
        """
        testing get msisdn information api
        """
        response = self.yo_test.getMSISDNInfo("256700000000")
        print(f"\n\tmsisdn info:{response}")
    
    def test_withdrawFunds(self):
        """
        Testing the withdraw funds endpoint
        """
        response = self.yo_test.withdrawMoney("256700000000",1000)
        print(f"\n\twithdraw money response:{response}")

    def test_sendAirtime(self):
        response = self.yo_test.sendAirtime("256700000000",500)
        print(f"\n\tsend airtime response:{response}")
        pass

    def test_buyAirtime(self):
        providers = ["mtn","MTN","airtel","AIRTEL","utl","UTL"]
        for provider in providers:
            response = self.yo_test.buyAirtime(provider,500)
            print(f"\n\tbuying airtime for {provider}\n {provider} Response: {response}")

    def test_depositMoney(self):
        response = self.yo_test.depositMoney("256700000000",500)
        print(f"\n\tdeposist money response:{response}")