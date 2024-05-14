import uuid

from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP, text, UUID
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

    addresses = relationship("Address", back_populates="user")


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    user = relationship(
        "User",
        back_populates="addresses",
        cascade='save-update, merge, delete',
        passive_deletes=True,
    )


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    photo = Column(String)

    calories = Column(Float)
    weight = Column(Float)
    type = Column()

# TODO:
# таблицу с блюдами

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)
    status = Column(String)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    address_id = Column(Integer, ForeignKey("addresses.id"))

    user = relationship("User", backref="orders")
    address = relationship("Address", backref="orders")


class OrderedProduct(Base):
    __tablename__ = "ordered_products"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)

    order = relationship("Order", backref="ordered_products")
    product = relationship("Product", backref="ordered_products")
