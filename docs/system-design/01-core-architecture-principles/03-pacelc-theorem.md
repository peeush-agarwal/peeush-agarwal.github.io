# PACELC Theorem

The PACELC Theorem is an extension of the CAP Theorem that provides a more comprehensive framework for understanding the trade-offs in distributed systems. Proposed by Daniel Abadi in 2010, PACELC stands for:
- **P**: Partition Tolerance
- **A**: Availability
- **C**: Consistency
- **E**: Else
- **L**: Latency
- **C**: Consistency

The theorem states that in the presence of a network partition (P), a distributed system must choose between availability (A) and consistency (C), similar to the CAP Theorem. However, PACELC adds that even when there is no partition (Else), the system must still make a trade-off between latency (L) and consistency (C).

## Implications of the PACELC Theorem

According to the PACELC Theorem, distributed systems can be categorized based on their behavior during partitions and normal operation:
1. **PA/EL Systems**: These systems prioritize availability over consistency during partitions and latency over consistency during normal operation. An example is Amazon DynamoDB, which is designed for high availability and low latency.
2. **PC/EC Systems**: These systems prioritize consistency over availability during partitions and consistency over latency during normal operation. An example is Google Spanner, which emphasizes strong consistency even at the cost of higher latency.
3. **PA/EC Systems**: These systems prioritize availability during partitions and consistency during normal operation. An example is Cassandra, which allows for eventual consistency but aims to provide consistent reads and writes when the system is stable.
4. **PC/EL Systems**: These systems prioritize consistency during partitions and latency during normal operation. An example is traditional relational databases that focus on strong consistency but may sacrifice latency for performance.

## Choosing the Right Configuration

When designing a distributed system, it is essential to understand the trade-offs imposed by the PACELC Theorem and choose the appropriate configuration based on the application's requirements:
- **PA/EL Systems**: Suitable for applications where availability and low latency are critical, such as e-commerce platforms or social media applications.
- **PC/EC Systems**: Suitable for applications where data accuracy and consistency are paramount, such as financial systems or inventory management.
- **PA/EC Systems**: Suitable for applications that require high availability but also need consistent data when the system is stable, such as content management systems.
- **PC/EL Systems**: Suitable for applications that require strong consistency but can tolerate higher latency, such as enterprise resource planning (ERP) systems.

![PACELC Theorem Diagram](https://www.scylladb.com/wp-content/uploads/PACELC-theorem-diagram-1.jpg)

## Conclusion

The PACELC Theorem provides a nuanced understanding of the trade-offs in distributed systems beyond the CAP Theorem. By considering both partition scenarios and normal operation, system architects can make more informed decisions that align with their application's needs and priorities.

---

[<< CAP Theorem](02-cap-theorem.md)

[Back to Core Architecture Principles](index.md) | [Back to System Design Concepts](../index.md)
