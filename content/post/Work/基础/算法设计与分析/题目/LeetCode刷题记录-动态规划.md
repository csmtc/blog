---
date: 2025/02/17,周一  16-50-13
lastmod: 2025/03/12,周三  00-14-19
aliases: 
keywords: 
categories: 
tags: 算法与数据结构
published: true
---



这类问题的求解思路是：
- 先尝试有 Cache 的暴力搜索，列出递推式
- 将上述搜索转化为使用 dp 数组的方法


### [70. 爬楼梯](https://leetcode.cn/problems/climbing-stairs/description/)

假设你正在爬楼梯。需要 `n` 阶你才能到达楼顶。
每次你可以爬 `1` 或 `2` 个台阶。你有多少种不同的方法可以爬到楼顶呢？

$$
\begin{cases}
f(n)=f(n-2)+f(n-1)\\
f(<=0)=0,f(1)=1,f(2)=2
\end{cases}
$$

### [746. 使用最小花费爬楼梯](https://leetcode.cn/problems/min-cost-climbing-stairs/)

给你一个整数数组 `cost` ，其中 `cost[i]` 是从楼梯第 `i` 个台阶向上爬需要支付的费用。一旦你支付此费用，即可选择向上爬一个或者两个台阶。
你可以选择从下标为 `0` 或下标为 `1` 的台阶开始爬楼梯。
输入：cost = [10,15,20]
输出：15
解释：你将从下标为 1 的台阶开始。
- 支付 15 ，向上爬两个台阶，到达楼梯顶部。
总花费为 15 。

### [62. 不同路径](https://leetcode.cn/problems/unique-paths/)

一个机器人位于一个 `m x n` 网格的左上角 （起始点在下图中标记为 “Start” ）。
机器人每次只能向下或者向右移动一步。机器人试图达到网格的右下角（在下图中标记为 “Finish” ）。
问总共有多少条不同的路径？

设 $dp[i][j]$ 表示由 (0,0) 走到(i,j)的路径数目
$$
\begin{cases}
dp[i][j]=0,i<=0||j<=0\\
dp[i][j]=dp[i][j-1]+dp[i-1][j]
\end{cases}
$$

### [343. 整数拆分](https://leetcode.cn/problems/integer-break/)

给定一个正整数 `n` ，将其拆分为 `k` 个 **正整数** 的和（ `k >= 2` ），并使这些整数的乘积最大化。
返回 _你可以获得的最大乘积_ 。

-  $dp[i]$ 表示拆解i可得的最大乘积
- 递推时，数 a 可拆解为 b+c 的形式，而 b，c 可以进一步拆分（其最大乘积为 $dp[b]$ ），也可以不拆分
$$
\begin{cases}
dp[2]=1\\
dp[i] =max(&max(i-1,dp[i-1])*1,\\
&...,\\
&max(2,dp[2])*(i-2))
\end{cases}
$$

### [96. 不同的二叉搜索树](https://leetcode.cn/problems/unique-binary-search-trees/)
#mark/leetcode 未做出来

给你一个整数 `n` ，求恰由 `n` 个节点组成且节点值从 `1` 到 `n` 互不相同的 **二叉搜索树** 有多少种？返回满足题意的二叉搜索树的种数。

思路：
- 设 $dp_n$ 为以 n 个结点的二叉搜索树的数目
- 以 n=3 为例， $dp_3$ =以 1 为根的搜索树数目+以 2 为根的搜索树数目+以 3 为根的搜索树数目
- 以 2 为根的搜索树数目=左子树数目×右子树数目= $dp[2-1]*dp[3-2]$

### [198. 打家劫舍](https://leetcode.cn/problems/house-robber/)

你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金，影响你偷窃的唯一制约因素就是相邻的房屋装有相互连通的防盗系统，如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警。
给定一个代表每个房屋存放金额的非负整数数组，计算你不触动警报装置的情况下，一夜之内能够偷窃到的最高金额。

- 设 $f[i]$ 偷窃前 i+1 家获得的最高金额
- 递推式： $f[i]=max(f[i-2]+v[i],f[i-1])$
- 初始条件： $f[0]=v[0],f[1]=max(v[0],v[1])$

### [213. 打家劫舍 II](https://leetcode.cn/problems/house-robber-ii/)

你是一个专业的小偷，计划偷窃沿街的房屋，每间房内都藏有一定的现金。这个地方所有的房屋都**围成一圈**，这意味着第一个房屋和最后一个房屋是紧挨着的。同时，相邻的房屋装有相互连通的防盗系统，如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警。
给定一个代表每个房屋存放金额的非负整数数组，计算你在不触动警报装置的情况下，今晚能够偷窃到的最高金额。

> 输入：nums = [2,3,2]
> 输出：3
> 解释：你不能先偷窃 1 号房屋（金额 = 2），然后偷窃 3 号房屋（金额 = 2）, 因为他们是相邻的。

思路：将环形数组从某处断开，形成一个普通数组。忽略数组的最后一个元素，然后用 198 题同样的思路求解。
遍历所有可能的断开的点，计算最大值
优化：只需考虑从 tail→head 处和 tail-1→tail 处断开的两种情况即可

### [337. 打家劫舍 III](https://leetcode.cn/problems/house-robber-iii/) (树形 DP)

小偷又发现了一个新的可行窃的地区。这个地区只有一个入口，我们称之为 root 。
除了 root 之外，每栋房子有且只有一个“父“房子与之相连。一番侦察之后，聪明的小偷意识到“这个地方的所有房屋的排列类似于一棵二叉树”。如果两个直接相连的房子在同一天晚上被打劫，房屋将自动报警。
给定二叉树的 root 。返回在不触动警报的情况下，小偷能够盗取的最高金额。

树的特点决定了，尽量不要跨 2 层及以上访问子结点，否则有很多判断情况，效率不高

思路：本质和  [198. 打家劫舍](https://leetcode.cn/problems/house-robber/)思路一样，但是这个思路的递推式 $f[j]=max(nums[j]+f[j-2],f[j-1])$ 会跨 2 层访问结点。优化思路是，后根遍历，计算每个树结点存储偷/不偷所能获得的最大金额（2 个数），这样无需跨 2 层访问。
```Python
def rob(self, root: Optional[TreeNode]) -> int:
	def maxAmount(root) -> tuple[int, int]:  # 返回偷，不偷root可以获得的最大金额
	    if root == None:
	        return (0, 0)
	    else:
	        lchild = maxAmount(root.left)
	        rchild = maxAmount(root.right)
	        theftAmount = root.val + lchild[1] + rchild[1]
	        noTheftAmount = max(lchild) + max(rchild) # 可偷可不偷
	
	        return (theftAmount, noTheftAmount)

return max(maxAmount(root))
```


### [5. 最长回文子串 - 力扣（LeetCode）](https://leetcode.cn/problems/longest-palindromic-substring/description/?envType=study-plan-v2&envId=top-100-liked)

给你一个字符串 s，找到 s 中最长的回文子串。

P(i,j) 表示$s[i:j]$是否为回文串。
- P(i,j)为回文串当且仅当 $s[i+1,j-1]$ 为回文串且 $s[i]=s[j]$
- 边界条件为：
	- 长度 1：$s[i,i]=true$
	- 长度 2：$s[i,i+1]=s[i]==s[j]$


### 买卖股票的最佳时机

#### 限制交易数
6.  [121. 买卖股票的最佳时机](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/)
给定一个数组 `prices` ，它的第 `i` 个元素 `prices[i]` 表示一支给定股票第 `i` 天的价格。
你只能选择 **某一天** 买入这只股票，并选择在 **未来的某一个不同的日子** 卖出该股票。设计一个算法来计算你所能获取的最大利润。
返回你可以从这笔交易中获取的最大利润。如果你不能获取任何利润，返回 `0` 。
7.  [122. 买卖股票的最佳时机 II](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-ii/)：可以先购买，然后在 **同一天** 出售。
8.  [123. 买卖股票的最佳时机 III](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-iii/)：最多可以完成 **两笔** 交易。注意：你不能同时参与多笔交易（你必须在再次购买前出售掉之前的股票）。
9. [188. 买卖股票的最佳时机 IV](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-iv/)：最多可以完成 `k` 笔交易。也就是说，你最多可以买 `k` 次，卖 `k` 次。

第 1,2 问可以用贪心做：遍历 prices，记录最低价格，利润=当前价格-最低价格，记录最大利润即可

第 3,4 问只能用动规：状态：不持有股票→持有股票（第 1 次）→不持有股票（第 1 次）→...→持有股票（第 k 次）→不持有股票（第 k 次）
$dp[i,j]$ ：表示第 i 天处于状态 j 可以获得的最大总利润
- 每天有以下 3 种可能的操作
$$
\begin{cases}
\text{买入}:dp[i,j-1]-p_i & j=1,3,5,...\\
\text{卖出}:dp[i,j-1]+p_i & j=2,4,6,...\\
\text{保持原状态}:dp[i-1,j]
\end{cases}
$$
- 因而递推式为
$$
dp[i,j]=\begin{cases}
买:max(dp[i-1,j],dp[i,j-1]-p_i)& j=1,3,5,...\\
卖:max(dp[i-1,j],dp[i,j-1]+p_i)& j=2,4,6,...
\end{cases}
$$
初始状态：dp = -Inf
优化 ：压缩 dp 数组：考虑到 $dp[*,0]\equiv 0$ 因而上述 dp 数组可以去掉第一行

例如允许买入卖出 2 次时，计算最大例如的程序如下
```Python
def maxProfit(self, prices: List[int]) -> int:
	day_cnt, state_cnt = len(prices), 4
	dp = [[0 for _ in range(state_cnt)] for _ in range(day_cnt + 1)]
	dp[0][0] = -prices[0]
	dp[0][2] = dp[0][0]
	for i in range(1, day_cnt + 1):
	    p = prices[i - 1]
	    dp[i][0] = max(dp[i - 1][0], -p)  # 买
	    dp[i][1] = max(dp[i - 1][1], dp[i][0] + p)  # 卖
	    dp[i][2] = max(dp[i - 1][2], dp[i][1] - p)  # 买
	    dp[i][3] = max(dp[i - 1][3], dp[i][2] + p)  # 卖
	    print(f"第{i}天,价格{p},总利润：{dp[i]}")
	return dp[day_cnt][state_cnt - 1]
```

#### 限制交易间隔

[309. 买卖股票的最佳时机含冷冻期](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-with-cooldown/)
给定一个整数数组`prices`，其中第  `prices[i]` 表示第 i 天的股票价格 。​
设计一个算法计算出最大利润。在满足以下约束条件下，你可以尽可能地完成更多的交易（多次买卖一支股票）:
- 卖出股票后，你无法在第二天买入股票 (即冷冻期为 1 天)。
注意：你不能同时参与多笔交易（你必须在再次购买前出售掉之前的股票）。

设第 i 天处于买入状态可以获得的最大利润为 $buy[i]$ ，处于卖出状态可以获得的最大总利润为 $sell[i]$ ,处于冻结状态可以获得的最大总利润为 $frozen[i]$
$$
\begin{cases}
buy[i] = max(buy[i-1],frozen[i-1]-p_i)\\
sell[i] = max(sell[i-1],buy[i]+p_i)\\
frozen[i] = sell[i-1]
\end{cases}
$$
初始条件： $buy[0]=-\infty,sell = 0,frozen=any$
![|332](./assets/LeetCode%E5%88%B7%E9%A2%98%E8%AE%B0%E5%BD%95-%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92/image-2024-07-31_15-46-33-081.png)

#### 含手续费

[714. 买卖股票的最佳时机含手续费](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/)
给定一个整数数组 prices，其中 $prices[i]$ 表示第 i 天的股票价格；整数 fee 代表了交易股票的手续费用。返回获得利润的最大值。
你可以无限次地完成交易，但是你每笔交易都需要付手续费。如果你已经购买了一个股票，在卖出它之前你就不能再继续购买股票了。
注意：这里的一笔交易指买入持有并卖出股票的整个过程，每笔交易你只需要为支付一次手续费。

思路：buy 的时候计算手续费即可
```
def maxProfit(self, prices: List[int], fee: int) -> int:
	n = len(prices) + 1
	buy = [-50000] * n
	sell = [0] * n
	for i in range(1, n):
	    p = prices[i - 1]
	    buy[i] = max(buy[i - 1], sell[i - 1] - p - fee)
	    sell[i] = max(sell[i - 1], buy[i] + p)
	
	return sell[-1]
```

### 子序列问题
#### [300. 最长递增子序列](https://leetcode.cn/problems/longest-increasing-subsequence/)

给你一个整数数组 nums ，找到其中最长严格递增子序列的长度。
子序列是由数组派生而来的序列，删除（或不删除）数组中的元素而不改变其余元素的顺序。例如，[3,6,2,7] 是数组 [0,3,1,6,2,2,7] 的子序列。
设 $dp[i]$ 为以 $nums[i]$ 为最后一个元素的增序列长度：
$$
dp[i]=max(1,max_j\{dp[j]+1|0\leq j<i,n_j<n_i \})
$$
```
def lengthOfLIS(self, nums: List[int]) -> int:
	dp = [1] * (len(nums))
	for i in range(1, len(nums)):
	    dp[i] = max((dp[j] + 1 for j in range(i) if nums[j] < nums[i]), default=1)
	    # print(f"{nums[:i+1]}:{dp[i]}")
	return max(dp)
```

#### [674. 最长连续递增序列](https://leetcode.cn/problems/longest-continuous-increasing-subsequence/)

给定一个未经排序的整数数组，找到最长且连续递增的子序列，并返回该序列的长度。
连续递增的子序列可以由两个下标 l 和 r（l < r）确定，如果对于每个 l <= i < r，都有 $nums[i] < nums[i + 1]$ ，那么子序列 $[nums[l], nums[l + 1], ..., nums[r - 1], nums[r]]$ 就是连续递增子序列。
```
def findLengthOfLCIS(self, nums: List[int]) -> int:
	dp = [1] * len(nums)
	for i in range(1, len(nums)):
	    dp[i] = dp[i - 1] + 1 if nums[i] > nums[i - 1] else 1
	return max(dp)
```

#### [718. 最长重复子数组](https://leetcode.cn/problems/maximum-length-of-repeated-subarray/)

给两个整数数组 A 和 B ，返回两个数组中公共的、长度最长的子数组的长度。

记 $f[i,j]$ 为以 $A_i,B_j$ 结尾的，最长公共子数组长度
$$
f[i,j]=\begin{cases}
f[i-1,j-1]+1&A[i]=B[j]\\
0 &others
\end{cases}
$$
边界条件：
$$
f[-1,*]=f[*,-1]=0
$$
优化空间占用：注意到计算第 i 层时只会用到 i-1 层小于 j 的元素，因而可以压缩 dp 数组成 1 维，从大到小遍历 j 即可。
```Python
def findLength(self, A: List[int], B: List[int]) -> int:
	dp = [0] * (len(B) + 1)
	M = 0
	for i in range(len(A)):
	    for j in range(len(B), 0, -1):
	        if A[i] == B[j - 1]:
	            dp[j] = dp[j - 1] + 1
	            M = max(M, dp[j])
	        else:
	            dp[j] = 0
	return M
```

#### [1143. 最长公共子序列](https://leetcode.cn/problems/longest-common-subsequence/)

给定两个字符串 text1 和 text2，返回这两个字符串的最长公共子序列的长度。如果不存在公共子序列，返回 0 。
一个字符串的 子序列 是指这样一个新的字符串：它是由原字符串在不改变字符的相对顺序的情况下删除某些字符（也可以不删除任何字符）后组成的新字符串。

例如，"ace" 是 "abcde" 的子序列。两个字符串的公共子序列是这两个字符串所共同拥有的子序列。

- 记 $f[i,j]$ 是以 $A[0:i],B[0:j]$ 中最长公共子序列的长度
$$
f[i,j]\begin{cases}
f[i-1,j-1]+1 & A_{i-1}=B_{j-1}\\
max(f[i-1,j],f[i,j-1])&else
\end{cases}
$$
- 边界条件： $f[0,*]=0,f[*,0]=0$
 ```
 def longestCommonSubsequence(self, A: str, B: str) -> int:
	 m, n = len(A) + 1, len(B) + 1
	 dp = [[0] * n for _ in range(m)]
	 for i in range(1, m):
	     for j in range(1, n):
	         if A[i - 1] == B[j - 1]:
	             dp[i][j] = dp[i - 1][j - 1] + 1
	         else:
	             dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
	 return dp[-1][-1]
 ```

## 背包问题
背包问题有多种背包⽅式，常⻅的有：01 背包、完全背包、多重背包、分组背包和混合背包等等。
⼀个商品如果可以重复多次放⼊是完全背包，⽽只能放⼊⼀次是 01 背包
### 01 背包

有 n 件物品和⼀个最多能背重量为 w 的背包。第 i 件物品的重量是 weight[i]，得到的价值是 value[i] 。每件物品**只能放入一次**，求解将哪些物品装⼊背包⾥物品价值总和最⼤。

-  用二维数组 $dp[i][j]$ 表示从下标为 $[0-i]$ 的物品⾥任意取，放进容量为 $j$ 的背包，价值总和的最⼤值。
- **递推公式**： $dp[i,j]=Max(dp[i-1,j],\,dp[i-1,j-W_i]+V_i)$ ，前者是不拿物品 i，后者是拿物品 i
- **初始化**：
	- 背包容量为 0 时，可携带的总价值为 0： $dp_{i,0}=0$
	- $dp_{i,j}$ 依赖于 $dp_{i-1,*}$ ，因而需要初始化 $dp[0,*]$ ： 
		- 背包容量小于 0 号物品大小时： $dp[0,j<W_0]=0$
		- 背包容量大于 0 号物品大小时： $dp[0,j\geq W_0]=V_0$

- **缓存优化**：注意到计算 $dp[I,J]$ 只用到了 $i-1$ 这一行 $j\leq J$ 的数据，因而实际只需要缓存一行的内容。更新时要注意新内容只能覆盖用不到的旧内容。也就是要按照 j 从大到小的顺序更新，这样更新到 $j=J$ 时， $dp[<=J]$ 存储的是第 i-1 行的内容， $dp[>J]$ 存储的是第 i 行的内容，而我们更新 $dp[j=J]$ 只会用到 i-1 行小于 J 的数据，因此覆盖掉 i-1 行大于 J 的数据没有影响。

```C
int maxValue_ver1(int backpackSize, vector<int> itemWeight,
                  vector<int> itemValue) {
  // dp[i][j]的含义：从下标为[0-i]的物品⾥任意取，放进容量为j的背包，价值总和最⼤是多少
  vector<int> dp(backpackSize + 1, 0);
  for (int i = 0; i < itemValue.size(); ++i) {             // 遍历物品
    for (int j = backpackSize; j >= itemWeight[i]; --j) {  // 遍历背包容量
      dp[i] = max(dp[j], dp[j - itemWeight[i]] + itemValue[i]);
    }
  }
  return dp[backpackSize];
}
```

#### [416. 分割等和子集](https://leetcode.cn/problems/partition-equal-subset-sum/)

给你一个 **只包含正整数** 的 **非空** 数组 `nums` 。请你判断是否可以将这个数组分割成两个子集，使得两个子集的元素和相等。

思路 1：每个数只能放到一个子集中，套 01 背包。计算 sum(nums)，检测是否能正好装满容量为(sum/2)的背包

思路 2：记忆化搜索， $f(i,j)$ 表示序列 $[0,i]$ 中是否包含和为 j 的子序列
-  $f(i,j)=f(i-1,j)\,or\,f(i-1,j-nums[i])if\,j>=nums[i]$
- $f(i<0,0)=T,f(i<0,!=0)=F$

#### [1049. 最后一块石头的重量 II](https://leetcode.cn/problems/last-stone-weight-ii/)

有一堆石头，用整数数组 `stones` 表示。其中 `stones[i]` 表示第 `i` 块石头的重量。
每一回合，从中选出**任意两块石头**，然后将它们一起粉碎。假设石头的重量分别为 `x` 和 `y`，且 `x <= y`。那么粉碎的可能结果如下：
- 如果 `x == y`，那么两块石头都会被完全粉碎；
- 如果 `x != y`，那么重量为 `x` 的石头将会完全粉碎，而重量为 `y` 的石头新重量为 `y-x`。
最后，**最多只会剩下一块** 石头。返回此石头 **最小的可能重量** 。如果没有石头剩下，就返回 `0`。

思路：本质是将数组分划为 2 个子集 N1 和 N2，计算 $min(\sum N_1-\sum N_2)$

#### [494. 目标和](https://leetcode.cn/problems/target-sum/)

给你一个非负整数数组 `nums` 和一个整数 `target` 。
向数组中的每个整数前添加 `'+'` 或 `'-'` ，然后串联起所有整数，可以构造一个 **表达式** ：
- 例如，`nums = [2, 1]` ，可以在 `2` 之前添加 `'+'` ，在 `1` 之前添加 `'-'` ，然后串联起来得到表达式 `"+2-1"` 
返回可以通过上述方法构造的、运算结果等于 `target` 的不同 **表达式** 的数目。

**思路 1**：记 $f(i,j)$ 为下标为 0~i 的数（ $N_0\rightarrow N_i$ ）构成的表达式中，和为 j 的个数
$$
f(i,j)=
\begin{cases}
(N_0=j)+(N_0=-j)&i=0\\
f(i-1,j-N_i)+f(i-1,j+N_i)&i>0

\end{cases}
$$
**思路 2**：利用表达式的特征，缩小搜索空间
对 nums 的若干项加负号，得到的新数组 A 中：记正项集合为 P，负项集合为 N。若 sum(P)-sum(N)=target，则意味着找到了一个。
这里 P 和 N 并不是独立的，根据关系联立方程组：
$$
\begin{split}
sum(P)+sum(N)&=target\\
sum(P)-sum(N)&=sum(nums)
\end{split}
$$
解得 $sum(P)=(target+sum(nums))/2$
问题转化为，求使得上述 P 和 nums 的关系成立的集合 P 的组成方式数

设 $f(i,j)$ 为 nums 中下标为 0~i 的数构成的子数组中，和为 j 的个数
- 递推式为：
$$f(i,j)=\begin{cases}
f(i-1,j)+f(i-1,j-N_i) &j\geq N_i\\
f(i-1,j) &j<N_i
\end{cases}
$$
- 初始条件为 i=-1 时
$$
f(0,j)=\begin{cases}
1&j=0\\
0&j\neq0
\end{cases}
$$
- 因为 nums 均为非负整数，其任意子数组和也是非负整数，因此要求target+sum(nums)必须为非负偶数。否则无解，数目为 0

#### [474. 一和零](https://leetcode.cn/problems/ones-and-zeroes/)

给你一个二进制字符串数组 `strs` 和两个整数 `m` 和 `n` 。

请你找出并返回 `strs` 的最大子集的长度，该子集中 **最多** 有 `m` 个 `0` 和 `n` 个 `1` 。
示例 1：
输入：strs = ["10", "0001", "111001", "1", "0"], m = 5, n = 3
输出：4
解释：最多有 5 个 0 和 3 个 1 的最大子集是 {"10","0001","1","0"} ，因此答案是 4 。
其他满足题意但较小的子集包括 {"0001","1"} 和 {"10","1","0"} 。{"111001"} 不满足题意，因为它含 4 个 1 ，大于 n 的值 3 。

- 缓存搜索： $f(i,j,k)$ 0~i 号字符串中使用不超过j个0，k个1所取得的最大子集长度
	- 递推式： 记当前字符串中 0,1 数目为 n0,n1，则 
$$
f(i,j,k)=\begin{cases}
Max(f(i-1,j,k),1+f(i-1,j-n_0,k-n_1)) & j\geq n_0,k\geq n_1\\
f(i-1,j,k) & other
\end{cases}
$$
	- 边界条件： i<=0 时，f=0

- 用 DP 数组处理
```
class Solution:
def findMaxForm(self, strs: List[str], m: int, n: int) -> int:
    cnts = []
    for s in strs:
        rn0 = s.count("0")
        cnts.append((rn0, len(s) - rn0))

    # 初始化DP数组
    dp = [[0 for _ in range(1 + n)] for _ in range(1 + m)]

    for i in range(len(strs)):
        rn0, rn1 = cnts[i]
        for n0 in range(m, rn0 - 1, -1):
            for n1 in range(n, rn1 - 1, -1):
                dp[n0][n1] = max(dp[n0][n1], dp[n0 - rn0][n1 - rn1] + 1)

    return dp[-1][-1]
```

### 完全背包

有 N 件物品和⼀个最多能背重量为 V 的背包。第 i 件物品的重量是 weight[i]，得到的价值是 value[i] 。每件物品都有 ⽆限个（也就是可以放⼊背包多次），求解将哪些物品装⼊背包⾥物品价值总和最⼤。

- $f(i,j)$ 为放入 0~i 类物品且总重量不超过 j 时，物品的总价值
$$
f(i,j)=\begin{cases}
max\{f(i-1,j-kW_i)+kV_i\,|\,0\leq k \leq j//W[i]\} &i>=0\\
0 & i<0
\end{cases}
$$
- 转化为 DP 数组时，只需 j 从小到大遍历即可，这样 $dp[<j]$ 实为 $dp[i][<j]$
```C
int maxValue_ver1(int backpackSize, vector<int> itemWeight,
                  vector<int> itemValue) {
  // dp[i][j]的含义：从下标为[0-i]的物品⾥任意取，放进容量为j的背包，价值总和最⼤是多少
  vector<int> dp(backpackSize + 1, 0);
  for (int i = 0; i < itemValue.size(); ++i) {             // 遍历物品
    for (int j = itemWeight[i]; j <= backpackSize ; ++j) {  // 遍历背包容量
      // 从小到大遍历，允许重复添加物品
      dp[i] = max(dp[j], dp[j - itemWeight[i]] + itemValue[i]);
    }
  }
  return dp[backpackSize];
}
```

#### 遍历顺序对方案数的影响
遍历 DP 数组，计算达到目标解的方案数时：
- **先遍历背包再遍历物品得到排列数**：相当于对每个容量的背包，依次考虑最后装入物品 $x_0,\dots,x_n$ 的情况，物品的不同顺序会被考虑到
- **先遍历物品再遍历背包得到组合数**：相当于每个物品，依次装入不同容量的背包。最终所有背包中物品装入的顺序一定是从 $x_0,\dots,x_n$ ，每种物品组合只会计数一次。

#### 转换为 01 背包

完全背包问题可以转化为 01 背包问题。
完全背包中，背包容量为 V，物品 i 重量 wi，因此相当于物品 i 最多有 n = V//wi 个，也就相当于有 n个的一模一样的物品 i 的选或不选的问题。

优化策略：将 n 表示成二进制形式，例如 7 表示成 $1*2^2+1*2^1+1*2^0$ 。
- 则完全背包转换为 01 背包时，的物品 i 可以转化为以下物品：物品 $i_0$ （重量 $2^0*w_i$ ，价值 $2^0*v_i$ ），物品 $i_1$ （重量 $2^1*w_i$ ，价值 $2^1*v_i$ ）,物品 $i_2$ （重量 $2^2*w_i$ ，价值 $2^2*v_i$ ）

#### [518. 零钱兑换 II](https://leetcode.cn/problems/coin-change-ii/)
#mark/leetcode 
给你一个整数数组 `coins` 表示不同面额的硬币，另给一个整数 `amount` 表示总金额。
请你计算并返回可以凑成总金额的硬币组合数。如果任何硬币组合都无法凑出总金额，返回 `0` 。
假设每一种面额的硬币有无限个。
EG: 输入：amount = 5, coins = [1, 2, 5]
输出：4


**方法**：缓存搜索：设 f(i,j)为用 0~i 种硬币凑出金额 j 的方案数。
- 有两种凑法：
    - 不再继续选第 i 种硬币凑出金额 j
    - 继续选一枚第 i 种硬币凑出金额 $j-coins[i]$
    - 因此 $f(i,j)=f(i-1,j)+f(i,j-c_i)$ 
- 递归边界：f(−1,0)=1, f(−1,>0)=0
- 递归入口：f(n−1,amount)。
等价于需要二维的$f[硬币种类数][金额+1]$缓存状态。

  

- **空间优化**：假设将二维的 $f[m][n]$ 压缩为一维的 $g[n]$ ，对应于 f 中的一行。只需从小到大遍历 j，则当计算 $g[j]=f[i][j]$ 时

$$

\begin{cases}

\forall_{j'<j} & g[j']=f[i][j']\\

\forall_{j'\geq j} & g[j']=f[i-1][j']

\end{cases}

$$

- 因此递推式可以转化为 $g[j]= g[j]+f[j-c_i]$
- 相应的初始条件转换为$g[0]=f(−1,0)=1$,$g[>0]=0$

```
def change(self, amount: int, coins: List[int]) -> int:
f = [0 for _ in range(amount + 1)]
f[0] = 1
for c in coins:
    for j in range(c, amount + 1):
        f[j] = f[j] + f[j - c]

return f[amount]
```

#### [377. 组合总和 Ⅳ](https://leetcode.cn/problems/combination-sum-iv/)

给你一个由 **不同** 整数组成的数组 `nums` ，和一个目标整数 `target` 。请你从 `nums` 中找出并返回总和为 `target` 的元素组合的个数。
请注意，顺序不同的序列被视作不同的组合。

> 例如：输入：nums = [1,2,3], target = 4
> 输出：7
> 所有可能的组合为：(1, 1, 1, 1)(1, 1, 2)(1, 2, 1)(1, 3)(2, 1, 1)(2, 2)(3, 1)

完全背包求排列数：先遍历背包再遍历物品
```
def combinationSum4(self, nums: List[int], target: int) -> int:
	f = [0 for _ in range(target + 1)]
	f[0] = 1
	for j in range(1, target + 1):
	    for n in nums:
	        if j >= n:
	            f[j] += f[j - n]
	return f[target]
```

#### [322. 零钱兑换](https://leetcode.cn/problems/coin-change/)

给你一个整数数组 `coins` ，表示不同面额的硬币；以及一个整数 `amount` ，表示总金额。
计算并返回可以凑成总金额所需的 **最少的硬币个数** 。如果没有任何一种硬币组合能组成总金额，返回 `-1` 。
你可以认为每种硬币的数量是无限的。

思路： $f[i,j]$ 表示使用前 i+1 种硬币凑出 j 的最少硬币个数
- 递推式：有两种凑法：
	- 使用前 i 种硬币： $f[i-1,j]$
	- 使用 i+1 种硬币： $\min_k (f[i,j-kc_i]+k),j\geq kc_i$ 
- 初始条件： $f[-1,0]=0,f[-1,else]=INT\_MAX$ ，个数为 INT_MAX 表示凑不出来

#### [279. 完全平方数](https://leetcode.cn/problems/perfect-squares/)

给你一个整数 n ，返回和为 n 的完全平方数的最少数量。
> 完全平方数 是一个整数，其值等于另一个整数的平方；换句话说，其值等于一个整数自乘的积。例如，1、4、9 和 16 都是完全平方数，而 3 和 11 不是。

思路：
- 变量定义：
	- 设完全平方数的数列为 $nums[100*100,99*99,...,1*1]$
	- 设 $f[i,j]$ 表示用前 i+1 个数构成 j 所需的完全平方数的个数
- 递推式： $f[i,j]=min\{f[i-1,j],min_k (f[i,j-kn_i])\},j\geq kc_i$
- 初始条件 $f[-1,0]=0,f[-1,else]=INT\_MAX$ ，个数为 INT_MAX 表示凑不出来

#### [139. 单词拆分](https://leetcode.cn/problems/word-break/)

给你一个字符串 s 和一个字符串列表 wordDict 作为字典。如果可以利用字典中出现的一个或多个单词拼接出 s 则返回 true。
注意：不要求字典中出现的单词全部都使用，并且字典中的单词可以重复使用。

> 输入: s = "leetcode", wordDict = ["leet", "code"]
> 输出: true
> 解释: 返回 true 因为 "leetcode" 可以由 "leet" 和 "code" 拼接成。

- 变量定义
	- 设 $f[i,j]$ 表示由前 i+1 个单词能否组成字符串 $s[:j]$
- 递推式：
	- $f[i,j]=f[i-1,j]\lor ((f[i,j-1]\land s[j-1] \in dict)\lor\dots\lor (f[i,0]\land s[1:] \in dict))$
	- $f[0,0]=true,f[0,else]=false$

### 多重背包

N 种物品，每种有 Mi 件，放入容量为 V 的背包，问怎么装价值最大。
分解方法：方法是将每种物品拆解为 Mi 种物品，详见完全背包中转换为 01 背包的小节

