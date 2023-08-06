
import Orange.data
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.data import Domain, ContinuousVariable, StringVariable

import math

from orange_starfrac.RpcClient import RpcClient
from orange_starfrac.InputMixin import InputMixin


class CompletionInput(OWWidget, RpcClient, InputMixin):
    name = "Completion Data Input"
    description = "Retreive completion data from selected wells in the active tab of locally running StarFrac application"
    icon = "icons/completionInput.svg"
    priority = 10
    predefinedColumns = [] # "Stage", "MD start", "MD end", "# of clusters", "Total Proppant", "Total Fluid" ]
    domainVars = list(map(lambda col: ContinuousVariable.make(col), predefinedColumns))
    domainMetas = [StringVariable.make("Well")]
    predefinedDomain = Domain(domainVars, metas = domainMetas)

    want_main_area = False

    class Outputs:
        data = Output("Completion table", Orange.data.Table)


    def __init__(self):
        OWWidget.__init__(self)
        RpcClient.__init__(self)
        InputMixin.__init__(self)
        gui.button(self.controlArea, self, "Update", callback=self.update)
        self.update()

    def update(self):
        self.requestData("getCompletions", self.dataReceived)




if __name__ == "__main__":
    WidgetPreview(CompletionInput).run()
