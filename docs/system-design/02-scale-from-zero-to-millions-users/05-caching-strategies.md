# Caching Strategies

Caching is a powerful technique for improving the performance and scalability of applications by storing frequently accessed data in a faster storage medium. This document explores various caching strategies, including in-memory caching, distributed caching, and content delivery networks (CDNs), along with their advantages and use cases.

## In-Memory Caching

In-memory caching involves storing data in the RAM of a server, allowing for extremely fast access times. This type of caching is ideal for frequently accessed data that can be stored temporarily, such as session data, user profiles, or the results of expensive database queries. Popular in-memory caching solutions include Redis and Memcached. These systems provide high performance and support various data structures, making them suitable for a wide range of applications.

## Distributed Caching

Distributed caching involves spreading cached data across multiple servers, allowing for greater scalability and fault tolerance. This approach is particularly useful for applications with high traffic volumes or those that require a large cache size that cannot be accommodated by a single server. Distributed caching systems, such as Apache Ignite and Hazelcast, provide features like data partitioning, replication, and failover to ensure high availability and performance.

## Content Delivery Networks (CDNs)

CDNs are a specialized form of caching that focuses on delivering static content, such as images, videos, and stylesheets, to users from geographically distributed servers. By caching content closer to the end-users, CDNs can significantly reduce latency and improve load times for websites and applications. Popular CDN providers include Cloudflare, Akamai, and Amazon CloudFront. CDNs also offer additional features like DDoS protection, SSL support, and analytics, making them a valuable tool for improving the performance and security of web applications.

## Cache Invalidation

Cache invalidation is the process of removing or updating cached data when it becomes stale or outdated. Effective cache invalidation strategies are crucial for maintaining data consistency and ensuring that users receive accurate information. Common cache invalidation techniques include time-based expiration, where cached data is automatically removed after a certain period, and event-based invalidation, where cached data is updated or removed in response to specific events (e.g., a database update).

## Considerations for using cache

- Consider using cache when data is read frequently but modified infrequently. Since cached data is stored in volatile memory, a cache server is not ideal for persisting data. For instance, if a cache server restarts, all the data in memory is lost.
- __Expiration policy:__ Once cached data is expired, it is removed from the cache. When there is no expiration policy, cached data will be stored in the memory permanently.
- __Consistency:__ This involves keeping the data store and the cache in sync. Inconsistency can happen because data-modifying operations on the data store and cache are not in a single transaction. When scaling across multiple regions, maintaining consistency between the data store and cache is challenging.
- __Mitigating failure:__ A single cache server represents a potential single point of failure (SPOF). Multiple cache servers across different data centers are recommended to avoid SPOF. Another recommended approach is to overprovision the required memory by certain percentages. This provides a buffer as the memory usage increases.
- __Eviction policy:__ Once the cache is full, any requests to add items to the cache might cause existing items to be removed. This is called Cache Eviction. Least-recently-used (LRU) is the most popular cache eviction policy. Lease-frequently-used (LFU) or First-in-first-out (FIFO) can be adopted to satisfy different use cases.

---

[<< Database Scaling](04-database-scaling.md) | [>> Stateful vs Stateless Services](06-stateful-vs-stateless-services.md)

[Back to Scale from Zero to Millions of Users](index.md) | [Back to System Design Concepts](../index.md)
