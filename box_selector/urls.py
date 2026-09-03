from django.urls import path

from .views import box_list, order_detail, order_list, product_list, recommend_box_view, home, recommendation_page, create_order

urlpatterns = [
    path("", home, name="home"),
    path("products/",product_list,name="product-list",),
    path("boxes/",box_list,name="box-list",),
    path("orders/",order_list,name="order-list",),
    path("orders/<int:order_id>/",order_detail,name="order-detail",),
    path("orders/<int:order_id>/recommend/",recommend_box_view,name="recommend-box",),
    path("orders/<int:order_id>/recommendation/",recommendation_page,name="recommendation-page",),
    path("orders/create/",create_order,name="create-order",),
]