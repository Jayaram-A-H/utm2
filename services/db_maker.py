import sqlite3
import os
# Define the path to the SQLite database file
db_path = 'flight_blender.sqlite3'

# Connect to the 3 database (or create it if it doesn't exist)
conn = sqlite3.connect(db_path)

# Create a cursor object
cursor = conn.cursor()

# Create the tables
tables = {
    "flight_declaration_operations_flightdeclaration": '''
        CREATE TABLE flight_declaration_operations_flightdeclaration (
            id INTEGER PRIMARY KEY,
            updated_at TEXT NOT NULL,
            created_at TEXT NOT NULL,
            is_approved TEXT NOT NULL,
            end_datetime TEXT NOT NULL,
            start_datetime TEXT NOT NULL,
            latest_telemetry_datetime TEXT NOT NULL,
            approved_by TEXT NOT NULL,
            submitted_by TEXT NOT NULL,
            originating_party TEXT NOT NULL,
            state TEXT NOT NULL,
            aircraft_id TEXT NOT NULL,
            bounds TEXT NOT NULL,
            type_of_operation TEXT NOT NULL,
            operational_intent TEXT NOT NULL,
            flight_declaration_raw_geojson TEXT_NOT_NULL
        )
    ''',
    "geo_fence_operations_geofence": '''
        CREATE TABLE geo_fence_operations_geofence (
            end_datetime TEXT NOT NULL,
            start_datetime TEXT NOT NULL
            
        )
    ''',
    "users": '''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT
        )
    ''',
    "uas_operations": '''
        CREATE TABLE uas_operations (
            id INTEGER PRIMARY KEY,
            operation_id TEXT NOT NULL,
            flight_declaration_id TEXT NOT NULL,
            status TEXT,
            timestamp TEXT,
            FOREIGN KEY (flight_declaration_id) REFERENCES flight_declaration_operations_flightdeclaration(id)
        )
    ''',
    "conflicts": '''
        CREATE TABLE conflicts (
            id INTEGER PRIMARY KEY,
            conflict_id TEXT NOT NULL,
            flight_declaration_id TEXT NOT NULL,
            conflict_details TEXT,
            status TEXT,
            resolution TEXT,
            FOREIGN KEY (flight_declaration_id) REFERENCES flight_declaration_operations_flightdeclaration(id)
        )
    ''',
    "permissions": '''
        CREATE TABLE permissions (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            resource TEXT NOT NULL,
            permission_level TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    '''
}

# Execute the table creation commands
for table_name, create_command in tables.items():
    cursor.execute(create_command)

# Commit the changes and close the connection
conn.commit()
conn.close()

# Confirm the file has been created
os.path.exists(db_path)
