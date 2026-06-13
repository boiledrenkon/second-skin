from collections import Counter


def people(whisp_cache, threshold=0):
    counts = Counter(whisp.author.name for whisp in whisp_cache)
    names = [author for author, n in counts.items() if n > threshold]
    print(names)
    return
