from collections import defaultdict
from functools import wraps

output_catch = {}
input_catch = {}


def lru_catch(func):
    catch = {}
    @wraps(func)
    def _warp(*args, **kwargs):
        if args in catch:
            return catch[args]
        else:
            catch[args], output_catch[args], input_catch[args] = func(*args, **kwargs)
            return catch[args]

    return _warp


@lru_catch
def get_distance(str1, str2):
    if len(str1) == 0:
        return len(str2), 'Remove ' + str2, ('', '')
    if len(str2) == 0:
        return len(str1), 'Add ' + str1, ('', '')

    if str1[-1] == str2[-1]:
        return get_distance(str1[:-1], str2[:-1]), 'Do nothing!', (str1[:-1], str2[:-1])
    else:
        dist_list = [1 + get_distance(str1[:-1], str2), 1 + get_distance(str1, str2[:-1])]
        min_dist = min(dist_list)
        if dist_list.index(min_dist) == 0:
            return min_dist, 'Add ' + str1[-1], (str1[:-1], str2)
        else:
            return min_dist, 'Remove ' + str2[-1], (str1, str2[:-1])


def get_solution(str1, str2):
    get_distance(str1, str2)
    args = (str1, str2)
    todo = []
    while args != ('', ''):
        todo.append(output_catch[args])
        args = input_catch[args]
    for i in todo[::-1]:
        if i != 'Do nothing!':
            print(i)


if __name__ == '__main__':
    get_solution('让我们来看看结果如何', '大家看一下结果会是什么')
