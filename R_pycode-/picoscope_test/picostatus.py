PICO_DRIVER_VERSION  = 0x00000000
PICO_USB_VERSION  = 0x00000001
PICO_HARDWARE_VERSION  = 0x00000002
PICO_VARIANT_INFO  = 0x00000003
PICO_BATCH_AND_SERIAL  = 0x00000004
PICO_CAL_DATE  = 0x00000005
PICO_KERNEL_VERSION  = 0x00000006
PICO_DIGITAL_HARDWARE_VERSION  = 0x00000007
PICO_ANALOGUE_HARDWARE_VERSION  = 0x00000008
PICO_MAC_ADDRESS  = 0x0000000B

PS2208_MAX_ETS_CYCLES	=500
PS2208_MAX_INTERLEAVE	=20

PS2207_MAX_ETS_CYCLES	=500
PS2207_MAX_INTERLEAVE	= 20

PS2206_MAX_ETS_CYCLES	=250
PS2206_MAX_INTERLEAVE	= 10

PS2000ARange = [
#1e-5,## PS2000A_10MV,
2e-5,##	  PS2000A_20MV,
5e-5,##	  PS2000A_50MV,
1e-4,##	  PS2000A_100MV,
2e-4,##	  PS2000A_200MV,
5e-4,##	  PS2000A_500MV,
1,##	 PS2000A_1V,
2,##	 PS2000A_2V,
5,##	 PS2000A_5V,
10,##	PS2000A_10V,
20,##	    PS2000A_20V,
50##	 PS2000A_50V,
##	PS2000A_MAX_RANGES,
]

PICO_OK  = 0x00000000
PICO_MAX_UNITS_OPENED  = 0x00000001
PICO_MEMORY_FAIL  = 0x00000002
PICO_NOT_FOUND  = 0x00000003
PICO_FW_FAIL  = 0x00000004
PICO_OPEN_OPERATION_IN_PROGRESS  = 0x00000005
PICO_OPERATION_FAILED  = 0x00000006
PICO_NOT_RESPONDING  = 0x00000007
PICO_CONFIG_FAIL  = 0x00000008
PICO_KERNEL_DRIVER_TOO_OLD  = 0x00000009
PICO_EEPROM_CORRUPT  = 0x0000000A
PICO_OS_NOT_SUPPORTED  = 0x0000000B
PICO_INVALID_HANDLE  = 0x0000000C
PICO_INVALID_PARAMETER  = 0x0000000D
PICO_INVALID_TIMEBASE  = 0x0000000E
PICO_INVALID_VOLTAGE_RANGE  = 0x0000000F
PICO_INVALID_CHANNEL  = 0x00000010
PICO_INVALID_TRIGGER_CHANNEL  = 0x00000011
PICO_INVALID_CONDITION_CHANNEL  = 0x00000012
PICO_NO_SIGNAL_GENERATOR  = 0x00000013
PICO_STREAMING_FAILED  = 0x00000014
PICO_BLOCK_MODE_FAILED  = 0x00000015
PICO_NULL_PARAMETER  = 0x00000016
PICO_ETS_MODE_SET  = 0x00000017
PICO_DATA_NOT_AVAILABLE  = 0x00000018
PICO_STRING_BUFFER_TO_SMALL  = 0x00000019
PICO_ETS_NOT_SUPPORTED  = 0x0000001A
PICO_AUTO_TRIGGER_TIME_TO_SHORT  = 0x0000001B
PICO_BUFFER_STALL  = 0x0000001C
PICO_TOO_MANY_SAMPLES  = 0x0000001D
PICO_TOO_MANY_SEGMENTS  = 0x0000001E
PICO_PULSE_WIDTH_QUALIFIER  = 0x0000001F
PICO_DELAY  = 0x00000020
PICO_CONDITIONS  = 0x00000022
PICO_DEVICE_SAMPLING  = 0x00000024
PICO_NO_SAMPLES_AVAILABLE  = 0x00000025
PICO_BUSY  = 0x00000027
PICO_STARTINDEX_INVALID  = 0x00000028
PICO_INVALID_INFO  = 0x00000029
PICO_INFO_UNAVAILABLE  = 0x0000002A
PICO_INVALID_SAMPLE_INTERVAL  = 0x0000002B
PICO_TRIGGER_ERROR  = 0x0000002C
PICO_SIG_GEN_PARAM  = 0x0000002E
PICO_SHOTS_SWEEPS_WARNING  = 0x0000002F
PICO_SIGGEN_TRIGGER_SOURCE  = 0x00000030
PICO_AUX_OUTPUT_CONFLICT  = 0x00000031
PICO_AUX_OUTPUT_ETS_CONFLICT  = 0x00000032
PICO_WARNING_EXT_THRESHOLD_CONFLICT  = 0x00000033
PICO_WARNING_AUX_OUTPUT_CONFLICT  = 0x00000034
PICO_SIGGEN_OUTPUT_OVER_VOLTAGE  = 0x00000035
PICO_DELAY_NULL  = 0x00000036
PICO_INVALID_BUFFER  = 0x00000037
PICO_SIGGEN_OFFSET_VOLTAGE  = 0x00000038
PICO_SIGGEN_PK_TO_PK  = 0x00000039
PICO_CANCELLED  = 0x0000003A
PICO_INVALID_CALL  = 0x0000003C
PICO_GET_VALUES_INTERRUPTED  = 0x0000003D
PICO_NOT_USED  = 0x0000003F
PICO_INVALID_SAMPLERATIO  = 0x00000040
PICO_INVALID_STATE  = 0x00000041
PICO_NOT_ENOUGH_SEGMENTS  = 0x00000042
PICO_DRIVER_FUNCTION  = 0x00000043
PICO_RESERVED  = 0x00000044
PICO_INVALID_COUPLING  = 0x00000045
PICO_BUFFERS_NOT_SET  = 0x00000046
PICO_RATIO_MODE_NOT_SUPPORTED  = 0x00000047
PICO_RAPID_NOT_SUPPORT_AGGREGATION  = 0x00000048
PICO_INVALID_TRIGGER_PROPERTY  = 0x00000049
PICO_INTERFACE_NOT_CONNECTED  = 0x0000004A
PICO_RESISTANCE_AND_PROBE_NOT_ALLOWED  = 0x0000004B
PICO_POWER_FAILED  = 0x0000004C
PICO_SIGGEN_WAVEFORM_SETUP_FAILED  = 0x0000004D
PICO_FPGA_FAIL  = 0x0000004E
PICO_POWER_MANAGER  = 0x0000004F
PICO_INVALID_ANALOGUE_OFFSET  = 0x00000050
PICO_PLL_LOCK_FAILED  = 0x00000051
PICO_ANALOG_BOARD  = 0x00000052
PICO_CONFIG_FAIL_AWG  = 0x00000053
PICO_INITIALISE_FPGA  = 0x00000054
PICO_EXTERNAL_FREQUENCY_INVALID  = 0x00000056
PICO_CLOCK_CHANGE_ERROR  = 0x00000057
PICO_PWQ_AND_EXTERNAL_CLOCK_CLASH  = 0x00000059
PICO_UNABLE_TO_OPEN_SCALING_FILE  = 0x0000005A
PICO_MEMORY_CLOCK_FREQUENCY  = 0x0000005B
PICO_NO_CAPTURES_AVAILABLE  = 0x0000005D
PICO_NOT_USED_IN_THIS_CAPTURE_MODE  = 0x0000005E
PICO_GET_DATA_ACTIVE  = 0x00000103
PICO_IP_NETWORKED  = 0x00000104
PICO_INVALID_IP_ADDRESS  = 0x00000105
PICO_IPSOCKET_FAILED  = 0x00000106
PICO_IPSOCKET_TIMEDOUT  = 0x00000107
PICO_SETTINGS_FAILED  = 0x00000108
PICO_NETWORK_FAILED  = 0x00000109
PICO_INVALID_IP_PORT  = 0x0000010B
PICO_COUPLING_NOT_SUPPORTED  = 0x0000010C
PICO_BANDWIDTH_NOT_SUPPORTED  = 0x0000010D
PICO_INVALID_BANDWIDTH  = 0x0000010E
PICO_AWG_NOT_SUPPORTED  = 0x0000010F
PICO_ETS_NOT_RUNNING  = 0x00000110
PICO_INVALID_DIGITAL_PORT  = 0x00000113
PICO_INVALID_DIGITAL_CHANNEL  = 0x00000114
PICO_INVALID_DIGITAL_TRIGGER_DIRECTION  = 0x00000115
PICO_ETS_NOT_AVAILABLE_WITH_LOGIC_CHANNELS  = 0x00000117
PICO_WARNING_REPEAT_VALUE  = 0x00000118
PICO_POWER_SUPPLY_CONNECTED  = 0x00000119
PICO_POWER_SUPPLY_NOT_CONNECTED  = 0x0000011A
PICO_POWER_SUPPLY_REQUEST_INVALID  = 0x0000011B
PICO_POWER_SUPPLY_UNDERVOLTAGE  = 0x0000011C
PICO_CAPTURING_DATA  = 0x0000011D
PICO_NOT_SUPPORTED_BY_THIS_DEVICE  = 0x0000011F
PICO_INVALID_DEVICE_RESOLUTION  = 0x00000120
PICO_INVALID_NO_CHANNELS_FOR_RESOLUTION  = 0x00000121
PICO_CHANNEL_DISABLED_DUE_TO_USB_POWERED  = 0x00000122
PICO_SIGGEN_DC_VOLTAGE_NOT_CONFIGURABLE  = 0x00000123
PICO_NO_TRIGGER_ENABLED_FOR_TRIGGER_IN_PRE_TRIG  = 0x00000124
PICO_AWG_CLOCK_FREQUENCY  = 0x00000128
PICO_TOO_MANY_CHANNELS_IN_USE  = 0x00000129
PICO_NULL_CONDITIONS  = 0x0000012A
PICO_DUPLICATE_CONDITION_SOURCE  = 0x0000012B
PICO_INVALID_CONDITION_INFO  = 0x0000012C
PICO_SETTINGS_READ_FAILED  = 0x0000012D
PICO_SETTINGS_WRITE_FAILED  = 0x0000012E
PICO_ARGUMENT_OUT_OF_RANGE  = 0x0000012F
PICO_HARDWARE_VERSION_NOT_SUPPORTED  = 0x00000130
PICO_DIGITAL_HARDWARE_VERSION_NOT_SUPPORTED  = 0x00000131
PICO_ANALOGUE_HARDWARE_VERSION_NOT_SUPPORTED  = 0x00000132
PICO_UNABLE_TO_CONVERT_TO_RESISTANCE  = 0x00000133
PICO_DUPLICATED_CHANNEL  = 0x00000134
PICO_INVALID_RESISTANCE_CONVERSION  = 0x00000135
PICO_INVALID_VALUE_IN_MAX_BUFFER  = 0x00000136
PICO_INVALID_VALUE_IN_MIN_BUFFER  = 0x00000137
PICO_SIGGEN_FREQUENCY_OUT_OF_RANGE  = 0x00000138
PICO_DEVICE_TIME_STAMP_RESET  = 0x01000000
PICO_WATCHDOGTIMER  = 0x10000000

pico_error_strings = {
    0x00000000: 'pico_ok',
    0x00000001: 'pico_max_units_opened',
    0x00000002: 'pico_memory_fail',
    0x00000003: 'pico_not_found',
    0x00000004: 'pico_fw_fail',
    0x00000005: 'pico_open_operation_in_progress',
    0x00000006: 'pico_operation_failed',
    0x00000007: 'pico_not_responding',
    0x00000008: 'pico_config_fail',
    0x00000009: 'pico_kernel_driver_too_old',
    0x0000000A: 'pico_eeprom_corrupt',
    0x0000000B: 'pico_os_not_supported',
    0x0000000C: 'pico_invalid_handle',
    0x0000000D: 'pico_invalid_parameter',
    0x0000000E: 'pico_invalid_timebase',
    0x0000000F: 'pico_invalid_voltage_range',
    0x00000010: 'pico_invalid_channel',
    0x00000011: 'pico_invalid_trigger_channel',
    0x00000012: 'pico_invalid_condition_channel',
    0x00000013: 'pico_no_signal_generator',
    0x00000014: 'pico_streaming_failed',
    0x00000015: 'pico_block_mode_failed',
    0x00000016: 'pico_null_parameter',
    0x00000017: 'pico_ets_mode_set',
    0x00000018: 'pico_data_not_available',
    0x00000019: 'pico_string_buffer_to_small',
    0x0000001A: 'pico_ets_not_supported',
    0x0000001B: 'pico_auto_trigger_time_to_short',
    0x0000001C: 'pico_buffer_stall',
    0x0000001D: 'pico_too_many_samples',
    0x0000001E: 'pico_too_many_segments',
    0x0000001F: 'pico_pulse_width_qualifier',
    0x00000020: 'pico_delay',
    0x00000022: 'pico_conditions',
    0x00000024: 'pico_device_sampling',
    0x00000025: 'pico_no_samples_available',
    0x00000027: 'pico_busy',
    0x00000028: 'pico_startindex_invalid',
    0x00000029: 'pico_invalid_info',
    0x0000002A: 'pico_info_unavailable',
    0x0000002B: 'pico_invalid_sample_interval',
    0x0000002C: 'pico_trigger_error',
    0x0000002E: 'pico_sig_gen_param',
    0x0000002F: 'pico_shots_sweeps_warning',
    0x00000030: 'pico_siggen_trigger_source',
    0x00000031: 'pico_aux_output_conflict',
    0x00000032: 'pico_aux_output_ets_conflict',
    0x00000033: 'pico_warning_ext_threshold_conflict',
    0x00000034: 'pico_warning_aux_output_conflict',
    0x00000035: 'pico_siggen_output_over_voltage',
    0x00000036: 'pico_delay_null',
    0x00000037: 'pico_invalid_buffer',
    0x00000038: 'pico_siggen_offset_voltage',
    0x00000039: 'pico_siggen_pk_to_pk',
    0x0000003A: 'pico_cancelled',
    0x0000003C: 'pico_invalid_call',
    0x0000003D: 'pico_get_values_interrupted',
    0x0000003F: 'pico_not_used',
    0x00000040: 'pico_invalid_sampleratio',
    0x00000041: 'pico_invalid_state',
    0x00000042: 'pico_not_enough_segments',
    0x00000043: 'pico_driver_function',
    0x00000044: 'pico_reserved',
    0x00000045: 'pico_invalid_coupling',
    0x00000046: 'pico_buffers_not_set',
    0x00000047: 'pico_ratio_mode_not_supported',
    0x00000048: 'pico_rapid_not_support_aggregation',
    0x00000049: 'pico_invalid_trigger_property',
    0x0000004A: 'pico_interface_not_connected',
    0x0000004B: 'pico_resistance_and_probe_not_allowed',
    0x0000004C: 'pico_power_failed',
    0x0000004D: 'pico_siggen_waveform_setup_failed',
    0x0000004E: 'pico_fpga_fail',
    0x0000004F: 'pico_power_manager',
    0x00000050: 'pico_invalid_analogue_offset',
    0x00000051: 'pico_pll_lock_failed',
    0x00000052: 'pico_analog_board',
    0x00000053: 'pico_config_fail_awg',
    0x00000054: 'pico_initialise_fpga',
    0x00000056: 'pico_external_frequency_invalid',
    0x00000057: 'pico_clock_change_error',
    0x00000059: 'pico_pwq_and_external_clock_clash',
    0x0000005A: 'pico_unable_to_open_scaling_file',
    0x0000005B: 'pico_memory_clock_frequency',
    0x0000005D: 'pico_no_captures_available',
    0x0000005E: 'pico_not_used_in_this_capture_mode',
    0x00000103: 'pico_get_data_active',
    0x00000104: 'pico_ip_networked',
    0x00000105: 'pico_invalid_ip_address',
    0x00000106: 'pico_ipsocket_failed',
    0x00000107: 'pico_ipsocket_timedout',
    0x00000108: 'pico_settings_failed',
    0x00000109: 'pico_network_failed',
    0x0000010B: 'pico_invalid_ip_port',
    0x0000010C: 'pico_coupling_not_supported',
    0x0000010D: 'pico_bandwidth_not_supported',
    0x0000010E: 'pico_invalid_bandwidth',
    0x0000010F: 'pico_awg_not_supported',
    0x00000110: 'pico_ets_not_running',
    0x00000113: 'pico_invalid_digital_port',
    0x00000114: 'pico_invalid_digital_channel',
    0x00000115: 'pico_invalid_digital_trigger_direction',
    0x00000117: 'pico_ets_not_available_with_logic_channels',
    0x00000118: 'pico_warning_repeat_value',
    0x00000119: 'pico_power_supply_connected',
    0x0000011A: 'pico_power_supply_not_connected',
    0x0000011B: 'pico_power_supply_request_invalid',
    0x0000011C: 'pico_power_supply_undervoltage',
    0x0000011D: 'pico_capturing_data',
    0x0000011F: 'pico_not_supported_by_this_device',
    0x00000120: 'pico_invalid_device_resolution',
    0x00000121: 'pico_invalid_no_channels_for_resolution',
    0x00000122: 'pico_channel_disabled_due_to_usb_powered',
    0x00000123: 'pico_siggen_dc_voltage_not_configurable',
    0x00000124: 'pico_no_trigger_enabled_for_trigger_in_pre_trig',
    0x00000128: 'pico_awg_clock_frequency',
    0x00000129: 'pico_too_many_channels_in_use',
    0x0000012A: 'pico_null_conditions',
    0x0000012B: 'pico_duplicate_condition_source',
    0x0000012C: 'pico_invalid_condition_info',
    0x0000012D: 'pico_settings_read_failed',
    0x0000012E: 'pico_settings_write_failed',
    0x0000012F: 'pico_argument_out_of_range',
    0x00000130: 'pico_hardware_version_not_supported',
    0x00000131: 'pico_digital_hardware_version_not_supported',
    0x00000132: 'pico_analogue_hardware_version_not_supported',
    0x00000133: 'pico_unable_to_convert_to_resistance',
    0x00000134: 'pico_duplicated_channel',
    0x00000135: 'pico_invalid_resistance_conversion',
    0x00000136: 'pico_invalid_value_in_max_buffer',
    0x00000137: 'pico_invalid_value_in_min_buffer',
    0x00000138: 'pico_siggen_frequency_out_of_range',
    0x01000000: 'pico_device_time_stamp_reset',
    0x10000000: 'pico_watchdogtimer',
    0x10000001: 'undocumented: probably missing picoipp.dll'
}

def pico_error_string(err):
    if err in pico_error_strings:
        return pico_error_strings[err]
    else:
        return "unknown error ({})".format(err)