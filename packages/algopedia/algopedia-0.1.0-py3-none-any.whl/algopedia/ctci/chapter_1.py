from algopedia.solver import register


@register("1.1", time="N", space="N")
def is_unique_1(string: str):
    hashset = {char for char in string}
    return len(hashset) == len(string)


@register("1.1", time="NlogN", space="1")
def is_unique_2(string: str):
    string = sorted(string)  # type: ignore
    for index in range(len(string) - 1):
        if string[index] == string[index + 1]:
            return False
    return True
