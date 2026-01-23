# Scaling

This document explores the concepts of vertical and horizontal scaling in system architecture. It discusses the advantages and disadvantages of each approach, as well as scenarios where one may be preferred over the other.

## TLDR;

Vertical scaling | Horizontal scaling
--- | ---
Adds resources (CPU, RAM, storage) to a single machine | Adds more machines to distribute load
Simpler to implement | More complex, requires architectural changes
Limited by hardware constraints | Can scale indefinitely
May require downtime for upgrades | Enhances availability and fault tolerance

![Vertical vs Horizontal Scaling Diagram](https://images.ctfassets.net/00voh0j35590/6wtOJjoIPbeqctg7dzjGS4/ca386d6416546a8ba6957e7b6407c5e4/vertical-versus-horizontal-scaling-compared-diagram.jfif)

## Vertical Scaling

Vertical scaling, also known as scaling up, involves adding more resources (CPU, RAM, storage) to an existing server or machine. This approach is often simpler to implement since it does not require changes to the application architecture. However, vertical scaling has limitations, such as hardware constraints and potential downtime during upgrades.

### Advantages of Vertical Scaling

- Simplicity: Easier to implement without significant changes to the application.
- Cost-Effective for Small Scale: May be more cost-effective for small-scale applications.
- Reduced Latency: All resources are on a single machine, which can reduce latency for certain applications.

### Disadvantages of Vertical Scaling

- Limited by Hardware: There is a maximum limit to how much a single machine can be upgraded.
- Downtime: Upgrading hardware may require downtime, affecting availability.
- Single Point of Failure: If the machine fails, the entire application goes down.

## Horizontal Scaling

Horizontal scaling, or scaling out, involves adding more machines or instances to a system to distribute the load. This approach is more complex as it often requires changes to the application architecture, such as implementing load balancing and data replication. However, horizontal scaling offers greater flexibility and resilience.

### Advantages of Horizontal Scaling

- Unlimited Growth: Can scale out indefinitely by adding more machines.
- High Availability: Distributes load across multiple machines, reducing the risk of a single point of failure.
- Flexibility: Easier to adapt to changing workloads by adding or removing instances as needed.

### Disadvantages of Horizontal Scaling

- Complexity: Requires changes to the application architecture and infrastructure.
- Cost: May incur higher costs due to the need for additional machines and infrastructure.
- Latency: Communication between distributed machines may introduce latency.

## When to Use Each Strategy

- Use vertical scaling for small to medium-sized applications with predictable workloads and when simplicity is a priority.
- Use horizontal scaling for large-scale applications with variable workloads, high availability requirements, and when future growth is anticipated.

---

[>> CAP Theorem](02-cap-theorem.md)

[Back to Core Architecture Principles](index.md) | [Back to System Design Concepts](../index.md)
