from django.test import TestCase
from .models import PurchaseHistory

class PurchaseHistoryTestCase(TestCase):
    def setUp(self):
        PurchaseHistory.objects.create(
            confirmation_code="48761360",
            name="10-Day Water Park Fun & More - No Expiration",
            price = float(74.32),
            fullName = "Joe Smoe",
            email = "you@whatever.com",
            phone = "(817)555-5555",
            quantityTickets = 5
        )
        PurchaseHistory.objects.create(
            confirmation_code="48712360",
            name="2-Day Park Fun - No Expiration",
            price = float(34.52),
            fullName = "Sam Doe",
            email = "him@whatever.com",
            phone = "(214)555-5555",
            quantityTickets = 2
        )

    def test_total_price(self):
        """Test if total price is returned correctly to 2 decimal places"""
        joeHistory = PurchaseHistory.objects.get(fullName="Joe Smoe")
        samHistory = PurchaseHistory.objects.get(fullName="Sam Doe")
        self.assertEqual(joeHistory.total_price(), '371.60')
        self.assertEqual(samHistory.total_price(), '69.04')
        
        