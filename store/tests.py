from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Product, ProductVariant, Basket, Order, OrderItem
from decimal import Decimal

class ProductModelTest(TestCase):
    def test_create_product_and_variant(self):
        category = Category.objects.create(name="Keyrings")
        product = Product.objects.create(name="Resin Keyring")
        product.categories.add(category)

        variant = ProductVariant.objects.create(
            product=product,
            description="Blue glitter keyring",
            color_name="Blue",
            price=Decimal("5.99"),
            color_codes=["#0000FF"]
        )

        self.assertEqual(str(product), "Resin Keyring")
        self.assertEqual(str(variant), "Resin Keyring - Blue")
        self.assertEqual(variant.price, Decimal("5.99"))
        self.assertEqual(variant.color_codes, ["#0000FF"])


class BasketModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        product = Product.objects.create(name="Phone Case")
        self.variant = ProductVariant.objects.create(
            product=product,
            description="Clear resin case",
            color_name="Clear",
            price=Decimal("12.50"),
            color_codes=["#FFFFFF"]
        )

    def test_basket_total_price(self):
        basket_item = Basket.objects.create(
            user=self.user,
            variant=self.variant,
            quantity=2
        )
        self.assertEqual(basket_item.get_total_price(), Decimal("25.00"))
        self.assertEqual(str(basket_item), "testuser - Phone Case - Clear x 2")


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="customer", password="password")
        self.product = Product.objects.create(name="Necklace")
        self.variant = ProductVariant.objects.create(
            product=self.product,
            description="Gold plated necklace",
            color_name="Gold",
            price=Decimal("20.00"),
            color_codes=["#FFD700"]
        )

    def test_order_and_items(self):
        order = Order.objects.create(
            user=self.user,
            total=Decimal("20.00"),
            delivery_method="locker",
            delivery_size="Medium",
            delivery=Decimal("2.99"),
            grand_total=Decimal("22.99"),
            full_name="Jane Doe",
            email="jane@example.com",
            street_address1="123 Test St",
            town_or_city="Testville",
            postcode="TE57 1NG",
            country="UK",
            phone_number="07123456789"
        )

        order_item = OrderItem.objects.create(
            order=order,
            product_variant=self.variant,
            quantity=1,
            price=self.variant.price
        )

        self.assertEqual(str(order), f"Order #{order.id} by customer")
        self.assertEqual(str(order_item), "Necklace (Gold) × 1")
        self.assertEqual(order_item.price, Decimal("20.00"))



