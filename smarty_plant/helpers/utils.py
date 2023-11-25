from functools import wraps
from threading import Thread

from smarty_plant.webgui.constants import PipelineMode, PipelineStatus


def run_in_thread(original):
    @wraps(original)
    def wrapper(*args, **kwargs):
        t = Thread(target=original, args=args, kwargs=kwargs, daemon=True)
        t.start()
        return t

    return wrapper


def get_status(mode):
    if mode == PipelineMode.STANDING_STILL.value:
        return PipelineStatus.RED.value
    elif mode == PipelineMode.RUNNING_NORMAL.value:
        return PipelineStatus.GREEN.value
    return PipelineStatus.YELLOW.value


def get_pipeline_data(message):
    mode = message["pipeline"]["status"]
    return message["pipeline"]["pipeline_number"], mode


color_mapping = {
    PipelineMode.STANDING_STILL.value: "rgb(255, 0, 0)",
    PipelineMode.RUNNING_NORMAL.value: "rgb(0, 255, 0)",
    PipelineMode.STOPPING.value: "rgb(255, 255, 0)",
    PipelineMode.STARTING.value: "rgb(255, 255, 0)",
}
