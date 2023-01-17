import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    submenus = relationship('SubMenu',
                            back_populates='menu', cascade='all, delete')


class SubMenu(Base):
    __tablename__ = 'submenu'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    parent_id = Column(UUID(as_uuid=True),
                       ForeignKey('menu.id', ondelete='CASCADE'))

    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship('Dish',
                          back_populates='submenu', cascade='all, delete')


class Dish(Base):
    __tablename__ = 'dish'

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    price = Column(String, nullable=False)
    parent_id = Column(UUID(as_uuid=True),
                       ForeignKey('submenu.id', ondelete='CASCADE'))

    submenu = relationship('SubMenu', back_populates='dishes')
