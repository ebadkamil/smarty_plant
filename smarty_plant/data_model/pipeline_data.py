class PipelineData:
    def __init__(self, status: str, order_type: str) -> None:
        self._status = status
        self._order_type = order_type

    def as_dict(self):
        return {"status": self._status, "order_type": self._order_type}


class OrderData:
    def __init__(self, id: int, pipeline: PipelineData) -> None:
        self._id = id
        self._pipeline = pipeline

    def as_dict(self):
        return {"id": self._id, "pipeline": self._pipeline.as_dict()}
