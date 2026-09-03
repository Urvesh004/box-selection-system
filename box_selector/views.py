from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import OrderItemFormSet
from .models import Box, Order, OrderItem, Product
from .services import recommend_box


def home(request):

    context = {
        "product_count": Product.objects.count(),
        "box_count": Box.objects.count(),
        "order_count": Order.objects.count(),
    }

    return render(request, "box_selector/home.html", context)


def product_list(request):

    products = Product.objects.all().order_by("name")

    return render(request, "box_selector/product_list.html", {"products": products})


def box_list(request):

    boxes = Box.objects.all().order_by("cost")

    return render(request, "box_selector/box_list.html", {"boxes": boxes})


def order_list(request):

    orders = Order.objects.all().order_by("-created_at")

    return render(request, "box_selector/order_list.html", {"orders": orders})


def order_detail(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    return render(request, "box_selector/order_detail.html", {"order": order})


def create_order(request):

    if request.method == "POST":

        formset = OrderItemFormSet(request.POST)

        if formset.is_valid():

            valid_items = []

            for form in formset:

                product = form.cleaned_data.get("product")
                quantity = form.cleaned_data.get("quantity")

                if not product and not quantity:
                    continue

                if product and quantity:
                    valid_items.append((product, quantity))

            with transaction.atomic():

                order = Order.objects.create()

                for product, quantity in valid_items:

                    OrderItem.objects.create(
                        order=order, product=product, quantity=quantity
                    )

            return redirect("order-detail", order_id=order.id)

    else:

        formset = OrderItemFormSet()

    return render(request, "box_selector/create_order.html", {"formset": formset})


def recommendation_page(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    box = recommend_box(order)

    return render(
        request, "box_selector/recommendation.html", {"order": order, "box": box}
    )


def recommend_box_view(request, order_id):

    if request.method != "GET":

        return JsonResponse(
            {"success": False, "message": "Only GET method is allowed."}, status=405
        )

    order = get_object_or_404(Order, id=order_id)

    box = recommend_box(order)

    if box is None:

        return JsonResponse(
            {
                "success": False,
                "order_id": order.id,
                "message": "No suitable box found for this order.",
            },
            status=404,
        )

    return JsonResponse(
        {
            "success": True,
            "order_id": order.id,
            "message": "Suitable box found.",
            "recommended_box": {
                "id": box.id,
                "name": box.name,
                "length": str(box.length),
                "width": str(box.width),
                "height": str(box.height),
                "max_weight": str(box.max_weight),
                "cost": str(box.cost),
            },
        }
    )
