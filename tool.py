import eliza
import json
import sys
# Eliza辅助工具

def txt2json(txt, out): #文本规则转JSON
    el = eliza.Eliza()
    el.load_text(txt)
    load_data = {"initials": el.initials, "finals": el.finals, "quits": el.quits, "pres": el.pres,
                 "posts": el.posts, "synons": el.synons, "keys": el.keys, "symbol": el.symbol, "sym_ch_en": el.sym_ch_en}
    json.dump(load_data, open(out, "w", encoding="utf-8"),
              indent=4, sort_keys=True,ensure_ascii=False, cls=eliza.elizaEncoder)


if __name__ == '__main__':
    if sys.argv[1:]:
        if sys.argv[1] == 'txt2json':
            txt2json(sys.argv[2], sys.argv[3])
