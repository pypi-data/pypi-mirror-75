
import Orange.data
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets import gui
from Orange.data import Domain, ContinuousVariable, StringVariable

from orange_starfrac.RpcClient import RpcClient
from orange_starfrac.InputMixin import InputMixin
from orange_starfrac.utils import rowToDict, tableToDictionary



class FracturesOutput(OWWidget, RpcClient, InputMixin):
    name = "Fractures Output"
    description = "Send Fractures table data to StarFrac application"
    icon = "icons/fracturesOutput.svg"
    priority = 100
    want_main_area = False

    class Inputs:
        data = Input("Fractures table", Orange.data.Table, default=True)


    def __init__(self):
        OWWidget.__init__(self)
        RpcClient.__init__(self)
        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(box, "No data on input yet, waiting to get something.")
        self.infob = gui.widgetLabel(box, "")

    @Inputs.data
    def set_data(self, dataset):
        if dataset is not None:
            self.infoa.setText("%d instances in input data set" % len(dataset))
            self.requestData("setFractures", self.dataReceived, tableToDictionary(dataset))
        else:
            self.infoa.setText("No data on input yet, waiting to get something.")

    def dataReceived(self, data):
        self.infoa.setText('\n'.join(data))




if __name__ == "__main__":
    WidgetPreview(CompletionInput).run()
