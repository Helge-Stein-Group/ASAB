config = dict()

projectFolder = "<path to project>" # edited prior to publication
auxiliaryFolderHardware = "tests\\filesForTests"

config["utility"] = {"ASAB": projectFolder + "...\\ASAB", # edited prior to publication
                    "QmixSDK_python": projectFolder + "...\\QmixSDK\\lib\\python", # edited prior to publication
                    "QmixSDK": projectFolder + "...\\QmixSDK"} # edited prior to publication

config["balanceDriver"] = {"serialPort": "<COM port>",
                    "settings": {'baudrate': 115200, 'bytesize': 8, 'parity': 'N', 'stopbits': 1, 'xonxoff': False, 'dsrdtr': False, 'rtscts': False, 'timeout': 0, 'write_timeout': None, 'inter_byte_timeout': None},
                    "simulated": True},

config["balance"] = {"simulated": True}

config["CetoniDeviceDriver"] = {"availableSyringes": auxiliaryFolderHardware + "\\syringes_test.pck",
                    "configPath": projectFolder + "...\\ASAB_Conf1_sim", # edited prior to publication
                    "syringeConfig": {"A0.0": "1_ml", "B0.0": "2_5_ml", "C0.0": "2_5_ml", "D0.0": "2_5_ml", "E0.0": "2_5_ml", "F0.0": "2_5_ml"},
                    "pumps": auxiliaryFolderHardware + "\\Pumps_test.pck",
                    "valves": auxiliaryFolderHardware + "\\Valves_test.pck",
                    "channels": auxiliaryFolderHardware + "\\Channels_test.pck",
                    "valvePositionDict": auxiliaryFolderHardware + "\\valvePositionDict_test.pck",
                    "setup": auxiliaryFolderHardware + "\\setup_test.pck",
                    "flow": 0.03,
                    "simulateBalance": True,
                    "outputTarget": {"prepareCetoni": {"syringeParams": {"A0.0": {"params": "syringe(inner_diameter_mm=4.60659, max_piston_stroke_mm=60.0)", "volUnit": "unit(prefix=<UnitPrefix.milli: -3>, unitid=<VolumeUnit.litres: 68>)", "flowUnit": "unit(prefix=<UnitPrefix.milli: -3>, unitid=<VolumeUnit.litres: 68>, time_unitid=<TimeUnit.per_second: 1>)"},
                    "B0.0": {"params": "syringe(inner_diameter_mm=7.283659999999999, max_piston_stroke_mm=60.0)", "volUnit": "unit(prefix=<UnitPrefix.milli: -3>, unitid=<VolumeUnit.litres: 68>)", "flowUnit": "unit(prefix=<UnitPrefix.milli: -3>, unitid=<VolumeUnit.litres: 68>, time_unitid=<TimeUnit.per_second: 1>)"},
                    "C0.0": {"params": "syringe(inner_diameter_mm=7.283659999999999, max_piston_stroke_mm=60.0)", "volUnit": "unit(prefix=<UnitPrefix.milli: -3>, unitid=<VolumeUnit.litres: 68>)", "flowUnit": "unit(prefix=<UnitPrefix.milli: -3>, unitid=<VolumeUnit.litres: 68>, time_unitid=<TimeUnit.per_second: 1>)"},
                    "D0.0": {"params": "syringe(inner_diameter_mm=7.283659999999999, max_piston_stroke_mm=60.0)", "volUnit": "unit(prefix=<UnitPrefix.milli: -3>, unitid=<VolumeUnit.litres: 68>)", "flowUnit": "unit(prefix=<UnitPrefix.milli: -3>, unitid=<VolumeUnit.litres: 68>, time_unitid=<TimeUnit.per_second: 1>)"},
                    "E0.0": {"params": "syringe(inner_diameter_mm=7.283659999999999, max_piston_stroke_mm=60.0)", "volUnit": "unit(prefix=<UnitPrefix.milli: -3>, unitid=<VolumeUnit.litres: 68>)", "flowUnit": "unit(prefix=<UnitPrefix.milli: -3>, unitid=<VolumeUnit.litres: 68>, time_unitid=<TimeUnit.per_second: 1>)"},
                    "F0.0": {"params": "syringe(inner_diameter_mm=7.283659999999999, max_piston_stroke_mm=60.0)", "volUnit": "unit(prefix=<UnitPrefix.milli: -3>, unitid=<VolumeUnit.litres: 68>)", "flowUnit": "unit(prefix=<UnitPrefix.milli: -3>, unitid=<VolumeUnit.litres: 68>, time_unitid=<TimeUnit.per_second: 1>)"}},
                    "enabled": True,
                    "faultState": False,
                    "valvePos": 0},
                    "valveInit": {"target": ['actual_valve_position', 'get_device_name', 'get_device_property', 'get_error_message', 'get_no_of_valves', 'get_node_id', 'handle', 'lookup_by_device_index', 'lookup_by_name', 'number_of_valve_positions', 'read_last_error', 'read_last_error_code', 'set_communication_state', 'set_device_property', 'switch_valve_to_position']},
                    "pumpInit": {"target": ['aspirate', 'calibrate', 'clear_fault', 'dispense', 'enable', 'generate_flow', 'get_device_name', 'get_device_property', 'get_dosed_volume', 'get_error_message', 'get_fill_level', 'get_flow_is', 'get_flow_rate_max', 'get_flow_unit', 'get_no_of_pumps', 'get_node_id', 'get_position_counter_value', 'get_pump_name', 'get_syringe_param', 'get_target_volume', 'get_valve', 'get_volume_max', 'get_volume_unit', 'handle', 'has_valve', 'is_calibration_finished', 'is_enabled', 'is_in_fault_state', 'is_pumping', 'lookup_by_device_index', 'lookup_by_name', 'name', 'pump_volume', 'read_last_error', 'read_last_error_code', 'restore_position_counter_value', 'set_communication_state', 'set_device_property', 'set_fill_level', 'set_flow_unit', 'set_syringe_param', 'set_volume_unit', 'status', 'stop_all_pumps', 'stop_pumping', 'syringe']}}}

config["CetoniDevice"] = {"testInputFillSyringe": [{"pump": "A0.0", "volume": 0.3, "waste": "Reservoir7", "valvePos":{'V1': 5, 'V2': 4, 'V3': 3, 'V4': 9, 'V5': 7, 'V6': 8, 'Av': 3, 'Bv': 1, 'Cv': 0, 'Dv': 1, 'Ev': 0, 'Fv': 0}}],
                    "testInputMix":[{"mixRatio": {"Reservoir1": 0.150, "Reservoir2": 0.400, "Reservoir3": 0.600}, "waste": "Reservoir6", "gas": "Reservoir5"}]}

config["syringes"] = {"savePath": auxiliaryFolderHardware + "\\syringes_test.pck",
                    "testInput": {"testInit": [{"designation": "a", "innerDia": 12.0, "pistonStroke": 55.0}, {"designation": "2_5_ml", "innerDia": 7.28366, "pistonStroke": 60}]}}

config["graph"] = {"pathNodes": auxiliaryFolderHardware + "\\nodes_test.csv",
                    "pathEdges": auxiliaryFolderHardware + "\\edges_test.csv",
                    "pathTubing": auxiliaryFolderHardware + "\\tubing_match_test.csv",
                    "savePath": auxiliaryFolderHardware + "\\setup_test.pck",
                    "saveNameValvePositionDict": auxiliaryFolderHardware + "\\valvePositionDict_test.pck",
                    "pumpList": ["A0.0", "B0.0", "C0.0", "D0.0", "E0.0", "F0.0"],
                    "testInput": {"findClosest": {"node": "NMRout", "candidates": ["A0.0", "B0.0", "C0.0", "D0.0", "E0.0", "F0.0"]},
                        "checkConsistency": {"path_nodes": auxiliaryFolderHardware + "\\nodes_test.csv", "path_edges": auxiliaryFolderHardware + "\\edges_test.csv", "path_tubing_match": auxiliaryFolderHardware + "\\tubing_match_test.csv", "path_tubing_newEdge": auxiliaryFolderHardware + "\\tubing_newNodeNewEdge_test.csv"},
                        "drawGraph": {"nodes": [("V1.0", {"name": "V1.0", "position": (-1,0)}), ("V1.1", {"name": "V1.1", "position": (-1.19,-0.06)}), ("V1.2", {"name": "V1.2", "position":(-1.12,-0.16)}),
                        ("V1.3", {"name": "V1.3", "position":(-1,-0.2)}), ("V1.4", {"name": "V1.4", "position":(-0.88,-0.16)}), ("V6.6", {"name": "V6.6","position": (-5.81,0.06)}),
                        ("V5.6", {"name": "V5.6","position": (-4.81,0.06)}), ("V6.8", {"name": "V6.8","position": (-6,0.2)}), ("Ev1", {"name": "Ev1","position": (-0.4,-2.1)}),
                        ("Q+Chip3", {"name": "Q+Chip3","position": (-7.0,0.2)}), ("Q+Chip9", {"name": "Q+Chip9","position": (-7.1,-0.2)}), ("lambdaOUT", {"name": "lambdaOUT","position": (-8.1,0)}),
                        ("V1.5", {"name": "V1.5","position": (-0.81,-0.06)})],
                        "edges": [("V1.0", "V1.1", {"name": "0004-XX-1", "ends": "XX", "length": float(4.33), "diameter": float(0.5), "dead_volume": float(0.0116)}),
                        ("V1.1", "V1.0", {"name": "0004-XX-1", "ends": "XX", "length": float(4.33), "diameter": float(0.5), "dead_volume": float(0.0116)}),
                        ("V1.0", "V1.2", {"name": "0004-XX-2", "ends": "XX", "length": float(4.33), "diameter": float(0.5), "dead_volume": float(0.0116)}),
                        ("V1.2", "V1.0", {"name": "0004-XX-2", "ends": "XX", "length": float(4.33), "diameter": float(0.5), "dead_volume": float(0.0116)}),
                        ("V1.0", "V1.3", {"name": "0004-XX-3", "ends": "XX", "length": float(4.33), "diameter": float(0.5), "dead_volume": float(0.0116)}),
                        ("V1.3", "V1.0", {"name": "0004-XX-3", "ends": "XX", "length": float(4.33), "diameter": float(0.5), "dead_volume": float(0.0116)}),
                        ("V1.0", "V1.4", {"name": "0004-XX-4", "ends": "XX", "length": float(4.33), "diameter": float(0.5), "dead_volume": float(0.0116)}),
                        ("V1.4", "V1.0", {"name": "0004-XX-4", "ends": "XX", "length": float(4.33), "diameter": float(0.5), "dead_volume": float(0.0116)}),
                        ("V1.0", "V1.5", {"name": "0004-XX-5", "ends": "XX", "length": float(4.33), "diameter": float(0.5), "dead_volume": float(0.0116)}),
                        ("V1.5", "V1.0", {"name": "0004-XX-5", "ends": "XX", "length": float(4.33), "diameter": float(0.5), "dead_volume": float(0.0116)}),
                        ("V6.6", "Q+Chip9", {"name": "0588-FT-8", "ends": "FT", "length": float(588), "diameter": float(0.3), "dead_volume": float(0.0416)}),
                        ("Q+Chip9", "V6.6", {"name": "0588-FT-8", "ends": "FT", "length": float(588), "diameter": float(0.3), "dead_volume": float(0.0416)}),
                        ("V5.6", "Q+Chip3", {"name": "0592-FT-3", "ends": "FT", "length": float(592), "diameter": float(0.3), "dead_volume": float(0.0418)}),
                        ("Q+Chip3", "V5.6", {"name": "0592-FT-3", "ends": "FT", "length": float(592), "diameter": float(0.3), "dead_volume": float(0.0418)}),
                        ("V6.8", "lambdaOUT", {"name": "0640-CT-2", "ends": "CT", "length": float(640), "diameter": float(0.3), "dead_volume": float(0.0452)}),
                        ("lambdaOUT", "V6.8", {"name": "0640-CT-2", "ends": "CT", "length": float(640), "diameter": float(0.3), "dead_volume": float(0.0452)}),
                        ("Ev1", "V1.5", {"name": "0286-NT-1", "ends": "NT", "length": float(286), "diameter": float(0.3), "dead_volume": float(0.0202)}),
                        ("V1.5", "Ev1", {"name": "0286-NT-1", "ends": "NT", "length": float(286), "diameter": float(0.3), "dead_volume": float(0.0202)})],
                        "testpositions": {"V1.0": (-1,0), "V1.1": (-1.19,-0.06), "V1.2": (-1.12,-0.16), "V1.3": (-1,-0.2), "V1.4": (-0.88,-0.16), "V6.6": (-5.81,0.06), "V5.6": (-4.81,0.06),
                            "V6.8": (-6,0.2), "Ev1": (-0.4,-2.1), "Q+Chip3": (-7.0,0.2), "Q+Chip9": (-7.1,-0.2), "lambdaOUT": (-8.1,0), "V1.5": (-0.81,-0.06)}},
                        "getEdgeDict": {"nodelist": ['A0.0', 'A0.1', 'Av1', 'V1.1', 'V1.0', 'V2.0', 'V2.7', 'V3.0', 'V3.1', 'Reservoir1']},
                        "generateGraph": {"savePath": auxiliaryFolderHardware + "\\setup_generateGraph_test.pck"},
                        "getValveSettings": {"vPd": {"V1": {"V1.0": None, "V1.1": 0, "V1.2": 1, "V1.3": 2, "V1.4": 3, "V1.5": 4, "V1.6": 5, "V1.7": 6, "V1.8": 7, "V1.9": 8, "V1.10": 9},
                            "V2": {"V2.0": None, "V2.1": 0, "V2.2": 1, "V2.3": 2, "V2.4": 3, "V2.5": 4, "V2.6": 5, "V2.7": 6, "V2.8": 7, "V2.9": 8, "V2.10": 9},
                            "V3": {"V3.0": None, "V3.1": 0, "V3.2": 1, "V3.3": 2, "V3.4": 3, "V3.5": 4, "V3.6": 5, "V3.7": 6, "V3.8": 7, "V3.9": 8, "V3.10": 9},
                            "V4": {"V4.0": None, "V4.1": 0, "V4.2": 1, "V4.3": 2, "V4.4": 3, "V4.5": 4, "V4.6": 5, "V4.7": 6, "V4.8": 7, "V4.9": 8, "V4.10": 9},
                            "V5": {"V5.0": None, "V5.1": 0, "V5.2": 1, "V5.3": 2, "V5.4": 3, "V5.5": 4, "V5.6": 5, "V5.7": 6, "V5.8": 7, "V5.9": 8, "V5.10": 9},
                            "V6": {"V6.0": None, "V6.1": 0, "V6.2": 1, "V6.3": 2, "V6.4": 3, "V6.5": 4, "V6.6": 5, "V6.7": 6, "V6.8": 7, "V6.9": 8, "V6.10": 9},
                            "Av": {"Av1": 1, "Av2": 0}, "Bv": {"Bv1": 1, "Bv2": 0}, "Cv": {"Cv1": 1, "Cv2": 0}, "Dv": {"Dv1": 1, "Dv2": 0}, "Ev": {"Ev1": 1, "Ev2": 0}, "Fv": {"Fv1": 1, "Fv2": 0}}},
                        "generateValvePositionDict": {"savePath": auxiliaryFolderHardware + "\\valvePositionDict_output.pck"},
                        "getValveFromName": {"names": ["V1.0", "V5.3", "V3.4", "V6.7", "V4.2", "V2.9", "V3.1", "V6.5", "V5.6", "V4.8", "V2.10"]},
                        "pathIsValid": {"path": {"wrong": ['A0.0', 'A0.1', 'Av1', 'V1.1', 'V1.0', 'V1.6', 'Fv1', 'F0.1', 'F0.0'], "correct": ['A0.0', 'A0.1', 'Av1', 'V1.1', 'V1.0', 'V2.0', 'V2.7', 'V3.0', 'V3.1', 'Reservoir1']}},
                        "getSystemStatus": auxiliaryFolderHardware + "\\setup_status_test.pck"},
                    "testOutput": {"findClosest":{"closest_target": "F0.0"},
                        "getEdgeDict": {"edgeDict_target": {"0215-NN-1": {"name": "0215-NN-1", "ends": "NN", "length": float(215), "diameter": float(0.3), "dead_volume": float(0.0152)},
                            "0000-XX-1": {"name": "0000-XX-1", "ends": "XX", "length": float(0), "diameter": float(0.6), "dead_volume": float(0.003)},
                            "0502-NT-1": {"name": "0502-NT-1", "ends": "NT", "length": float(502), "diameter": float(0.3), "dead_volume": float(0.0355)},
                            "0004-XX-1": {"name": "0004-XX-1", "ends": "XX", "length": float(4.33), "diameter": float(0.5), "dead_volume": float(0.0116)},
                            "0192-TT-1": {"name": "0192-TT-1", "ends": "TT", "length": float(192), "diameter": float(0.3), "dead_volume": float(0.0136)},
                            "0004-XX-17": {"name": "0004-XX-17", "ends": "XX", "length": float(4.33), "diameter": float(0.5), "dead_volume": float(0.0116)},
                            "0255-TT-1": {"name": "0255-TT-1", "ends": "TT", "length": float(255), "diameter": float(0.3), "dead_volume": float(0.018)},
                            "0004-XX-21": {"name": "0004-XX-21", "ends": "XX", "length": float(4.33), "diameter": float(0.5), "dead_volume": float(0.0116)},
                            "0476-CT-1": {"name": "0476-CT-1", "ends": "CT", "length": float(476), "diameter": float(0.3), "dead_volume": float(0.0336)}}},
                        "getValveFromName": {"valves": ["V1", "V5", "V3", "V6", "V4", "V2", "V3", "V6", "V5", "V4", "V2"]}}}