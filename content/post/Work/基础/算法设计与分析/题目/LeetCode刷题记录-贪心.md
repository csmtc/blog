---
title: LeetCode刷题记录-贪心
date: 2024-07-25 17:13:03
lastmod: 2024-07-25 17:13:03
aliases: 
keywords: 
categories: 算法与数据结构
tags: []
share: true
---


### [55. 跳跃游戏](https://leetcode.cn/problems/jump-game/description/)
给你一个非负整数数组 `nums` ，你最初位于数组的 **第一个下标** 。数组中的每个元素代表你在该位置可以跳跃的最大长度。
判断你是否能够到达最后一个下标，如果可以，返回 `true` ；否则，返回 `false` 。

核心策略：看覆盖范围，覆盖范围内⼀定是可以跳过来的，不⽤管是怎么跳的。问题就转化为跳跃覆盖范围究竟可不可以覆盖到终点。

### [45. 跳跃游戏 II](https://leetcode.cn/problems/jump-game-ii/description)

给定一个长度为 `n` 的 **0 索引**整数数组 `nums`。初始位置为 `nums[0]`。

每个元素 `nums[i]` 表示从索引 `i` 向前跳转的最大长度。换句话说，如果你在 `nums[i]` 处，你可以跳转到任意 `nums[i + j]` 处:
- `0 <= j <= nums[i]` 
- `i + j < n`

返回到达 `nums[n - 1]` 的最小跳跃次数。生成的测试用例保证可以到达 `nums[n - 1]` 。


核心策略：同样看覆盖范围，当前下标达到了上次跳跃的最大位置，且未达到终点，则需要跳跃一次。
```C++
if (nums.size() == 1)
  return 0;
int max_pos = 0, last_max_pos = 0, cnt = 0, target = nums.size() - 1;

for (int i = 0; i <= target; ++i) {
  // 跳跃的情况：当前下标达到了上次跳跃的最大位置，且未达到终点，则需要跳跃一次
  max_pos = max(max_pos, i + nums[i]);
  if (i == last_max_pos) {
    ++cnt;
    last_max_pos = max_pos;
    if (last_max_pos >= target)
      break;
  }
}
```


### [134. 加油站](https://leetcode.cn/problems/gas-station/)

```
情况⼀：如果 gas 的总和⼩于 cost 总和，那么⽆论从哪⾥出发，⼀定是跑不了⼀圈的
情况⼆：rest[i] = gas[i]-cost[i]为⼀天剩下的油，i 从 0 开始计算累加到最后⼀站，如果累加没有出现负数，说明从 0 出发，油就没有断过，那么 0 就是起点。
情况三：如果累加的最⼩值是负数，汽⻋就要从⾮0 节点出发，从后向前，看哪个节点能把这个负数填平，能把这个负数填平的节点就是出发节点。
```

### [376. 摆动序列](https://leetcode.cn/problems/wiggle-subsequence/)

如果连续数字之间的差严格地在正数和负数之间交替，则数字序列称为摆动序列。第一个差（如果存在的话）可能是正数或负数。仅有一个元素或者含两个不等元素的序列也视作摆动序列。

**思路 1**：统计转折点个数，+1 即为摆动序列个数
```python
def wiggleMaxLength(self, nums: List[int]) -> int:
	# 统计转折点个数即可
	trend = 0  # 大于0增，小于0减
	n = len(nums)
	cnt = 0
	for i in range(1, n):
	    diff = nums[i] - nums[i - 1]
	    if diff > 0 and (cnt == 0 or trend < 0):
	        cnt += 1
	    elif diff < 0 and (cnt == 0 or trend > 0):
	        cnt += 1
	    elif diff == 0:
	        continue
	
	    trend = diff
	return cnt + 1
```

**思路 2**：动态规划
某个序列被称为「上升摆动序列」，当且仅当该序列是摆动序列，且最后一个元素呈上升趋势。如序列 [1,3,2,4] 即为「上升摆动序列」。
某个序列被称为「下降摆动序列」，当且仅当该序列是摆动序列，且最后一个元素呈下降趋势。如序列 [4,2,3,1] 即为「下降摆动序列」。

up[i] 表示以前 i 个元素中的某一个为结尾的最长的「上升摆动序列」的长度。up[i+1]=down[i]+1
down[i] 表示以前 i 个元素中的某一个为结尾的最长的「下降摆动序列」的长度。down[i+1]=up[i]+1

```Java
public int wiggleMaxLength(int[] nums) {
    int down = 1, up = 1;
    for (int i = 1; i < nums.length; i++) {
        if (nums[i] > nums[i - 1])
            up = down + 1;
        else if (nums[i] < nums[i - 1])
            down = up + 1;
    }
    return nums.length == 0 ? 0 : Math.max(down, up);
}
```

## 多维度问题
### [135. 分发糖果](https://leetcode.cn/problems/candy/description/)

其难点就在于贪⼼的策略，如果在考虑局部的时候想两边兼顾，就会顾此失彼。
那么本题我采⽤了两次贪⼼的策略：
- ⼀次是从左到右遍历，只⽐较右边孩⼦评分⽐左边⼤的情况。
- ⼀次是从右到左遍历，只⽐较左边孩⼦评分⽐右边⼤的情况。

### [406. 根据身高重建队列](https://leetcode.cn/problems/queue-reconstruction-by-height/description/)
#mark/leetcode 

假设有打乱顺序的一群人站成一个队列，数组 `people` 表示队列中一些人的属性（不一定按顺序）。每个 `people[i] = [hi, ki]` 表示第 `i` 个人的身高为 `hi` ，前面 **正好** 有 `ki` 个身高大于或等于 `hi` 的人。

目标：排序数组

思路：考虑多维度问题，首先确定一个维度。例如这里先确定身高维度（如身高降序），再考虑位序维度，将人插到合适的位置。

![](./assets/LeetCode%E5%88%B7%E9%A2%98%E8%AE%B0%E5%BD%95-%E8%B4%AA%E5%BF%83/image-2024-07-21_21-41-24-557.png)

### [452. 用最少数量的箭引爆气球](https://leetcode.cn/problems/minimum-number-of-arrows-to-burst-balloons/description/)

给定一些气球在 x 轴的投影范围，垂直 x 轴方向射箭，问击穿所有气球所需的最小箭的数量（若 `x_start ≤ x ≤ x_end` 该气球会被 **引爆**）。

思路：
- 将所有的投影区间按照左端点自小到大排序
- 当前交区间[L,R]，新区间[pL,pR]，两者存在交集的条件就是，R>=pR
- 每多一个没有交集的区间，就要多一根箭


### [435. 无重叠区间](https://leetcode.cn/problems/non-overlapping-intervals/description/)

给定一个区间的集合 `intervals` ，其中 `intervals[i] = [starti, endi]` 。返回需要移除区间的最小数量，使剩余区间互不重叠。

策略：
- 将所有的区间按照左端点自小到大排序
- 当前的并区间(L,R)，新区间(pL,pR)，若存在重叠（即 pL<R）,则需要移除

### [763. 划分字母区间](https://leetcode.cn/problems/partition-labels/description/)

给你一个字符串 `s` 。我们要把这个字符串划分为尽可能多的片段，同一字母最多出现在一个片段中。
注意，划分结果需要满足：将所有划分结果按顺序连接，得到的字符串仍然是 `s` 。
返回一个表示每个字符串片段的长度的列表。
Example:
输入：s = "ababcbacadefegdehijhklij"
输出：[9,7,8]
解释：划分结果为 "ababcbaca"、"defegde"、"hijhklij" 。每个字母最多出现在一个片段中。像 "ababcbacadefegde", "hijhklij" 这样的划分是错误的，因为划分的片段数较少。

策略：
- 统计字符串中每类字母出现的区间，将这些区间分为尽可能多的组，要求组和组之间不重叠
具体做法
- 将这些区间按照左端点递增排序
- 遍历区间，检查该区间和先前的区间是否重叠，若不重叠则意味着一个新的区间段可以执行一次划分
```
[0,8] [1,5] [4,7] / [9,14] [10,15] [11,11] [13,13] / [16,19] [17,22] [18,23] [20,20] [21,21]
```

### [738. 单调递增的数字](https://leetcode.cn/problems/monotone-increasing-digits/description/)
#mark/leetcode 
给定⼀个⾮负整数 N，找出⼩于或等于 N 的最⼤的整数，同时这个整数需要满⾜其各个位数上的数字是单调递增(eg.1234)。
当且仅当每个相邻位数上的数字 x 和 y 满⾜ x <= y 时，我们称这个整数是单调递增的。

例如 98，一旦出现高位>低位的情况，则需要将高位-1，并将高位以后的位均设置为 9，即 9-1,0=89

```C++
int monotoneIncreasingDigits(int n) {
  string strNum = to_string(n);
  // flag⽤来标记赋值9从哪⾥开始
  // 设置为这个默认值，为了防⽌第⼆个for循环在flag没有被赋值的情况下执⾏
  int flag = strNum.size();
  // 自低位向高位
  for (int i = strNum.size() - 1; i > 0; i--) {
    // 高位>低位，需要舍入
    if (strNum[i - 1] > strNum[i]) {
      flag = i;
      strNum[i - 1]--;
    }
  }
  for (int i = flag; i < strNum.size(); i++) {
    strNum[i] = '9';
  }
  return stoi(strNum);
}
```

### [968. 监控二叉树 - 力扣（LeetCode）](https://leetcode.cn/problems/binary-tree-cameras/description/)

给定一个二叉树，我们在树的节点上安装摄像头。
节点上的每个摄影头都可以监视**其父对象、自身及其直接子对象。**
计算监控树的所有节点所需的最小摄像头数量。

思路：从 NULL 结点往上，每隔 2 层安装一个摄像头
![](./assets/LeetCode%E5%88%B7%E9%A2%98%E8%AE%B0%E5%BD%95-%E8%B4%AA%E5%BF%83/image-2024-07-24_18-44-59-416.png)
每个结点有 3 种情况：装了摄像头、被摄像头覆盖、未被摄像头覆盖
- 任何一个孩子没有摄像头都要安装摄像头
- 任何一个孩子有摄像头，则自身被摄像头覆盖
- 两个孩子都被信号覆盖，自身不被覆盖
最后，若根结点没有被覆盖，根结点再装一个摄像头

