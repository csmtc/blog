---
title: Spring-AOP
date: 2023-12-13 20:17:04
lastmod: 2025-03-10 18:12:27
aliases: 
keywords: 
categories:
  - Java
tags: 
share: true
---

### 框架

框架的基本特点：
- 框架（Framework），是基于基础技术之上，从众多业务中抽取出的通用解决方案;
- 框架是一个半成品，使用框架规定的语法开发可以提高开发效率，可以用简单的代码就能完成复杂的基础业务;
- 框架内部使用大量的设计模式、算法、底层代码操作技术，如反射、内省、xml 解析、注解解析等;
- 框架一般都具备扩展性;
- 有了框架，我们可以将精力尽可能的投入在纯业务开发上而不用去费心技术实现以及一些辅助业务。

Java 中常用的框架：可以分为基础框架和服务框架：
- 基础框架：完成基本业务操作的框架，如 MyBatis、Spring、SpringMVC、Struts2、Hibernate 等
- 服务框架：特定领域的框架，一般还可以对外提供服务框架，如 MQ、ES、NacOs 等

## 控制反转原理

### 为何需要 IOC，什么是 IOC

1. 接口和实现，层与层紧密耦合（例如业务层 new 一个数据库对象，后续更换数据库不便）
2. 通用的事务功能耦合在业务代码中：例如通用的日志功能耦合在业务代码中

解决思路：程序代码中不要手动 new 对象，第三方根据要求为程序提供需要的 Bean 对象的代理对象

**IOC 控制反转**：不由应用程序直接创建对象，创建对象的控制权转到外部，而由第三方创建对象
**DI 依赖注入**：指将对象 B 注入到对象 A 之中（例如 A 持有 B 的引用）
**Aspect Oriented Programing**：面向切面编程，主要通过 Proxy 实现

### SpringIOC

在Spring中，构成应用程序主干并由Spring IoC容器管理的对象称为**bean**，离开了 SpringIOC 容器这些 bean 只是普通的 Java 对象

`org.springframework.context.ApplicationContext` 接口表示**Spring IOC容器**，负责实例化、配置和组装Bean。
- 容器通过读取**配置元数据**获取有关组件的指令，以实例化、配置和组装 Bean，Spring IOC容器本身与配置元数据完全分离
- 配置元数据可以表示为带注释的组件类、带有工厂方法的配置类或外部XML文件或Groovy脚本
- 大多数应用场景中，不需要显式用户代码来实例化 Spring IoC 容器的一个或多个实例。
	- 在 Spring Boot 场景中，应用程序上下文是根据常见的设置约定隐式引导的
![](./assets/Spring-Bean-%E5%AE%B9%E5%99%A8/file-20241204151852421.png)



### 使用 SpringIOC 实现 IoC+DI

分为三步，实现代码只定义接口，实现通过配置元数据绑定：
1. 定义接口和实现
2. 写 bean 文件注册实现类
3. 代码中只定义接口对象，再通过 beanFactory.getBean 方法获取实现类绑定到接口对象

4. 定义接口和实现：
```
package org.example;
public interface ExampleService {
    void sayHello();
}
```

```
package org.example.impl;
import org.example.ExampleService;
public class ExampleServiceImpl implements ExampleService {
    @Override
    public void sayHello() {
        System.out.println("Hello World");
    }
}
```


2. **在资源目录中创建一个描述 beans 的定义文件**
- `id` 属性是标识单个Bean定义的字符串，可用于引用协作对象（详见[Dependencies](https://docs.spring.io/spring-framework/reference/core/beans/dependencies.html)）
- `class` 属性定义了Bean的类型，并使用完全限定的类名
```XML
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">
    <bean id="user-service" class="org.example.impl.ExampleServiceImpl"/>
</beans>
```

3. **用 BeanFactory 将实现类绑定到接口对象**
```Java
package org.example;

import org.springframework.beans.factory.BeanFactory;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class Main {
    public static void main(String[] args) {
        BeanFactory beanFactory = new ClassPathXmlApplicationContext("applicationContext.xml");
        ExampleService serv = (ExampleService)beanFactory.getBean("user-service");
        System.out.println(serv); //org.example.impl.ExampleServiceImpl@14a2f921
    }
}
```

## 配置元数据

配置元数据可以定义如何将实现绑定到接口。

配置元数据：
- **基于注解的配置**：在应用程序的组件类上使用基于注释的配置元数据定义 Bean
- **基于 Java的配置**：通过使用基于Java的配置类在应用程序类外部定义Bean。要使用这些功能，请参阅 `@Configuration` 、 `@Bean` 、 `@Import` 和 `@DependsOn` 批注

### XML 方式

所有使用 XML 文件进行配置信息加载的 Spring IoC 容器，都采用统一的 XML 格式：
```
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">
    <bean id="producer" class="org.example.impl.ProducerImpl"/>
    <bean id="consumer" class="org.example.impl.ConsumerImpl"/>
    <bean id="application" class="org.example.Application">
        <property name="producer" ref="producer"/>
        <property name="consumer" ref="consumer"/>
    </bean>
</beans>
```

`<beans>` 是 XML 配置文件中最顶层的元素：
- 它拥有相应的属性(attribute)对所辖的 `<bean>` 进行统一的默认行为设置：
	- default-lazy-init
	- default-autowire
![](./assets/Spring-%E5%AE%B9%E5%99%A8%E4%BF%A1%E6%81%AF%E7%AE%A1%E7%90%86-XML%E9%85%8D%E7%BD%AE/file-20241204210851524.png)


#### Bean 的元数据配置

Bean 的完整配置
![](./assets/Spring-Bean-%E5%AE%B9%E5%99%A8/file-20241206214243860.png)
##### 属性

- 用于依赖注入，为类中名为 `name` 的field 注入特定的类型 `ref`
-  bean 依赖注入的 ref 属性指定 bean，必须在容器中存在
```xml
<bean id="bookService" class="com.itheima.service.impl.BookServiceImpl">
    <property name="bookDao" ref="bookDao"/>
</bean>
```

##### 别名
- **别名**：定义 bean 的别名，可以有多个，可用 `,` , `;` , 空格 ` ` 分隔。
- 后续可以通过别名获取到这个 bean
```xml
<bean id="bookService" name="service service4 bookEbi" class="com.itheima.service.impl.BookServiceImpl">
</bean>
```

```Java
ApplicationContext ctx = new ClassPathXmlApplicationContext("applicationContext.xml");
//此处根据bean标签的id属性和name属性的任意一个值来获取bean对象
BookService bookService = (BookService) ctx.getBean("service4");
```

##### scope 单例模式

scope 决定一个 Bean 是单例的还是非单例的
- 可选值 `singloton` 和 `prototype`
- scope 属性默认值为 singloton，即默认 bean 是单例的

```xml
<!--scope：为bean设置作用范围，可选值为单例singloton，非单例prototype-->
<bean id="bookDao" name="dao" class="com.itheima.dao.impl.BookDaoImpl" scope="prototype"/>
```


## Bean 的实例
### Bean 的实例化

bean 本质上就是对象，对象在 new 的时候会使用构造方法完成，那创建 bean 也是使用构造方法完成的。
实例化bean的三种方式， `构造方法` , `静态工厂` 和 `实例工厂`

#### 构造方法实例化

**默认使用类的无参构造方法**

- 例如将 BookDaoImpl 类绑定到 BookDao 接口
```
<bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl"/>
```

- 后续调用 ctx.getBean("bookDao") 方法就会调用 BookDaoImpl 的无参构造方法
```Java
public class BookDaoImpl implements BookDao {
    public BookDaoImpl() {
        System.out.println("book dao constructor is running ....");
    }
}
public class AppForInstanceBook {
    public static void main(String[] args) {
        var ctx = new ClassPathXmlApplicationContext("applicationContext.xml");
        BookDao bookDao = (BookDao) ctx.getBean("bookDao");
        // 此时调用了BookDaoImpl()

    }
}
```

- 如果相应类没有无参构造方法就会报错
```
Caused by: java.lang.NoSuchMethodException: com.itheima.dao.impl.BookDaoImpl.<init>()
```


#### 静态工厂实例化

应用场景：在工厂的静态方法中，我们除了 new 对象还可以做其他的一些业务操作
- 基本可以被实例工厂替代
配置方法：在配置文件中定义工厂类和**静态工厂方法**
```xml
<bean id="orderDao" class="com.itheima.factory.OrderDaoFactory" factory-method="getOrderDao"/>
```

```Java
//静态工厂创建对象
public class OrderDaoFactory {
    public static OrderDao getOrderDao(){
        return new OrderDaoImpl();
    }
}
```

#### 实例工厂实例化

配置方法：
- 先定义工厂 bean
- 再定义实例 bean，并填入 factory-method 和 factory-bean 属性
```xml
<bean id="userFactory" class="com.itheima.factory.UserDaoFactory"/>
<bean id="userDao" factory-method="getUserDao" factory-bean="userFactory"/>
```

工厂 bean 需要实现 `FactoryBean<实例类型>` 接口，
- getObject 方法创建对象
- getObjectType 方法返回实例类型
```Java
public class UserDaoFactoryBean implements FactoryBean<UserDao> {
    //代替原始实例工厂中创建对象的方法
    public UserDao getObject() throws Exception {
        return new UserDaoImpl();
    }
    //返回所创建类的Class对象
    public Class<?> getObjectType() {
        return UserDao.class;
    }
    // 指定实例类型是否为单例
    public boolean isSingleton() {
        return false;
    }
}
```

FactoryBean 接口：
```Java
public interface FactoryBean<T> {
    String OBJECT_TYPE_ATTRIBUTE = "factoryBeanObjectType";

    @Nullable
    T getObject() throws Exception;

    @Nullable
    Class<?> getObjectType();

    default boolean isSingleton() {
        return true;
    }
}
```

### 依赖注入

#### Setter 注入（推荐）

在类中创建相应属性的 setter 方法
- name 属性：设置注入的属性名，实际是 set 方法对应的名称
	- 例如 setAge，则 property 中 name 就填 age
- value属性：设置注入简单类型数据值
- ref 属性：设置注入引用类型 bean 的 id 或 name

```xml
<bean ...>
	<property name="" ref=""/> 简单数据类型
	<property name="" value=""/> 引用数据类型
</bean>
```


#### 构造器装入

标签 `<constructor-arg>` 中
* name属性对应的值为构造函数中方法形参的参数名，必须要保持一致。
* ref属性指向的是spring的IOC容器中其他bean对象。

多个 `<contructor-arg>` 的配置顺序可以任意

```xml
<bean id="bookService" class="com.itheima.service.impl.BookServiceImpl">
    <constructor-arg name="bookDao" ref="bookDao"/>
    <constructor-arg name="userDao" ref="userDao"/>
</bean>
```

```java
public class BookServiceImpl implements BookService{
    private BookDao bookDao;
    private UserDao userDao;

    public BookServiceImpl(BookDao bookDao,UserDao userDao) {
        this.bookDao = bookDao;
        this.userDao = userDao;
    }
}
```

SP：按名查找参数的问题，与其他查找参数的方式
* 当构造函数中方法的参数名发生变化后，配置文件中的 name 属性也需要跟着变
* 这两块存在紧耦合，具体该如何解决?

方式一:删除 name 属性，添加 type 属性，按照类型注入

```xml
<bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl">
    <constructor-arg type="int" value="10"/>
    <constructor-arg type="java.lang.String" value="mysql"/>
</bean>
```

方式二:删除 type 属性，添加 index 属性，按照索引下标注入，下标从 0 开始

```xml
<bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl">
    <constructor-arg index="1" value="100"/>
    <constructor-arg index="0" value="mysql"/>
</bean>
```

#### 自动注入

为某个 bean 开启自动装配：
- 将 `<property>` 标签删除
- 在 `<bean>` 标签中添加 autowire 属性。

需要注意：
* 需要注入属性的类中对应属性的 setter 方法不能省略
* 被注入的对象必须要被 Spring 的 IOC 容器管理
* 自动装配优先级低于 setter 注入与构造器注入，同时出现时自动装配配置失效
```xml
<!--autowire属性：开启自动装配，通常使用按类型装配-->
<bean id="bookService" class="com.itheima.service.impl.BookServiceImpl" autowire="byType"/>
```

autowire 有四种取值：
* ==byType（常用）==：必须保障容器中相同类型的 bean 唯一，在Spring的IOC容器中如果找到多个对象，会报 `NoUniqueBeanDefinitionException`
* byName：这里的 Name 就是 setXXX 中的 XXX，不过将 XXX 的首字母小写
	* 如果按照名称去找对应的 bean 对象，找不到则注入 Null
	* 因变量名与配置耦合，不推荐使用
* 按构造方法
* 不启用自动装配

#### 集合注入

```
<!--数组注入-->
<property name="array">
    <array>
        <value>100</value>
        <value>200</value>
        <value>300</value>
    </array>
</property>

<!--list集合注入-->
<property name="list">
    <list>
        <value>itcast</value>
        <value>itheima</value>
        <value>boxuegu</value>
        <value>chuanzhihui</value>
    </list>
</property>

<!--set集合注入-->
<property name="set">
    <set>
        <value>itcast</value>
        <value>itheima</value>
        <value>boxuegu</value>
        <value>boxuegu</value>
    </set>
</property>

<!--map集合注入-->
<property name="map">
    <map>
        <entry key="country" value="china"/>
        <entry key="province" value="henan"/>
        <entry key="city" value="kaifeng"/>
    </map>
</property>

<!--Properties注入-->
<property name="properties">
    <props>
        <prop key="country">china</prop>
        <prop key="province">henan</prop>
        <prop key="city">kaifeng</prop>
    </props>
</property>
```

#### 注入 Properties 中的值


##### 步骤 1:准备 properties 配置文件

resources 下创建一个 jdbc.properties 文件,并添加对应的属性键值对

```properties
jdbc.driver=com.mysql.jdbc.Driver
jdbc.url=jdbc:mysql://127.0.0.1:3306/spring_db
jdbc.username=root
jdbc.password=root
```

##### 步骤2:开启 `context` 命名空间

在applicationContext.xml中 beans 中开 `context` 命名空间
```
xmlns:context="http://www.springframework.org/schema/context"
```
完整配置：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="
            http://www.springframework.org/schema/beans
            http://www.springframework.org/schema/beans/spring-beans.xsd
            http://www.springframework.org/schema/context
            http://www.springframework.org/schema/context/spring-context.xsd">
</beans>
```

##### 步骤 3:加载 properties 配置文件

在配置文件中使用 `context` 命名空间下的标签来加载 properties 配置文件

```xml
<context:property-placeholder location="jdbc.properties"/>
```

如果需要避免加载系统环境变量：
```xml
<context:property-placeholder location="jdbc.properties" system-properties-mode="NEVER"/>
```

批量加载：
- Location 属性值中可以使用通配符 `*` 
- `classpath:` 代表的是从当前项目根路径下开始查找
- `classpath*:` 代表从系统 classpath 下开始查找

```xml
<!--方式二-->
<context:property-placeholder location="*.properties" system-properties-mode="NEVER"/>
<!--方式三 -->
<context:property-placeholder location="classpath:*.properties" system-properties-mode="NEVER"/>
<!--加载当前工程类路径和当前工程所依赖的所有jar包中的所有properties文件-->
<context:property-placeholder location="classpath*:*.properties" system-properties-mode="NEVER"/>
```

##### 步骤 4:完成属性注入

使用 `${key}` 来读取 properties 配置文件中的内容并完成属性注入

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="
            http://www.springframework.org/schema/beans
            http://www.springframework.org/schema/beans/spring-beans.xsd
            http://www.springframework.org/schema/context
            http://www.springframework.org/schema/context/spring-context.xsd">
    
    <context:property-placeholder location="jdbc.properties"/>
    <bean id="dataSource" class="com.alibaba.druid.pool.DruidDataSource">
        <property name="driverClassName" value="${jdbc.driver}"/>
        <property name="url" value="${jdbc.url}"/>
        <property name="username" value="${jdbc.username}"/>
        <property name="password" value="${jdbc.password}"/>
    </bean>
</beans>
```
### 容器

#### 创建容器

1. 基于 ApplicationContext
可以从类路径或文件系统路径加载 XML 配置
```java
ApplicationContext ctx = new ClassPathXmlApplicationContext("applicationContext.xml");
ApplicationContext ctx = new FileSystemXmlApplicationContext("applicationContext.xml");
```

2. 基于 BeanFactory
```Java
Resource resources = new ClassPathResource("applicationContext.xml");
BeanFactory bf = new XmlBeanFactory(resources);
BookDao bookDao = bf.getBean(BookDao.class);
```

默认情况下：
* BeanFactory 是延迟加载，只有在获取 bean 对象的时候才会去创建
* ApplicationContext 是立即加载，容器加载的时候就会创建 bean 对象

#### 从容器中获取 Bean

1. 按名获取
   ```java
   BookDao bookDao = (BookDao) ctx.getBean("bookDao");
   BookDao bookDao = ctx.getBean("bookDao"，BookDao.class);
   ```
2. 按类型获取
```java
BookDao bookDao = ctx.getBean(BookDao.class);
```

### Bean 的生命周期
创建容器：
分配对象内存
执行构造方法
执行属性注入
Hook 点：init-method/afterPropertiesSet 
使用容器：
关闭容器：
1. Hook 点：destroy-method/destroy


**注意：若不关闭容器，distory 方法不会执行**，JVM 停止时只会销毁而不会触发 destroy 回调
* 运行 main 方法后,JVM 启动,Spring 加载配置文件生成 IOC 容器,从容器获取 bean 对象，然后调方法执行
* main 方法执行完后，JVM 退出，这个时候 IOC 容器中的 bean 还没有来得及销毁就已经结束了，所以没有调用对应的 destroy 方法

关闭容器的方法：
1. 手动关闭：
   ```Java
   ClassPathXmlApplicationContext ctx = new ClassPathXmlApplicationContext("applicationContext.xml");
   ctx.close();
   ```
2. 注册 shutdownHook，在 JVM 退出前自动调用调用 close。
   ```Java
   ctx.registerShutdownHook();
   ```


**有两种方式实现 Bean 初始化和销毁前的 hook**，两者择一即可：
- 配置元数据 init-method 和 destroy-method
- 实现接口 InitializingBean, DisposableBean

#### 配置 bean 元数据
Spring 可以指定 Bean 的初始化和销毁时执行的 Hook 方法：
* init-method：bean 创建之后执行，可以用来初始化需要用到资源
* destroy-method：bean 销毁之前执行，可以用来释放用到的资源

```xml
<bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl" init-method="init" destroy-method="destory"/>
```
这是 BookDaoImpl 类的定义：
```java
public class BookDaoImpl implements BookDao {
    public void save() {
        System.out.println("book dao save ...");
    }
    //表示bean初始化对应的操作
    public void init(){
        System.out.println("init...");
    }
    //表示bean销毁前对应的操作
    public void destory(){
        System.out.println("destory...");
    }
}
```


#### 实现类添加接口

- InitializingBean 提供实例化后的回调
- DisposableBean 提供销毁前的回调
```Java
public interface InitializingBean {
    void afterPropertiesSet() throws Exception;
}
public interface DisposableBean {
    void destroy() throws Exception;
}
```

## 基于注解的开发

### Bean 实例类添加注解

原本 XML 方式定义的 bean 的属性，均可通过注解形式配置在实例类上

#### Bean 的定义@Component

`@Component("bookDao")` 注解定义了一个 Bean 对象
- 注解的默认 Value 属性是 bean.id
```Java
@Component("bookDao")
public class BookDaoImpl implements BookDao {
    public void save() {
        System.out.println("book dao save ..." );
    }
}
```

后续可以用这个 ID 获取对象：
```Java
BookDao bookDao = (BookDao) ctx.getBean("bookDao");
```

**也可以不设置 Value**：
```Java
@Component
public class BookServiceImpl implements BookService{...}
```
后续可以通过类型获取对象：
```Java
BookService bookService = ctx.getBean(BookService.class);
```

等效于：
```xml
<bean id="bookDao" class="com.itheima.dao.impl.BookDaoImpl"/>
```

#### 单例@Scope

Spring 所创建的Bean默认是**单例（singleton）​**的。
这意味着在整个应用程序上下文中，每个通过该 `@Bean` 方法定义的Bean类型只有一个实例存在。

通过指定 Scope 标签，可以让每次请求时都创建一个新的 Bean 实例
**@Scope** 默认值 `singleton`（单例），可选值 `prototype`（非单例，每次请求时都创建一个新的 Bean 实例）
```Java
@Repository
//@Scope设置bean的作用范围，
@Scope("prototype")
public class BookDaoImpl implements BookDao {

    public void save() {
        System.out.println("book dao save ...");
    }
}
```

#### init 和 destroy

导入以下 Jar
```Java
<dependency>
  <groupId>javax.annotation</groupId>
  <artifactId>javax.annotation-api</artifactId>
  <version>1.3.2</version>
</dependency>
```

在相应方法上添加 PostConstruct 和 PreDestroy 注解
```Java
@Repository
public class BookDaoImpl implements BookDao {
    public void save() {
        System.out.println("book dao save ...");
    }
    @PostConstruct //在构造方法之后执行，替换 init-method
    public void init() {
        System.out.println("init ...");
    }
    @PreDestroy //在销毁方法之前执行,替换 destroy-method
    public void destroy() {
        System.out.println("destroy ...");
    }
}
```

#### 自动注入@Autowired
| 名称  | @Autowired                                   |
| --- | -------------------------------------------- |
| 类型  | 属性注解  或  方法注解（了解）  或  方法形参注解（了解）             |
| 位置  | 属性定义上方  或  标准set方法上方  或  类set方法上方  或  方法形参前面 |
| 作用  | 为引用类型属性设置值                                   |
| 属性  | required：true/false，定义该属性是否允许为null           |
* @Autowired可以写在属性上，也可也写在setter方法上，最简单的处理方式是 `写在属性上并将setter方法删除掉`
	* 为什么 setter 方法可以删除呢?
		* 自动装配基于反射设计创建对象并通过暴力反射为私有属性进行设值
		* 普通反射只能获取public修饰的内容
		* 暴力反射除了获取public修饰的内容还可以获取private修改的内容
		* 所以此处无需提供setter方法
```Java
@Service
public class BookServiceImpl implements BookService {
    @Autowired
    private BookDao bookDao;
}
```
 * @Autowired默认按照类型自动装配，如果IOC容器中同类的Bean找到多个，就按照变量名和Bean的名称匹配。因为变量名叫 `bookDao` 而容器中也有一个 `booDao` ，所以可以成功注入。

**手动按名注入**：添加 `@Qualifier(bean-id)` 。注意 @Qualifier 不能独立使用，必须和@Autowired 一起使用
```Java
@Service
public class BookServiceImpl implements BookService {
    @Autowired
    @Qualifier("bookDao1")
    private BookDao bookDao;
}
```
简单类型注入： `@Value(value)`

#### 读取配置文件 @PropertySource

1. resource 下准备 properties 文件
2. 在配置类上添加 `@PropertySource` 注解
```
@Configuration
@ComponentScan("com.itheima")
@PropertySource("jdbc.properties")
public class SpringConfig {}
```
3. 使用@Value 读取配置文件中的内容
```java
@Repository("bookDao")
public class BookDaoImpl implements BookDao {
    @Value("${name}")
    private String name;
    public void save() {
        System.out.println("book dao save ..." + name);
    }
}
```

关于 PropertySource 注解：
* 如果读取的properties配置文件有多个，可以使用 `@PropertySource` 的属性来指定多个
  ```java
  @PropertySource({"jdbc.properties","xxx.properties"})
  ```

* `@PropertySource` 注解属性中不支持使用通配符 `*` ,运行会报错
  ```java
  @PropertySource({"*.properties"})
  ```

* `@PropertySource` 注解属性中可以把 `classpath:` 加上,代表从当前项目的根路径找文件
  ```java
  @PropertySource({"classpath:jdbc.properties"})
  ```

#### 第三方 bean 的配置@Bean

1. 导入对应的 jar 包

```xml
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>druid</artifactId>
    <version>1.1.16</version>
</dependency>
```

2. 在配置类中添加一个方法
- 该方法的返回值就是要创建的 Bean 对象类型
- 方法前添加@Bean 注解

```java
@Configuration
public class SpringConfig {
	@Bean
    public DataSource dataSource(){
        DruidDataSource ds = new DruidDataSource();
        ds.setDriverClassName("com.mysql.jdbc.Driver");
        ds.setUrl("jdbc:mysql://localhost:3306/spring_db");
        ds.setUsername("root");
        ds.setPassword("root");
        return ds;
    }
}
```

3. 至此，可以在 IOC 容器中获取对象

```Java
public class App {
    public static void main(String[] args) {
        AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext(SpringConfig.class);
        DataSource dataSource = ctx.getBean(DataSource.class);
        System.out.println(dataSource);
    }
}
```

#### @Controller、@Service、@Repository

@Controller、@Service、@Repository 均继承自 @Component

| 注解          |     | 用途    | 适用场景                                      |
| ----------- | --- | ----- | ----------------------------------------- |
| @Component  |     | 通用组件  | 任何通用逻辑组件，例如工具类、辅助功能类                      |
| @Controller |     | 控制器   | MVC 中的控制器层，用于处理 HTTP 请求，返回视图或数据           |
| @Service    |     | 业务逻辑  | 业务层，用于封装业务逻辑，协调 Controller 和 Repository 层 |
| @Repository |     | 持久化操作 | DAO 层，封装数据库操作，自动处理持久化异常                   |
- `@Repository` 会启用持久化异常转换。
- 其他注解如 `@Controller` 和 `@Service` 并没有额外的功能，仅是语义化分类。

### 配置类@Configuration


#### 指示 Spring 管理对象：@Bean

| 名称  | @Bean                       |
| --- | --------------------------- |
| 类型  | 方法注解                        |
| 位置  | 方法定义上方                      |
| 作用  | 设置该方法的返回值作为 spring 管理的 bean |
| 属性  | value（默认）：定义 bean 的 id      |

例如：
```Java
public class JdbcConfig {
	@Bean
    public DataSource dataSource(){
        DruidDataSource ds = new DruidDataSource();
        ds.setDriverClassName("com.mysql.jdbc.Driver");
        ds.setUrl("jdbc:mysql://localhost:3306/spring_db");
        ds.setUsername("root");
        ds.setPassword("root");
        return ds;
    }
}
```

#### 启用组件扫描@ComponentScan

- 定义一个 Configuration 类，添加 Configuration 注解和 ComponentScan 注解
- 主程序中载入这个配置类
```Java
//声明当前类为Spring配置类
@Configuration
//设置bean扫描路径，多个路径书写为字符串数组格式
@ComponentScan({"com.itheima.service","com.itheima.dao"})
public class SpringConfig {
}
```
- @ComponentScan 不填 value，则扫描路径为当前类所在路径

**载入配置类**：AnnotationConfigApplicationContext 加载 Spring 配置类初始化 Spring 容器
```Java
ApplicationContext ctx = new AnnotationConfigApplicationContext(SpringConfig.class);
```


**以上方法等效于用 XML 配置**，并在主程序中载入这个配置：
- base-package 指定 Spring 框架扫描的包路径
- 指定包及其子包中的所有类上的注解均会被扫描
```
<context:component-scan base-package="com.itheima"/>
```

```
ApplicationContext ctx = new ClassPathXmlApplicationContext("applicationContext.xml");
```

#### 导入其他配置类：@Import

| 名称 | @Import                                                      |
| ---- | ------------------------------------------------------------ |
| 类型 | 类注解                                                       |
| 位置 | 类定义上方                                                   |
| 作用 | 导入配置类                                                   |
| 属性 | value（默认）：定义导入的配置类类名，<br/>当配置类有多个时使用数组格式一次性导入多个配置类 |
被导入的类不能添加@Configuration 注解

#### 多个配置类

方法 1：基于组件扫描：可以有多个配置类，每个配置类均采用@Configuration 注解标识，只需要这些配置类可以被组件扫描扫描到即可
```java
@Configuration
public class JdbcConfig {
	@Bean
    public DataSource dataSource(){
        DruidDataSource ds = new DruidDataSource();
        ds.setDriverClassName("com.mysql.jdbc.Driver");
        ds.setUrl("jdbc:mysql://localhost:3306/spring_db");
        ds.setUsername("root");
        ds.setPassword("root");
        return ds;
    }
}
```

方法 2：手动 Import，此时可以无需组件扫描
* @Import 参数需要的是一个数组，可以引入多个配置类。
* @Import 注解在配置类中只能写一次，一个配置类不能有两条 Import 语句
```Java
@Configuration
//@ComponentScan("com.itheima.config")
@Import({JdbcConfig.class})
public class SpringConfig {}
```

### 载入配置类

```Java
ApplicationContext ctx = new AnnotationConfigApplicationContext(SpringConfig.class);  
AccountService accountService = ctx.getBean(AccountService.class);
```

### 与第三方库的整合
Spring-DB-MyBatis-JDBC