# ACID vs BASE

This document compares the ACID properties of traditional relational databases with the BASE properties commonly associated with NoSQL databases. Understanding these concepts is crucial for designing systems that meet specific consistency and availability requirements.

## ACID Properties

ACID is an acronym that stands for Atomicity, Consistency, Isolation, and Durability. These properties ensure reliable processing of database transactions:
1. **Atomicity**: Ensures that a transaction is treated as a single unit, which either completes entirely or not at all. If any part of the transaction fails, the entire transaction is rolled back.
2. **Consistency**: Guarantees that a transaction brings the database from one valid state to another valid state, maintaining all predefined rules, such as constraints and triggers.
3. **Isolation**: Ensures that concurrent transactions do not interfere with each other. The effects of a transaction are not visible to other transactions until it is committed.
4. **Durability**: Guarantees that once a transaction is committed, it will remain so, even in the event of a system failure. This is typically achieved through logging and backup mechanisms.

## BASE Properties

BASE is an acronym that stands for Basically Available, Soft state, and Eventual consistency. These properties are often associated with NoSQL databases and distributed systems:
1. **Basically Available**: The system guarantees availability, meaning that it will respond to requests, but not necessarily with the most recent data. This is a trade-off to ensure that the system remains operational.
2. **Soft state**: The state of the system may change over time, even without input, due to eventual consistency. This means that the system does not need to be in a consistent state at all times.
3. **Eventual consistency**: The system will eventually become consistent over time, given that no new updates are made. This means that while data may be temporarily inconsistent, it will converge to a consistent state eventually.

## Comparison of ACID and BASE

| Aspect               | ACID                                      | BASE                                      |
|----------------------|-------------------------------------------|-------------------------------------------|
| Focus                | Strong consistency and reliability       | High availability and scalability        |
| Transaction Model    | Rigid, with strict rules                  | Flexible, allowing for temporary inconsistencies |
| Use Cases            | Financial systems, inventory management   | Social media, content delivery networks |
| Performance         | May have higher latency due to strict rules | Optimized for low latency and high throughput |
| Scalability         | Limited by the need for strong consistency | Designed for horizontal scaling and distributed architectures |

![ACID vs BASE Diagram](https://www.wikitechy.com/wp-content/uploads/2025/10/ACID-vs.-BASE-1024x683.webp)

## When to Use Each Approach

- Use **ACID** for applications that require strong consistency, such as banking systems, where data integrity is critical.
- Use **BASE** for applications that prioritize availability and scalability, such as social media platforms, where temporary inconsistencies are acceptable.

---

[<< PACELC Theorem](03-pacelc-theorem.md)

[Back to Core Architecture Principles](index.md) | [Back to System Design Concepts](../index.md)
