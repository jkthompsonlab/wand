""" Driver for Leoni eol/mol 1xn fibre switches """

import pyvisa


class LeoniSwitch:
    def __init__(self, serial_addr, simulation=False):

        self.simulation = simulation
        if simulation:
            self._num_channels = 16
            return

        self.rm = pyvisa.ResourceManager()
        self.dev = self.rm.open_resource(serial_addr)
        self.dev.baud_rate = 57600

        self._num_channels = None
        self.get_num_channels()

    def get_num_channels(self):
        """ Returns the number of channels on the switch """
        if self.simulation:
            return 16

        if self._num_channels is None:
            resp = self.dev.query("type?").strip()
            assert resp.startswith("eol 1x") or resp.startswith("mol 1x")
            self._num_channels = int(resp[6:])
        return self._num_channels

    def set_active_channel(self, channel):
        """ Sets the active channel.

        :param channel: the channel number to select, not zero-indexed
        """
        if channel < 1 or channel > self._num_channels:
            raise ValueError('Channel out of bounds')
        if self.simulation:
            return
        self.dev.write("ch{}".format(channel))

    def get_active_channel(self):
        """ Returns the active channel number
        :return: the active channel, not zero-indexed
        """
        if self.simulation:
            return 1

        resp = self.dev.query("ch?")
        return int(resp.strip())

    def get_firmware_rev(self):
        """ Returns a firmware revision string, such as 'v8.09' """
        if self.simulation:
            return "Leoni fibre switch simulator"

        resp = self.dev.query("firmware?")
        return resp.strip()

    def ping(self):
        if self.simulation:
            return True
        return bool(self.get_num_channels())

    def close(self):
        if self.simulation:
            return
        self.dev.close()
