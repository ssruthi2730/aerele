from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from database import init_db, get_session, close_session
from models import Event, Resource, EventResourceAllocation
from forms import EventForm, ResourceForm, AllocationForm, ReportForm
from utils import check_resource_conflict, get_conflicting_allocations, generate_utilization_report, validate_event_times
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

@app.before_request
def before_request():
    pass

@app.teardown_appcontext
def shutdown_session(exception=None):
    close_session()

@app.route('/')
def index():
    session = get_session()
    event_count = session.query(Event).count()
    resource_count = session.query(Resource).count()
    allocation_count = session.query(EventResourceAllocation).count()
    
    upcoming_events = session.query(Event).filter(
        Event.start_time >= datetime.now()
    ).order_by(Event.start_time).limit(5).all()
    
    return render_template('index.html', 
                         event_count=event_count,
                         resource_count=resource_count,
                         allocation_count=allocation_count,
                         upcoming_events=upcoming_events)

@app.route('/events')
def list_events():
    session = get_session()
    events = session.query(Event).order_by(Event.start_time.desc()).all()
    return render_template('events/list.html', events=events)

@app.route('/events/add', methods=['GET', 'POST'])
def add_event():
    form = EventForm()
    
    if form.validate_on_submit():
        valid, error_msg = validate_event_times(form.start_time.data, form.end_time.data)
        if not valid:
            flash(error_msg, 'error')
            return render_template('events/add.html', form=form)
        
        session = get_session()
        event = Event(
            title=form.title.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            description=form.description.data
        )
        session.add(event)
        session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('list_events'))
    
    return render_template('events/add.html', form=form)

@app.route('/events/edit/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    session = get_session()
    event = session.query(Event).get(event_id)
    
    if not event:
        flash('Event not found!', 'error')
        return redirect(url_for('list_events'))
    
    form = EventForm(obj=event)
    
    if form.validate_on_submit():
        valid, error_msg = validate_event_times(form.start_time.data, form.end_time.data)
        if not valid:
            flash(error_msg, 'error')
            return render_template('events/edit.html', form=form, event=event)
        
        resource_ids = [a.resource_id for a in event.allocations]
        if resource_ids:
            conflicts = get_conflicting_allocations(
                form.start_time.data, 
                form.end_time.data, 
                resource_ids,
                exclude_event_id=event_id
            )
            if conflicts:
                flash('Time change would create resource conflicts!', 'error')
                return render_template('events/edit.html', form=form, event=event, conflicts=conflicts)
        
        event.title = form.title.data
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        event.description = form.description.data
        session.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('list_events'))
    
    return render_template('events/edit.html', form=form, event=event)

@app.route('/events/delete/<int:event_id>')
def delete_event(event_id):
    session = get_session()
    event = session.query(Event).get(event_id)
    
    if event:
        session.delete(event)
        session.commit()
        flash('Event deleted successfully!', 'success')
    else:
        flash('Event not found!', 'error')
    
    return redirect(url_for('list_events'))

@app.route('/resources')
def list_resources():
    session = get_session()
    resources = session.query(Resource).order_by(Resource.resource_type, Resource.resource_name).all()
    return render_template('resources/list.html', resources=resources)

@app.route('/resources/add', methods=['GET', 'POST'])
def add_resource():
    form = ResourceForm()
    
    if form.validate_on_submit():
        session = get_session()
        resource = Resource(
            resource_name=form.resource_name.data,
            resource_type=form.resource_type.data
        )
        session.add(resource)
        session.commit()
        flash('Resource created successfully!', 'success')
        return redirect(url_for('list_resources'))
    
    return render_template('resources/add.html', form=form)

@app.route('/resources/edit/<int:resource_id>', methods=['GET', 'POST'])
def edit_resource(resource_id):
    session = get_session()
    resource = session.query(Resource).get(resource_id)
    
    if not resource:
        flash('Resource not found!', 'error')
        return redirect(url_for('list_resources'))
    
    form = ResourceForm(obj=resource)
    
    if form.validate_on_submit():
        resource.resource_name = form.resource_name.data
        resource.resource_type = form.resource_type.data
        session.commit()
        flash('Resource updated successfully!', 'success')
        return redirect(url_for('list_resources'))
    
    return render_template('resources/edit.html', form=form, resource=resource)

@app.route('/resources/delete/<int:resource_id>')
def delete_resource(resource_id):
    session = get_session()
    resource = session.query(Resource).get(resource_id)
    
    if resource:
        session.delete(resource)
        session.commit()
        flash('Resource deleted successfully!', 'success')
    else:
        flash('Resource not found!', 'error')
    
    return redirect(url_for('list_resources'))

@app.route('/allocations')
def manage_allocations():
    session = get_session()
    allocations = session.query(EventResourceAllocation).all()
    events = session.query(Event).filter(Event.end_time >= datetime.now()).all()
    resources = session.query(Resource).all()
    
    form = AllocationForm()
    form.event_id.choices = [(e.event_id, f"{e.title} ({e.start_time.strftime('%Y-%m-%d %H:%M')})") for e in events]
    form.resource_ids.choices = [(r.resource_id, f"{r.resource_name} ({r.resource_type})") for r in resources]
    
    return render_template('allocations/manage.html', 
                         allocations=allocations, 
                         form=form)

@app.route('/allocations/add', methods=['POST'])
def add_allocation():
    session = get_session()
    events = session.query(Event).filter(Event.end_time >= datetime.now()).all()
    resources = session.query(Resource).all()
    
    form = AllocationForm()
    form.event_id.choices = [(e.event_id, f"{e.title} ({e.start_time.strftime('%Y-%m-%d %H:%M')})") for e in events]
    form.resource_ids.choices = [(r.resource_id, f"{r.resource_name} ({r.resource_type})") for r in resources]
    
    if form.validate_on_submit():
        event = session.query(Event).get(form.event_id.data)
        
        conflicts = get_conflicting_allocations(
            event.start_time,
            event.end_time,
            form.resource_ids.data
        )
        
        if conflicts:
            flash('Cannot allocate: Resource conflicts detected!', 'error')
            return redirect(url_for('view_conflicts', 
                                  event_id=form.event_id.data,
                                  resource_ids=','.join(map(str, form.resource_ids.data))))
        
        for resource_id in form.resource_ids.data:
            existing = session.query(EventResourceAllocation).filter_by(
                event_id=form.event_id.data,
                resource_id=resource_id
            ).first()
            
            if not existing:
                allocation = EventResourceAllocation(
                    event_id=form.event_id.data,
                    resource_id=resource_id
                )
                session.add(allocation)
        
        session.commit()
        flash('Resources allocated successfully!', 'success')
    
    return redirect(url_for('manage_allocations'))

@app.route('/allocations/delete/<int:allocation_id>')
def delete_allocation(allocation_id):
    session = get_session()
    allocation = session.query(EventResourceAllocation).get(allocation_id)
    
    if allocation:
        session.delete(allocation)
        session.commit()
        flash('Allocation removed successfully!', 'success')
    else:
        flash('Allocation not found!', 'error')
    
    return redirect(url_for('manage_allocations'))

@app.route('/conflicts')
def view_conflicts():
    event_id = request.args.get('event_id', type=int)
    resource_ids_str = request.args.get('resource_ids', '')
    
    session = get_session()
    conflicts = []
    event = None
    
    if event_id and resource_ids_str:
        event = session.query(Event).get(event_id)
        resource_ids = [int(rid) for rid in resource_ids_str.split(',') if rid]
        
        conflicts = get_conflicting_allocations(
            event.start_time,
            event.end_time,
            resource_ids
        )
    
    return render_template('allocations/conflicts.html', 
                         conflicts=conflicts, 
                         event=event)

@app.route('/reports/utilization', methods=['GET', 'POST'])
def utilization_report():
    form = ReportForm()
    report_data = None
    
    if form.validate_on_submit():
        report_data = generate_utilization_report(
            form.start_date.data,
            form.end_date.data
        )
    
    return render_template('reports/utilization.html', 
                         form=form, 
                         report_data=report_data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
