import json
import logging
from time import sleep, time

from .comm_package import validate_data, define_package, data_to_parsed_string
from .serialib import SerialComm
from .const import *
from .exceptions import NoAnswer, InvalidAnswer, InvalidCommand, CRCError

logger = logging.getLogger(__name__)


class Ziva(SerialComm):
    def __init__(self, recv_address:int, port:str, baudrate:int, timeout=0.5, rf:bool = True):
        super().__init__()
        self.recv_address = recv_address
        self.port = port
        self.baudrate = baudrate
        self.rf = rf
        self.package_counter = 0
        self.rv_units = []
        self.open(port=port, baudrate=baudrate, timeout=timeout)

    def __increment_counter(self):
        if self.package_counter == 255:
            self.package_counter = 0
        else:
            self.package_counter += 1

    def define_package(self, app_cmd:str = None, var_name:str = None, var_val:str = None):
        package = define_package(
            recv_addr=self.recv_address,
            app_cmd=app_cmd,
            var_name=var_name,
            var_val=var_val,
            counter=self.package_counter,
            rf=self.rf
        )
        return package

    def send_receive(self, app_cmd: str, var_name: str = None, var_val: str = None, retry_limit: int = None,
                     timeout:float = 1, stream_channel: bool = False, parse: bool = True) -> dict:
        '''Sent package and receive answer.'''

        self.ser.timeout = timeout
        for error_count in range(20):
            try:
                self.__increment_counter()
                package = self.define_package(
                    app_cmd=app_cmd,
                    var_name=var_name,
                    var_val=var_val,
                )
                self.write(data=package)
                data = self.read(last_char=END_MARKER_BYTES)
                data = validate_data(data, stream_channel=stream_channel)
                if stream_channel:
                    # data['data'] = data_decompress(data=data['data'])
                    data['data'] = ''.join(chr(i) for i in data['data'])
                else:
                    data['data'] = data_to_parsed_string(data=data['data'])
            except (NoAnswer, InvalidAnswer, CRCError, InvalidCommand, Exception) as e:
                logger.exception(e)
                if retry_limit:
                    if retry_limit == error_count:
                        raise
                else:
                    if type(e).__name__ == NoAnswer.__name__:
                        retry = RETRY_NO_ANSWER
                    elif type(e).__name__ == InvalidAnswer.__name__:
                        retry = RETRY_INVALID_ANSWER
                    elif type(e).__name__ == CRCError.__name__:
                        retry = RETRY_CRC_ERROR
                    elif type(e).__name__ == InvalidCommand.__name__:
                        retry = RETRY_INVALID_COMMAND
                    else:
                        retry = 2
                    if error_count == retry:
                        raise
            else:
                return data

    def read_variable(self, name) -> dict:
        return self.send_receive(app_cmd=VALUE_READ, var_name=name)

    def write_variable(self, name, value) -> dict:
        return self.send_receive(app_cmd=VALUE_WRITE, var_name=name, var_val=value)

    def read_real_values(self) -> list:
        name = REAL_VALUES
        real_values = self.read_variable(name=name)['data']
        if self.rv_units:
            real_values_units = []
            i = 0
            for val in real_values:
                try:
                    float(val)
                    real_values_units.append((val, self.rv_units[i]))
                    i += 1
                except ValueError as e:
                    real_values_units.append(val)
            real_values = real_values_units
        return real_values

    def read_params(self):
        i = 0
        data = []
        error_count = 0
        max_error_count = 5
        for i in range(500):
            var_name = f'PAR[{i}]'
            try:
                params = self.send_receive(app_cmd=VALUE_READ, var_name=var_name)['data']
                if params == 'End':
                    break
                elif len(params) > 0:
                    params_dict = {}
                    for par in params:
                        if '=' in par:
                            params_dict[par.split('=')[0]] = par.split('=')[1]
                        else:
                            params_dict[par] = True
                    value = self.read_variable(name=params_dict['Name'])['data']
                    params_dict['Value'] = value
                    data.append(params_dict)
            except Exception as e:
                logger.warning(f'Cant read param {var_name}, e:{e}')
                error_count += 1
                if error_count == max_error_count:
                    break
                else:
                    continue
        logger.info(f'Settings parameters read, count:{len(data)}')
        return data

    def memory_status(self):
        data = self.send_receive(app_cmd=MEMORY_STATUS)['data']
        size, free, used = int(data[0]), int(data[1]), int(data[2])
        return {'size':size, 'free': free, 'used':used, 'used_percentage':round(used / size * 100, 1)}

    def read_memory_data(self, filepath: str = 'data.jda'):
        """Read memory from device and save data to filepath"""

        self.send_receive(app_cmd=OPEN_MEMORY_DIR)
        data_out = ''
        while True:
            data = self.send_receive(app_cmd=MEMORY_START_READING, stream_channel=True, timeout=2)
            print ('data ', data)
            data_out += data['data']
            if data['status'] == 'OT':
                break
        if data_out:
            with open(filepath, 'w', encoding='latin1') as f:
                f.write(data_out)

    def save_params(self, filepath:str = 'settings.txt'):
        """Save params to filepath"""
        data = self.read_params()
        with open(filepath, 'w') as f:
            f.write(json.dumps(data))

    def load_params(self, filepath: str):
        with open(filepath) as f:
            data = json.load(f)

    def read_info_variables(self):
        """Get info params"""
        data = {
            'ident_a':None,
            'ident_b':None,
            'ident_c':None,
            'rv_mask':None,
            'rv_units':None,
        }

        for name in data.keys():
            try:
                data[name] = self.read_variable(name=name.upper())['data']
            except Exception as e:
                data[name] = None

        self.rv_units = []
        if data['rv_units'] and data['rv_mask']:
            rv_units = data['rv_units'].split(';')
            for i, mask in enumerate(data['rv_mask']):
                if bool(int(mask)):
                    self.rv_units.append(rv_units[i])

        try:
            data['rv'] = self.read_real_values()
            print ('kaj', data['rv'])
        except Exception as e:
            print (e)
            data['rv'] = None

        return data

    def reset_rf_device(self):
        pass

    def reset_cpu(self):
        return self.send_receive(app_cmd=RESET_CPU)

    def goto_sleep(self):
        return self.send_receive(app_cmd=DEVICE_SLEEP)


    def start_wake_up_routine(self):
        start = time()
        app_cmd = f"{WAKE_UP_DEVICE}{self.recv_address},{WAKE_UP_TIME_STEP}"
        wake_up_count = WAKE_UP_TIME_TOTAL // WAKE_UP_TIME_STEP
        try:
            for i in range(wake_up_count):
                self.send_receive(app_cmd=app_cmd, retry_limit=20, timeout=0.1)
                sleep(WAKE_UP_TIME_STEP)
                try:
                    self.read_real_values()
                    break
                except NoAnswer:
                    if (i == wake_up_count - 1):
                        raise
                sleep(2)
        except NoAnswer:
            raise NoAnswer('USB router is busy or not working properly')
        wake_time = round(time() - start, 1)
        logger.info(f'Device woke up in {wake_time} seconds')

    def go_online(self) -> dict:
        """
        Go online. If remote device is RF start wake_up procedure.
        :return: dict of info parameters
        """
        if self.rf:
            self.start_wake_up_routine()

        info_vars = self.read_info_variables()
        return info_vars

