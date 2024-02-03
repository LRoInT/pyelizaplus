# ELIZA-CHANGE

## 介绍

ELIZA 的 Python 实现. ELIZA 是基于规则的聊天机器人, 用于扮演一个心理医生.
规则文件在 `doctor.txt`. 如何写规则文件见 [rule.md](./rule.md)

## 使用

从文件运行:

```
$ python eliza.py
How do you do.  Please tell me your problem.
> I would like to have a chat bot.
You say you would like to have a chat bot ?
> bye
Goodbye.  Thank you for talking to me.
```

作为包使用:

```python
import eliza

eliza = eliza.Eliza()
eliza.load('doctor.txt')

print(eliza.initial())
while True:
    said = input('> ')
    response = eliza.respond(said)
    if response is None:
        break
    print(response)
print(eliza.final())
```

## 说明

源代码来自[github:wadetb/eliza](https://github.com/wadetb/eliza)

### 参考

eliza1目录:[github:wadetb/eliza](https://github.com/wadetb/eliza)

eliza2目录:[github:jezhiggins/eliza.py](https://github.com/jezhiggins/eliza.py)
