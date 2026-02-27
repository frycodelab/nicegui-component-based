import logging

logger = logging.getLogger(__name__)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Order


# CREATE
async def create_order(
    db: AsyncSession,
    customer_name: str,
    product: str,
    quantity: int
):

    logger.info(f"Creating order: {customer_name} - {product} qty:{quantity}")
    try:
        order = Order(
            customer_name=customer_name,
            product=product,
            quantity=quantity
        )

        db.add(order)
        await db.commit()
        logger.info(f"Order {order.id} created successfully")
        return order
    except Exception as e:
        logger.error(f"Failed to create order: {e}")
        raise


# READ ALL
async def get_orders(
    db: AsyncSession
):

    result = await db.execute(
        select(Order)
    )

    return result.scalars().all()


# READ ONE
async def get_order(
    db: AsyncSession,
    order_id: int
):

    result = await db.execute(
        select(Order).where(
            Order.id == order_id
        )
    )

    return result.scalar_one_or_none()


# UPDATE
async def update_order(
    db: AsyncSession,
    order_id: int,
    customer_name: str,
    product: str,
    quantity: int
):

    order = await get_order(
        db,
        order_id
    )

    if not order:
        return None

    order.customer_name = customer_name
    order.product = product
    order.quantity = quantity

    await db.commit()

    await db.refresh(order)

    return order


# DELETE
async def delete_order(
    db: AsyncSession,
    order_id: int
):

    order = await get_order(
        db,
        order_id
    )

    if not order:
        return None

    await db.delete(order)

    await db.commit()

    return order