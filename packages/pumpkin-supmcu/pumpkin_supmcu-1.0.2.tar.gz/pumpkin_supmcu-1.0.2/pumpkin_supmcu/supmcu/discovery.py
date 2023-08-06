# coding: utf-8
# ##############################################################################
#  (C) Copyright 2019 Pumpkin, Inc. All Rights Reserved.                       #
#                                                                              #
#  This file may be distributed under the terms of the License                 #
#  Agreement provided with this software.                                      #
#                                                                              #
#  THIS FILE IS PROVIDED AS IS WITH NO WARRANTY OF ANY KIND,                   #
#  INCLUDING THE WARRANTY OF DESIGN, MERCHANTABILITY AND                       #
#  FITNESS FOR A PARTICULAR PURPOSE.                                           #
# ##############################################################################
"""
The discovery modules allow for automated discovery of all SupMCU and module telemetry definitions for a given I2C
address. The list of telemetry items can be serialized after the fact and loaded again at a later time to avoid the
lengthy discovery process.
"""
import time
from typing import Union, Optional, List, Any

from .i2c import SupMCUMaster
from .serial import SupMCUSerialMaster
from .parsing import parse_telemetry, _format_to_length
from .types import SupMCUTelemetryDefinition, SupMCUModuleDefinition, TelemetryType, \
    _supmcu_fmt_data_type, _data_type_sizes, TelemetryDataItem
from ..i2c import I2CMaster

SIZEOF_HEADER_FOOTER = 13
SUPMCU_VERSION_DEFINITION = SupMCUTelemetryDefinition("Firmware Version", 77, 0, "S")
SUPMCU_LENGTH_DEFINITION = SupMCUTelemetryDefinition("Length", 2 + SIZEOF_HEADER_FOOTER, 0, "s")
SUPMCU_NAME_DEFINITION = SupMCUTelemetryDefinition("Name", 33 + SIZEOF_HEADER_FOOTER, 0, "S")
SUPMCU_FORMAT_DEFINITION = SupMCUTelemetryDefinition("Format", 25 + SIZEOF_HEADER_FOOTER, 0, "S")
SUPMCU_TELEMETRY_AMOUNT_DEFINITION = SupMCUTelemetryDefinition("Amount", 4 + SIZEOF_HEADER_FOOTER, 14, "s,s")
SUPMCU_TELEMETRY_AMOUNT_STR = "SUP:TEL? 14\n"
_DEFAULT_RESPONSE_DELAY = 0.1  # 100 ms between I2C Write and Read


def _write_read_supcmu_i2c(i2c_master: I2CMaster,
                           address: int,
                           cmd: str,
                           read_length: int,
                           response_delay: float) -> bytes:
    """
    Writes to the I2C bus `cmd` to I2C Address `address`, then sleeps `response_delay` seconds, and finally reads
    `read_length` bytes from the I2C Address. Meant for internal usage in the request_telemetry_definition function.

    :param i2c_master: The I2CMaster object to use for the telemetry request.
    :param address: The I2C address to send the command to.
    :param cmd: The command to send to the I2C device.
    :param read_length: The amount of bytes to read back from the I2C device.
    :param response_delay: The amount of time in seconds to wait between the I2C write and read.
    :return: The response in bytes.
    """
    i2c_master.write(address, cmd.encode('ascii'))
    time.sleep(response_delay)
    return i2c_master.read(address, read_length)


def get_version_string(master: Union[I2CMaster, SupMCUSerialMaster], address: int = None, cmd_name: str = None) -> str:
    """
    Gets the version string for the module at the provided address

    :param i2c_master: The I2CMaster to use.
    :param address: The address of the device to request information from. Only required when using a :any:`I2CMaster`
    :param cmd_name: The name of the module to request information from.  Only required when using a :any:`SupMCUSerialMaster`
    :return: The version string
    """

    module_def = SupMCUModuleDefinition("", "", address, {0: SUPMCU_VERSION_DEFINITION}, {})
    if isinstance(master, I2CMaster) and address is not None:
        master = SupMCUMaster(master, (module_def,))
        version = master.request_telemetry(address, TelemetryType.SupMCU, 0).items[0].value
    elif isinstance(master, SupMCUSerialMaster) and cmd_name is not None:
        version = master.send_command(cmd_name, 'SUP:TEL? 0,ASCII')
    elif isinstance(master, I2CMaster) or isinstance(master, SupMCUSerialMaster):
        raise TypeError("'address' or 'cmd_name' were not supplied, though they were needed")
    else:
        raise TypeError("'master' must either be an 'I2CMaster' or a 'SupMCUSerialMaster'")
    # print(version)
    return version


def get_values(i2c_master: I2CMaster, address: int, module_cmd_name: str, idx: int, format: str, response_delay: Optional[float] = None) -> List[TelemetryDataItem]:
    """
    Retrieves the current values of the telemetry object that is indicated by the provided index

    :param i2c_master: The I2CMaster device to use.
    :param address: The address of the device to request information from.
    :param module_cmd_name: The module name used in the context of SCPI commands (e.g. DCPS for Desktop CubeSat Power
                            Supply).
    :param idx: The telemetry index to grab the information for.
    :param response_delay: The amount of time in seconds to wait between I2C Write and read. Can be None, or set
                            from SupMCUMaster passed in as `i2c_master`.
    :return: A list of :any:`TelemetryDataItem`
    """
    if response_delay is None:
        # None was set by the SupMCU master or the passed in variable.
        response_delay = _DEFAULT_RESPONSE_DELAY
    try:
        size = _format_to_length(format) + SIZEOF_HEADER_FOOTER
    except ValueError:
        # Size of version string
        size = SUPMCU_VERSION_DEFINITION.telemetry_length
    # size = SIZEOF_HEADER_FOOTER + sum((_data_type_sizes[f] for f in fmt))
    raw_bytes = _write_read_supcmu_i2c(i2c_master, address, f'{module_cmd_name}:TEL? {idx}\n',
        size, response_delay)
    # raw_bytes = raw_bytes[SIZEOF_HEADER_FOOTER:]
    vals = parse_telemetry(raw_bytes, SupMCUTelemetryDefinition('', size, idx, format))
    return vals.items


def set_values(master: Union[I2CMaster, SupMCUMaster, SupMCUSerialMaster],
               address: int, module_cmd_name: str, idx: int, items: List[TelemetryDataItem],
               response_delay: Optional[float] = None):
    """
    Sets the current values of the SupMCU module connected through the provided master
    to the values in the provided :any:`TelemetryDataItem`s

    :param master: The :any:`I2CMaster` device, :any:`SupMCUMaster`, or :any:`SupMCUSerialMaster` to use to connect the SupMCU module.
    :param address: The address of the device to request information from. (unused for :any:`SupMCUSerialMaster`)
    :param module_cmd_name: The module name used in the context of SCPI commands (e.g. DCPS for Desktop CubeSat Power
                            Supply).
    :param idx: The telemetry index to grab the information for.
    :param items: A list of :any:`TelemetryDataItem` objects to supply the values to set.
    :param response_delay: The amount of time in seconds to wait between I2C Write and read. Can be None, or set
                            from SupMCUMaster passed in as `i2c_master`.
    """
    if response_delay is None:
        # None was set by the SupMCU master or the passed in variable.
        response_delay = _DEFAULT_RESPONSE_DELAY
    values = ','.join((item.string_value for item in items))
    if isinstance(master, I2CMaster):
        master.write(address, f'{module_cmd_name}:TEL {idx},{values}\n'.encode('ascii'))
    elif isinstance(master, SupMCUMaster):
        master.i2c_master.write(address, f'{module_cmd_name}:TEL {idx},{values}\n'.encode('ascii'))
    elif isinstance(master, SupMCUSerialMaster):
        master.send_command(module_cmd_name, f'{module_cmd_name}:TEL {idx},{values}\n')


def request_telemetry_definition(i2c_master: Union[I2CMaster, SupMCUMaster],
                                 address: int,
                                 module_cmd_name: str,
                                 idx: int,
                                 response_delay: Optional[float] = None,
                                 is_simulatable_mod: bool = False) -> SupMCUTelemetryDefinition:
    """
    Requests the formatting, name and length information from the device at I2C address `address`, using the module
    short name `module_cmd_name` (e.g. BM for Battery Module), concatenating that with `idx` in a telemetry request
    s.t. cmd_to_send is `<module_cmd_name>:TEL? <idx>,NAME/FORMAT/LENGTH`

    :param i2c_master: The I2CMaster device to use.
    :param address: The address of the device to request information from.
    :param module_cmd_name: The module name used in the context of SCPI commands (e.g. DCPS for Desktop CubeSat Power
                            Supply).
    :param idx: The telemetry index to grab the information for.
    :param response_delay: The amount of time in seconds to wait between I2C Write and read. Can be None, or set
                            from SupMCUMaster passed in as `i2c_master`.
    :param is_simulatable_mod: Whether or not the module is simulatable.
    :return: The SupMCUTelemetryDefinition that represents the Telemetry data.
    """
    is_simulatable = False
    if isinstance(i2c_master, SupMCUMaster):
        if response_delay is None:
            response_delay = i2c_master.request_delay
        i2c_master = i2c_master.i2c_master
    if response_delay is None:
        # None was set by the SupMCU master or the passed in variable.
        response_delay = _DEFAULT_RESPONSE_DELAY

    # Find out format, name and length information
    format_bytes = _write_read_supcmu_i2c(i2c_master, address, f'{module_cmd_name}:TEL? {idx},FORMAT\n',
                                          SUPMCU_FORMAT_DEFINITION.telemetry_length, response_delay)
    name_bytes = _write_read_supcmu_i2c(i2c_master, address, f'{module_cmd_name}:TEL? {idx},NAME\n',
                                        SUPMCU_NAME_DEFINITION.telemetry_length, response_delay)
    length_bytes = _write_read_supcmu_i2c(i2c_master, address, f'{module_cmd_name}:TEL? {idx},LENGTH\n',
                                          SUPMCU_LENGTH_DEFINITION.telemetry_length, response_delay)
    if is_simulatable_mod:
        simulatable_bytes = _write_read_supcmu_i2c(i2c_master, address, f'{module_cmd_name}:TEL? {idx},SIMULATABLE\n',
                                                  SUPMCU_LENGTH_DEFINITION.telemetry_length, response_delay)
    # Parse the response bytes as telemetry items, then check to see if any are not ready yet
    format_response = parse_telemetry(format_bytes, SUPMCU_FORMAT_DEFINITION)
    name_response = parse_telemetry(name_bytes, SUPMCU_NAME_DEFINITION)
    length_response = parse_telemetry(length_bytes, SUPMCU_LENGTH_DEFINITION)
    if is_simulatable_mod:
        simulatable_response = parse_telemetry(simulatable_bytes, SUPMCU_LENGTH_DEFINITION)
        is_simulatable = bool(simulatable_response.items[0].value)
    if is_simulatable:
        defaults = get_values(i2c_master, address, module_cmd_name, idx, format_response.items[0].value, response_delay)
        defaults = [item.value for item in defaults]
    # Raise exception if any of the responses are flagged as not ready.
    if not format_response.header.ready:
        raise RuntimeError(
            f'`{module_cmd_name}:TEL? {idx},FORMAT` returned a non-ready response. Try increasing `response_delay`.')
    if not name_response.header.ready:
        raise RuntimeError(
            f'`{module_cmd_name}:TEL? {idx},NAME` returned a non-ready response. Try increasing `response_delay`.')
    if not length_response.header.ready:
        raise RuntimeError(
            f'`{module_cmd_name}:TEL? {idx},LENGTH` returned a non-ready response. try increasing `response_delay`.')
    if is_simulatable_mod:
        if not simulatable_response.header.ready:
            raise RuntimeError(
                f'`{module_cmd_name}:TEL? {idx},SIMULATABLE` returned a non-ready response. try increasing `response_delay`.')
    # Create the telemetry definition
    return SupMCUTelemetryDefinition(name_response.items[0].value,
                                     length_response.items[0].value,
                                     idx,
                                     format_response.items[0].value,
                                     False if not is_simulatable_mod else simulatable_response.items[0].value,
                                     None if not is_simulatable else defaults)


def get_name_from_version(version: str) -> str:
    """
    Gets the Short Module name from the version string

    :param version: A version string to extract the name from
    """
    return version.split()[0].split("-")[0]


def request_module_definition(i2c_master: Union[I2CMaster, SupMCUMaster],
                              address: int,
                              module_cmd_name: Optional[str] = None,
                              module_name: Optional[str] = None,
                              response_delay: Optional[float] = None) -> SupMCUModuleDefinition:
    """
    Requests all of the telemetry definitions from the module at I2C Address `address`, using `module_cmd_name` when
    requesting module telemetry definitions.

    :param i2c_master: The I2C master to write/read the requests from.
    :param address: The address of the module on the I2C bus.
    :param module_cmd_name: Optional, short name of the module as used in telemetry requests (e.g. BM for Battery Module).
    :param module_name: Optional name to give module, if None, then is set to `module_cmd_name`
    :param response_delay: The delay in seconds to wait between I2C read and I2C write.
    :return: The module definition for the device at I2C Address `address`
    """
    if isinstance(i2c_master, SupMCUMaster):
        if response_delay is None:
            response_delay = i2c_master.request_delay
        i2c_master = i2c_master.i2c_master
    version = get_version_string(i2c_master, address)
    if module_cmd_name is None:
        module_cmd_name = get_name_from_version(version)
    if response_delay is None:
        # None was set by the SupMCU master or the passed in variable.
        response_delay = _DEFAULT_RESPONSE_DELAY
    if module_name is None:
        module_name = module_cmd_name

    # Grab the amount of telemetry items on the module, then start requesting ALL telemetry definitions.
    amount_resp = _write_read_supcmu_i2c(i2c_master,
                                         address,
                                         SUPMCU_TELEMETRY_AMOUNT_STR,
                                         SUPMCU_TELEMETRY_AMOUNT_DEFINITION.telemetry_length,
                                         response_delay)
    amount_telemetry = parse_telemetry(amount_resp, SUPMCU_TELEMETRY_AMOUNT_DEFINITION)
    supmcu_amount, module_amount = amount_telemetry.items[0].value, amount_telemetry.items[1].value

    is_simulatable_mod = "(on STM)" in version or "(on QSM)" in version

    supmcu_defs = {}
    for idx in range(supmcu_amount):
        supmcu_defs[idx] = request_telemetry_definition(i2c_master, address, 'SUP', idx, response_delay, is_simulatable_mod)
    module_defs = {}
    for idx in range(module_amount):
        module_defs[idx] = request_telemetry_definition(i2c_master, address, module_cmd_name, idx, response_delay, is_simulatable_mod)
    return SupMCUModuleDefinition(module_name, module_cmd_name, address, supmcu_defs, module_defs)
