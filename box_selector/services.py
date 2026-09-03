from .models import Box


def recommend_box(order):
    items = order.items.all()

    if not items.exists():
        return None

    total_weight = sum(
        item.product.weight * item.quantity
        for item in items
    )

    required_length = max(
        item.product.length
        for item in items
    )

    required_width = max(
        item.product.width
        for item in items
    )

    required_height = max(
        item.product.height
        for item in items
    )

    suitable_boxes = Box.objects.filter(
        length__gte=required_length,
        width__gte=required_width,
        height__gte=required_height,
        max_weight__gte=total_weight,
    ).order_by("cost")

    return suitable_boxes.first()