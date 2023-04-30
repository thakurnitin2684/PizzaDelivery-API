# from sqlalchemy.orm import Session
from models import User,Order
from schemas import OrderModel,OrderStatusModel
from fastapi import HTTPException,status,Depends
from fastapi.encoders import jsonable_encoder
from database import SessionLocal,engine

session=SessionLocal(bind=engine)

def hello():
    return {"message":"Hello World!, orders"}



def place_an_order(order:OrderModel,current_username ):
    user=session.query(User).filter(User.username==current_username).first()
    new_order=Order(
        pizza_size=order.pizza_size,
        quantity=order.quantity
    )

    new_order.user=user

    session.add(new_order)

    session.commit()


    response={
        "pizza_size":new_order.pizza_size,
        "quantity":new_order.quantity,
        "id":new_order.id,
        "order_status":new_order.order_status
    }
    return response



def list_all_orders(current_username):
    user=session.query(User).filter(User.username==current_username).first()

    if user.is_staff:
        orders=session.query(Order).all()

        return jsonable_encoder(orders)

    raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not a superuser"
        )


def get_order_by_id(id:int,current_username):
    current_user=session.query(User).filter(User.username==current_username).first()

    if current_user.is_staff:
        order=session.query(Order).filter(Order.id==id).first()

        return jsonable_encoder(order)

    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not alowed to carry out request"
        )

def get_user_orders(current_username):
    current_user=session.query(User).filter(User.username==current_username).first()
    return jsonable_encoder(current_user.orders)


def get_specific_order(id:int,current_username):
    current_user=session.query(User).filter(User.username==current_username).first()
    orders=current_user.orders
    for o in orders:
        if o.id == id:
            return jsonable_encoder(o)
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="No order with such id"
    )

def update_order(id:int,order:OrderModel):
    order_to_update=session.query(Order).filter(Order.id==id).first()

    order_to_update.quantity=order.quantity
    order_to_update.pizza_size=order.pizza_size
    session.commit()
    response={
                "id":order_to_update.id,
                "quantity":order_to_update.quantity,
                "pizza_size":order_to_update.pizza_size,
                "order_status":order_to_update.order_status,
            }

    return jsonable_encoder(order_to_update)

    
def update_order_status(id:int,
        order:OrderStatusModel,
        current_username):
    current_user=session.query(User).filter(User.username==current_username).first()

    if current_user.is_staff:
        order_to_update=session.query(Order).filter(Order.id==id).first()
        order_to_update.order_status=order.order_status
        session.commit()
        response={
                "id":order_to_update.id,
                "quantity":order_to_update.quantity,
                "pizza_size":order_to_update.pizza_size,
                "order_status":order_to_update.order_status,
            }
        return jsonable_encoder(response)

def delete_an_order(id:int):
    order_to_delete=session.query(Order).filter(Order.id==id).first()
    session.delete(order_to_delete)
    session.commit()
    return order_to_delete
