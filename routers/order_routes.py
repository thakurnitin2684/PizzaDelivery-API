from fastapi import APIRouter,Depends,status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from models import User,Order
from schemas import OrderModel,OrderStatusModel
from fastapi.encoders import jsonable_encoder
import oauth2
from repository import orders
order_router=APIRouter(
    prefix="/orders",
    tags=['orders']
)


@order_router.get('/')
async def hello(current_user: User = Depends(oauth2.get_current_user)):
    """
        ## A sample hello world route
        This returns Hello world
    """
    return orders.hello()


@order_router.post('/order',status_code=status.HTTP_201_CREATED)
async def place_an_order(order:OrderModel,current_username = Depends(oauth2.get_current_user)):
    """
        ## Placing an Order
        This requires the following
        - quantity : integer
        - pizza_size: str
    """
    return orders.place_an_order(order,current_username)



    
@order_router.get('/orders')
async def list_all_orders(current_username: User = Depends(oauth2.get_current_user)):
    """
        ## List all orders
        This lists all  orders made. It can be accessed by superusers
    """
    return orders.list_all_orders(current_username)


@order_router.get('/orders/{id}')
async def get_order_by_id(id:int,current_username: User = Depends(oauth2.get_current_user)):
    """
        ## Get an order by its ID
        This gets an order by its ID and is only accessed by a superuser
    """
    return orders.get_order_by_id(id,current_username)

    
@order_router.get('/user/orders')
async def get_user_orders(current_username: User = Depends(oauth2.get_current_user)):
    """
        ## Get a current user's orders
        This lists the orders made by the currently logged in users
    
    """
    return orders.get_user_orders(current_username)


@order_router.get('/user/order/{id}/')
async def get_specific_order(id:int,current_username: User = Depends(oauth2.get_current_user)):
    """
        ## Get a specific order by the currently logged in user
        This returns an order by ID for the currently logged in user
    """
    return orders.get_specific_order(id,current_username)

@order_router.put('/order/update/{id}/')
async def update_order(id:int,order:OrderModel,current_username: User = Depends(oauth2.get_current_user)):
    """
        ## Updating an order
        This udates an order and requires the following fields
        - quantity : integer
        - pizza_size: str
    """
    return orders.update_order(id,order)

    
@order_router.patch('/order/update/{id}/')
async def update_order_status(id:int,
        order:OrderStatusModel,
        current_username: User = Depends(oauth2.get_current_user)):

    """
        ## Update an order's status
        This is for updating an order's status and requires ` order_status ` in str format
    """
    return orders.update_order_status(id,order,current_username)


@order_router.delete('/order/delete/{id}/',status_code=status.HTTP_204_NO_CONTENT)
async def delete_an_order(id:int,current_username: User = Depends(oauth2.get_current_user)):
    """
        ## Delete an Order
        This deletes an order by its ID
    """
    return orders.delete_an_order(id)
