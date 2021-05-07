def filterByShipping(site_ls, site_data, shipping):
    if shipping == "available":
        if site_ls[4] == "available":
            site_data.append(site_ls)
        else:
            site_data.append(site_ls)

    return site_data


def filterByOrder(site_data, order):
    if order == 'ascending':
        site_data.sort(key = lambda l: l[2])
    elif order == 'descending':
        site_data.sort(key = lambda l: l[2], reverse=True)


def convertCurrency(price, currency, site):
    if site == 'amazon':
        if currency == 'azn':
            price = round(float(price) * 1.70, 2)
        else:
            price = round(float(price), 2)

    elif site == 'tapaz':
        if currency == 'usd':
            price = round(float(price) / 1.70, 2)
        else:
            price = round(float(price), 2)

    return price
