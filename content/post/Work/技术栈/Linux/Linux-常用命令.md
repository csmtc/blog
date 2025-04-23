---
title: Linux
date: 2024-12-18 17:35:27
lastmod: 2025-04-23 16:22:33
aliases: 
keywords: 
categories:
  - Linux
tags:
  - Linux
share: true
---



## 一、基础知识
### Linux 系统的文件结构

```
/bin        二进制文件，系统常规命令
/boot       系统启动分区，系统启动时读取的文件
/dev        设备文件
/etc        大多数配置文件
/home       普通用户的家目录
/lib        32位函数库
/lib64      64位库
/media      手动临时挂载点
/mnt        手动临时挂载点
/opt        第三方软件安装位置。用户级的程序目录，可以理解为 D:/Sof                                ware ，opt有可选的意思，这里可以用于放置第三方大型软件（或游戏），当你不需要时，直接rm -rf掉即可
/proc       进程信息及硬件信息
/root       系统管理员，也称作超级权限者的用户主目录。
/sbin       s即Super User，sbin 存放系统管理员使用的系统管理程序。
/srv        一些服务启动之后需要提取的数据
/var        var 是 variable(变量) 的缩写，习惯将那些经常被修改的目录放在这个目录下。包括各种日志文件。
/sys        内核相关信息
/tmp        临时文件
/run        临时文件系统，存储系统启动以来的信息。当系统重启时，这个目录下的文件应该被清除。
            如果你的系统上有 /var/run 目录，应该让它指向 run。
/usr        用户相关设定
/usr/bin    系统用户使用的应用程序。
/usr/sbin   超级用户使用的比较高级的管理程序和系统守护程序。
/usr/src    内核源代码默认的放置目录。
/usr/local ：用户级的程序目录，可以理解为 C:/Progrem Files/ 。 用户自己编译的软件默认会安装到这个目录下。
```
### Shell 基础
#### Shell 快捷键
```
ctrl+a： 将光标跳到行首

ctrl+e : 将光标跳到行尾

ctrl+k : 删除从光标到行尾的部分（还有剪切功能）

ctrl+u : 删除从光标到行首的部分（还有剪切功能）

ctrl+d： 删除从光标到当前单词结尾的部分

ctrl+w： 删除从光标到当前单词开头的部分

ctrl+y：粘贴使用 ctrl+w，ctrl+u 和 ctrl+k 快捷键擦除的文本。如果你删除了错误的文本或需要在某处使用已擦除的文本，这将派上用场。

ctrl+r：使用该快捷键来搜索历史命令

ctrl + l：清屏

先单击 Esc 键，然后再按 b 键： 往回(左)移动一个单词，backward
先单击 Esc 键，然后再按 f 键： 往后(右)移动一个单词，forward
```

#### shell 标头的含义
```
示例：root@app00:~# 
root    //用户名，root 为超级用户
@       //分隔符
app00   //主机名称
~       //当前所在目录，默认用户目录为~
##      //表示当前用户是超级用户，普通用户为 $
```

#### Shell 输入/输出重定向

- n > file	将文件描述符为 n 的文件重定向到 file。
- n >> file	将文件描述符为 n 的文件以追加的方式重定向到 file。
- n >& m	将输出文件 m 和 n 合并。
- n <& m	将输入文件 m 和 n 合并。
- << tag	将开始标记 tag 和结束标记 tag 之间的内容作为输入。

程序输出重定向
- command > file	将输出重定向到 file。
- command < file	将输入重定向到 file。
- command >> file	将输出以追加的方式重定向到 file。

一般情况下，每个 Unix/Linux 命令运行时都会打开三个文件：
- 标准输入文件(stdin)：stdin 的文件描述符为 0，Unix 程序默认从 stdin 读取数据。
- 标准输出文件(stdout)：stdout 的文件描述符为 1，Unix 程序默认向 stdout 输出数据。
- 标准错误文件(stderr)：stderr 的文件描述符为 2，Unix 程序会向 stderr 流中写入错误信息。
将 stdout 和 stderr 合并后重定向到 file
```
$ command > file 2>&1
# or
$ command >> file 2>&1
```

#### 多条命令连续执行

顺序执行
使用`&&`或`||`或`;`（根据需要选择连接符号）等来连接多条命令
`&&`："与"，一条命令执行出错，则后面命令不执行
`||`："或"，一条命令执行成功，则后面命令不执行
`;` ：无论执行成功与否，一路执行下去

异步执行：`&`
Default 模式下，shell 命令是阻塞执行的，可以通过其后添加&让这条命令异步执行，例如：
```
command &  # 将你的命令替换为"command"
echo $!    # 打印上一条指令的pid
```

#### 将命令 a 的输出作为命令 b 的输入
1. $() ：括起来的字符串被 shell 解释为命令行，在执行时，shell 首先执行该命令行，并以它的标准输出结果取代整个部分
2. 符号：反引号，反引号括起来的字符串被 shell 解释为命令行，效果同上
3. xarg：xargs 是给命令传递参数的一个过滤器，也是组合多个命令的一个工具。它把一个数据流分割为一些足够小的块，以方便过滤器和命令进行处理。通常情况下，xargs 从管道或者 stdin 中读取数据，但是它也能够从文件的输出中读取数据。xargs 的默认命令是 echo，这意味着通过管道传递给 xargs 的输入将会包含换行和空白，不过通过 xargs 的处理，换行和空白将被空格取代。
	- xargs 优点：由于是批处理的，所以执行效率比较高（通过缓冲方式）
	- xargs 缺点：有可能由于参数数量过多（成千上万），导致后面的命令执行失败
```sh
rm -f $(find . -name fname)
rm -f `find . -name fname`
find . -name fname | xargs rm -f
```

#### 后台执行


使用 `nohup` 可以让任务在终端关闭后继续运行。

```
nohup command &
```

输出会保存到 `nohup.out` 文件。


### 系统启动过程

启动过程可以分为 5 个阶段：内核引导→ 运行 init 启动进程→ 系统初始化→ 建立终端→ 用户登录系统
![](./assets/Linux-%E5%B8%B8%E7%94%A8%E5%91%BD%E4%BB%A4/image-2024-03-02_09-53-21-969.png)
- init 进程：许多程序需要开机启动。它们在 Windows 叫做"服务"（service），在 Linux 就叫做"守护进程"（daemon），init 进程的一大任务，就是去运行这些开机启动的程序。
- 运行级别：Linux 允许为不同的场合，分配不同的开机启动程序，这就叫做"运行级别"（runlevel）。也就是说，启动时根据"运行级别"，确定要运行哪些程序。
- 系统初始化：依次执行
	- /etc/rc*.d：每一个运行级别都要首先运行的，激活交换分区，检查磁盘，加载硬件模块等要优先执行的任务
	  实际上都是一些连接文件，真正的 rc 启动脚本实际上都是放在/etc/rc.d/init.d/目录下
	- systemd

## 二、基础操作

### 常用快捷键

1、tab //命令或路径等的补全键，linux 用的最多的一个快捷键 ⭐️
2、**ctrl+a //光标迅速回到行首 ⭐️**
3、**ctrl+e //光标迅速回到行尾 ⭐️**
4、ctrl+f //光标向右移动一个字符
5、ctrl+b //光标向左移动一个字符
6、**ctrl+insert //复制命令行内容（mac 系统不能使用）**
7、**shift+insert //粘贴命令行内容（mac 系统不能使用）**
8、**ctrl+k //剪切（删除）光标处到行尾的所有字符 ⭐️**
9、**ctrl+u //剪切（删除）光标处到行首的所有字符 ⭐️**
10、ctrl+w //剪切（删除）光标前的一个字符
11、ctrl+y //粘贴 ctrl+k、ctrl+u、ctrl+w 删除的字符 ⭐️
12、ctrl+c //中断终端正在执行的任务并开启一个新的一行 ⭐️
13、ctrl+h //删除光标前的一个字符（相当于退格键）
14、ctrl+d //退出当前 shell 命令行，如果是切换过来的用户，则执行这个命令回退到原用户 ⭐️
15、ctrl+r //搜索命令行使用过的历史命令记录 ⭐️
16、ctrl+g //从 ctrl+r 的搜索历史命令模式中退出
17、ctrl+l //清楚屏幕所有的内容，并开启一个新的一行 ⭐️
18、**ctrl+s //锁定终端，停留在当前屏**
19、**ctrl+q // 恢复刷屏**
20、ctrl+z //暂停在终端运行的任务,使用"fg"命令可以使暂停恢复 ⭐️
21、**!! //执行上一条命令** ⭐️
22、!pw //这是一个例子，是执行以 pw 开头的命令，这里的 pw 可以换成任何已经执行过的字符 ⭐️
23、!pw:p //这是一个例子，是仅打印以 pw 开头的命令，但不执行，最后的那个“p”是命令固定字符 ⭐️
24、!num //执行历史命令列表的第 num 条命令，num 代指任何数字（前提是历史命令里必须存在）⭐️
25、!$ //代指上一条命令的最后一个参数，该命令常用于 shell 脚本中 ⭐️
26、esc+. //注意那个".“ 意思是获取上一条命令的(以空格为分隔符)最后的部分 ⭐️
27、esc+b //移动到当前单词的开头
28、esc+f //移动到当前单词的结尾

### 重启系统
```
(1)立刻关机  
  shutdown -h now 或者 poweroff  
(2)两分钟后关机  
  shutdown -h 2
```
  
### 关闭系统
```
(1)立刻重启  
  shutdown -r now 或者 reboot  
(2)两分钟后重启  
  shutdown -r 2  
```

### 帮助命令（help）
```
ifconfig  --help     //查看 ifconfig 命令的用法  
```

### 命令说明书（man）
```
man shutdown         //打开命令说明后，可按"q"键退出 
``` 

### 切换用户（su）
```
su yao               //切换为用户"yao",输入后回车需要输入该用户的密码  
exit                 //退出当前用户  
sudo su              //切换为root用户
```

### Sudo

  sudo 命令以系统管理者的身份执行指令，也就是说，经由 sudo 所执行的指令就好像是 root 亲自执行。需要输入自己账户密码。  
  使用权限：在 /etc/sudoers 中有出现的使用者
```
sudo -l                              //列出目前的权限
sudo -u yao vi ~www/index.html    //以 yao 用户身份编辑  home 目录下 www 目录中的 index.html 文件
```

### Grep 查找字符串
查找文件里符合条件的字符串或正则表达式
```
grep [options] pattern [files]
```
- 选项：
	- `-o`（只输出匹配的部分）
	 - `-v` ：反向匹配，显示不包含匹配模式的行。如 `grep -v "world" file.txt` 会显示文件中所有不包含 `world` 的行。
	- `-i`：忽略大小写。如`grep -i "hello" file.txt`会搜索文件中所有包含`hello`、`Hello`、`HELLO`等的行。
	- `-n`：显示匹配行的行号。如`grep -n "apple" file.txt`会在显示匹配行的同时，显示行号。
	- `-c`：只显示匹配的行数。如`grep -c "cat" file.txt`会返回文件中包含`cat`的行数。
	- `-r`：递归搜索目录下的所有文件。如`grep -r "python" /path/to/directory`会在指定目录及其子目录下的所有文件中搜索包含`python`的行。
```
grep -i "the" demo_file              //在文件中查找字符串(不区分大小写)
grep -A 3 -i "example" demo_text     //输出成功匹配的行，以及该行之后的三行
grep -r "ramesh" *                   //在一个文件夹中递归查询包含指定字符串的文件
```
在标准输入中查找字符串 "world"，并只打印匹配的行数：
```
echo "hello world" | grep -c world
```
## 三、目录操作

| 命令          | 作用           | 对应英文                 |
|-------------|--------------|----------------------|
| ls          | 查看当前文件夹下的内容  | list                 |
| pwd         | 查看当前所在的文件夹   | print wrok directory |
| cd [目录名]    | 进入文件夹        | change directory     |
| touch [文件名] | 如果文件不存在，新建文件 | touch                |
| mkdir [目录名] | 创建目录         | make directory       |
| rm [文件名]    | 删除指定的文件或目录   | remove               |
| clear       | 清空终端屏        | clear                |

### 切换目录（cd）
```
  cd /                 //切换到根目录  
  cd /bin              //切换到根目录下的 bin 目录  
  cd ../               //切换到上一级目录或者使用命令：cd ..  
  cd ~                 //切换到 home 目录  
  cd -                 //切换到上次访问的目录  
  cd xx(文件夹名)       //切换到本目录下的名为 xx 的文件目录，如果目录不存在报错  
  cd /xxx/xx/x         //可以输入完整的路径，直接切换到目标目录，输入过程中可以使用 tab 键快速补全  
```

### 查看目录（ls）
```
  ls                   //查看当前目录下的所有目录和文件  
  ls -a                //查看当前目录下的所有目录和文件（包括隐藏的文件）  
  ls -l                //列表查看当前目录下的所有目录和文件（列表查看，显示更多信息），与命令"ll"效果一样  
  ls /bin              //查看指定目录下的所有目录和文件 
``` 
- 可以传递多个目录，并让它们一个接一个地列出。

可选参数：
- -l 选项以长格式显示文件和目录的详细信息，包括权限、所有者、组、大小和修改日期。
- -a 选项显示所有目录和文件，包括隐藏文件和目录。
- -t 选项按修改时间排序文件和目录，最近修改的排在前面。
- -r 选项反转默认的排序顺序。
- -S 选项按大小排序文件和目录，最大的排在前面。
- -R 选项递归地列出文件和目录，包括子目录。
- -i 选项显示每个文件和目录的索引号（inode）。
- -g 选项显示文件和目录的组所有权，而不是所有者。
- -h 选项以人类可读的格式打印**文件大小**（例如，1K, 234M, 2G）。
- -d 选项只列出目录本身，而不是它们的内容。

- 列出所有文件：`find . -maxdepth 1 -type f` 在当前目录（.）中查找最大深度为1（-maxdepth 1）的类型为文件（-type f）的内容

### 创建目录（mkdir）
  ```
mkdir tools          //在当前目录下创建一个名为 tools 的目录  
mkdir /bin/tools     //在指定目录下创建一个名为 tools 的目录 
mkdir -p /bin/tools  //递归创建目录，no error if existing
```

### 删除目录与文件（rm）
```
rm 文件名              //删除当前目录下的文件  
rm -f 文件名           //删除文件，不询问
rm -i 文件名           // -i：和 -f 正好相反，在删除文件或目录之前，系统会给出提示信息
rm -r 文件夹名         //递归删除当前目录下此名的目录  
rm -rf 文件夹名        //递归删除当前目录下此名的目录（不询问）  
rm -rf *              //将当前目录下的所有目录和文件全部删除  
rm -rf /*             //将根目录下的所有文件全部删除【慎用！相当于格式化系统】  
```

### 移动目录（mv）
```
mv 当前目录名新目录名          //修改目录名，同样适用与文件操作  
mv /usr/tmp/tool /opt       //将/usr/tmp 目录下的 tool 目录剪切到 /opt 目录下面  
mv -r /usr/tmp/tool /opt    //递归剪切目录中所有文件和文件夹  
```

### 拷贝目录（cp）
```
cp /usr/tmp/tool /opt       //将/usr/tmp 目录下的 tool 目录复制到 /opt 目录下面  
cp -r /usr/tmp/tool /opt    //递归剪复制目录中所有文件和文件夹  
```

### 搜索目录（find）
```
find /bin -name 'a*'        //查找/bin 目录下的所有以 a 开头的文件或者目录  
```

### 查看当前目录（pwd）
```
pwd                         //显示当前位置路径  
```

## 四、文件操作

### Find
```
find . -name "*.c"     //将目前目录及其子目录下所有延伸档名是 c 的文件列出来
find . -type f         //将目前目录其其下子目录中所有一般文件列出
find . -ctime -20      //将目前目录及其子目录下所有最近 20 天内更新过的文件列出
find /var/log -type f -mtime +7 -ok rm {} \;     //查找/var/log 目录中更改时间在7日以前的普通文件，并在删除之前询问它们
find . -type f -perm 644 -exec ls -l {} \;       //查找前目录中文件属主具有读、写权限，并且文件所属组的用户和其他用户具有读权限的文件
find / -type f -size 0 -exec ls -l {} \;         //为了查找系统中所有文件长度为0的普通文件，并列出它们的完整路径
```

### Whereis
```
whereis ls             //将和 ls 文件相关的文件都查找出来
```

### Which
which 指令会在环境变量$PATH 设置的目录里查找符合条件的文件。
```
which bash             //查看指令"bash"的绝对路径
```

### 新增文件（touch）
   touch  a.txt         //在当前目录下创建名为 a 的 txt 文件（文件不存在），如果文件存在，将文件时间属性修改为当前系统时间  

### 删除文件（rm）
  rm 文件名              //删除当前目录下的文件  
  rm -f 文件名           //删除当前目录的的文件（不询问）  

#### 创建软链接

创建文件的软链接（类似快捷方式）
```
sudo ln -s /path/to/fname.ext /path/to/dst/
# or
sudo ln -s /path/to/fname.ext /path/to/dst/fname.ext
```

### 编辑文件（vi、vim）
vi 文件名 ：打开需要编辑的文件  
进入后，操作界面有三种模式：命令模式（command mode）、插入模式（Insert mode）和底行模式（last line mode）  
- **命令模式**  ：刚进入文件就是命令模式，通过方向键控制光标位置
	- 使用命令"dd"删除当前整行  
	- 按"o"在光标所在行的下面另起一新行插入  
	- 按"a"在光标所在字符后开始插入  
	- 按"i"在光标所在字符前开始插入  
	- 使用命令"/字段"进行查找  
	- 按":"进入底行模式  
- **插入模式**  ：此时可以对文件内容进行编辑，左下角会显示 "-- 插入 --""  
	- 按"ESC"进入底行模式  
- **底行模式**  
	- 退出编辑：      :q  
	- 强制退出：      :q!  
	- 保存并退出：    :wq

**操作步骤示例**  
1.保存文件：按"ESC" -> 输入":" -> 输入"wq",回车     //保存并退出编辑  
2.取消操作：按"ESC" -> 输入":" -> 输入"q!",回车     //撤销本次修改并退出编辑

**Tisp**：  
```
vim +10 filename.txt                   //打开文件并跳到第10行  
vim -R /etc/passwd                     //以只读模式打开文件
```

### 查看文件
```
cat a.txt          //查看文件最后一屏内容
less a.txt         //PgUp 向上翻页，PgDn 向下翻页，"q"退出查看
more a.txt         //显示百分比，回车查看下一行，空格查看下一页，"q"退出查看
tail -100 a.txt    //查看文件的后100行，"Ctrl+C"退出查看
```
可以指定 -f 选项，持续刷新文件内容

### 查看文件大小

```
size filename
```

### 查看目录大小
查看当前目录下，所有一级子目录的大小
```
du -h --max-depth=1
```
-h：以易于人类阅读的单位打印大小

## 五、文件存储

### 文件所有者

更换目录所有者：其中 new_group 可以省略，只保留冒号
```
sudo chown new_owner:new_group /path/to/directory
```

递归更换：
```
sudo chown -R new_owner:new_group /path/to/directory
```


### 文件权限

Linux 文件模式由 10 个字符构成，第一位表示文件类型，后 9 位每 3 位一组，分别表示所有者、群组、其他用户的权限
- 常见的文件类型：-：普通文件，d：目录，l：符号链接

**文件类型**：UNIX 文件模式的第一个字符表示文件的类型。以下是一些常见的文件类型：
**权限位**：UNIX 文件模式的其余九个字符表示文件的权限。这些字符分为三组，每组三个字符：
- 所有者权限：表示文件所有者对文件的权限。
- 群组权限：表示文件所属群组的成员对文件的权限。
- 其他用户权限：表示其他用户（不是文件所有者或群组成员）对文件的权限。
每组权限字符包括以下三个选项：
- r：读取权限
- w：写入权限
- x：执行权限
> 例如，rw-r--r-- 表示：文件所有者具有读取和写入权限。群组成员只有读取权限。其他用户也只有读取权限。

**数字表示法**：除了字符表示法外，UNIX 文件模式还可以使用数字表示法。每个权限位都对应一个 3 位二进制数：
- r：4
- w：2
- x：1
> 因此，rw-r--r-- 可以用数字表示为 644。
```
文件权限信息示例：-rwxrw-r--
  -第一位：'-'就代表是文件，'d'代表是文件夹
  -第一组三位：拥有者的权限
  -第二组三位：拥有者所在的组，组员的权限
  -第三组三位：代表的是其他用户的权限
```

```
普通授权    chmod +x a.txt    
8421法     chmod 777 a.txt     //1+2+4=7，"7"说明授予所有权限
```
### 检视文件系统 

df -h：显示已挂载的文件系统

### 格式化磁盘

```
mkfs # 查看系统支持哪些格式化类型
mkfs.ext4 /dev/sda1 # 将sda1格式化为ext4格式
```

### Mount 挂载磁盘

#### 检视磁盘
lsblk：列出系统上的所有磁盘列表
blkid：查看文件系统类型
```
sudo blkid /dev/sda1
```

#### 手动挂载
查看已挂载的磁盘
```
df -kh
```
挂载磁盘
```
mount -t ntfs /dev/sda1 /home/disk #/dev/sda1需替换为自己的硬盘名
```
- `-t` 参数指定文件系统类型，可以设置为 auto 自动检测
取消挂载
```
umount /dev/sda1
```

**开机自动挂载**
```
 进入 fstab 修改配置
vim /etc/fstab
 在最后面加入指定信息 fdisk -l 查看
UUID=eeda1671-709a-4a7b-a19b-1b275643e825 /vdb1 ntfs defaults 0 1 # 挂载硬盘
```

9A2E98B82E988EBF   # WD
FCD0C88AD0C84C98 # HARD

#### fstab
/etc/fstab 文件包含了如下字段，通过空格或 Tab 分隔
- options：
	- auto - 在启动时或键入了 mount -a 命令时自动挂载。noauto - 只在你的命令下被挂载。
	- rw - 以读写模式挂载文件系统。ro - 以只读模式挂载文件系统。
	- async - I/O 异步进行。sync - I/O 同步进行。
	- defaults - 使用文件系统的默认挂载参数，例如 ext4 的默认参数为:rw, suid, dev, exec, auto, nouser, async
	- users - 允许所有 users 组中的用户挂载文件系统.若无显示定义，隐含启用 noexec, nosuid, nodev 参数。
- dump：dump 工具通过它决定何时作备份. dump 会检查其内容，并用数字来决定是否对这个文件系统进行备份。允许的数字是 0 和 1 。0 表示忽略， 1 则进行备份。
- pass：fsck 读取 pass 的数值来决定需要检查的文件系统的检查顺序。允许的数字是 0, 1, 和 2。根目录应当获得最高的优先权 1, 其它所有需要被检查的设备设置为 2. 0 表示设备不会被 fsck 所检查。

|         | file system                                   | dir    | type   | options  | dump                   | pass      |
| ------- | --------------------------------------------- | ------ | ------ | -------- | ---------------------- | --------- |
| 说明      | 要挂载的分区设备号                                     | 挂载位置   | 文件系统类型 | 挂载选项     | 是否用 dump 备份<br>可选值 0,1 | fsck 检查顺序 |
| Example | UUID=e943fbb7-020a-<br>4c64-a48a-2597eb2496df | /vdb1  | ext4   | defaults | 0                      | 0         |
| Example | https://atcra.top/dav                         | /alist | davfs  | defaults | 0                      | 0         |
修改完后刷新 Fstab
```
mount -a
```

#### 挂载 Webdav
!Linux-文件共享-SMB-Webdav

## 用户管理

!Linux-用户管理-用户组

## 六、打包与解压
### 说明
```
.zip、.rar        //windows 系统中压缩文件的扩展名
.tar              //Linux 中打包文件的扩展名
.gz               //Linux 中压缩文件的扩展名
.tar.gz           //Linux 中打包并压缩文件的扩展名
```

**必选参数**：这五个是独立的命令，压缩解压都要用到其中一个，可以和别的命令连用但只能用其中一个。
-c: 建立压缩档案
-x：解压
-t：查看内容
-r：向压缩归档文件末尾追加文件
-u：更新原压缩包中的文件

**可选参数**：
-z：有 gzip 属性的
-j：有 bz2 属性的
-Z：有 compress 属性的
-v：显示所有过程
-O：将文件解开到标准输出

### 打包文件
##### zip

```
查看文件内容
zip -l archive_name.zip
```

```
# 打包文件
zip archive_name.zip file1.txt file2.txt file3.txt 
# 打包整个目录
zip -r archive_name.zip directory_name
# 使用 `-x` 选项来排除不需要打包的文件或目录
zip -r archive_name.zip my_folder -x "*.log" "*.tmp"
# 将新的文件或修改过的文件添加到已有的 zip 文件中
zip -u archive_name.zip new_file.txt
# 使用 `-e` 选项设置密码
zip -re archive_name.zip my_folder
```
##### tar
```
tar -zcvf file1,file2
  ```
**参数说明**：
- z：调用 gzip 压缩命令进行压缩; 
- c：打包文件; 
- x：解压文件
- v：显示运行过程; 
- f：指定文件名;

示例：
>tar -zcvf a.tar file1 file2,...      //多个文件压缩打包

##### ar
Linux ar 命令用于建立或修改备存文件，或是从备存文件中抽取文件。
ar 可让您集合许多文件，成为单一的备存文件。在备存文件中，所有成员文件皆保有原来的属性与权限。

```
ar[-dmpqrtx][cfosSuvV][a<成员文件>][b<成员文件>][i<成员文件>][备存文件][成员文件]
```

必要参数：
- -d 　删除备存文件中的成员文件。
- -m 　变更成员文件在备存文件中的次序。
- -p 　显示备存文件中的成员文件内容。
- -q 　将文件附加在备存文件末端。
- -r 　将文件插入备存文件中。
- -t 　显示备存文件中所包含的文件。
- -x 　自备存文件中取出成员文件。
可选参数：
- c 　建立备存文件。
- f 　为避免过长的文件名不兼容于其他系统的 ar 指令指令，因此可利用此参数，截掉要放入备存文件中过长的成员文件名称。
- o 　保留备存文件中文件的日期。
- s 　若备存文件中包含了对象模式，可利用此参数建立备存文件的符号表。
- u 　只将日期较新文件插入备存文件中。
- a<成员文件> 　将文件插入备存文件中指定的成员文件之后。
- b<成员文件> 　将文件插入备存文件中指定的成员文件之前。
- i<成员文件> 　将文件插入备存文件中指定的成员文件之前。

### 解压文件

```
tar -zxvf a.tar                      //解包tar.gz至当前目录
tar -zxvf a.tar -C /usr/...       //指定解压tar.gz的位置
unzip test.zip             //解压*.zip 文件 
unzip -l test.zip          //查看*.zip 文件的内容 
gzip file.gz             // 解压纯gz文件
```


## 七、系统管理
### 防火墙操作
```
service iptables status      //查看 iptables 服务的状态
service iptables start       //开启 iptables 服务
service iptables stop        //停止 iptables 服务
service iptables restart     //重启 iptables 服务
chkconfig iptables off       //关闭 iptables 服务的开机自启动
chkconfig iptables on        //开启 iptables 服务的开机自启动
###centos7 防火墙操作
systemctl status firewalld.service     //查看防火墙状态
systemctl stop firewalld.service       //关闭运行的防火墙
systemctl disable firewalld.service    //永久禁止防火墙服务
```

### 修改主机名（CentOS 7）
hostnamectl set-hostname 主机名

### 快速清屏
  ctrl+l        //清屏，往上翻可以查看历史操作  

### 远程主机
  ssh IP       //远程主机，需要输入用户名和密码

#### 设置用户密码

```
passwd [选项] [用户名]
```
选项：
- 不加选项：设置用户密码
- -S  显示密码信息 


## 网络操作
### 查看网络
ifconfig  

### 查看连接和端口占用
使用 netstat 命令可以列出系统上的网络连接、路由表和网络接口等信息。
常用参数如下：
```
-a, --all                display all sockets (default: connected)
-n, --numeric            don't resolve names
-o, --timers             display timers
-p, --programs           display PID/Program name for sockets
```

```sh
netstat -an    //查看当前系统端口  
netstat -an | grep 8080     //查看指定端口  
netstat -tulpn | grep <端口号>

ping IP        //查看与此 IP 地址的连接情况  
```
### 配置映射
  修改文件： vi /etc/hosts  
  在文件最后添加映射地址，示例如下：  
   192.168.1.101  node1  
   192.168.1.102  node2  
   192.168.1.103  node3  
  配置好以后保存退出，输入命令：ping node1 ，可见实际 ping 的是 192.168.1.101。  

### 修改 IP
```
修改网络配置文件，文件地址：/etc/sysconfig/network-scripts/ifcfg-eth0
  ------------------------------------------------
  主要修改以下配置：  
  TYPE=Ethernet               //网络类型
  BOOTPROTO=static            //静态 IP
  DEVICE=ens00                //网卡名
  IPADDR=192.168.1.100        //设置的 IP
  NETMASK=255.255.25      //子网掩码
  GATEWAY=192.168.        //网关
  DNS1=192.168.           //DNS
  DNS2=8.8.               //备用 DNS
  ONBOOT=yes                  //系统启动时启动此设置
  -------------------------------------------------
修改保存以后使用命令重启网卡：service network restart  
```

### wget 
  说明：使用 wget 从网上下载软件、音乐、视频 
```
示例：wget <http://prdownloads.sourceforge.net/sourceforge/nagios/nagios-3.2.1.tar.gz>
//下载文件并以指定的文件名保存文件
wget -O nagios.tar.gz <http://prdownloads.sourceforge.net/sourceforge/nagios/nagios-3.2.1.tar.gz>
```

Using Proxy:
- 永久：为 wget 使用代理，可以直接修改/etc/wgetrc，也可以在主文件夹下新建.wgetrc，设置 https_proxy，http_proxy 和 ftp_proxy 参数
```
## You can set the default proxies for Wget to use for http, https, and ftp.
## They will override the value in the environment.
https_proxy = http://127.0.0.1:8087/
http_proxy = http://127.0.0.1:8087/
ftp_proxy = http://127.0.0.1:8087/

## If you do not want to use proxy at all, set this to off.
use_proxy = on
```
- 临时："-e"参数，可以在命令行上指定一个原本出现在".wgetrc"中的设置。于是可以变相在命令行上指定代理：
```
wget -e "http_proxy=http://proxy.example.com:port" http://example.com/file.zip
wget -e "http_proxy=http://username:password@proxy.example.com:port" http://example.com/file.zip
```


### Ftp
```
ftp IP/hostname    //访问 ftp 服务器
mls *.html -       //显示远程主机上文件列表
```

### Scp
```
scp /opt/data.txt  192.168.1.101:/opt/    //将本地 opt 目录下的 data 文件发送到192.168.1.101服务器的 opt 目录下

scp  -r  ./soft  root@192.168.0.100:/root/software // 复制文件夹
```

### nslookup

DNS 解析，查找域名的 IP 地址

nslookup 的语法为 nslookup –qt=RECORD_TYPE 目标域名 DNS 服务器地址
RECORD_TYPE主要有:
- A 地址记录(Ipv4)
- AAAA 地址记录（Ipv6）
- CNAME 别名记录
- MX 邮件服务器记录
- NS 名字服务器记录
```
nslookup -q=ns www.baidu.com 223.5.5.5
```



## 资源占用分析
### 进程操作

#### 启动进程并获得 pid

可以使用&运算符将命令放入后台运行，然后使用特殊的 shell 变量$! 来获取该命令的 PID
```
command &  # 将你的命令替换为"command"
echo $!
```

#### 查看进程
ps
参数：
-A 列出所有的进程
-w 显示加宽可以显示较多的资讯
-au 显示较详细的资讯
-aux 显示所有包含其他使用者的进程

显示格式：
```
USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND
```
- VSZ: 占用的虚拟记忆体大小
- RSS: 占用的记忆体大小
- STAT: 该行程的状态
	- D: 无法中断的休眠状态 (通常 IO 的进程)
	- R: 正在执行中，S: 静止状态，T: 暂停执行
	- W: 没有足够的记忆体分页可分配
- START: 行程开始时间
- TIME: 执行的时间
- COMMAND: 所执行的指令

#### 结束进程
"kill"指令可以通过进程号,结束单个进程,  
"killall"指令可以通过进程名称,同时结束多个相同名称的进程

#### Kill
kill pid       //杀死该 pid 的进程  
kill -9 pid    //强制杀死该进程  

#### Killall
killall vim

### 资源占用
#### Free
  说明：这个命令用于显示系统当前内存的使用情况，包括已用内存、可用内存和交换内存的情况 
```
free -g            //以 G 为单位输出内存的使用量，-g 为 GB，-m 为 MB，-k 为 KB，-b 为字节 
free -t            //查看所有内存的汇总
```


#### 查看网速

```
sudo apt install nload
```
输入nload命令则会跳出来显示，我们系统中一般有一个或者多个网卡，用左右键可以切换要查看的网卡。

#### 查看显卡占用

查看一次
```
nvidia-smi
```

持续刷新：2 表示每隔 2 秒刷新一次
```
watch -n 2 nvidia-smi
```

#### Top
```
top               //显示当前系统中占用资源最多的一些进程, shift+m 按照内存大小查看
```

第三行：cpu状态
	0.3% us — 用户空间占用CPU的百分比。
	0.0% sy — 内核空间占用CPU的百分比。
	0.0% ni — 改变过优先级的进程占用CPU的百分比
	99.7% id — 空闲CPU百分比
	0.0% wa — IO等待占用CPU的百分比
	0.0% hi — 硬中断（Hardware IRQ）占用CPU的百分比
	0.0% si — 软中断（Software Interrupts）占用CPU的百分比

PR：进程的优先级别，越小越优先被执行
NI：The nice value of the task.  A negative nice value means higher priority, whereas a  positive  nice  value  means  lower  priority.   Zero  in  this field simply means priority will not be adjusted in determining a task's dispatch-ability.
VIRT：进程占用的虚拟内存
RES：进程占用的物理内存
SHR：进程使用的共享内存
S：进程的状态：
		D = uninterruptible sleep
		I = idle
		R = running
		S = sleeping
		T = stopped by job control signal
		t = stopped by debugger during trace
		Z = zombie
%CPU：进程占用 CPU 的使用率
%MEM：进程使用的物理内存和总内存的百分比
TIME+：该进程启动后占用的总的 CPU 时间，即占用 CPU 使用时间的累加值。

#### lsof
检查打开的文件信息

- 检查端口占用
```sh
lsof -i :<端口号>
```

### Pref 性能分析

#### Perf top
实时显示系统/进程的性能统计信息

常用参数
-e：指定性能事件
-a：显示在所有 CPU 上的性能统计信息
-C：显示在指定 CPU 上的性能统计信息
-p：指定进程 PID
-t：指定线程 TID
-K：隐藏内核统计信息
-U：隐藏用户空间的统计信息
-s：指定待解析的符号信息
graph: 使用调用树，将每条调用路径进一步折叠。这种显示方式更加直观。
    每条调用路径的采样率为绝对值。也就是该条路径占整个采样域的比率。
fractal
    默认选项。类似与 graph，但是每条路径前的采样率为相对值。
flat
    不折叠各条调用
选项 call_order 用以设定调用图谱的显示顺序，该选项有 2 个取值，分别是

callee 与 caller。
   将该选项设为 callee 时，perf 按照被调用的顺序显示调用图谱，上层函数被下层函数所调用。
   该选项被设为 caller 时，按照调用顺序显示调用图谱，即上层函数调用了下层函数路径，也不显示每条调用路径的采样率

#### Perf stat
分析系统/进程的整体性能概况

- task‐clock 事件表示目标任务真正占用处理器的时间，单位是毫秒。也称任务执行时间
- context-switches 是系统发生上下文切换的次数
- CPU-migrations 是任务从一个处理器迁往另外一个处理器的次数
- page-faults 是内核发生缺页的次数
- cycles 是程序消耗的处理器周期数
- instructions 是指命令执行期间产生的处理器指令数
- branches 是指程序在执行期间遇到的分支指令数。
- branch‐misses 是预测错误的分支指令数。
- XXX seconds time elapsed 系程序持续时间。任务执行时间/任务持续时间大于 1，那可以肯定是多核引起的

**参数设置**：
-e：选择性能事件
-i：禁止子任务继承父任务的性能计数器。
-r：重复执行 n 次目标程序，并给出性能指标在 n 次执行中的变化范围。
-n：仅输出目标程序的执行时间，而不开启任何性能计数器。
-a：指定全部 cpu
-C：指定某个 cpu
-A：将给出每个处理器上相应的信息。
-p：指定待分析的进程 id
-t：指定待分析的线程 id

#### Perf record
记录一段时间内系统/进程的性能时间

参数：
 -e：选择性能事件
 -p：待分析进程的 id
 -t：待分析线程的 id
 -a：分析整个系统的性能
 -C：只采集指定 CPU 数据
 -c：事件的采样周期
 -o：指定输出文件，默认为 perf. data
 -A：以 append 的方式写输出文件
 -f：以 OverWrite 的方式写输出文件
 -g：记录函数间的调用关系
 -F：采样频率，采样频率建议在 4000 以内，避免造成太多开销

#### Perf Report
读取 perf record 生成的数据文件，并显示分析数据

参数
-i：输入的数据文件
-v：显示每个符号的地址
`-d <dos>`：只显示指定 dos 的符号
-C：只显示指定 comm 的信息（Comm. 触发事件的进程名）
-S：只考虑指定符号
-U：只显示已解析的符号
-g[type, min, order]：显示调用关系，具体等同于 perf top 命令中的-g
-c：只显示指定 cpu 采样信息
-M：以指定汇编指令风格显示
–source：以汇编和 source 的形式进行显示
`-p<regex>`：用指定正则表达式过滤调用函数

性能调优时，我们通常需要分析查找到程序百分比高的热点代码片段，这便需要使用 perf record 记录单个函数级别的统计信息，并使用 perf report 来显示统计结果；


举例：perf record -e cpu-clock -g -p 22
-g 选项是告诉 perf record 额外记录函数的调用关系
-e cpu-clock 指 perf record 监控的指标为 cpu 周期
-p 指定需要 record 的进程 pid


## 其他常用命令

### 包管理

#### Apt

更新软件源
```
sudo apt-get update
```
更新软件
```
sudo apt-get upgrade
```
从 deb 文件安装：
```
sudo apt install path_to_deb_file
```

删除软件
- 删除软件包, 保留配置文件 apt-get remove PackageName
- 删除软件包, 同时删除配置文件 apt-get --purge remove PackageName
- 删除软件包, 同时删除为满足依赖，而自动安装且不再使用的软件包 apt-get purge PackageName
- 删除软件包, 删除配置文件 apt-get autoremove PackageName
- 删除不再使用的依赖包 apt-get --purge autoremove PackageName
- 清除已下载的软件包和旧软件包 apt-get clean && apt-get autoclean

清除所有无用的软件
> 如果是旧的、过时的、无用的软件造成的错误，运行如下命令
```
sudo apt autoremove
```

#### Yum
```
yum install httpd      //使用 yum 安装 apache 
yum update httpd       //更新 apache 
yum remove httpd       //卸载/删除 apache 
```

#### Rpm
```
rpm -ivh httpd-2.2.3-22.0.1.el5.i386.rpm      //使用 rpm 文件安装 apache 
rpm -uvh httpd-2.2.3-22.0.1.el5.i386.rpm      //使用 rpm 更新 apache 
rpm -ev httpd                                 //卸载/删除 apache 
```

### Service

service 命令用于运行 System V init 脚本，这些脚本一般位于/etc/init.d 文件下，这个命令可以直接运行这个文件夹里面的脚本，而不用加上路径
```
service ssh status      //查看服务状态 
service --status-all    //查看所有服务状态 
service ssh restart     //重启服务 
```

### Uname
说明：uname 可以显示一些重要的系统信息，例如内核名称、主机名、内核版本号、处理器类型之类的信息 
```
uname -a // 显示全部信息
```


### Date
```
date -s "01/31/2010 23:59:53"   ///设置系统时间
```

### alias别名

格式：注意，等号两边不要空格，若命令包含空格，则一定要加‘’
```
alias [别名]=[需要别名的命令]
```
>eg：`alias load_esp='. $HOME/dev/esp/esp-idf/export.sh'`


**alias 可以将多个命令包含在 value 中，各个命令用分号分隔。**

> 别名 l 首先启动 pwd 显示当前路径，然后启动 ls 显示当前的文件目录。  
```
alias l=‘pwd;ls’ 
```

**可以用别名来调用其他的别名**

**别名永久生效**

如果想要文件永久生效，只需将上述别名命令写到相应用户的 .bashrc 文件的末尾。

- /home/user/.bashrc 使用于用户 user 的终端
- /root/.bashrc 适用于管理员用户的终端
