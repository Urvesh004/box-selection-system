from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .forms import OrderItemFormSet
from .models import Box, Order, OrderItem, Product
from .services import recommend_box

class BoxRecommendationTests(TestCase):

    def setUp(self):
        self.small_box = Box.objects.create(
            name="Small Box",
            length=20,
            width=20,
            height=10,
            max_weight=2,
            cost=10,
        )

        self.medium_box = Box.objects.create(
            name="Medium Box",
            length=35,
            width=25,
            height=10,
            max_weight=5,
            cost=20,
        )

        self.large_box = Box.objects.create(
            name="Large Box",
            length=50,
            width=40,
            height=20,
            max_weight=10,
            cost=40,
        )

        self.laptop = Product.objects.create(
            name="Laptop",
            length=30,
            width=20,
            height=5,
            weight=2,
        )

    def test_product_fits_in_medium_box(self):
        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=self.laptop,
            quantity=1,
        )

        result = recommend_box(order)

        self.assertEqual(result, self.medium_box)

    def test_product_too_large(self):
        product = Product.objects.create(
            name="Large Product",
            length=100,
            width=100,
            height=100,
            weight=2,
        )

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
        )

        result = recommend_box(order)

        self.assertIsNone(result)

    def test_product_too_heavy(self):
        product = Product.objects.create(
            name="Heavy Product",
            length=30,
            width=20,
            height=5,
            weight=20,
        )

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
        )

        result = recommend_box(order)

        self.assertIsNone(result)

    def test_exact_dimensions_are_allowed(self):
        product = Product.objects.create(
            name="Exact Product",
            length=35,
            width=25,
            height=10,
            weight=5,
        )

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
        )

        result = recommend_box(order)

        self.assertEqual(result, self.medium_box)

    def test_cheapest_suitable_box_is_selected(self):
        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=self.laptop,
            quantity=1,
        )

        result = recommend_box(order)

        self.assertEqual(result.cost, 20)
        self.assertEqual(result.name, "Medium Box")

    def test_empty_order_returns_none(self):
        order = Order.objects.create()

        result = recommend_box(order)

        self.assertIsNone(result)

    def test_quantity_is_considered_for_weight(self):
        product = Product.objects.create(
            name="Mouse",
            length=10,
            width=6,
            height=4,
            weight=0.2,
        )

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=10,
        )

        result = recommend_box(order)

        self.assertEqual(result, self.small_box)

    def test_multiple_products(self):
        mouse = Product.objects.create(
            name="Mouse",
            length=10,
            width=6,
            height=4,
            weight=0.2,
        )

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=self.laptop,
            quantity=1,
        )

        OrderItem.objects.create(
            order=order,
            product=mouse,
            quantity=2,
        )

        result = recommend_box(order)

        self.assertEqual(result, self.medium_box)


class ModelValidationTests(TestCase):

    def test_product_cannot_have_negative_length(self):

        product = Product(
            name="Invalid Product",
            length=-10,
            width=10,
            height=10,
            weight=1,
        )

        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_product_cannot_have_zero_weight(self):

        product = Product(
            name="Invalid Product",
            length=10,
            width=10,
            height=10,
            weight=0,
        )

        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_box_cannot_have_negative_cost(self):

        box = Box(
            name="Invalid Box",
            length=20,
            width=20,
            height=10,
            max_weight=5,
            cost=-10,
        )

        with self.assertRaises(ValidationError):
            box.full_clean()

class OrderFormSetTests(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Laptop",
            length=Decimal("30.00"),
            width=Decimal("20.00"),
            height=Decimal("5.00"),
            weight=Decimal("2.00"),
        )

    def test_empty_order_is_invalid(self):
        formset = OrderItemFormSet(
            data={
                "form-TOTAL_FORMS": "1",
                "form-INITIAL_FORMS": "0",
                "form-0-product": "",
                "form-0-quantity": "",
            }
        )

        self.assertFalse(formset.is_valid())
    
    def test_valid_order_formset(self):
        formset = OrderItemFormSet(
            data={
                "form-TOTAL_FORMS": "1",
                "form-INITIAL_FORMS": "0",
                "form-0-product": str(self.product.id),
                "form-0-quantity": "2",
            }
        )

        self.assertTrue(formset.is_valid())
    def test_duplicate_product_is_invalid(self):
        formset = OrderItemFormSet(
            data={
                "form-TOTAL_FORMS": "2",
                "form-INITIAL_FORMS": "0",
                "form-0-product": str(self.product.id),
                "form-0-quantity": "1",
                "form-1-product": str(self.product.id),
                "form-1-quantity": "2",
            }
        )

        self.assertFalse(formset.is_valid())

    def test_zero_quantity_is_invalid(self):
        formset = OrderItemFormSet(
            data={
                "form-TOTAL_FORMS": "1",
                "form-INITIAL_FORMS": "0",
                "form-0-product": str(self.product.id),
                "form-0-quantity": "0",
            }
        )

        self.assertFalse(formset.is_valid())

    def test_zero_quantity_is_invalid(self):
        formset = OrderItemFormSet(
            data={
                "form-TOTAL_FORMS": "1",
                "form-INITIAL_FORMS": "0",
                "form-0-product": str(self.product.id),
                "form-0-quantity": "0",
            }
        )

        self.assertFalse(formset.is_valid())