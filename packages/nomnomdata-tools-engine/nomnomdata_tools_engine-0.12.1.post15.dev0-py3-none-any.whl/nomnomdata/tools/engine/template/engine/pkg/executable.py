import logging

from nomnomdata.engine.components import Engine, Parameter, ParameterGroup
from nomnomdata.engine.parameters import Int, String

logger = logging.getLogger("engine.hello_world")

engine = Engine(
    uuid="CHANGE-ME-PLEASE",
    alias="Hello World",
    description="Engine that repeats Hello World a specified number of times.",
    categories=["general"],
)


@engine.action(
    display_name="Hello World", description="This action prints hello world to the logs. "
)
@engine.parameter_group(
    name="general_parameters",
    display_name="General Parameters",
    description="Parameters for the Hello World action",
    parameter_group=ParameterGroup(
        Parameter(
            type=Int(),
            name="repeat",
            display_name="Repeat",
            description="Number of times to repeat in the logs",
            default=1,
        ),
        Parameter(
            type=String(),
            name="myname",
            display_name="Name",
            description="A name to use instead of 'World'",
        ),
    ),
)
def hello_world(parameters):
    logger.info(str(parameters))
    i = 0
    while i < parameters["repeat"]:
        x = f"Hello {parameters.get('myname', 'World')}"
        logger.info(x)
        i += 1
    return i, x
