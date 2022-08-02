from django.urls import path

from . import views

app_name = "product"

urlpatterns = [
    path('',views.product_list,name="product_list"),
    path('<int:id>',views.product_detail, name ="product_detail"),
    path('update/<int:id>',views.product_update, name ="product_update"),
    path('updatecomment/<int:id>',views.comment_update, name ="comment_update"),
]