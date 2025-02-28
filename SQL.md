### 1. get all statuses, not repeating, alphabetically ordered
```sql
SELECT DISTINCT status 
FROM tasks 
ORDER BY status ASC;
```

### 2. get the count of all tasks in each project, order by tasks count descending
```sql 
SELECT p.id, p.name, COUNT(t.id) AS tasks_count
FROM projects p
LEFT JOIN tasks t ON p.id = t.project_id
GROUP BY p.id, p.name
ORDER BY tasks_count DESC;
```

### 3. get the count of all tasks in each project, order by projects names
```sql
SELECT p.id, p.name, COUNT(t.id) AS tasks_count
FROM projects p
LEFT JOIN tasks t ON p.id = t.project_id
GROUP BY p.id, p.name
ORDER BY p.name;
```

### 4. get the tasks for all projects having the name beginning with "N" letter
```sql
SELECT t.*
FROM tasks t
JOIN projects p ON t.project_id = p.id
WHERE p.name LIKE 'N%';
```

### 5. get the list of al projects containing the 'a' letter in the middle of the name, and show the tasks count near each project. Mention that there can exist projects without tasks and tasks with project_id= NULL
```sql
SELECT p.id, p.name, COUNT(t.id) AS tasks_count
FROM projects p
LEFT JOIN tasks t ON p.id = t.project_id
WHERE p.name LIKE '_%a%_'
GROUP BY p.id, p.name;
```

### 6. get the list of tasks with duplicate names. Order alphabetically
```sql
SELECT name
FROM tasks
GROUP BY name
HAVING COUNT(name) > 1
ORDER BY name;
```

### 7. get the list of tasks having several exact matches of both name and status, from the project 'Delivery’. Order by matches count
```sql
SELECT t.name, t.status, COUNT(*) AS matches_count
FROM tasks t
JOIN projects p ON t.project_id = p.id
WHERE p.name = 'Delivery'
GROUP BY t.name, t.status
HAVING COUNT(*) > 1
ORDER BY matches_count;
```

### 8. get the list of project names having more than 10 tasks in status 'completed'. Order by project_id
```sql
SELECT p.name
FROM projects p
JOIN tasks t ON p.id = t.project_id
WHERE t.status = 'completed'
GROUP BY p.id, p.name
HAVING COUNT(t.id) > 10
ORDER BY p.id;
```