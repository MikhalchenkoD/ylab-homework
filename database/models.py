from typing import Any

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID

Base: Any = declarative_base()


class Menu(Base):
    __tablename__ = 'menu'
    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String)
    description = Column(String)
    submenus = relationship(
        'Submenu', back_populates='menu', cascade='all, delete-orphan'
    )


class Submenu(Base):
    __tablename__ = 'submenu'
    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String)
    description = Column(String)
    menu_id = Column(UUID(as_uuid=True), ForeignKey('menu.id'))
    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship(
        'Dish', back_populates='submenu', cascade='all, delete-orphan'
    )


class Dish(Base):
    __tablename__ = 'dish'
    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String)
    description = Column(String)
    price = Column(String)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey('submenu.id'))
    submenu = relationship('Submenu', back_populates='dishes')
