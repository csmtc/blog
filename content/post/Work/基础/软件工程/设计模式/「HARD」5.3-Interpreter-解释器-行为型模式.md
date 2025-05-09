---
title: 「HARD」5.3-Interpreter-解释器-行为型模式
date: 2024-03-28 15:49:58
lastmod: 2025-03-12 02:52:22
aliases: 
keywords: 
categories:
  - 设计模式
tags:
  - 
share: true
---




### 目的
给定一个语言，定义它的文法的一种表示，并定义一个解释器，这个解释器使用该表示来解释语言中的句子。

### 示例

考虑解析简单的正则表达式，包含如下文法：
- expression ::= literal | alternation | sequence | repretition |  ' (' expression ')'
- alternation ::= expression '|' expression
- sequence ::= expression '&' expression
- repetition ::= expression '\*'
- literal ::= 'a' | 'b' | 'c'... ( 'a' | 'b' | 'c'...)*

使用类去描述上述文法：
![](./assets/%E3%80%8CHARD%E3%80%8D5.3-Interpreter-%E8%A7%A3%E9%87%8A%E5%99%A8-%E8%A1%8C%E4%B8%BA%E5%9E%8B%E6%A8%A1%E5%BC%8F/image-2023-10-09_15-09-53-908.png)

- 每个用这个文法定义的正则表达式都被表示为一个由这些类的实例构成的抽象语法树 AST
- 如果我们为 RegularExpression 的每一子类都定义解释（Interpret） 操作，那么就得到了这些正则表达式的一个解释器。


### 适用性

当有一个语言需要解释执行，并且你可将该语言中的句子表示为一个抽象语法树时，可使用解释器模式。

最好具备以下特性：
- 文法简单。对于复杂的文法，文法的类层次变得庞大而无法管理。此时语法分析程序生成器这样的工具是更好的选择。它们无须构建抽象语法树即可解释表达式，这样可以节省空间而且还可能节省时间。
- 不太在意效率。最高效的解释器通常不是通过直接解释语法分析树实现的，而是首先将它们转换成另一种形式。例如，正则表达式通常被转换成状态机。但即使在这种情况下，转换器也可用解释器模式实现，该模式仍是有用的。

### 结构

![](./assets/%E3%80%8CHARD%E3%80%8D5.3-Interpreter-%E8%A7%A3%E9%87%8A%E5%99%A8-%E8%A1%8C%E4%B8%BA%E5%9E%8B%E6%A8%A1%E5%BC%8F/image-2023-10-09_15-17-01-856.png)
- AbstractExpression：定义抽象的解释操作
- TerminalExpression：（终结符表达式，如 LiteralExpression）
	- 定义终结符的解释操作
	- **终结符**：指的是文法中的运算单元，也就是不可再分的最小元素。
	- 文法中的每一个终结符都有一个具体终结表达式与之相对应。
- NonterminalExpression（非终结符表达式，如 AlternationExpression、Repetition-Expression、SequenceExpressions）：
	- 文法中的每一条规则 R::=R1 R2…Rn 都需要一个 NonterminalExpression 类
	- 为从 R1 到 Rn 的每个符号都维护一个 AbstractExpression 类型的实例变量。
- Context（上下文）：解释器之外的全局信息
- Client（客户）：构建（或被给定）表示该文法定义的语言中一个特定的句子的抽象语法树。
	- 最后调用解释操作

**工作流程**：Client 构建（或被给定）一个句子，它是 NonterminalExpression 和 TerminalExpression 的实例的一个抽象语法树。然后初始化上下文并调用解释操作。

说明：每一结点的解释操作用上下文来存储和访问解释器的状态。

### 优缺点

- **易于修改、扩展文法**：因为该模式使用类来表示文法规则，你可使用继承来改变或扩展该文法。
	- 已有的表达式可被增量式地改变
	- 新的表达式可定义为旧表达式的变体。
- **易于实现文法**：定义抽象语法树中各个结点的类的实现大体类似。
	- 这些类易于直接编写，通常它们也可用一个编译器或语法分析程序生成器自动生成。
- **复杂的文法难以维护**：
	- 解释器模式为文法中的每一条规则至少定义了一个类，文法过多时难以管理和维护
	- *文法非常复杂时，建议使用语法分析器或者编译器*
- **易于增加解释表达式的方式**：解释器模式使得实现新表达式“计算”变得容易。
	- 例如，你可以在表达式类上定义一个新的操作以支持优美打印或表达式的类型检查。
	- 如果你经常创建新的解释表达式的方式，那么可以考虑使用 Visitor（5.11）模式以避免修改这些代表文法的类。


### 实现

- 创建抽象语法树：解释器模式不涉及语法分析，AST 可以使用表示驱动的语法分析程序生成，也可以直接由用户提供
- 定义解释操作：并不一定要在表达式类中定义解释操作
	- 如果经常要创建一种新的解释器，那么使用 Visitor（5.11）模式将解释放入一个独立的“访问者”对象更好一些
		- 例如，一个程序设计语言会有许多在抽象语法树上的操作，比如类型检查、优化、代码生成，等等。恰当的做法是使用一个访问者以避免在每一个类上都定义这些操作。
- 与 Flyweight 模式共享终结符：一些文法中，一个句子可能多次出现同一个终结符。此时最好共享那个符号的单个拷贝
	- 例如计算机程序的文法，每个程序变量在整个代码中将会出现多次。
	- 为何适用 Flyweight 模式：终结结点通常不存储关于它们在抽象语法树中位置的信息。在解释过程中，任何它们所需要的上下文信息都由父结点传递给它们

### 相关模式
Composite（4.3）：抽象语法树是一个组合模式的实例。 
Flyweight（4.6）：说明了如何在抽象语法树中共享终结符。
Iterator（5.4）：解释器可用一个迭代器遍历该结构。
Visitor（5.11）：可用来在一个类中维护抽象语法树中各结点的行为。