def rowToDict(columns, metas, row, table):
    res = {}
    for col in columns:
        index = table.domain.index(col)
        res[col] = row[index].value
    for i in range (0, len(row.metas)):
        res[metas[i]] = row.metas[i]
    return res


def tableToDictionary(table):
    dict = {}
    dict["columns"] = []
    dict["metas"] = []
    data = []
    for atr in table.domain.attributes:
        dict["columns"].append(atr.name)
    for meta in table.domain.metas:
        dict["metas"].append(meta.name)

    for row in table:
        data.append(rowToDict(dict["columns"], dict["metas"], row, table))

    dict["data"] = data
    return dict
