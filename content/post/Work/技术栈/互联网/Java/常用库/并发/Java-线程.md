---
title: Java-线程
date: 2023-11-15 14:26:28
lastmod: 2025-02-27 09:20:52
aliases: 
keywords: 
categories:
  - Java
tags: 
share: true
---


## 线程

Java语言内置了多线程支持。当Java程序启动的时候，实际上是启动了一个JVM进程，然后，JVM启动主线程来执行 `main()` 方法。

### 创建线程

总体有两类方法

#### 继承 Thread
方法一：从`Thread`派生一个自定义类，然后覆写`run()`方法：

```java
// 多线程
public class Main {
    public static void main(String[] args) {
        Thread t = new MyThread();
        t.start(); // 启动新线程
    }
}

class MyThread extends Thread {
    @Override
    public void run() {
        System.out.println("start new thread!");
    }
}
```

执行上述代码，注意到`start()`方法会在内部自动调用实例的`run()`方法。

#### 实现 Runnable 接口
方法二：创建`Thread`实例时，传入一个`Runnable`实例：

```java
// 多线程
public class Main {
    public static void main(String[] args) {
        Thread t = new Thread(new MyRunnable());
        t.start(); // 启动新线程
    }
}

class MyRunnable implements Runnable {
    @Override
    public void run() {
        System.out.println("start new thread!");
    }
}
```

或者用Java 8引入的lambda语法进一步简写为：

```java
// 多线程
public class Main {
    public static void main(String[] args) {
        Thread t = new Thread(() -> {
            System.out.println("start new thread!");
        });
        t.start(); // 启动新线程
    }
}
```

### 线程的优先级

可以对线程设定优先级，设定优先级的方法是：

```java
Thread.setPriority(int n) // 1~10, 默认值5
```

JVM自动把1（低）~10（高）的优先级映射到操作系统实际优先级上（不同操作系统有不同的优先级数量）。优先级高的线程被操作系统调度的优先级较高，操作系统对高优先级线程可能调度更频繁，但我们决不能通过设置优先级来确保高优先级的线程一定会先执行。


### 线程的状态

Java线程的状态有以下几种：
- New：新创建的线程，尚未执行；
- Runnable：运行中的线程，正在执行`run()`方法的Java代码；
- Blocked：运行中的线程，因为某些操作被阻塞而挂起；
- Waiting：运行中的线程，因为某些操作在等待中；
- Timed Waiting：运行中的线程，因为执行`sleep()`方法正在计时等待；
- Terminated：线程已终止，因为`run()`方法执行完毕。


- 等待执行完毕：可以通过 `t.join()` 等待 `t` 线程结束后再继续运行
- 中断执行：在其他线程中对目标线程调用`interrupt()`方法

### 守护线程

守护线程是指为其他线程服务的线程。在JVM中，所有非守护线程都执行完毕后，无论有没有守护线程，虚拟机都会自动退出。
- 可以用于执行定时任务等
- **注意守护线程不能持有任何需要关闭的资源**，例如打开文件等，因为虚拟机退出时，守护线程没有任何机会来关闭文件，这会导致数据丢失。

创建守护线程需要在调用 `start()` 方法前，调用 `setDaemon(true)` 把该线程标记为守护线程：
```java
Thread t = new MyThread();
t.setDaemon(true);
t.start();
```

### 线程池

创建线程需要操作系统资源（线程资源，栈空间等），频繁创建和销毁大量线程需要消耗大量时间
线程池维护一定数量的线程，能接收大量小任务并分发到这些线程上进行处理。

Java标准库提供了`ExecutorService`接口表示线程池，它的典型用法如下：

```java
// 创建固定大小的线程池:
ExecutorService executor = Executors.newFixedThreadPool(3);
// 提交任务:
executor.submit(task1);
// 关闭线程池: 等待正在执行的任务先完成，然后再关闭
executor.shutdown();
```



**三类关闭线程池的方法**：
- `shutdown()`方法等待正在执行的任务先完成，然后再关闭
- `shutdownNow()` 会立刻停止正在执行的任务
- `awaitTermination()`则会等待指定的时间让线程池关闭。

#### 限制线程池的线程数量

因为 `ExecutorService` 只是接口，Java 标准库提供的几个常用实现类有：
- FixedThreadPool：线程数固定的线程池；
- CachedThreadPool：线程数根据任务动态调整的线程池；
- SingleThreadExecutor：仅单线程执行的线程池。

也可以通过 ThreadPoolExecutor 自定义：
```java
int min = 4;
int max = 10;
ExecutorService es = new ThreadPoolExecutor(
        min, max,
        60L, TimeUnit.SECONDS,
        new SynchronousQueue<Runnable>());
```

#### ScheduledThreadPool

放入 `ScheduledThreadPool` 的任务可以定期反复执行。

创建一个`ScheduledThreadPool`仍然是通过`Executors`类：

```java
ScheduledExecutorService ses = Executors.newScheduledThreadPool(4);
```

我们可以提交一次性任务，它会在指定延迟后只执行一次：

```java
// 1秒后执行一次性任务:
ses.schedule(new Task("one-time"), 1, TimeUnit.SECONDS);
```

如果任务以固定的每3秒执行，我们可以这样写：

```java
// 2秒后开始执行定时任务，每3秒执行:
ses.scheduleAtFixedRate(new Task("fixed-rate"), 2, 3, TimeUnit.SECONDS);
```

如果任务结束后间隔 3 秒重复执行，我们可以这样写：

```java
// 2秒后开始执行定时任务，以3秒为间隔执行:
ses.scheduleWithFixedDelay(new Task("fixed-delay"), 2, 3, TimeUnit.SECONDS);
```


#### ForkJoinPool

Fork/Join任务的原理：判断一个任务是否足够小，如果是，直接计算，否则，就分拆成几个小任务分别计算。这个过程可以反复“裂变”成一系列小任务。

**定义一个 Fork/Join 任务**：核心代码 `SumTask` 继承自 `RecursiveTask` ，在 `compute()` 方法中，关键是如何“分裂”出子任务并且提交子任务：
```java
class SumTask extends RecursiveTask<Long> {
    protected Long compute() {
    	if(/*任务足够小*/){
    		return ...;
    	}
        // “分裂”子任务:
        SumTask subtask1 = new SumTask(...);
        SumTask subtask2 = new SumTask(...);
        // invokeAll会并行运行两个子任务:
        invokeAll(subtask1, subtask2);
        // 获得子任务的结果:
        Long subresult1 = subtask1.join();
        Long subresult2 = subtask2.join();
        // 汇总结果:
        return subresult1 + subresult2;
    }
}
```

**提交任务**
```java
// fork/join:
        ForkJoinTask<Long> task = new SumTask(array, 0, array.length);
        Long result = ForkJoinPool.commonPool().invoke(task);
```


### Future

####  Callable 和 Future
`Runnable` 的方法没有返回值
`Callable` 接口的方法有一个泛型返回值：

```java
class Task implements Callable<String> {
    public String call() throws Exception {
        return longTimeCalculation(); 
    }
}
```

`ExecutorService.submit()` 方法，可以看到，它返回了一个 `Future` 类型，一个 `Future` 类型的实例代表一个未来能获取结果的对象，提供如下方法
- `get()` ：获取结果（可能会等待）
	- 如果异步任务已经完成，我们就直接获得结果
	- 如果异步任务还没有完成，那么 `get()` 会阻塞，直到任务完成后才返回结果
- `get(long timeout, TimeUnit unit)`：获取结果，但只等待指定的时间；
- `cancel(boolean mayInterruptIfRunning)`：取消当前任务；
- `isDone()`：判断任务是否已完成。

#### CompletableFuture

当异步任务完成或者发生异常时，自动调用回调对象的回调方法

创建一个 `CompletableFuture` 是通过 `CompletableFuture.supplyAsync()` 实现的，它需要一个实现了 `Supplier` 接口的对象：
```java
public interface Supplier<T> {
    T get();
}
```

**串行执行**：CompletableFuture 还有 thenApplyAsync 用于成功后执行下一个任务，thenAccept 获取结果
```java
// cfQuery成功后继续执行下一个任务:
CompletableFuture<Double> cfFetch = cfQuery.thenApplyAsync((code) -> {
	return fetchPrice(code);
});
// cfFetch成功后打印结果:
cfFetch.thenAccept((result) -> {
	System.out.println("price: " + result);
});
```

组合：
- `anyOf()` 可以实现“任意个 `CompletableFuture` 只要一个成功”
- `allOf()`可以实现“所有`CompletableFuture`都必须成功”
```java
// 两个CompletableFuture执行异步查询:
CompletableFuture<Double> cfFetchFromSina = cfQuery.thenApplyAsync((code) -> {
	return fetchPrice((String) code, "https://finance.sina.com.cn/price/");
});
CompletableFuture<Double> cfFetchFrom163 = cfQuery.thenApplyAsync((code) -> {
	return fetchPrice((String) code, "https://money.163.com/price/");
});

// 用anyOf合并为一个新的CompletableFuture:
CompletableFuture<Object> cfFetch = CompletableFuture.anyOf(cfFetchFromSina, cfFetchFrom163);
```


完整案例：
```java
import java.util.concurrent.CompletableFuture;

public class Main {
    public static void main(String[] args) throws Exception {
        // 创建异步执行任务:
        CompletableFuture<Double> cf = CompletableFuture.supplyAsync(Main::fetchPrice);
        // 如果执行成功:
        cf.thenAccept((result) -> {
            System.out.println("price: " + result);
        });
        // 如果执行异常:
        cf.exceptionally((e) -> {
            e.printStackTrace();
            return null;
        });
        // 主线程不要立刻结束，否则CompletableFuture默认使用的线程池会立刻关闭:
        Thread.sleep(200);
    }

    static Double fetchPrice() {
        try {
            Thread.sleep(100);
        } catch (InterruptedException e) {
        }
        if (Math.random() < 0.3) {
            throw new RuntimeException("fetch price failed!");
        }
        return 5 + Math.random() * 20;
    }
}
```


## 线程同步

### 线程安全和原子操作

线程安全：如果一个类被设计为允许多线程正确访问，我们就说这个类就是“线程安全”的（thread-safe）
- 不可变对象也是线程安全的，因为它们只能读不能写
- 类似`Math`这些只提供静态方法，没有成员变量的类，也是线程安全的。

**JVM规范定义了几种原子操作**：
- 基本类型（`long`和`double`除外）赋值，例如：`int n = m`；
- 引用类型赋值，例如：`List<String> list = anotherList`。


### 线程安全容器

| interface | non-thread-safe         | thread-safe                              |
| --------- | ----------------------- | ---------------------------------------- |
| List      | ArrayList               | CopyOnWriteArrayList                     |
| Map       | HashMap                 | ConcurrentHashMap                        |
| Set       | HashSet / TreeSet       | CopyOnWriteArraySet                      |
| Queue     | ArrayDeque / LinkedList | ArrayBlockingQueue / LinkedBlockingQueue |
| Deque     | ArrayDeque / LinkedList | LinkedBlockingDeque                      |

### synchronized

Java synchronized 的锁是可重入的：对同一个线程，可以在获取到锁以后继续获取同一个锁

#### 当成函数使用

语法是：
```Java
synchronized(Object) { // 获取锁
    ...
} // 释放锁
```


例如：实现一个线程安全的计数器（允许并发访问）
```java
public class Counter {
    private int count = 0;

    public void add(int n) {
        synchronized(this) {
            count += n;
        }
    }

    public int get() {
        return count;
    }
}
```

#### 修饰方法

**对于实例方法，用 `synchronized` 修饰这个方法等同于锁住 this 对象**。下面两种写法是等价的：

```java
public synchronized void add(int n) { // 锁住this
    count += n;
} // 解锁
```

```java
public void add(int n) {
    synchronized(this) { // 锁住this
        count += n;
    } // 解锁
}
```



**对 static方法添加 synchronized ，锁住的是该类的 `Class` 实例**。（对于 `static` 方法，是没有 `this` 实例的，因为 `static` 方法是针对类而不是实例。但是我们注意到任何一个类都有一个由JVM自动创建的 `Class` 实例）

以下两者等价
```java
public synchronized static void test(int n) {
    ...
}
public static void test(int n) {
	synchronized(Counter.class) {
		...
	}
}
```

### java.util.concurrent

#### ReentrantLock 重入锁

我们知道Java语言直接提供了`synchronized`关键字用于加锁，但这种锁一是很重，二是获取时必须一直等待，没有额外的尝试机制。

`java.util.concurrent.locks` 包提供的 `ReentrantLock` 用于替代 `synchronized` 加锁，例如：

```java
public class Counter {
    private final Lock lock = new ReentrantLock();
    private int count;

    public void add(int n) {
        lock.lock();
        try {
            count += n;
        } finally {
            lock.unlock();
        }
    }
}
```

因为`synchronized`是Java语言层面提供的语法，所以我们不需要考虑异常，而`ReentrantLock`是Java代码实现的锁，我们就必须先获取锁，然后在`finally`中正确释放锁。

#### 条件锁

可以通过以下方法由某个锁获取条件锁
```Java
private final Lock lock = new ReentrantLock();
private final Condition condition = lock.newCondition();
```

`Condition`提供的`await()`、`signal()`、`signalAll()`原理和`synchronized`锁对象的`wait()`、`notify()`、`notifyAll()`是一致的，并且其行为也是一样的：

- `await()` 会释放当前锁，进入等待状态；和 `tryLock()` 类似， `await()` 可以在等待指定时间后，如果还没有被其他线程通过 `signal()` 或 `signalAll()` 唤醒，可以自己醒来
- `signal()`会唤醒某个等待线程；
- `signalAll()`会唤醒所有等待线程；
- 唤醒线程从`await()`返回后需要重新获得锁。

```java
if (condition.await(1, TimeUnit.SECOND)) {
    // 被其他线程唤醒
} else {
    // 指定时间内没有被其他线程唤醒
}
```

例如创建一个任务队列
```java
class TaskQueue {
    private final Lock lock = new ReentrantLock();
    private final Condition condition = lock.newCondition();
    private Queue<String> queue = new LinkedList<>();

    public void addTask(String s) {
        lock.lock();
        try {
            queue.add(s);
            condition.signalAll();
        } finally {
            lock.unlock();
        }
    }

    public String getTask() {
        lock.lock();
        try {
            while (queue.isEmpty()) {
                condition.await();
            }
            return queue.remove();
        } finally {
            lock.unlock();
        }
    }
}
```

#### 读写锁

允许多个线程同时读，但只要有一个线程在写，其他线程就必须等待

```java
public class Counter {
    private final ReadWriteLock rwlock = new ReentrantReadWriteLock();
    // 注意: 一对读锁和写锁必须从同一个rwlock获取:
    private final Lock rlock = rwlock.readLock();
    private final Lock wlock = rwlock.writeLock();
    private int[] counts = new int[10];

    public void inc(int index) {
        wlock.lock(); // 加写锁
        try {
            counts[index] += 1;
        } finally {
            wlock.unlock(); // 释放写锁
        }
    }

    public int[] get() {
        rlock.lock(); // 加读锁
        try {
            return Arrays.copyOf(counts, counts.length);
        } finally {
            rlock.unlock(); // 释放读锁
        }
    }
}
```

#### 版本锁

读写锁偏向于读者：如果有线程正在读，写线程需要等待读线程释放锁后才能获取写锁，即读的过程中不允许写

版本锁 `StampedLock` 通过维护一个版本，允许在读的过程中写。
- StampedLock 可以提高并发率，代价是逻辑更为复杂
- StampedLock 是不可重入锁，不能在一个线程中反复获取同一个锁
- `StampedLock`还提供了更复杂的将悲观读锁升级为写锁的功能，它主要使用在if-then-update的场景：即先读，如果读的数据满足条件，就返回，如果读的数据不满足条件，再尝试写。

写的过程和读写锁一样，但是读的过程比较复杂：
- 创建一个 StampedLock 对象
- 尝试获取一个乐观读锁：stampedLock.tryOptimisticRead();
- 检查获取乐观读锁后是否有其他写锁发生：stampedLock.validate(stamp)
- 若有新的写，需要获取悲观读锁并重新读。由于写入的概率不高，程序在绝大部分情况下可以通过乐观读锁获取数据，极少数情况下使用悲观读锁获取数据。
**乐观**：乐观地估计读的过程中大概率不会有写入
**悲观**：读的过程中拒绝有写入

**版本锁的读取过程**：
```Java
long stamp = stampedLock.tryOptimisticRead(); // 获得一个乐观读锁
// Read...
if (!stampedLock.validate(stamp)) { // 检查乐观读锁后是否有其他写锁发生
    stamp = stampedLock.readLock(); // 获取一个悲观读锁
    try {
        // Re-read
    } finally {
        stampedLock.unlockRead(stamp); // 释放悲观读锁
    }
}
```

#### 信号量

`Semaphore` 本质上就是一个信号计数器，用于限制同一时间的最大访问数量。
- acquire 加锁，release 解锁
- tryAcquire 可以指定最大等待时间

```java
public class AccessLimitControl {
    // 任意时刻仅允许最多3个线程获取许可:
    final Semaphore semaphore = new Semaphore(3);

    public String access() throws Exception {
        // 如果超过了许可数量,其他线程将在此等待:
        semaphore.acquire();
        try {
            // TODO:
            return UUID.randomUUID().toString();
        } finally {
            semaphore.release();
        }
    }
}
```

#### 原子操作

Java的 `java.util.concurrent` 包除了提供底层锁、并发集合外，还提供了一组原子操作的封装类，它们位于 `java.util.concurrent.atomic` 包。

例如 `AtomicInteger` 提供的主要操作有：
- 增加值并返回新值：`int addAndGet(int delta)`
- 加1后返回新值：`int incrementAndGet()`
- 获取当前值：`int get()`
- 用CAS方式设置：`int compareAndSet(int expect, int update)`



### 线程间通信
#### 线程间的共享变量

在Java虚拟机中，变量的值保存在主内存中，但是，当线程访问变量时，它会先获取一个副本，并保存在自己的工作内存中。
如果线程修改了变量的值，虚拟机会在某个时刻把修改后的值回写到主内存，但是，这个时间是不确定的！（在x86的架构下，JVM回写主内存的速度非常快，但是，换成ARM的架构，会有显著的延迟）

线程间共享的变量应采用关键字 `volatile` 声明， `volatile` 关键字的目的是告诉虚拟机：
- 每次访问变量时，总是获取主内存的最新值；
- 每次修改变量后，立刻回写到主内存。

#### Wait 和 Notify

- `wait()` 方法必须在当前获取的锁对象上调用，例如获取的是 `this` 锁，则调用 `this.wait()`
- 必须在 `synchronized` 块中才能调用 `wait()` 方法， `wait()` 调用时，会释放线程获得的锁， `wait()` 返回时，线程又会重新试图获得锁
- 在相同的锁对象上调用 `notify()` 方法，可以让等待的线程被重新唤醒
- 使用`notifyAll()`将唤醒所有当前正在`this`锁等待的线程，而`notify()`只会唤醒其中一个（具体哪个依赖操作系统，有一定的随机性）

例如一个任务队列
```java
class TaskQueue {
    Queue<String> queue = new LinkedList<>();

    public synchronized void addTask(String s) {
        this.queue.add(s);
        this.notifyAll();
    }

    public synchronized String getTask() throws InterruptedException {
    // 必须是while而非if
    // wait()方法返回时需要重新获得this锁。假设当前有3个线程被唤醒，唤醒后，首先要等待执行addTask()的线程结束此方法后，才能释放this锁，随后，这3个线程中只能有一个获取到this锁，剩下两个将继续等待
        while (queue.isEmpty()) {
            this.wait();
        }
        return queue.remove();
    }
}
```


#### 线程上下文

Java标准库提供了一个特殊的 `ThreadLocal` ，它可以在一个线程中传递同一个对象。

`ThreadLocal` 实例通常总是以静态字段初始化如下：

```java
static ThreadLocal<User> threadLocalUser = new ThreadLocal<>();
```

```java
void processUser(user) {
    try {
        threadLocalUser.set(user);
        // ...线程中的所有方法都可以随时获取到该`User`实例：
    } finally {
        threadLocalUser.remove();
    }
}
```
