Here’s a **side-by-side comparison of performance tuning commands** in:

* **Oracle Database**
* **MySQL**
* **PostgreSQL**

We’ll compare:

1. Query plan inspection
2. Runtime analysis
3. Statistics management
4. Index monitoring
5. Session/system monitoring
6. Memory & configuration tuning

---

# 🟠 Oracle Performance Tuning

Oracle provides the most enterprise-grade built-in tuning stack.

---

## 1️⃣ Execution Plan

```sql
EXPLAIN PLAN FOR
SELECT * FROM employees WHERE salary > 50000;

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```

✅ Shows estimated plan

---

## 2️⃣ Actual Runtime Plan

```sql
SELECT * FROM employees WHERE salary > 50000;

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR(NULL,NULL,'ALLSTATS LAST'));
```

✅ Shows actual execution stats (rows, buffers, time)

---

## 3️⃣ SQL Trace

```sql
ALTER SESSION SET sql_trace = TRUE;
```

Or:

```sql
EXEC DBMS_MONITOR.SESSION_TRACE_ENABLE;
```

---

## 4️⃣ Automatic Workload Repository (AWR)

```sql
@?/rdbms/admin/awrrpt.sql
```

Enterprise feature:

* Historical performance snapshots
* Top SQL
* Wait events

---

## 5️⃣ Gather Statistics

```sql
EXEC DBMS_STATS.GATHER_TABLE_STATS('HR','EMPLOYEES');
```

Critical for optimizer accuracy.

---

## 6️⃣ Index Monitoring

```sql
ALTER INDEX idx_salary MONITORING USAGE;

SELECT * FROM V$OBJECT_USAGE;
```

---

## 7️⃣ System Monitoring Views

```sql
SELECT * FROM V$SESSION;
SELECT * FROM V$SQL;
SELECT * FROM V$ACTIVE_SESSION_HISTORY;
```

---

## 8️⃣ Memory Tuning

```sql
SHOW PARAMETER pga_aggregate_target;
SHOW PARAMETER sga_target;
```

Modify:

```sql
ALTER SYSTEM SET sga_target=2G;
```

---

# 🟡 MySQL Performance Tuning

MySQL tuning is simpler but effective.

---

## 1️⃣ Execution Plan

```sql
EXPLAIN SELECT * FROM employees WHERE salary > 50000;
```

Extended:

```sql
EXPLAIN ANALYZE SELECT * FROM employees WHERE salary > 50000;
```

✅ Shows actual timing (8.0+)

---

## 2️⃣ Optimizer Trace

```sql
SET optimizer_trace="enabled=on";
SELECT * FROM employees;
SELECT * FROM INFORMATION_SCHEMA.OPTIMIZER_TRACE;
```

---

## 3️⃣ Analyze Table

```sql
ANALYZE TABLE employees;
```

Updates statistics.

---

## 4️⃣ Show Index Usage

```sql
SHOW INDEX FROM employees;
```

---

## 5️⃣ Performance Schema

Enable and query:

```sql
SELECT * FROM performance_schema.events_statements_summary_by_digest;
```

Used to:

* Identify slow queries
* Monitor waits

---

## 6️⃣ Slow Query Log

Enable:

```sql
SET GLOBAL slow_query_log = 'ON';
```

Set threshold:

```sql
SET GLOBAL long_query_time = 2;
```

---

## 7️⃣ Buffer Pool Tuning

```sql
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';
```

Change:

```sql
SET GLOBAL innodb_buffer_pool_size = 2147483648;
```

---

# 🟢 PostgreSQL Performance Tuning

Postgres is highly transparent and statistics-driven.

---

## 1️⃣ Execution Plan

```sql
EXPLAIN SELECT * FROM employees WHERE salary > 50000;
```

With runtime stats:

```sql
EXPLAIN ANALYZE SELECT * FROM employees WHERE salary > 50000;
```

With buffers:

```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM employees;
```

---

## 2️⃣ Update Statistics

```sql
ANALYZE employees;
```

Or:

```sql
VACUUM ANALYZE employees;
```

---

## 3️⃣ Index Usage Stats

```sql
SELECT * FROM pg_stat_user_indexes;
```

---

## 4️⃣ Query Statistics Extension

Enable:

```sql
CREATE EXTENSION pg_stat_statements;
```

Query:

```sql
SELECT * FROM pg_stat_statements
ORDER BY total_exec_time DESC;
```

---

## 5️⃣ Active Sessions

```sql
SELECT * FROM pg_stat_activity;
```

---

## 6️⃣ Auto Vacuum Monitoring

```sql
SELECT * FROM pg_stat_user_tables;
```

---

## 7️⃣ Memory Parameters

```sql
SHOW shared_buffers;
SHOW work_mem;
```

Change:

```sql
ALTER SYSTEM SET work_mem = '64MB';
```

---

# 📊 Feature Comparison

| Feature                 | Oracle             | MySQL    | PostgreSQL         |
| ----------------------- | ------------------ | -------- | ------------------ |
| EXPLAIN Plan            | ✅                  | ✅        | ✅                  |
| EXPLAIN ANALYZE         | Via DBMS_XPLAN     | ✅        | ✅                  |
| Historical Performance  | AWR (Enterprise)   | Limited  | pg_stat_statements |
| Built-in Slow Query Log | Advanced           | ✅        | Extension          |
| Automatic Statistics    | DBMS_STATS         | Basic    | Auto + ANALYZE     |
| Index Usage Monitoring  | Yes                | Limited  | Yes                |
| Memory Granularity      | Very Fine          | Moderate | Fine               |
| Enterprise Diagnostics  | Extremely Advanced | Moderate | Advanced           |

---

# 🏆 Tuning Philosophy Differences

### 🟠 Oracle

* Most automated
* Enterprise deep diagnostics
* Complex but powerful
* Best for mission-critical systems

### 🟡 MySQL

* Simpler tuning
* Focus on InnoDB buffer pool
* Good for web-scale workloads

### 🟢 PostgreSQL

* Transparent statistics
* Very strong query introspection
* Manual tuning but powerful

---

# 🔥 Quick Practical Advice

If query is slow:

1. Run `EXPLAIN ANALYZE`
2. Check missing indexes
3. Check statistics
4. Check memory settings
5. Monitor top queries
6. Look for full table scans

---

If you'd like, I can next provide:

* 🔍 Real-world slow query troubleshooting example in all 3
* 📈 Index tuning strategy comparison
* 🧠 Wait event analysis comparison
* ⚡ High concurrency tuning comparison

What would you like next?
