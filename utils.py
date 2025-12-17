from datetime import datetime, timedelta
from sqlalchemy import and_, or_
from models import Event, Resource, EventResourceAllocation
from database import get_session

def check_resource_conflict(resource_id, start_time, end_time, exclude_event_id=None):
    session = get_session()
    
    query = session.query(EventResourceAllocation).join(Event).filter(
        EventResourceAllocation.resource_id == resource_id,
        or_(
            and_(Event.start_time < end_time, Event.end_time > start_time),
            and_(Event.start_time >= start_time, Event.start_time < end_time),
            and_(Event.end_time > start_time, Event.end_time <= end_time)
        )
    )
    
    if exclude_event_id:
        query = query.filter(Event.event_id != exclude_event_id)
    
    conflicts = query.all()
    return len(conflicts) > 0, conflicts

def get_conflicting_allocations(start_time, end_time, resource_ids, exclude_event_id=None):
    session = get_session()
    conflicts = []
    
    for resource_id in resource_ids:
        has_conflict, conflict_list = check_resource_conflict(
            resource_id, start_time, end_time, exclude_event_id
        )
        if has_conflict:
            for allocation in conflict_list:
                conflicts.append({
                    'resource': allocation.resource,
                    'event': allocation.event,
                    'allocation': allocation
                })
    
    return conflicts

def generate_utilization_report(start_date, end_date):
    session = get_session()
    resources = session.query(Resource).all()
    report_data = []
    
    for resource in resources:
        allocations = session.query(EventResourceAllocation).join(Event).filter(
            EventResourceAllocation.resource_id == resource.resource_id,
            Event.start_time <= end_date,
            Event.end_time >= start_date
        ).all()
        
        total_hours = 0
        upcoming_bookings = []
        
        for allocation in allocations:
            event = allocation.event
            overlap_start = max(event.start_time, start_date)
            overlap_end = min(event.end_time, end_date)
            
            if overlap_start < overlap_end:
                duration = (overlap_end - overlap_start).total_seconds() / 3600
                total_hours += duration
            
            if event.start_time >= datetime.now():
                upcoming_bookings.append(event)
        
        report_data.append({
            'resource': resource,
            'total_hours': round(total_hours, 2),
            'upcoming_bookings': upcoming_bookings,
            'allocation_count': len(allocations)
        })
    
    return report_data

def validate_event_times(start_time, end_time):
    if start_time >= end_time:
        return False, "Start time must be before end time"
    if start_time < datetime.now():
        return False, "Cannot create events in the past"
    return True, ""
