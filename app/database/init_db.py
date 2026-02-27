from .db import engine, Base


async def init_db():

    async with engine.begin() as conn:

        await conn.run_sync(
            Base.metadata.create_all
        )
    # seed some initial orders each time (wipe previous data)
    from .db import AsyncSessionLocal
    from .models import Order
    from sqlalchemy import delete

    async with AsyncSessionLocal() as db:
        # clear existing rows
        await db.execute(delete(Order))
        await db.commit()
        samples = [
            ('Acme Corp',  'Gear Box',      3),
            ('Beta GmbH',  'Sensor Kit',    1),
            ('Gamma Ltd',  'Panel Module',  5),
            ('Delta AG',   'Cable Harness', 2),
            ('Epsilon BV', 'Widget A',      10),
        ]
        for cust, prod, qty in samples:
            order = Order(customer_name=cust, product=prod, quantity=qty)
            db.add(order)
        await db.commit()
