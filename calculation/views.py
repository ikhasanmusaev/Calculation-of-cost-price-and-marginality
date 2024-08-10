from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from calculation.models import Product
from calculation.paginations import ProductPagination
from calculation.serializers import ProductSerializer, ProductGetSerializer


class ProductCostCalculationView(APIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    @swagger_auto_schema(
        operation_description="Рассчитывает себестоимость и маржинальность товара на основе предоставленных данных.",
        request_body=ProductSerializer,
        responses={
            200: openapi.Response(
                description="Успешный расчет",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_cost': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                     description="Общая себестоимость товара"),
                        'selling_price': openapi.Schema(type=openapi.TYPE_NUMBER, description="Цена продажи"),
                        'fbs_commission': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'fbo_commission': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'dbs_commission': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'delivery_cost': openapi.Schema(type=openapi.TYPE_NUMBER, description="Стоимость доставки"),
                        'profit_per_item': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                          description="Прибыль с одного товара"),
                        'profit_per_batch': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                           description="Прибыль с партии товара"),
                    }
                )
            ),
            400: "Неверные входные данные"
        }
    )
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()

            # Расчеты
            data = ProductGetSerializer(product).data
            return Response(data)
        return Response(serializer.errors, status=400)

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        paginator = ProductPagination()
        paginated_products = paginator.paginate_queryset(products, request)

        serializer = ProductGetSerializer(paginated_products, many=True)
        return paginator.get_paginated_response(serializer.data)
