# Note: This class is no longer used, but wanted to show possible solution using custom classes
class ProductionCompany(object):
    def __init__(self, production_company_id, production_company_name):
        self.production_company_id = production_company_id
        self.production_company_name = production_company_name

    # In order to use set, had to set up Equality and Hash
    def __eq__(self, other):
        return isinstance(other, ProductionCompany) and self.production_company_id == other.production_company_id
        # Note: Updated from old recommendation to new
        # if isinstance(other, ProductionCompany):
        #     return self.production_company_id == other.production_company_id
        # else:
        #     return NotImplemented

    def __hash__(self):
        return hash(self.production_company_id)
