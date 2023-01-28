import supervisor
from keeb_display import DisplayLayers

supervisor.set_next_stack_limit(4096 + 4096)

DisplayLayers.display_splash_fox()