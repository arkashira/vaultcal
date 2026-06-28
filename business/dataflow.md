```markdown
# Dataflow Architecture for VaultCal

## External Data Sources
- Radicale (calendar and contact server)
- User input (contact and calendar data)
- Security compliance frameworks (for guidance and protection features)

## Ingestion Layer
```
+---------------------+
|  Ingestion Layer    |
|                     |
|  +---------------+  |
|  | User Input    |  |
|  +---------------+  |
|  | Radicale API  |  |
|  +---------------+  |
+---------------------+
```
- User Input: Captures contact and calendar data securely.
- Radicale API: Interfaces with Radicale for data retrieval and management.

## Processing/Transform Layer
```
+---------------------------+
|  Processing/Transform     |
|                           |
|  +---------------------+  |
|  | Data Validation     |  |
|  +---------------------+  |
|  | Security Checks     |  |
|  +---------------------+  |
|  | Data Transformation  |  |
|  +---------------------+  |
+---------------------------+
```
- Data Validation: Ensures input data integrity.
- Security Checks: Implements built-in protection features.
- Data Transformation: Prepares data for storage and querying.

## Storage Tier
```
+---------------------+
|     Storage Tier    |
|                     |
|  +---------------+  |
|  | Database      |  |
|  +---------------+  |
|  | Backup System |  |
|  +---------------+  |
+---------------------+
```
- Database: Stores contacts and calendar data securely.
- Backup System: Ensures data redundancy and recovery.

## Query/Serving Layer
```
+---------------------+
|   Query/Serving     |
|                     |
|  +---------------+  |
|  | API Gateway   |  |
|  +---------------+  |
|  | Query Engine  |  |
|  +---------------+  |
+---------------------+
```
- API Gateway: Manages user requests and routes them to the appropriate services.
- Query Engine: Processes queries and retrieves data from the storage tier.

## Egress to User
```
+---------------------+
|   Egress to User    |
|                     |
|  +---------------+  |
|  | User Interface |  |
|  +---------------+  |
|  | Notification   |  |
|  +---------------+  |
+---------------------+
```
- User Interface: Provides a secure and intuitive interface for users to manage contacts and calendars.
- Notification System: Alerts users of important events or security issues.

## Auth Boundaries
- User Authentication: Ensures only authorized users can access the system.
- API Security: Protects data in transit between layers using encryption and secure tokens.
```
