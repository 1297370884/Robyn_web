from robyn import Request, Response, jsonify, status_codes
from apps.market import crud
from apps.market.models import Product
from core.database import AsyncSessionLocal

"""
    crud -> services -> api
    服务层:根据业务逻辑整合crud数据操作 封装业务方法 可以由上层函数直接调用
    服务层 应该完成 业务逻辑（如判断数据是否存在、响应失败的处理逻辑）
"""

async def get_product_by_id(request):
    """
    通过产品ID获取单个产品
    """
    try:
        async with AsyncSessionLocal() as db:
            product_id = request.path_params.get("product_id")
            product_obj = await crud.get_product(db, product_id) # 获取产品
            if not product_obj:
                return Response(status_code=status_codes.HTTP_404_NOT_FOUND,
                                headers={"Content-Type": "application/json"},
                                description=jsonify({"message": "Product not found"}))

            return Response(status_code=status_codes.HTTP_200_OK,
                            headers={"Content-Type": "application/json"},
                            description=jsonify(product_obj.to_dict()))
    except Exception as e:
        print(f"Error: {e}")
        return Response(status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR, message="获取产品失败")


async def get_product_by_name(request):
    """
    通过产品名称获取单个产品
    """
    try:
        async with AsyncSessionLocal() as db:
            product_name = request.path_params.get("product_name")
            product_obj = await crud.get_product_by_filter(db, {"name": product_name})
            if not product_obj:
                return Response(status_code=status_codes.HTTP_404_NOT_FOUND,
                                headers={"Content-Type": "application/json"},
                                description=jsonify({"message": "Product not found"}))

            return Response(status_code=status_codes.HTTP_200_OK,
                            headers={"Content-Type": "application/json"},
                            description=jsonify(product_obj.to_dict()))
    except Exception as e:
        print(f"Error: {e}")
        return Response(status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR, message="获取产品失败")

async def get_products_service(request):
    """
    获取所有产品
    """
    try:
        async with AsyncSessionLocal() as db:
            products = await crud.get_products_by_filters(db)
            
            products_data = [product.to_dict() for product in products]

        return Response(
            status_code=status_codes.HTTP_200_OK,
            headers={"Content-Type": "application/json"},
            description=jsonify(products_data)
        )
    except Exception as e:
        print(f"Error: {e}")
        return Response(status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR, description="获取产品失败")

async def create_product_service(request):
    """
    创建产品
    """
    try:
        # 根据产品名称检查产品是否已存在
        product_data = request.json() # 获取请求体中的JSON数据,将json数据转换为字典
        product_name = product_data.get("name")
        print(f'product_data: {product_data}')
        print(f'product_name: {product_name}')

        # 确保商品名称存在
        if not product_name:
            return Response(status_code=status_codes.HTTP_400_BAD_REQUEST,
                          headers={"Content-Type": "application/json"},
                          description=jsonify({"message": "Missing required fields"}))
        
        async with AsyncSessionLocal() as db:
            product_exists = await crud.get_product_by_filter(db, {"name": product_name})
            if product_exists:
                return Response(status_code=status_codes.HTTP_409_CONFLICT,
                                headers={"Content-Type": "application/json"},
                                description=jsonify({"message": "Product already exists"}))
            
            try:
                # 创建产品
                inserted_product_obj = await crud.create_product(db, product_data)
                if not inserted_product_obj:
                    raise Exception("Product creation failed")
                return Response(status_code=status_codes.HTTP_200_OK,
                                headers={"Content-Type": "application/json"},
                                description=jsonify(inserted_product_obj.to_dict()))
            except Exception as e:
                raise Exception(f"Database integrity error: {str(e)}")
            
    except Exception as e:
        print(f"Error: {e}")
        return Response(status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR, description="创建产品失败")

async def update_product_service(request):
    """
    更新产品
    """
    try:
        async with AsyncSessionLocal() as db:
            product_id = request.path_params.get("product_id")
            product_obj = await crud.get_product(db, product_id)
            if not product_obj:
                return Response(status_code=status_codes.HTTP_404_NOT_FOUND,
                                headers={"Content-Type": "application/json"},
                                description=jsonify({"message": "Product not found"}))
            updated_product_obj = await crud.update_product(db, product_id, request.json())

            return Response(status_code=status_codes.HTTP_200_OK,
                            headers={"Content-Type": "application/json"},
                            description=jsonify(updated_product_obj.to_dict()))
    except Exception as e:
        print(f"Error: {e}")
        return Response(status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR, message="更新产品失败")

async def delete_product_service(request):
    """
    删除产品
    """
    try:
        async with AsyncSessionLocal() as db:
            product_id = request.path_params.get("product_id")
            product_obj = await crud.get_product(db, product_id)
            if not product_obj:
                return Response(status_code=status_codes.HTTP_404_NOT_FOUND,
                                headers={"Content-Type": "application/json"},
                                description=jsonify({"message": "Product not found"}))
            
            await crud.delete_product(db, product_id)
            return Response(status_code=status_codes.HTTP_200_OK,
                            headers={"Content-Type": "application/json"},
                            description=jsonify({"message": "Product deleted successfully"}))
    except Exception as e:
        print(f"Error: {e}")
        return Response(status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR, message="删除产品失败")

