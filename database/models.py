import uuid

from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey, TIMESTAMP, text, UUID
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))

    addresses = relationship(
        'Address',
        back_populates="user",
        cascade='save-update, merge, delete',
        passive_deletes=True,
    )

    food_basket = relationship(
        "FoodBasket",
        back_populates="user",
        cascade='save-update, merge, delete',
        passive_deletes=True,
    )

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete='CASCADE'))
    user = relationship(
        "User",
        back_populates="addresses",
        cascade='save-update, merge, delete',
        passive_deletes=True,
    )


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    photo = Column(String)
    calories = Column(Float)
    weight = Column(Float)
    type = Column(String)  # Type can indicate if it's a vegetable, fruit, dish, etc.
    is_dish = Column(Boolean, nullable=False, default=False)
    price = Column(Float, nullable=False, default=100)

    food_basket = relationship("FoodBasket", back_populates="item")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)
    status = Column(String)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    address_id = Column(Integer, ForeignKey("addresses.id"))

    user = relationship("User", backref="orders")
    address = relationship("Address", backref="orders")


class FoodBasket(Base):
    __tablename__ = "food_basket"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    quantity = Column(Integer, default=0)

    user = relationship(
        "User",
        back_populates="food_basket",
        cascade='save-update, merge, delete',
        passive_deletes=True,
    )
    
    order = relationship("Order", backref="food_basket")
    item = relationship("Item", back_populates="food_basket")