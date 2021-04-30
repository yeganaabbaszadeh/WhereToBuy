class Shipping:
    def __init__(self, site_ls, site_data, shipping):
        self.site_ls = site_ls
        self.site_data = site_data
        self.shipping = shipping

    def filterByShipping(self, site_ls, site_data, shipping):
        if shipping == "available":
            if site_ls[4] == "available":
                site_data.append(site_ls)
        else:
            site_data.append(site_ls)


class Order:
    def __init__(self, site_data, order):
        self.site_data = site_data
        self.order = order

    def filterByOrder(self, site_data, order):
        if order == 'ascending':
            site_data.sort(key = lambda l: l[2])
        elif order == 'descending':
            site_data.sort(key = lambda l: l[2], reverse=True)


