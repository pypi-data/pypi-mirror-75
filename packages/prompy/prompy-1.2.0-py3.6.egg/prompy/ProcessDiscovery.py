class Miner:
    def __init__(self, log_filename, settings=None, variable_prefix=''):
        self.log_filename = log_filename
        self.settings.update(settings)
        self.variable_prefix = variable_prefix

    def to_java(self):
        raise NotImplementedError

    def _get_log(self):
        return f'System.out.println("Loading log");log = open_xes_log_file("{self.log_filename}");'

    def _get_classifier(self):
        return f'XEventClassifier classifier = new XEventNameClassifier();'

    def _get_imports(self):
        return 'import org.deckfour.xes.classification.XEventClassifier;import org.deckfour.xes.classification.XEventNameClassifier;'


class Alpha(Miner):
    def __init__(self, log_filename, settings=None, variable_prefix=''):
        self.available_settings = {
            'robust': {'causalThreshold':         float,
                       'noiseThresholdLeastFreq': float,
                       'noiseThresholdMostFreq':  float},
            'plus':   {'ignoreLengthOneLoops':    bool},
            'alphaVersion': ['CLASSIC', 'ROBUST', 'PLUS', 'PLUS_PLUS', 'SHARP', 'DOLLAR']
        }
        self.settings = {
            'alphaVersion': 'ROBUST'
        }
        super().__init__(log_filename, settings)

    def to_java(self):
        return f'''
{self._get_imports()}
{self._get_log()}
{self._get_classifier()}
{self.__get_settings()}
print("Mining model");
net_and_marking = alpha_miner(log, classifier, parameters);
petrinet = net_and_marking[0];
marking = net_and_marking[1];'''

    def __get_settings(self):
        alphaVersion = {
                'CLASSIC':   'AlphaRobustMinerParameters parameters = new AlphaRobustMinerParameters(AlphaVersion.CLASSIC);',
                'ROBUST':    'AlphaRobustMinerParameters parameters = new AlphaRobustMinerParameters(AlphaVersion.ROBUST);',
                'PLUS':      'AlphaPlusMinerParameters parameters = new AlphaPlusMinerParameters(AlphaVersion.PLUS);',
                'PLUS_PLUS': 'AlphaPlusMinerParameters parameters = new AlphaPlusMinerParameters(AlphaVersion.PLUS_PLUS);',
                'SHARP':     'AlphaPlusMinerParameters parameters = new AlphaPlusMinerParameters(AlphaVersion.SHARP);',
                'DOLLAR':    'AlphaPlusMinerParameters parameters = new AlphaPlusMinerParameters(AlphaVersion.DOLLAR);',
            }
        if 'robust' in self.settings:
            if not all([key in self.settings['robust'] for key in ['causalThreshold', 'noiseThresholdLeastFreq', 'noiseThresholdMostFreq']]):
                raise ValueError('Not all parameters specified (causalThreshold, noiseThresholdLeastFreq, noiseThresholdMostFreq)')
            arguments = f"{self.settings['robust']['causalThreshold']}, {self.settings['robust']['noiseThresholdLeastFreq']}, {self.settings['robust']['noiseThresholdMostFreq']}"
            parameters = f'AlphaRobustMinerParameters parameters = new AlphaRobustMinerParameters({arguments});'
        elif 'plus' in self.settings:
            if not all([key in self.settings['robust'] for key in ['causalThreshold', 'noiseThresholdLeastFreq', 'noiseThresholdMostFreq']]):
                raise ValueError('Not all parameters specified (causalThreshold, noiseThresholdLeastFreq, noiseThresholdMostFreq)')
            ignore_length_one_loops = 'true' if self.settings['plus']['ignoreLengthOneLoops'] else 'false'
            arguments = f"{self.settings['alphaVersion']}, {ignore_length_one_loops}"
            parameters = f'AlphaPlusMinerParameters parameters = new AlphaPlusMinerParameters({arguments});'
        else:
            parameters = alphaVersion[self.settings['alphaVersion']]

        return parameters

    def _get_imports(self):
        return f'''
{super(Alpha, self)._get_imports()}
import org.processmining.alphaminer.parameters.AlphaRobustMinerParameters;
import org.processmining.alphaminer.parameters.AlphaPlusMinerParameters;
import org.processmining.alphaminer.parameters.AlphaVersion;'''


class Inductive(Miner):
    def __init__(self, log_filename, settings=None):
        self.settings = {
            'parameters': 'imf',
            'noiseThreshold': 0.2
        }
        super().__init__(log_filename, settings)
        self.available_settings = {
            'parameters': ['imf', 'eks', 'im', 'ima', 'imc', 'imcpt', 'imfa', 'imflc', 'imfpt', 'imlc']
        }

    def to_java(self):
        return f'''
{self._get_imports()}
{self._get_log()}
{self.__get_settings()}
net_and_marking = mine_petri_net_with_inductive_miner_with_parameters(log, parameters);
petrinet = net_and_marking[0];
marking = net_and_marking[1];'''

    def __get_settings(self):
        self.settings['parameters'] = self.settings['parameters'].lower()
        if self.settings['parameters'] not in self.available_settings['parameters']:
            raise ValueError('Parameter not known.')
        script_lines = {
            'imf': 'import org.processmining.plugins.InductiveMiner.mining.MiningParametersIMf;parameters = new MiningParametersIMf();',
            'eks': 'import org.processmining.plugins.InductiveMiner.mining.MiningParametersEKS;parameters = new MiningParametersEKS();',
            'im': 'import org.processmining.plugins.InductiveMiner.mining.MiningParametersIM;parameters = new MiningParametersIM();',
            'ima': 'import org.processmining.plugins.InductiveMiner.mining.MiningParametersIMa;parameters = new MiningParametersIMa();',
            'imc': 'import org.processmining.plugins.InductiveMiner.mining.MiningParametersIMc;parameters = new MiningParametersIMc();',
            'imcpt': 'import org.processmining.plugins.InductiveMiner.mining.MiningParametersIMcpt;parameters = new MiningParametersIMcpt();',
            'imfa': 'import org.processmining.plugins.InductiveMiner.mining.MiningParametersIMfa;parameters = new MiningParametersIMfa();',
            'imflc': 'import org.processmining.plugins.InductiveMiner.mining.MiningParametersIMflc;parameters = new MiningParametersIMflc();',
            'imfpt': 'import org.processmining.plugins.InductiveMiner.mining.MiningParametersIMfpt;parameters = new MiningParametersIMfpt();',
            'imlc': 'import org.processmining.plugins.InductiveMiner.mining.MiningParametersIMlc;parameters = new MiningParametersIMlc();',
        }

        return script_lines[self.settings['parameters']]

    def _get_imports(self):
        return super(Inductive, self)._get_imports()


class ILP(Miner):
    def __init__(self, log_filename, settings=None):
        self.settings = {}
        self.available_settings = {}
        super().__init__(log_filename, settings)

    def to_java(self):
        return f'''
{self._get_imports()}
{self._get_log()}
{self._get_classifier()}
loginfo = XLogInfoFactory.createLogInfo(log);
{self.__get_settings()}
net_and_marking = ilp_miner(log, loginfo, settings);
petrinet = net_and_marking[0];
marking = net_and_marking[1];'''

    def __get_settings(self):
        return 'ILPMinerSettings settings = new ILPMinerSettings();'

    def _get_imports(self):
        return f'''
{super(ILP, self)._get_imports()}
import org.processmining.plugins.ilpminer.ILPMinerSettings;
import org.deckfour.xes.info.XLogInfoFactory;'''


class Heuristics(Miner):
    def __init__(self, log_filename, settings=None):
        self.settings = {
            'RELATIVE_TO_BEST_THRESHOLD': 0.05,
            'POSITIVE_OBSERVATIONS_THRESHOLD': 1,
            'DEPENDENCY_THRESHOLD': 0.90,
            'L1L_THRESHOLD': 0.90,
            'L2L_THRESHOLD': 0.90,
            'LONG_DISTANCE_THRESHOLD': 0.90,
            'DEPENDENCY_DIVISOR': 1,
            'AND_THRESHOLD': 0.10,
            'extraInfo': False,
            'useAllConnectedHeuristics': True,
            'useLongDistanceDependency': False
        }
        self.available_settings = {
            'RELATIVE_TO_BEST_THRESHOLD': float,
            'POSITIVE_OBSERVATIONS_THRESHOLD': float,
            'DEPENDENCY_THRESHOLD': float,
            'L1L_THRESHOLD': float,
            'L2L_THRESHOLD': float,
            'LONG_DISTANCE_THRESHOLD': float,
            'DEPENDENCY_DIVISOR': float,
            'AND_THRESHOLD': float,
            'extraInfo': bool,
            'useAllConnectedHeuristics': bool,
            'useLongDistanceDependency': bool
        }
        super().__init__(log_filename, settings)

    def to_java(self):
        return f'''
{self._get_imports()}
{self._get_log()}
{self._get_classifier()}
loginfo = XLogInfoFactory.createLogInfo(log);
{self.__get_settings()}
heuristicsNet = mine_for_a_heuristics_net_using_heuristics_miner(log, settings, loginfo);
net_and_marking = convert_heuristics_net_into_petri_net(heuristicsNet);
petrinet = net_and_marking[0];
marking = net_and_marking[1];'''

    def __get_settings(self):
        extra_info = 'true' if {self.settings['extraInfo']} else 'false'
        use_all_connected_heuristics = 'true' if {self.settings['useAllConnectedHeuristics']} else 'false'
        use_long_distance_dependency = 'true' if {self.settings['useLongDistanceDependency']} else 'false'
        return f'''
settings = new HeuristicsMinerSettings();
settings.setRelativeToBestThreshold({self.settings["RELATIVE_TO_BEST_THRESHOLD"]});
settings.setPositiveObservationThreshold({self.settings["POSITIVE_OBSERVATIONS_THRESHOLD"]});
settings.setDependencyThreshold({self.settings["DEPENDENCY_THRESHOLD"]});
settings.setL1lThreshold({self.settings["L1L_THRESHOLD"]});
settings.setL2lThreshold({self.settings["L2L_THRESHOLD"]});
settings.setLongDistanceThreshold({self.settings["LONG_DISTANCE_THRESHOLD"]});
settings.setDependencyDivisor({self.settings["DEPENDENCY_DIVISOR"]});
settings.setAndThreshold({self.settings["AND_THRESHOLD"]});
settings.setExtraInfo({extra_info});
settings.setUseAllConnectedHeuristics({use_all_connected_heuristics});
settings.setUseLongDistanceDependency({use_long_distance_dependency});
settings.setClassifier(classifier);'''

    def _get_imports(self):
        return f'''
{super(Heuristics, self)._get_imports()}
import org.deckfour.xes.info.XLogInfoFactory;
import org.processmining.plugins.heuristicsnet.miner.heuristics.miner.settings.HeuristicsMinerSettings;
'''

