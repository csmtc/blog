---
title: Java-Lombok-基于注解的样板代码生成
date: 2024-02-09 00:05:48
lastmod: 2025-03-11 15:36:08
aliases: 
keywords: 
categories:
  - Java
tags: 
share: true
---


### 简介
Lombok 是一个 Java 库，用于简化 Java 类的代码，特别是那些需要大量样板代码的类。通过注解的方式，Lombok 自动生成常见的代码结构，例如 getter、setter、构造函数、toString、hashCode 和 equals 方法等，从而大大减少了代码冗余，提高了代码的可读性和可维护性。

Lombok 的优势
- **性能**：Lombok 是通过编译时注解处理器生成字节码的，它不会影响运行时性能，但你需要在编译时支持 Lombok。
- **减少冗余代码**：生成大量样板代码，避免手动编写 getter/setter、toString、equals、hashCode 等方法。
- **提高开发效率**：减少代码的编写量，专注于业务逻辑。
- **提高可维护性**：避免由于手动编写冗余代码而产生的潜在错误。


### 引入

注意 Scope
```
<dependency>
	<groupId>org.projectlombok</groupId>
	<artifactId>lombok</artifactId>
	<scope>annotationProcessor</scope>
</dependency>
```

在编译插件中引入注解处理：
```
    <build>
        <plugins>
            <!-- 其他插件 -->

            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
<!--                <version>3.8.1</version> -->
                <configuration>
                    <annotationProcessorPaths>
                        <path>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                            <version>${lombok.version}</version>
                        </path>
                    </annotationProcessorPaths>
                    <compilerArgs>
                    </compilerArgs>
                    <source>${maven.compiler.source}</source>
                    <target>${maven.compiler.target}</target>
                </configuration>
            </plugin>
        </plugins>
    </build>
```

若在 Spring 环境下使用，需在打包插件中排除
```
<plugin>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-maven-plugin</artifactId>
	<configuration>
		<excludes>
			<exclude>
				<groupId>org.projectlombok</groupId>
				<artifactId>lombok</artifactId>
			</exclude>
		</excludes>
	</configuration>
</plugin>
```

### Lombok 的常用注解

####  **@Getter 和 @Setter**

- 自动为类中的每个字段生成 getter 和 setter 方法。

```java
import lombok.Getter;
import lombok.Setter;
@Getter @Setter
public class Person {
	private String name;
	private int age;
}
```

生成的代码：

```java
public String getName() {
	return name;
}

public void setName(String name) {
	this.name = name;
}

public int getAge() {
	return age;
}

public void setAge(int age) {
	this.age = age;
}
```

#### @Accessors(chain = true)
用于生成链式调用的 `setter` 方法。
```
Blog blog = new Blog().setTitle("My Blog").setContent("This is my blog content");
```

####  **@ToString**

- 自动生成 `toString` 方法，通常会包含所有字段的值。

```java
@ToString
public class Person {
	private String name;
	private int age;
}
```

生成的 `toString` 方法：

```java
public String toString() {
	return "Person(name=" + name + ", age=" + age + ")";
}
```

#### **@EqualsAndHashCode**

- 自动生成 `equals` 和 `hashCode` 方法，通常根据字段值来比较对象。
	- @EqualsAndHashCode(callSuper = false)：callSuper 表示是否考虑父类属性

```java
@EqualsAndHashCode
public class Person {
	private String name;
	private int age;
}
```

#### **@AllArgsConstructor 和 @NoArgsConstructor**

- 自动生成包含所有字段的构造函数（`@AllArgsConstructor`）或无参构造函数（`@NoArgsConstructor`）。

```java
@AllArgsConstructor
public class Person {
	private String name;
	private int age;
}
```

生成的构造函数：

```java
public Person(String name, int age) {
	this.name = name;
	this.age = age;
}
```

#### **@RequiredArgsConstructor**

- 自动生成一个包含所有 `final` 字段和 `@NonNull` 注解字段的构造函数。

```java
@RequiredArgsConstructor
public class Person {
	private final String name;
	private int age;
}
```

生成的构造函数：

```java
public Person(String name) {
	this.name = name;
}
```

 #### **@Value**

- 是一个复合注解，用于创建不可变类，相当于组合使用 `@Getter` 、 `@AllArgsConstructor` 、 `@ToString` 、 `@EqualsAndHashCode` 和 `@Immutable` 注解。

```java
@Value
public class Person {
	private String name;
	private int age;
}
```

生成的类是不可变的，所有字段都有 `final` 修饰符。

#### **@Data**

 `@Data` 是一个复合注解用于创建可变类，相当于组合使用 `@Getter` 、 `@Setter` 、 `@EqualsAndHashCode` 、 `@ToString` 和 `@RequiredArgsConstructor` 。





 #### **@Slf4j**

- 用于生成 SLF4J 日志记录器，自动在类中创建 `private static final Logger logger = LoggerFactory.getLogger(ClassName.class);`。

```java
@Slf4j
public class Person {
	public void doSomething() {
		logger.info("Doing something");
	}
}
```

#### **@Builder**

- 为类生成一个建造者模式的实现，方便创建复杂对象。

```java
@Builder
public class Person {
	private String name;
	private int age;
}
```

使用示例：

```java
Person person = Person.builder()
					  .name("John")
					  .age(30)
					  .build();
```
    