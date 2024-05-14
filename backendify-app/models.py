# {
#   "id": "string, the company id requested by a customer",
#   "name": "string, the company name, as returned by a backend",
#   "active": "boolean, indicating if the company is still active according to the active_until date",
#   "active_until": "RFC 3339 UTC date-time expressed as a string, optional."
# }
# Your solution should always reply with the following JSON object to the customer:
class Response:
    def __init__(self, company_id=None, name=None, active=False, active_until=None) -> None:
        self.id = company_id
        self.name = name
        self.active = active
        self.active_until = active_until