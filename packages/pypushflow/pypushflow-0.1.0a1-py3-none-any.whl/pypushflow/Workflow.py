#
# Copyright (c) European Synchrotron Radiation Facility (ESRF)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__authors__ = ["O. Svensson"]
__license__ = "MIT"
__date__ = "28/05/2019"


import pprint
import logging
from pypushflow.representation import Scheme
from pypushflow.PythonActor import PythonActor as ActorFactory
from pypushflow.StartActor import StartActor
from pypushflow.StopActor import StopActor
from pypushflow.JoinActor import JoinUntilStopSignal
from pypushflow.addon import utils
from pypushflow.addon.classes import BaseWorkflowAddOn


logger = logging.getLogger('pypushflow')


class _BaseWorkflow:
    def __init__(self, configuration):
        self._configuration = configuration or {}
        self._add_ons = []
        for add_on_class in self._getAddOnsClasses():
            self._add_ons.append(add_on_class(workflow=self,
                                              configuration=self._configuration
                                              ))

    def _getAddOnsClasses(self):
        add_ons = []
        for _, classes in utils.get_registered_add_ons_classes().items():
            for class_ in classes:
                import inspect
                if BaseWorkflowAddOn in (inspect.getmro(class_)):
                    add_ons.append(class_)
        return add_ons


class Workflow(_BaseWorkflow):
    """TODO"""
    def __init__(self, name):
        super(Workflow, self).__init__()
        self.name = name
        self.listOnErrorActor = []

    def connectOnError(self, actor):
        logger.debug("In connectOnError in subModule {0}, actor name {1}".format(self.name, actor.name))
        self.listOnErrorActor.append(actor)

    def triggerOnError(self, inData):
        logger.debug(pprint.pformat(inData))
        for onErrorActor in self.listOnErrorActor:
            logger.debug(onErrorActor.trigger)
            onErrorActor.trigger(inData)

    def getActorPath(self):
        return '/' + self.name


class ProcessableWorkflow(_BaseWorkflow):
    """Define a workflow that can be executed

    :param scheme: the workflow scheme
    :param configuration: some configuration / settings that can be pass to
                          the add-on.
    """

    def __init__(self, scheme, configuration=None):
        super(ProcessableWorkflow, self).__init__(configuration=configuration)
        assert isinstance(scheme, Scheme)
        self._representation = scheme
        # first load node handlers if any
        scheme.load_handlers()

        self._actor_factory = {}
        for node in self._representation.nodes:
            name = '-'.join((str(node.id), node._process_pt))
            self._actor_factory[node] = ActorFactory(parent=None,
                                                     name=name,
                                                     node=node,
                                                     errorHandler=None)

        # deal with connect
        for node in self._representation.nodes:
            actor_factory = self._actor_factory[node]
            for downstream_node in node.downstream_nodes:
                downstream_actor_factory = self._actor_factory[downstream_node]
                actor_factory.connect(downstream_actor_factory)

        # add start actor
        self._start_actor = StartActor()
        for node in self._representation.start_nodes():
            actor_factory = self._actor_factory[node]
            self._start_actor.connect(actor_factory)

        def connect_finals_nodes(actor):
            # add end actor
            for node in self._representation.final_nodes():
                actor_factory = self._actor_factory[node]
                actor_factory.connect(actor)

        self._end_actor = StopActor()

        if self.has_final_join():
            self._join_actor = JoinUntilStopSignal('stop join')
            connect_finals_nodes(self._join_actor)
            self._join_actor.connect(self._end_actor)
        else:
            connect_finals_nodes(self._end_actor)

    def has_final_join(self):
        """True if we need to send a 'end' signal before closing the workflow
        This is needed for DataList and DataWatcher
        """
        for node in self._representation.nodes:
            if node.need_stop_join:
                return True
        return False
