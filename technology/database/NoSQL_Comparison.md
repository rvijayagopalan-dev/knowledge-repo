Here’s a **detailed feature comparison** of **MongoDB, Redis, and Amazon DynamoDB** across querying, consistency, scaling, indexing, transactions, and more.

---

# 🟢 MongoDB (Document Database)

![Image](https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/MongoDB_Logo.svg/960px-MongoDB_Logo.svg.png)

![Image](https://webimages.mongodb.com/_com_assets/cms/lge07rl27hhp3drxy-scheduled-report.gif)

![Image](https://www.mongodb.com/community/forums/uploads/default/original/2X/d/ded7cefecee3b2b0b9dd0cc0e3d88a980da98aa2.png)

![Image](https://i.gyazo.com/e6df848a005f34d2fbc5ba6ad5ff4e65.jpg)

### 🔎 Data Model

* Document-oriented (BSON/JSON-like)
* Flexible schema (schema-less)
* Nested documents & arrays

### 🔍 Query Capabilities

* Rich query language (aggregation pipeline, joins via `$lookup`)
* Secondary indexes (compound, text, geospatial, hashed, wildcard)
* Full-text search (Atlas Search)
* Vector search (AI embeddings)
* Strong filtering, grouping, transformations

### 🔐 Consistency Model

* Strong consistency (primary reads)
* Configurable read preferences (eventual consistency for replicas)
* ACID transactions (multi-document, multi-collection)

### 📈 Scaling

* Horizontal scaling via **sharding**
* Replica sets for high availability
* Auto-scaling in MongoDB Atlas

### ⚡ Performance Strength

* Balanced read/write workloads
* Large, complex JSON documents
* Analytics + operational workloads together

### 🏆 Best For

* Content management
* Catalog systems
* Event-driven apps
* Applications requiring flexible schema

---

# 🔴 Redis (In-Memory Multi-Model)

![Image](https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/Logo-redis.svg/3840px-Logo-redis.svg.png)

![Image](https://media.licdn.com/dms/image/v2/D4E12AQEUTqxcuPgyoQ/article-cover_image-shrink_600_2000/article-cover_image-shrink_600_2000/0/1674494655446?e=2147483647\&t=SZHK8-G4v_Dk4alpCngtq1eJVVwdPIYSaigywXMd0d4\&v=beta)

![Image](https://substackcdn.com/image/fetch/%24s_%21lZd6%21%2Cf_auto%2Cq_auto%3Agood%2Cfl_progressive%3Asteep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F903484b2-8c0c-4ce9-b4ab-e967538aeb78_1972x1197.jpeg)

![Image](https://miro.medium.com/v2/resize%3Afit%3A1400/1%2AkY2ozXJ_zesMWozi8roD5A.png)

### 🔎 Data Model

* Key-Value primary model
* Supports:

  * Strings
  * Hashes
  * Lists
  * Sets / Sorted Sets
  * JSON
  * Streams
  * Time Series
  * Vector data types

### 🔍 Query Capabilities

* Key-based lookups (O(1) speed)
* Secondary indexing via modules
* Redis Query Engine (for JSON, search, vector)
* Pub/Sub & Streams (event-driven patterns)

### 🔐 Consistency Model

* Strong consistency (single-threaded core per shard)
* Replication for HA
* No traditional multi-document ACID (but supports transactions via MULTI/EXEC)

### 📈 Scaling

* Redis Cluster (sharding across nodes)
* Multi-threaded I/O in Redis 8
* Memory-first, optional disk persistence (RDB/AOF)

### ⚡ Performance Strength

* Ultra-low latency (<1ms)
* Real-time workloads
* Caching & session storage
* AI semantic search (vector sets)

### 🏆 Best For

* Caching layer
* Real-time analytics
* Leaderboards
* Message brokering
* AI inference caching

---

# 🔵 Amazon DynamoDB (Managed Key-Value / Document)

![Image](https://upload.wikimedia.org/wikipedia/commons/f/fd/DynamoDB.png)

![Image](https://substackcdn.com/image/fetch/%24s_%21Pk7N%21%2Cf_auto%2Cq_auto%3Agood%2Cfl_progressive%3Asteep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3dd04d59-7ea9-487c-911b-3ccc225e7b9a_1600x944.png)

![Image](https://awsfundamentals.com/_next/image?q=75\&url=%2Fassets%2Fblog%2Fdynamodb-global-tables%2Fdiagram-illustrating-bidirectional-synchronization-between-aws-regions-us-east-1-and-eu-west-1-using-dynamodb-global-tables-with-arrows-indicating-data-flow-and-labeled-components..gif\&w=3840)

![Image](https://d1.awsstatic.com/onedam/marketing-channels/website/aws/en_US/product-categories/databases/non-relational/approved/images/ca2d2a4b-c2dd-4018-96c8-b1760e3610f0.203f1fc8b521ba3894090064a01d2b01bd08bf5f.png)

### 🔎 Data Model

* Key-Value + Document (JSON)
* Strict primary key (Partition key + Sort key)
* No joins

### 🔍 Query Capabilities

* Key-based queries (fast)
* Global Secondary Indexes (GSI)
* Local Secondary Indexes (LSI)
* PartiQL (SQL-like query support)
* No complex joins or aggregations like MongoDB

### 🔐 Consistency Model

* Eventually consistent reads (default)
* Optional strongly consistent reads
* Global tables with multi-region replication

### 📈 Scaling

* Fully serverless auto-scaling
* Virtually unlimited throughput
* Multi-region active-active

### ⚡ Performance Strength

* Predictable low-latency at massive scale
* High-traffic workloads
* Serverless architecture

### 🏆 Best For

* High-scale web/mobile backends
* Gaming leaderboards
* IoT data ingestion
* Serverless AWS architectures

---

# 📊 Feature Comparison Table

| Feature            | MongoDB       | Redis                   | DynamoDB                |
| ------------------ | ------------- | ----------------------- | ----------------------- |
| Data Model         | Document      | Key-Value + Multi-model | Key-Value + Document    |
| Schema Flexibility | High          | High                    | Moderate                |
| Joins              | Yes ($lookup) | No                      | No                      |
| Transactions       | Full ACID     | Limited                 | ACID (within partition) |
| Horizontal Scaling | Sharding      | Cluster Sharding        | Automatic               |
| Query Complexity   | High          | Low-Medium              | Low-Medium              |
| Latency            | Low           | Ultra-low               | Low                     |
| Best Role          | Primary DB    | Cache / Real-time       | Serverless Primary DB   |
| Managed Service    | Atlas         | Redis Cloud             | AWS Native              |

---

# 🧠 When To Choose What?

* ✅ Choose **MongoDB** if you need flexible schema + rich querying.
* ✅ Choose **Redis** if you need ultra-fast real-time performance.
* ✅ Choose **DynamoDB** if you want fully managed, auto-scaling at global AWS scale.

---