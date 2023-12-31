class PipelineData:
    def __init__(self, pipeline_number: int, status: str, order_type: str) -> None:
        self._pipeline_number = pipeline_number
        self._status = status
        self._order_type = order_type

    def as_dict(self):
        return {
            "pipeline_number": self._pipeline_number,
            "status": self._status,
            "order_type": self._order_type,
        }


class OrderData:
    def __init__(self, id: int, pipeline: PipelineData) -> None:
        self._id = id
        self._pipeline = pipeline

    def as_dict(self):
        return {"id": self._id, "pipeline": self._pipeline.as_dict()}


# {
#   "ProductTypeID": 1,
#   "TypeName": "TypeA"
# }

# {
#   "LineID": 1,
#   "LineNumber": "PL001",
#   "Status": "Green",
#   "LastUpdateTimestamp": "2023-11-26T12:00:00Z",
#   "ProductType": {
#     "ProductTypeID": 1,
#     "TypeName": "TypeA"
#   }
# }

# {
#   "OrderID": 101,
#   "OrderNumber": "ORD001",
#   "ProductType": {
#     "ProductTypeID": 1,
#     "TypeName": "TypeA"
#   }
# }

# {
#   "MappingID": 201,
#   "LineID": 1,
#   "OrderID": 101
# }
#