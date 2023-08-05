def digit_format(score, n=4):
    """
    score: 分数
    n: 小数点后保留几位
    """
    return format(float(score), f'.{n}f')
