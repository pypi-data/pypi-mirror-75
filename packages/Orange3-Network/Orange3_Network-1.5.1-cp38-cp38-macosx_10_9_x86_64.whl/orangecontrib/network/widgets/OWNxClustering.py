from AnyQt.QtCore import Qt

from Orange.data import Table
from Orange.data.util import get_unique_names
from Orange.widgets import gui, widget, settings
from Orange.widgets.widget import Input, Output
from orangecontrib.network import Network
from orangecontrib.network.network import community as cd


class OWNxClustering(widget.OWWidget):
    name = 'Network Clustering'
    description = 'Orange widget for community detection in networks.'
    icon = "icons/NetworkClustering.svg"
    priority = 6430

    class Inputs:
        network = Input("Network", Network, default=True)

    class Outputs:
        network = Output("Network", Network)
        items = Output("Items", Table)

    resizing_enabled = False
    want_main_area = False

    want_control_area = True
    want_main_area = False

    method = settings.Setting(0)
    iterations = settings.Setting(1000)
    use_random_state = settings.Setting(False)
    hop_attenuation = settings.Setting(0.1)
    autoApply = settings.Setting(True)

    def __init__(self):
        super().__init__()
        self.net = None
        self.cluster_feature = None
        commit = lambda: self.commit()
        gui.spin(self.controlArea, self, "iterations", 1,
                   100000, 1, label="Max. iterations:",
                   callback=commit)
        self.random_state = gui.checkBox(self.controlArea, self, "use_random_state",
                                         label="Replicable clustering",
                                         callback=commit)
        ribg = gui.radioButtonsInBox(
            self.controlArea, self, "method",
            btnLabels=["Label propagation clustering (Raghavan et al., 2007)",
                       "Label propagation clustering (Leung et al., 2009)"],
            box="Clustering method", callback=commit)

        gui.doubleSpin(gui.indentedBox(ribg), self, "hop_attenuation",
                         0, 1, 0.01, label="Hop attenuation (delta): ")

        self.infolabel = gui.widgetLabel(self.controlArea, ' ')

        gui.auto_commit(self.controlArea, self, "autoApply", 'Commit',
                        checkbox_label='Auto-commit', orientation=Qt.Horizontal)
        commit()

    @Inputs.network
    def set_network(self, net):
        self.net = net
        self.commit()

    def commit(self):
        self.infolabel.setText(' ')

        kwargs = {'iterations': self.iterations}
        if self.method == 0:
            alg = cd.label_propagation

        elif self.method == 1:
            alg = cd.label_propagation_hop_attenuation
            kwargs['delta'] = self.hop_attenuation

        if self.net is None:
            self.Outputs.items.send(None)
            self.Outputs.network.send(None)
            self.cluster_feature = None
            return

        if self.use_random_state:
            kwargs['seed'] = 0

        labels = alg(self.net, **kwargs)
        domain = self.net.nodes.domain
        # Tie a name for presenting clustering results to the widget instance
        if self.cluster_feature is None:
            self.cluster_feature = get_unique_names(domain, 'Cluster')
        cd.add_results_to_items(self.net, labels, self.cluster_feature)

        self.infolabel.setText('%d clusters found' % len(set(labels.values())))
        self.Outputs.items.send(self.net.nodes)
        self.Outputs.network.send(self.net)


if __name__ == "__main__":
    from AnyQt.QtWidgets import QApplication
    a = QApplication([])
    ow = OWNxClustering()
    ow.show()

    def set_network(data, id=None):
        ow.set_network(data)

    import OWNxFile
    from os.path import join, dirname
    owFile = OWNxFile.OWNxFile()
    owFile.Outputs.network.send = set_network
    owFile.open_net_file(join(dirname(dirname(__file__)), 'networks', 'leu_by_genesets.net'))

    a.exec_()
    ow.saveSettings()
    owFile.saveSettings()
