from taipy import Core, Gui

from pages.root import root_md
from pages.vcustomers.vcustomers import vcustomers_md
from pages.vtrainers.vtrainers import vtrainers_md

pages = {
    "/": root_md,
    "vcustomers": vcustomers_md,
    "vtrainers": vtrainers_md,
    # "scenes": scenes_md,
    # "trainings": trainings_md
}

Core().run()
gui = Gui(pages=pages)
gui.run(title="AI销售培训")
