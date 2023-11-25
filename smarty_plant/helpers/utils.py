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
        return PipelineStatus.RED
    elif mode == PipelineMode.RUNNING_NORMAL.value:
        return PipelineStatus.GREEN
    return PipelineStatus.YELLOW


def get_pipeline_data(message):
    return message["pipeline"]["pipeline_number"], get_status(message["pipeline"]["status"])


color_mapping = {
    PipelineStatus.RED: "rgb(255, 0, 0)",
    PipelineStatus.GREEN: "rgb(0, 255, 0)",
    PipelineStatus.YELLOW: "rgb(255, 255, 0)"
}
