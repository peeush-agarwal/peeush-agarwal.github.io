# Database replication and scaling

Database replication and scaling are essential strategies for managing increasing data loads and ensuring high availability in modern applications. This document explores various techniques for replicating and scaling databases, including master-slave replication, master-master replication, sharding, and the use of distributed databases.

## Database Replication

Database replication involves creating copies of a database across multiple servers to improve data availability and fault tolerance. Database replication usually follows a master/slave relationship between the original (master) and the copies (slaves).

A master database generally only supports write operations. A slave database gets copies of the data from the master database and only supports read operations. All the data-modifying commands like insert, delete, or update must be sent to the master database. Most applications require a much higher ratio of reads to writes; thus, the number of slave databases in a system is usually larger than the number of master databases.

<!-- TODO: Add a diagram of master-slave database replication -->

Another common replication strategy is master-master replication, where multiple servers can handle both read and write operations. This allows for greater flexibility and availability but can be more complex to manage due to potential conflicts between writes.

### Advantages of database replication

- __Better performance:__ In the master-slave model, all writes and updates happen in master nodes; whereas, read operations are distributed across slave nodes. This model improves performance because it allows more queries to be processed in parallel.
- __Reliability:__ If one of your database servers is destroyed by a natural disaster, such as typhoon or an earthquake, data is still preserved. You do not need to worry about the data loss because data is replicated across multiple locations.
- __High availability:__ By replicating data across different locations, your website remains in operation even if a database is offline as you can access data stored in another database server.

The architectural design discussed in the above diagram can handle this case:
- If only one slave database is available and it goes offline, read operations will be directed to the master database temporarily.
- If the master database goes offline, a slave database will be promoted to be the new master. All the database operations will be temporarily executed on the new master database. A new slave database will replace the old one for data replication immediately. In production systems, promoting a new master is more complicated as the data in a slave database might not be up to date. The missing data needs to be updated by running data recovery scripts. Other replication methods like multi-masters, and circular replication could help, those setups are more complicated.

## Database Sharding

Sharding is a technique for horizontally partitioning a database into smaller, more manageable pieces called shards. Each shard contains a subset of the data, and together they form the complete dataset. Sharding can improve performance and scalability by distributing the load across multiple servers, but it requires careful design to ensure data consistency and efficient querying.

<!-- TODO: Add a diagram of database sharding -->

Sharding strategies include:
- **Range-Based Sharding**: Data is partitioned based on a specific range of values (e.g., user IDs).
- **Hash-Based Sharding**: Data is partitioned based on a hash of a key (e.g., user ID), which can help distribute data more evenly across shards.
- **Directory-Based Sharding**: A directory service is used to map data to specific shards, allowing for more flexible partitioning.

Sharding introduces complexities and new challenges to the system:

- __Resharding data:__ Resharding data is needed when
  - a single shard could no longer hold more data due to rapid growth
  - Certain shards might experience shard exhaustion faster than others due to uneven data distribution.

  When shard exhaustion happens, it requires updating the sharding function and moving data around. Consistent hashing is a commonly used technique to solve this problem.

- __Celebrity problem:__ This is also called a _hotspot key problem_. Excessive access to a specific shard could cause server overload. Imagine data for Katy Perry, Justin Bieber, and Lady Gaga all end up on the same shard. For social applications, that shard will be overwhelmed with read operations. To solve this problem, we may need to allocated shard for each celebrity. Each shard might even require further partition.

- __Join and de-normalization:__ Once a database has been sharded across multiple servers, it is hard to perform join operations across database shards. A common workaround is to de-normalize the database so that queries can be performed in a single table.

## Distributed Databases

Distributed databases are designed to operate across multiple servers and locations, providing high availability and scalability. They often use a combination of replication and sharding techniques to manage data across the distributed environment. Examples of distributed databases include Apache Cassandra, MongoDB, and Google Spanner.

Implementing effective database replication and scaling strategies requires careful consideration of your application's data access patterns, consistency requirements, and infrastructure capabilities. It's important to monitor the performance of your database systems and make adjustments as needed to ensure optimal performance and reliability.

---

[<< Load Balancing](03-load-balancing.md) | [>> Caching Strategies](05-caching-strategies.md)

[Back to Scale from Zero to Millions of Users](index.md) | [Back to System Design Concepts](../index.md)
