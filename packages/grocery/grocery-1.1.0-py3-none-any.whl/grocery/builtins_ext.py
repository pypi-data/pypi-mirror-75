from collections import Counter as BuiltInCounter
import operator


class list_ext(list):
    def __cmp_dict(self, dictionary: dict, **kwargs):
        if not isinstance(dictionary, dict):
            return False
        for key__cmp, val in kwargs.items():
            key, cmp = key__cmp.split('__')
            if not getattr(operator, cmp)(dictionary.get(key), val):
                return False
        return True

    def filter_dict(self, *args, **kwargs):
        for item in self:
            if self.__cmp_dict(item, **kwargs):
                yield item


class Counter(BuiltInCounter):
    def __add__(self, other):
        """与builtin的Counter一样，只是Counter相加后，不过滤值为0的key"""
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem, count in self.items():
            newcount = count + other[elem]
            result[elem] = newcount
        for elem, count in other.items():
            if elem not in self:
                result[elem] = count
        return result
