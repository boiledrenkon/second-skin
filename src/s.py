def people(whisp_cache, threshold=0):
    group = {
        whisp.author.name: whisp.author.name.append(whisp) or [whisp]
        for whisp in whisp_cache
    }
    dictionary = {
        author: len(messages)
        for author, messages in group
        if len(messages) > threshold
    }
    print(list(dictionary.keys()))
    return
