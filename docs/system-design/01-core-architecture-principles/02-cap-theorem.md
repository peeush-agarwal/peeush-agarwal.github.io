# CAP Theorem

The CAP Theorem, also known as Brewer's Theorem, is a fundamental principle in distributed systems that states that it is impossible for a distributed data store to simultaneously provide more than two out of the following three guarantees:
1. **Consistency (C)**: Every read receives the most recent write or an error. This means that all nodes in the system see the same data at the same time.
2. **Availability (A)**: Every request (read or write) receives a response, without guarantee that it contains the most recent write. This ensures that the system remains operational and responsive.
3. **Partition Tolerance (P)**: The system continues to operate despite arbitrary partitioning due to network failures. This means that the system can handle communication breakdowns between nodes.

## Implications of the CAP Theorem

According to the CAP Theorem, in the presence of a network partition (P), a distributed system must choose between consistency (C) and availability (A). This leads to three possible configurations:
1. **CP (Consistency and Partition Tolerance)**: The system prioritizes consistency over availability. In the event of a network partition, the system may become unavailable to ensure that all nodes remain consistent. An example of a CP system is a traditional relational database that uses strong consistency models.
2. **AP (Availability and Partition Tolerance)**: The system prioritizes availability over consistency. In the event of a network partition, the system remains available but may return stale or inconsistent data. An example of an AP system is a NoSQL database like Cassandra, which allows for eventual consistency.
3. **CA (Consistency and Availability)**: The system prioritizes both consistency and availability, but cannot tolerate network partitions. This configuration is not feasible in distributed systems where network failures can occur.

## Choosing the Right Configuration

When designing a distributed system, it is essential to understand the trade-offs imposed by the CAP Theorem and choose the appropriate configuration based on the application's requirements:

- **CP Systems**: Suitable for applications where data accuracy and consistency are critical, such as banking systems or inventory management.
- **AP Systems**: Suitable for applications where availability is more important than immediate consistency, such as social media platforms or content delivery networks.
- **CA Systems**: Rarely used in practice due to the inevitability of network partitions, but may be applicable in tightly controlled environments with reliable networks.

![CAP Theorem Diagram](https://media.geeksforgeeks.org/wp-content/uploads/20240813184051/cap.png)

## Conclusion

The CAP Theorem highlights the inherent trade-offs in designing distributed systems. By understanding the implications of consistency, availability, and partition tolerance, system architects can make informed decisions that align with their application's needs and priorities.

---

[<< Scaling](01-scaling.md) | [>> PACELC Theorem](03-pacelc-theorem.md)

[Back to Core Architecture Principles](index.md) | [Back to System Design Concepts](../index.md)
