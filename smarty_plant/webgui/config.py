from smarty_plant.webgui.constants import OrderType

config = {
    OrderType.TYPE_A.value: {"pipelines": list(range(1, 20))},
    OrderType.TYPE_B.value: {"pipelines": list(range(20, 60))},
    OrderType.TYPE_C.value: {"pipelines": list(range(60, 100))},
}
