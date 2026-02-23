# Single Server Setup

To start with something simple, everything running on a single server.

<!-- TODO: Add diagram of single server setup. -->

This is the most basic setup for any application. It is easy to set up and manage, making it ideal for small applications or during the initial stages of development. However, as the user base grows, this setup can quickly become a bottleneck, leading to performance issues and downtime.

Following are some of the key characteristics of a single server setup:
- All components of the application (web server, application server, database) run on a single machine.
- Limited resources (CPU, RAM, storage) are shared among all components.
- Single point of failure: if the server goes down, the entire application becomes unavailable.
- Scalability is limited by the hardware capabilities of the server.

To overcome these limitations, as the user base grows, you may need to consider scaling strategies such as vertical scaling (upgrading the server) or horizontal scaling (adding more servers).

---

[>> Vertical scaling vs Horizontal scaling](02-vertical-vs-horizontal-scaling.md)

[Back to Scale from Zero to Millions of Users](index.md) | [Back to System Design Concepts](../index.md)
