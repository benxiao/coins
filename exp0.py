import pydash

print(pydash
      .chain([4, 2, 3, 4])
      .sort()
      .initial()
      .value())

print(pydash.count_substr("reorieorieo", 'ri'))
print(pydash.iteratee('a.b.c')({"a": {"b": {"c": 1}}}))


def tee(obj, path):
    if not path:
        return obj
    h, *t = path
    if not isinstance(obj, dict):
        return
    if not obj.get(h):
        return
    return tee(obj[h], t)


def iter_path(s):
    h, *rest = s.split('.', maxsplit=1)
    if not rest:
        yield h, None
    else:
        yield h, iter_path(rest[0])


def iter_path2(ss):
    s = 0
    for i, ch in enumerate(ss):
        if ss[i] == '.':
            yield ss[s: i]
            s = i + 1
    if s < len(ss) - 1:
        yield ss[s:]


if __name__ == '__main__':
    g = iter_path('a.b.c.d')
    while g:
        h, g = next(g)
        print(h)
    print(list(iter_path2('aa.bbb.cc.dddd.uuuuuu.d.lll')))
