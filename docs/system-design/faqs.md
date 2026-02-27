# FAQs

## Why is it important to iterate on System Designs rather than relying on the first solution, especially in real-world applications?

> Iterating on system designs is crucial because the first solution often reveals unforeseen bottlenecks or limitations when tested in real-world scenarios. By continuously revising and improving the design based on actual performance and feedback, engineers can enhance scalability, reliability, and maintainability. This process helps create systems that are better aligned with real-world demands and can adapt to changing requirements over time.

## What might change in a developer’s day-to-day work once they start seeing their tasks as connected parts of a larger system rather than isolated features?

> When developers see their tasks as connected parts of a larger system, they can make more informed decisions about architecture, anticipate how changes might affect other components, and identify potential integration issues early on. This perspective fosters better design choices and enhances collaboration across teams.

## A common question in a System Design interview is why we don’t design a system that can handle more work than necessary or predicted.

> In a system design interview, we avoid designing a system that can handle more work than needed because it can lead to wasted resources, increased complexity, and higher costs. It’s more efficient to design systems that meet current requirements well and can be scaled easily later. This approach keeps the system simpler, more cost-effective, and easier to maintain.

## You are in a System Design interview. The interviewer presents an open-ended question, such as: “Design a video streaming service like YouTube.”

```
Your task is to identify:
- Two functional requirements (what the system does) and
- Two non-functional requirements (how the system performs).
```

A: Here’s the answer for designing a video streaming service like YouTube:
   - Functional requirements:
     - Uploading videos: Users should be able to upload their own videos to the platform.
     - Streaming/watching content: Users should be able to stream and watch videos seamlessly.
   - Non-functional requirements:
     - Scalability: The system should handle a large number of users and high traffic efficiently.
     - Low Latency: Videos should load quickly with minimal buffering to ensure a smooth viewing experience.

It’s worth adding that user authentication (login/signup) and features like searching for videos or liking/commenting are also common functional requirements. Additionally, availability and reliability are important non-functional aspects to consider for a robust service.

## After identifying requirements for a video streaming service in the previous step, your next task is to ask two clarifying questions from the interviewer to scope the problem (specifically regarding data characteristics or user load).

A: Here are two good questions you could ask the interviewer to scope the problem for designing a video streaming service like YouTube:
- How many daily active users (DAU) do we expect to support?
- What is the average size of the video files we will be handling?

These questions help clarify the scale and data characteristics, which are crucial for designing the system architecture effectively.

## Imagine a design review where someone suggests treating late responses as simple crash failures. Why might this lead to incorrect assumptions when evaluating system behavior?

> Treating late responses as simple crash failures can be misleading because crash failures hide the node’s state completely, making it seem like the node is simply offline. Temporal failures, on the other hand, still produce correct results but too late, which can impact the usefulness of the system. Ignoring this difference can lead to incorrect assumptions about system behavior, especially regarding timing and reliability.
