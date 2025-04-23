---
title: LLM-如何使用预训练LLM
date: 2025-04-22 13:19:22
lastmod: 2025-04-23 15:05:06
aliases: 
keywords: 
categories:
  - LLM
tags:
  - LLM应用
share: true
---


## 使用预训练 LLM

模型命名规范：
- 无 instruct：基础模型，进行了预训练
- 含 instruct：还额外进行了指令对齐等操作

### 模型结构

示例： "Qwen/Qwen2.5-0.5B-Instruct"
- Model 是一个嵌入模型+若干 layers
- lm_head 将模型输出映射回词表
```
Qwen2ForCausalLM(
  (model): Qwen2Model(
    (embed_tokens): Embedding(151936, 896)
    (layers): ModuleList(
      (0-23): 24 x Qwen2DecoderLayer(
        (self_attn): Qwen2SdpaAttention(
          (q_proj): Linear(in_features=896, out_features=896, bias=True)
          (k_proj): Linear(in_features=896, out_features=128, bias=True)
          (v_proj): Linear(in_features=896, out_features=128, bias=True)
          (o_proj): Linear(in_features=896, out_features=896, bias=False)
          (rotary_emb): Qwen2RotaryEmbedding()
        )
        (mlp): Qwen2MLP(
          (gate_proj): Linear(in_features=896, out_features=4864, bias=False)
          (up_proj): Linear(in_features=896, out_features=4864, bias=False)
          (down_proj): Linear(in_features=4864, out_features=896, bias=False)
          (act_fn): SiLU()
        )
        (input_layernorm): Qwen2RMSNorm()
        (post_attention_layernorm): Qwen2RMSNorm()
      )
    )
    (norm): Qwen2RMSNorm()
  )
  (lm_head): Linear(in_features=896, out_features=151936, bias=False)
)
```


### 特殊符号

每一个模型的特殊符号均有差异，一般而言：
- 未指令对齐的基础模型通常包含 end of text 词元，标记文本结束
```
{'bos_token': '<endoftext>',
 'eos_token': '<endoftext>',
 'unk_token': '<endoftext>'}
```

- 对齐的多模态模型具有以下词元
	- eos：“end of sentence”（句子结束）标记，用于指示文本序列的结束。在生成文本时，当模型输出这个 Token 时，表示当前生成的内容已经结束。
	- pad：主要用于在将不同长度的文本序列处理成相同长度时进行填充。在训练过程中，为了方便将文本批次处理，需要将所有文本序列的长度统一，短的序列就会用 <|endoftext|> 进行填充，以便于模型进行并行计算
	- `<|im_start|>` 表明一段对话内容的起始， `<|im_end|>` 则代表结束。在多轮对话场景中，它们可以帮助模型清晰地识别不同轮次的对话边界。
	- <|box_start|> 和 <|box_end|>：或许用于标记与 “框” 相关的信息，比如在图像识别结合文本处理的场景中，可能用于标记图像中某个框选区域的描述信息的起始和结束。
	- <|quad_start|> 和 <|quad_end|>：类似于 <|box_start|> 和 <|box_end|>，可能用于标记与四边形区域相关的信息，在图像或图形处理相关的文本描述中使用。
```
{'eos_token': '<|im_end|>',
 'pad_token': '<|endoftext|>',
 'additional_special_tokens': ['<|im_start|>',
  '<|im_end|>',
  '<|object_ref_start|>',
  '<|object_ref_end|>',
  '<|box_start|>',
  '<|box_end|>',
  '<|quad_start|>',
  '<|quad_end|>',
  '<|vision_start|>',
  '<|vision_end|>',
  '<|vision_pad|>',
  '<|image_pad|>',
  '<|video_pad|>']}
```


### 使用基础 API
#### chat-Template

```Python
prompt= "写一段描写春天的散文"
messages = [
    {"role":"system","content":"You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
    {"role":"user","content":prompt}
]
text = tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
print(text)
```

输出的结果：
```
<|im_start|>system
You are Qwen, created by Alibaba Cloud. You are a helpful assistant.<|im_end|>
<|im_start|>user
写一段描写春天的散文<|im_end|>
<|im_start|>assistant
```

#### 词元化

```
model_inputs = tokenizer([text],return_tensors="pt").to(model.device)
print(model_inputs)
```
输出：
```
{'input_ids': tensor([[151644,   8948,    198,   2610,    525,   1207,  16948,     11,   3465,
            553,  54364,  14817,     13,   1446,    525,    264,  10950,  17847,
             13, 151645,    198, 151644,    872,    198,  61443, 104383, 109478,
         105303,   9370, 110401, 151645,    198, 151644,  77091,    198]],
       device='cuda:0'), 'attention_mask': tensor([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]], device='cuda:0')}
```

#### 推理和解码

```Python
# 推理
generated_ids = model.generate(
    **model_inputs,
    max_new_tokens = 512
)
print(generated_ids.shape)
print(tokenizer.batch_decode(generated_ids,skip_special_tokens=True))
```

输出：
```
torch.Size([1, 322])
['system\nYou are Qwen, created by Alibaba Cloud. You are a helpful assistant.\nuser\n写一段描写春天的散文\nassistant\n春，是一个充满生机与希望的季节。当第一缕晨光穿透云层，映照出一片嫩绿，万物苏醒，一切都仿佛在向我们宣告着生命的复苏和新生的美好。在这个时节里，大自然呈现出一幅幅生动而和谐的画面。\n\n山间的小溪边，溪水潺潺，仿佛是大地母亲的轻抚，带来了一丝清凉与宁静。树木被唤醒了，它们开始抽芽，枝叶间挂满了晶莹剔透的新绿，空气中弥漫着泥土与花香混合后的清新气息。蝴蝶们在花朵间飞舞，蜜蜂忙碌地采集花粉，为这生机勃勃的春天增添了几分活力。\n\n田野上，麦苗破土而出，一望无际的绿色铺展在面前，那是农民伯伯辛勤耕耘的成果。孩子们在田埂上奔跑嬉戏，欢声笑语充满了整个春天。远处，山峦起伏，群山环抱，仿佛是大自然精心绘制的一幅壮丽画卷，让人不禁感叹大自然的神奇与伟大。\n\n春天，不仅仅是一季的更迭，它更是对生命的一种呼唤，是对自然美的赞美。在这片充满希望的季节里，每一个生命都在用自己的方式绽放着自己的光彩，让这个世界变得更加美好。\n\n春天，就像一首未完的诗，等待着我们去细细品味、去感受那份生机与希望。']
```

注意到 generated_ids 包含前文的用户输入、系统输入，只需要模型输出的话需要做切断
```Python
# 移除用户输入，只保留模型输出
generated_ids = [output_ids[len(input_ids):] for input_ids,output_ids in zip(model_inputs.input_ids,generated_ids)]
response = tokenizer.batch_decode(generated_ids,skip_special_tokens=True)
response
```
输出：
```
['春，是一个充满生机与希望的季节。当第一缕晨光穿透云层，映照出一片嫩绿，万物苏醒，一切都仿佛在向我们宣告着生命的复苏和新生的美好。在这个时节里，大自然呈现出一幅幅生动而和谐的画面。\n\n山间的小溪边，溪水潺潺，仿佛是大地母亲的轻抚，带来了一丝清凉与宁静。树木被唤醒了，它们开始抽芽，枝叶间挂满了晶莹剔透的新绿，空气中弥漫着泥土与花香混合后的清新气息。蝴蝶们在花朵间飞舞，蜜蜂忙碌地采集花粉，为这生机勃勃的春天增添了几分活力。\n\n田野上，麦苗破土而出，一望无际的绿色铺展在面前，那是农民伯伯辛勤耕耘的成果。孩子们在田埂上奔跑嬉戏，欢声笑语充满了整个春天。远处，山峦起伏，群山环抱，仿佛是大自然精心绘制的一幅壮丽画卷，让人不禁感叹大自然的神奇与伟大。\n\n春天，不仅仅是一季的更迭，它更是对生命的一种呼唤，是对自然美的赞美。在这片充满希望的季节里，每一个生命都在用自己的方式绽放着自己的光彩，让这个世界变得更加美好。\n\n春天，就像一首未完的诗，等待着我们去细细品味、去感受那份生机与希望。']
```

### 使用 Pipeline

注意要根据模型的类型选择传入 pipeline 的类型：
- decode only 的模型：text-generation
- encoder-decoder 的模型：text2text-generation

```Python
pipeline = transformers.pipeline(
    "text-generation",
    model = model,
    tokenizer=tokenizer,
    return_full_text = False,
    max_new_tokens=500,
    do_sample = False
)
output = pipeline(messages)
output
```

输出：
```
[{'generated_text': '春，是四季中最温柔、最充满希望的季节。它以一种不同于其他季节的独特魅力，悄然降临在每一个角落。\n\n春风拂面，万物复苏。那温暖而湿润的气息，仿佛能洗净心灵的尘埃，让人心旷神怡。小草从土里探出头来，嫩绿的叶片轻轻摇曳，像是在向世界宣告着生命的开始。花朵们也竞相开放，粉红、淡紫、鹅黄……它们争奇斗艳，为大地披上了一袭色彩斑斓的锦衣，散发出阵阵芬芳。鸟儿们也开始活跃起来，清脆的鸣叫声和欢快的歌声，如同一首首动人的乐章，奏响了春天的赞歌。\n\n田野里的麦苗随风摆动，金黄色的麦浪翻滚起伏，宛如一片金色的海洋。农民伯伯们忙碌的身影穿梭其间，他们的脸上洋溢着丰收的喜悦。孩子们则在田间嬉戏打闹，欢声笑语回荡在空气中，充满了童年的快乐与纯真。\n\n春天，是一个充满生机与活力的季节。它教会我们珍惜生命中的每一刻，感恩大自然的馈赠。在这个季节里，我们可以感受到生活的美好，也可以体验到人与自然和谐共处的美好。春天，是大自然赋予我们的礼物，让我们在这美好的时光中，感受生命的奇迹。'}]
```

