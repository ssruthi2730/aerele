from datetime import datetime, timedelta
from database import get_session, init_db
from models import Event, Resource, EventResourceAllocation

def create_sample_data():
    init_db()
    session = get_session()
    
    print("Creating sample resources...")
    resources = [
        Resource(resource_name="Conference Room A", resource_type="room"),
        Resource(resource_name="Conference Room B", resource_type="room"),
        Resource(resource_name="Dr. Smith", resource_type="instructor"),
        Resource(resource_name="Projector", resource_type="equipment"),
    ]
    
    for resource in resources:
        session.add(resource)
    session.commit()
    print(f"Created {len(resources)} resources")
    
    print("Creating sample events...")
    base_date = datetime(2025, 12, 20)
    events = [
        Event(
            title="Python Workshop",
            start_time=base_date.replace(hour=10, minute=0),
            end_time=base_date.replace(hour=12, minute=0),
            description="Introduction to Python programming"
        ),
        Event(
            title="Flask Training",
            start_time=base_date.replace(hour=11, minute=0),
            end_time=base_date.replace(hour=13, minute=0),
            description="Web development with Flask framework"
        ),
        Event(
            title="Data Science Seminar",
            start_time=base_date.replace(hour=14, minute=0),
            end_time=base_date.replace(hour=16, minute=0),
            description="Machine Learning and AI fundamentals"
        ),
        Event(
            title="Database Workshop",
            start_time=base_date.replace(hour=15, minute=0),
            end_time=base_date.replace(hour=17, minute=0),
            description="SQL and database design"
        ),
    ]
    
    for event in events:
        session.add(event)
    session.commit()
    print(f"Created {len(events)} events")
    
    print("Creating sample allocations (non-conflicting)...")
    allocations = [
        EventResourceAllocation(event_id=1, resource_id=1),
        EventResourceAllocation(event_id=1, resource_id=3),
        EventResourceAllocation(event_id=2, resource_id=2),
        EventResourceAllocation(event_id=2, resource_id=4),
        EventResourceAllocation(event_id=3, resource_id=1),
        EventResourceAllocation(event_id=4, resource_id=2),
    ]
    
    for allocation in allocations:
        session.add(allocation)
    session.commit()
    print(f"Created {len(allocations)} allocations")
    
    print("\n=== Sample Data Summary ===")
    print(f"Resources: {session.query(Resource).count()}")
    print(f"Events: {session.query(Event).count()}")
    print(f"Allocations: {session.query(EventResourceAllocation).count()}")
    print("\nSample data created successfully!")
    print("Run 'python app.py' and visit http://127.0.0.1:5000")

if __name__ == "__main__":
    create_sample_data()
