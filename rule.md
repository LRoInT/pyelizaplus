# 规则文件写法

## 格式

Text:

```Text
maintype: p1-1 p1-2 ... # Note ...
  (type2: p2-1 p2-2 ...)

```

- `maintype`: 规则名称
- `type2`: 次级规则
- `p1,p2,...`: 规则内容, 数量不定, 以空格分隔
- `#`: 注释

JSON:

```JSON
{
  "type1": [...],
  "type2": {
    "p1":null,
    "type3":[...]
  }
}
```

- `type...`: 规则名称
- `p...`: 规则内容

## 规则汇总

| 名称 | 说明 | 变量 |
| ---- | ---- | ---- |
| initial | 开始语 | self.initials = [] |
| final | 结束语 |  self.finals = [] |
| quit | 触发退出 | self.quits = [] |
| pre | ? | self.pres = {} |
| post | 人称转换 | self.posts = {} |
| synon | ? | self.synons = {} |
| key | 关键词 | self.keys = {} |
| key-decomp | key 规则属性 | self.keys[...].decomps = [Decomp] |
| key-decomp-reasmb | key-decomp 规则属性 | self.keys[...].decomps[...].reasmb = [] |

### 具体说明

> `key`: 关键词规则
>
``` 格式
key: key_name
  decomp: *
    reasmb: ... #回复语句
    reasmb: ...
    ...```
