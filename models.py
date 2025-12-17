from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'
    
    event_id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    description = Column(Text)
    
    allocations = relationship('EventResourceAllocation', back_populates='event', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Event {self.title}>'

class Resource(Base):
    __tablename__ = 'resources'
    
    resource_id = Column(Integer, primary_key=True)
    resource_name = Column(String(200), nullable=False)
    resource_type = Column(String(50), nullable=False)
    
    allocations = relationship('EventResourceAllocation', back_populates='resource', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Resource {self.resource_name}>'

class EventResourceAllocation(Base):
    __tablename__ = 'event_resource_allocations'
    
    allocation_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.event_id'), nullable=False)
    resource_id = Column(Integer, ForeignKey('resources.resource_id'), nullable=False)
    
    event = relationship('Event', back_populates='allocations')
    resource = relationship('Resource', back_populates='allocations')
    
    def __repr__(self):
        return f'<Allocation {self.allocation_id}>'
