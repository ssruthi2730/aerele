# Event Scheduling & Resource Allocation System

A Flask-based web application for managing events and resources with conflict detection and utilization reporting.

## Features

- **Event Management**: Create, edit, view, and delete events with start/end times
- **Resource Management**: Manage different types of resources (rooms, instructors, equipment)
- **Resource Allocation**: Allocate resources to events with automatic conflict detection
- **Conflict Detection**: Prevents double-booking of resources with overlapping time slots
- **Utilization Reports**: Generate reports showing resource usage hours and upcoming bookings

## Technology Stack

- **Backend**: Flask 3.0.0
- **Database**: SQLite with SQLAlchemy ORM
- **Forms**: WTForms with Flask-WTF
- **Frontend**: HTML5, CSS3 (Minimalistic Design)

## Project Structure

```
e:\aerele\
├── app.py                    # Main Flask application
├── models.py                 # Database models
├── database.py               # Database initialization
├── utils.py                  # Business logic
├── forms.py                  # WTForms
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
├── static/
│   └── style.css            # CSS styling
└── templates/
    ├── base.html            # Base template
    ├── index.html           # Dashboard
    ├── events/              # Event templates
    ├── resources/           # Resource templates
    ├── allocations/         # Allocation templates
    └── reports/             # Report templates
```

## Installation

### Prerequisites
- Python 3.8 or higher
- Virtual environment (recommended)

### Setup Steps

1. **Clone or download the project**
   ```bash
   cd e:\aerele
   ```

2. **Activate virtual environment**
   ```bash
   .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and navigate to: `http://127.0.0.1:5000`

## Usage Guide

### 1. Add Resources
- Navigate to **Resources** → **Add New Resource**
- Enter resource name and select type (room, instructor, equipment, other)
- Click "Create Resource"

**Example Resources:**
- Conference Room A (room)
- Conference Room B (room)
- Dr. Smith (instructor)
- Projector (equipment)

### 2. Add Events
- Navigate to **Events** → **Add New Event**
- Fill in event title, start time, end time, and description
- Click "Create Event"

**Example Events:**
- Python Workshop (2025-12-20 10:00 - 12:00)
- Flask Training (2025-12-20 11:00 - 13:00)
- Data Science Seminar (2025-12-20 14:00 - 16:00)
- Database Workshop (2025-12-20 15:00 - 17:00)

### 3. Allocate Resources
- Navigate to **Allocations**
- Select an event from dropdown
- Select one or more resources (hold Ctrl/Cmd for multiple)
- Click "Allocate Resources"

**Conflict Detection:**
If you try to allocate the same resource to overlapping events, the system will:
- Show an error message
- Redirect to the conflict detection page
- Display which events are conflicting

### 4. View Conflicts
- The **Conflicts** page shows detailed information about resource conflicts
- Lists conflicting resources, events, and time ranges

### 5. Generate Utilization Report
- Navigate to **Reports**
- Select start and end date range
- Click "Generate Report"
- View total hours utilized per resource
- See upcoming bookings for each resource

## Database Schema

### Event Table
- `event_id` (Primary Key)
- `title` (String, 200 chars)
- `start_time` (DateTime)
- `end_time` (DateTime)
- `description` (Text)

### Resource Table
- `resource_id` (Primary Key)
- `resource_name` (String, 200 chars)
- `resource_type` (String, 50 chars)

### EventResourceAllocation Table
- `allocation_id` (Primary Key)
- `event_id` (Foreign Key → Event)
- `resource_id` (Foreign Key → Resource)

## Conflict Detection Logic

The system validates resource allocations using sophisticated overlap detection:

1. **Time Overlap Detection**: Checks if new allocation overlaps with existing ones
2. **Edge Cases Handled**:
   - Exact time matches
   - Partial overlaps (start or end within existing booking)
   - Nested intervals (fully contained bookings)
   - Same start or end times

3. **Validation Points**:
   - When creating new allocations
   - When editing event times
   - Before displaying allocation form

## Key Features Implemented

✅ CRUD operations for Events and Resources
✅ Resource allocation with multi-select
✅ Automatic conflict detection
✅ Time overlap validation
✅ Utilization report with date range
✅ Flash messages for user feedback
✅ Responsive minimalistic UI
✅ SQLite database with SQLAlchemy
✅ Form validation with WTForms
✅ Cascading deletes for data integrity

## Testing Scenarios

### Scenario 1: Create Resources
1. Add 4 different resources (rooms, instructors, equipment)
2. Verify they appear in the resources list

### Scenario 2: Create Overlapping Events
1. Create Event A: 10:00 - 12:00
2. Create Event B: 11:00 - 13:00 (overlaps with A)
3. Create Event C: 14:00 - 16:00
4. Create Event D: 15:00 - 17:00 (overlaps with C)

### Scenario 3: Test Conflict Detection
1. Allocate Resource X to Event A (success)
2. Try to allocate Resource X to Event B (conflict detected)
3. System shows error and conflict details
4. Allocate different resource to Event B (success)

### Scenario 4: Utilization Report
1. Allocate resources to multiple events
2. Generate report for date range covering all events
3. Verify total hours calculation
4. Check upcoming bookings list

## Screenshots

### Dashboard

### Events List


### Add Event


### Resources List

### Allocations


### Conflict Detection


### Utilization Report


## Video Demonstration

(https://drive.google.com/file/d/13uXZGl9CTh2KFTfMC4C36g-IkiMJ2Ptu/view?usp=sharing)

## Code Quality

- **No Comments**: As requested, code is self-documenting with clear variable/function names
- **Structured Format**: Modular architecture with separation of concerns
- **Best Practices**: 
  - SQLAlchemy ORM for database operations
  - WTForms for validation
  - Template inheritance for DRY principle
  - CSS classes for reusable styling
  - Flash messages for user feedback

## Future Enhancements

- User authentication and authorization
- Email notifications for upcoming events
- Calendar view for events
- Export reports to PDF/Excel
- Recurring events support
- Mobile app integration



#author
**sruthilakshmi**
