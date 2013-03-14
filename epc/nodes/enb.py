from ..utils.io import IoService
from ..messages.rrc import RRC_CONNECTION_SETUP_ESTABLISHMENT_PROCEDURE_MESSAGES
from ..procedures.enb.rrc import RrcConnectionEstablishmentProcedureHandler


class Enb(object):

    def __init__(self, name, port):
        self.ioService = IoService(name, port)
        self.ues = {}
        self.rrcConnectionEstablishmentProcedureHandler = RrcConnectionEstablishmentProcedureHandler(
            5, 0.7, self.ioService, self.__handleNewRrcConnectionEstablishment__)

    def execute(self):
        self.ioService.addIncomingMessageCallback(self.__handleIncomingMessage__)
        self.ioService.start()

    def terminate(self):
        self.ioService.stop()

    def __handleNewRrcConnectionEstablishment__(self, parameters):
        cRnti = parameters["cRnti"]
        self.ues[cRnti] = parameters

    def __handleIncomingMessage__(self, source, interface, channelInfo, message):
        messageName = message["messageName"]
        if messageName in RRC_CONNECTION_SETUP_ESTABLISHMENT_PROCEDURE_MESSAGES:
            self.rrcConnectionEstablishmentProcedureHandler.handleIncomingMessage(
                source, interface, channelInfo, message)