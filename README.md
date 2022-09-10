# Using Asyncio in Python by Caleb Hattingh

## 1. Introducing Asyncio
## 2. The Truth About Threads
## 3. Asyncio Walk-Through
## 4. 20 Asyncio Libraries You Aren't Using
## 5. Concluding Thoughts

---
---

# 1. Introducing Asyncio

## What Problem Is Asyncio Trying to Solve ?

For I/O-bound workloads, there are exactly (only!) two reasons to use async-based concurrency over thread-based concurrency:

* Asyncio offers a safer alternative to preemptive multitasking (i.e., using threads), thereby avoiding the bugs, race conditions, and other nondeterministic dangers that frequently occur in nontrivial threaded applications.

* Asyncio offers a simple way to support many thousands of simultaneous socket connections, including being able to handle many long-lived connections for newer technologies like WebSockets, or MQTT for Internet of Things (IoT) applications.

That’s it.

Threading—as a programming model—is best suited to certain kinds of computational tasks that are best executed with multiple CPUs and shared memory for efficient communication between the threads. In such tasks, the use of multicore processing with shared memory is a necessary evil because the problem domain requires it.

Network programming is not one of those domains. The key insight is that network programming involves a great deal of “waiting for things to happen,” and because of this, we don’t need the operating system to efficiently distribute our tasks over multiple CPUs. Furthermore, we don’t need the risks that preemptive multitasking brings, such as race conditions when working with shared memory.

However, there is a great deal of misinformation about other supposed benefits of event-based programming models. Here are a few of the things that just ain’t so:

* *Asyncio will make my code blazing fast.*
  * Unfortunately, no. In fact, most benchmarks seem to show that threading solutions are slightly faster than their comparable Asyncio solutions. If the extent of concurrency itself is considered a performance metric, Asyncio does make it a bit easier to create very large numbers of concurrent socket connections, though. Operating systems often have limits on how many threads can be created, and this number is significantly lower than the number of socket connections that can be made. The OS limits can be changed, but it is certainly easier to do with Asyncio. And while we expect that having many thousands of threads should incur extra context-switching costs that coroutines avoid, it turns out to be difficult to benchmark this in practice.1 No, speed is not the benefit of Asyncio in Python; if that’s what you’re after, try Cython instead!
* *Asyncio makes threading redundant.*
  * Definitely not! The true value of threading lies in being able to write multi-CPU programs, in which different computational tasks can share memory. The numerical library numpy, for instance, already makes use of this by speeding up certain matrix calculations through the use of multiple CPUs, even though all the memory is shared. For sheer performance, there is no competitor to this programming model for CPU-bound computation.
* *Asyncio removes the problems with the GIL.*
  * Again, no. It is true that Asyncio is not affected by the GIL,2 but this is only because the GIL affects multithreaded programs. The “problems” with the GIL that people refer to occur because it prevents true multicore parallelism when using threads. Since Asyncio is single-threaded (almost by definition), it is unaffected by the GIL, but it cannot benefit from multiple CPU cores either.3 It is also worth pointing out that in multithreaded code, the Python GIL can cause additional performance problems beyond what has already been mentioned in other points: Dave Beazley presented a talk on this called “Understanding the Python GIL” at PyCon 2010, and much of what is discussed in that talk remains true today.
* *Asyncio prevents all race conditions.*
  * False. The possibility of race conditions is always present with any concurrent programming, regardless of whether threading or event-based programming is used. It is true that Asyncio can virtually eliminate a certain class of race conditions common in multithreaded programs, such as intra-process shared memory access. However, it doesn’t eliminate the possibility of other kinds of race conditions, such as the interprocess races with shared resources common in distributed microservices architectures. You must still pay attention to how shared resources are being used. The main advantage of Asyncio over threaded code is that the points at which control of execution is transferred between coroutines are visible (because of the presence of await keywords), and thus it is much easier to reason about how shared resources are being accessed.
* *Asyncio makes concurrent programming easy.*
  * Ahem, where do I even begin?

The last myth is the most dangerous one. Dealing with concurrency is always complex, regardless of whether you’re using threading or Asyncio. When experts say “Asyncio makes concurrency easier,” what they really mean is that Asyncio makes it a little easier to avoid certain kinds of truly nightmarish race condition bugs—the kind that keep you up at night and that you tell other programmers about in hushed tones over campfires, wolves howling in the distance.

Even with Asyncio, there is still a great deal of complexity to deal with. How will your application support health checks? How will you communicate with a database that may allow only a few connections—much fewer than your five thousand socket connections to clients? How will your program terminate connections gracefully when you receive a signal to shut down? How will you handle (blocking!) disk access and logging? These are just a few of the many complex design decisions that you will have to answer.

Application design will still be difficult, but the hope is that you will have an easier time reasoning about your application logic when you have only one thread to deal with