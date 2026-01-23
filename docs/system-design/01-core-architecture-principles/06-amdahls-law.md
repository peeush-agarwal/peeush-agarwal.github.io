# Amdahl's Law

Amdahl's Law is a principle that quantifies the potential speedup of a task when only a portion of the task can be parallelized. It is named after computer scientist Gene Amdahl, who formulated the law in 1967. Amdahl's Law is particularly relevant in the context of parallel computing and system design, as it highlights the limitations of parallelization.

## Definition

Amdahl's Law states that the maximum speedup (S) of a task using multiple processors is limited by the fraction of the task (P) that cannot be parallelized. The law can be expressed mathematically as:

$S = \frac{1}{(1 - P) + \frac{P}{N}}$

Where:
- S is the overall speedup of the task.
- P is the proportion of the task that can be parallelized (0 ≤ P < 1).
- N is the number of processors.

## Implications of Amdahl's Law

1. **Diminishing Returns**: As the number of processors (N) increases, the speedup (S) approaches a limit determined by the non-parallelizable portion of the task (1 - P). This means that adding more processors yields diminishing returns in performance improvement.
2. **Importance of Serial Portion**: The serial portion of the task (1 - P) has a significant impact on the overall speedup. Even a small serial portion can limit the effectiveness of parallelization, emphasizing the need to minimize non-parallelizable components in system design.
3. **Optimal Resource Allocation**: Amdahl's Law suggests that there is an optimal number of processors for a given task, beyond which adding more processors does not result in significant performance gains. This has implications for resource allocation and cost-effectiveness in system design.

![Amdahl's Law Graph](https://upload.wikimedia.org/wikipedia/commons/e/ea/AmdahlsLaw.svg)

## Example

Consider a task where 90% of the work can be parallelized (P = 0.9) and 10% is inherently serial (1 - P = 0.1). Using Amdahl's Law, we can calculate the speedup for different numbers of processors:
- For N = 1 (single processor):
  $S = \frac{1}{(1 - 0.9) + \frac{0.9}{1}} = 1$
- For N = 2:
  $S = \frac{1}{(1 - 0.9) + \frac{0.9}{2}} \approx 1.82$
- For N = 4:
  $S = \frac{1}{(1 - 0.9) + \frac{0.9}{4}} \approx 3.08$
- For N = 10:
  $S = \frac{1}{(1 - 0.9) + \frac{0.9}{10}} \approx 5.26$
- For N = 100:
  $S = \frac{1}{(1 - 0.9) + \frac{0.9}{100}} \approx 9.09$

As seen in the example, even with 100 processors, the maximum speedup is limited to approximately 9.09 due to the 10% serial portion of the task.

## Conclusion

Amdahl's Law provides valuable insights into the limitations of parallelization in system design. It highlights the importance of minimizing the serial portion of tasks to achieve significant performance improvements. System architects and engineers must consider Amdahl's Law when designing parallel systems to ensure optimal resource utilization and performance outcomes.

---

[<< Throughput vs Latency](05-throughput-vs-latency.md)

[Back to Core Architecture Principles](index.md) | [Back to System Design Concepts](../index.md)
