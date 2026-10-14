"""文档的三层：docstring（给调用者）、注释（解释"为什么"）、doctest（可执行的示例）"""

def chunk(items: list, size: int) -> list[list]:
    """把列表按固定大小切块。

    Args:
        items: 待切分的列表。
        size: 每块大小，必须为正整数。

    Returns:
        切分后的列表的列表；最后一块可能不足 size。

    Raises:
        ValueError: size <= 0 时。

    Examples:
        >>> chunk([1, 2, 3, 4, 5], 2)
        [[1, 2], [3, 4], [5]]
        >>> chunk([], 3)
        []
    """
    if size <= 0:
        raise ValueError("size 必须为正整数")
    # 用切片而不是逐个 append：可读性更好，且对大列表更快（为什么，而不是做什么）
    return [items[i:i + size] for i in range(0, len(items), size)]

if __name__ == "__main__":
    import doctest
    result = doctest.testmod(verbose=False)
    print(f"doctest: 尝试 {result.attempted} 个示例，失败 {result.failed} 个")
    help(chunk)
