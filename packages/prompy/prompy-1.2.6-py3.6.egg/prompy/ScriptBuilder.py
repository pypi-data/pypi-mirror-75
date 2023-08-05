import importlib
import textwrap
import os

from prompy.ProcessDiscovery import *


def to_java_array(python_list, array_variable_name, help=False):
    if help:
        helpString = 'Takes the python list as input as return the Java code for initializing this list as a Java array.\n'
        helpString += 'Throws a ValueError if the value type in the list is not one of [str, int, float].\n'
        helpString += 'Variables declared:\n' \
                      ' - <array_variable_name>'
        print(helpString)
        return ''
    if len(python_list) == 0:
        return ''
    if type(python_list[0]).__name__ == 'str':
        return f'String[] {array_variable_name} = {{' + '"'.join(str(python_list)[1:-1].split("'")) + '};'
    elif type(python_list[0]).__name__ == 'int':
        return f'Integer[] {array_variable_name} = {{{str(python_list)[1:-1]}}};'
    elif type(python_list[0]).__name__ == 'float':
        return f'Double[] {array_variable_name} = {{{str(python_list)[1:-1]}}};'
    else:
        raise ValueError(f'{type(python_list[0]).__name__} type not supported.')


def visualize(j_component_variable_name, width, height, filename='', variable_prefix='', help=False):
    if help:
        helpString = 'Writes the visualization in the JComponent to a PNG file.\n'
        helpString += 'Variables declared:\n' \
                      ' - <variable_prefix>frame\n' \
                      ' - <variable_prefix>image\n'
        print(helpString)
        return ''
    if filename == '':
        cwd = '/'.join(os.getcwd().split('\\'))
        filename = f'{cwd}/temp.png'
    return f'''
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
JFrame {variable_prefix}frame = new JFrame();
frame.add({j_component_variable_name});
frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
frame.setSize({width}, {height});
frame.setVisible(true);
Thread.sleep(500);
BufferedImage {variable_prefix}image = new BufferedImage({width}, {height}, 1);
Graphics2D graphics2D = image.createGraphics();
frame.paint(graphics2D);
ImageIO.write(image, "png", new File("{filename}"));
'''


def end(help=False):
    if help:
        helpString = 'Exits the scripts'
        print(helpString)
        return ''
    return 'print("Done, exiting.");exit();'


def show_script(script_string, help=False):
    if help:
        helpString = 'Returns the script with aligned lines and a newline after each semicolon. It also includes the line numbers.'
        print(helpString)
        return ''
    script = textwrap.dedent(';\n'.join(script_string.split(';')))
    lines = script.split('\n')
    return '\n'.join([f'{i + 1:>3}: {line}' for i, line in enumerate(lines)])


def get_petrinet(petrinet_filename, from_variable=False, variable_prefix='', help=False):
    if help:
        helpString = 'Load the petrinet either from file <petrinet_filename> or previously declared variable name (when ' \
                     '<from_variable> is set to True).\n'
        helpString += 'Variables declared:\n' \
                      ' - <variable_prefix>_petrinetImportResult\n' \
                      ' - <variable_prefix>petrinet\n' \
                      ' - <variable_prefix>marking\n'
        print(helpString)
        return ''
    if from_variable:
        script_string = f'{variable_prefix}_petrinetImportResult = import_petri_net_from_pnml_file({petrinet_filename});'
    else:
        script_string = f'{variable_prefix}_petrinetImportResult = import_petri_net_from_pnml_file("{petrinet_filename}");'
    script_string += f'\n{variable_prefix}petrinet = {variable_prefix}_petrinetImportResult[0];'
    script_string += f'\n{variable_prefix}marking = {variable_prefix}_petrinetImportResult[1];'
    return script_string



def export_petrinet(net_variable_name, filename, help=False):
    if help:
        helpString = 'Export the petrinet to a file <filename>.'
        print(helpString)
        return ''
    return f'pnml_export_petri_net_({net_variable_name}, new File("{filename}"));'


def get_log(log_filename, from_variable=False, variable_prefix='', help=False):
    if help:
        helpString = 'Load the log either from file <log_filename> or previously declared variable name (when ' \
                     '<from_variable> is set to True).\n'
        helpString += 'Variables declared:\n' \
                      ' - <variable_prefix>log\n'
        print(helpString)
        return ''
    if from_variable:
      return f'{variable_prefix}log = open_xes_log_file({log_filename});'
    else:
      return f'{variable_prefix}log = open_xes_log_file("{log_filename}");'


def get_mapping(net_variable_name, log_variable_name, classifier='default', variable_prefix='', help=False):
    if help:
        helpString = 'Get the mapping between a petrinet and log, by either using the default or \'eventname\' classifier.\n'
        helpString += 'Variables declared:\n' \
                      ' - <variable_prefix>classifier\n' \
                      ' - <variable_prefix>eventClasses\n' \
                      ' - <variable_prefix>mapping\n'
        print(helpString)
        return ''
    imports = 'import org.processmining.plugins.connectionfactories.logpetrinet.TransEvClassMapping;'
    imports += '\nimport org.processmining.pnetreplayer.utils.TransEvClassMappingUtils;'
    imports += '\nimport org.processmining.log.utils.XUtils;'
    imports += '\nimport org.deckfour.xes.classification.XEventClasses;'
    imports += '\nimport org.deckfour.xes.classification.XEventClassifier;'
    imports += '\nimport org.deckfour.xes.classification.XEventNameClassifier;'
    if classifier == 'default':
        classifier = f'XEventClassifier {variable_prefix}classifier = XUtils.getDefaultClassifier({log_variable_name});'
    elif classifier == 'eventname':
        classifier = f'XEventClassifier {variable_prefix}classifier = new XEventNameClassifier();'
    else:
        raise NotImplementedError()
    event_classes = f'{variable_prefix}eventClasses = XEventClasses.deriveEventClasses({variable_prefix}classifier, {log_variable_name}).getClasses();\nSet activities = new HashSet({variable_prefix}eventClasses);'
    mapping = f'{variable_prefix}mapping = TransEvClassMappingUtils.getInstance().getMapping({net_variable_name}, activities, classifier);'
    return  '\n'.join([imports, classifier, event_classes, mapping])


def get_fitness(net_variable_name, log_variable_name, mapping_variable_name, event_classes_variable_name='eventClasses',
                parameter_variable_name=None, variable_prefix='', help=False):
    if help:
        helpString = 'Get the fitness of a petrinet to a log, both specified by their previously declared variable names. ' \
                     'The mapping between the petrinet and log have to be declared as well. The variable name specified by ' \
                     '<event_classes_variable_name> must match the one declared for creating the mapping. Option is to ' \
                     'include previously declared parameters by <parameter_variable_name>, if not specified, default parameters ' \
                     'are used.\n'
        helpString += 'Variables declared:\n' \
                      ' - <variable_prefix>algorithm\n' \
                      ' - <variable_prefix>parameters\n' \
                      ' - <variable_prefix>result\n'
        print(helpString)
        return ''
    imports = 'import org.processmining.plugins.astar.petrinet.PetrinetReplayerWithoutILP;'
    algorithm = f'{variable_prefix}algorithm = new PetrinetReplayerWithoutILP();'
    parameters = ''
    if parameter_variable_name is None:
        parameters = 'import org.processmining.plugins.petrinet.replayer.algorithms.costbasedcomplete.CostBasedCompleteParam;'
        parameters += f'{variable_prefix}parameters = new CostBasedCompleteParam({event_classes_variable_name}, {mapping_variable_name}.getDummyEventClass(), {net_variable_name}.getTransitions());'
    result = f'{variable_prefix}result = replay_a_log_on_petri_net_for_conformance_analysis({net_variable_name}, {log_variable_name}, {mapping_variable_name}, {variable_prefix}algorithm, {variable_prefix}parameters);'
    return '\n'.join([imports, algorithm, parameters, result])


def get_precision(net_variable_name, marking_variable_name, mapping_variable_name=None, log_variable_name=None,
                  alignment_result_variable_name=None, strategy='precgen', variable_prefix='', help=False):
    if help:
        helpString = 'Get the precision of a petrinet to a log, with the former specified by their previously declared variable names. ' \
                     'Two strategies are possible specified by <strategy>: precgen and eigenvalue_based. For precgen, ' \
                     'the mapping between the petrinet and log has to be declared as well, specified by <mapping_variable_name>. ' \
                     'Furthermore, the result from the fitness computation has to be declared as well, specified by ' \
                     '<alignment_result_variable_name>. For eigenvalue_based, the variable name of the log must be specified by ' \
                     '<log_variable_name>.\n'
        helpString += 'Variables declared:\n' \
                      ' - <variable_prefix>precGeneralization (in case of strategy=precgen)\n' \
                      ' - <variable_prefix>result\n'
        print(helpString)
        return ''
    if strategy == 'precgen':
        if mapping_variable_name is None:
            raise ValueError('mapping_variable_name missing.')
        script = 'import org.processmining.plugins.pnalignanalysis.conformance.AlignmentPrecGen;'
        script += f'\nAlignmentPrecGen {variable_prefix}precGeneralization = new AlignmentPrecGen();'
        script += f'\n{variable_prefix}result = {variable_prefix}precGeneralization.measureConformanceAssumingCorrectAlignment(null, {mapping_variable_name}, {alignment_result_variable_name}, {net_variable_name}, {marking_variable_name}, false);'
    elif strategy == 'eigenvalue_based':
        script = f'{variable_prefix}result = eigenvalue_based_precision_petrinet_({log_variable_name}, {net_variable_name});'
    return script



def get_conformance(net_variable_name, marking_variable_name, log_variable_name, classifier='default',
                    precision_strategy='precgen', variable_prefix='', help=False):
    if help:
        helpString = 'Get the conformance (fitness and precision) of a petrinet to a log. For more information, have a ' \
                     'look at the help documentation of get_fitness() and get_precision().\n'
        helpString += 'Variables declared:\n' \
                      ' - <variable_prefix>algorithm\n' \
                      ' - <variable_prefix>parameters\n' \
                      ' - <variable_prefix>precGeneralization (in case of strategy=precgen)\n' \
                      ' - <variable_prefix>_fitness_result\n' \
                      ' - <variable_prefix>_precision_result\n'
        print(helpString)
        return ''
    script = get_mapping(net_variable_name, log_variable_name, classifier, variable_prefix)
    script += get_fitness(net_variable_name, log_variable_name,  f'{variable_prefix}mapping', variable_prefix=f'{variable_prefix}_fitness_')
    script += get_precision(net_variable_name, marking_variable_name,  f'{variable_prefix}mapping',
                           alignment_result_variable_name=f'{variable_prefix}_fitness_result',
                           strategy=precision_strategy,
                           variable_prefix=f'{variable_prefix}_precision_')
    return script


def get_soundness(net_variable_name, reduce_model=True, variable_prefix='', help=False):
    if help:
        helpString = 'Get the soundness of a petrinet. For faster computation, the petrinet model is reduced first. This ' \
                     'can be avoided by setting <reduce_model> to False.\n'
        helpString += 'Variables declared:\n' \
                      ' - <variable_prefix>reducedModel (in case of reduce_model=True)\n' \
                      ' - <variable_prefix>woflanResult\n' \
                      ' - <variable_prefix>soundness\n'
        print(helpString)
        return ''
    script = ''
    if reduce_model:
        script += f'{variable_prefix}reducedModel = reduce_all_transitions_retain_sink_source_places({net_variable_name});'
        woflan_input = f'{variable_prefix}reducedModel'
    else:
        woflan_input = net_variable_name
    script += f'\n{variable_prefix}woflanResult = analyze_with_woflan({woflan_input});'
    script += f'\n{variable_prefix}soundness = {variable_prefix}woflanResult.isSound();'
    return script


def mine(log_filename, algorithm='alpha', settings={}, help=False):
    if help:
        helpString = 'Mine petrinet from the log specified by its filename. The process discovery algorithm to use is specified ' \
                     'by <algorithm> and should be one of [alpha, heuristics, inductive, ILP]. Furthermore, settings can be ' \
                     'specified by <settings>. The available settings for each algorithm is shown below:\n'
        helpString += 'alpha:\n'
        helpString += str(Alpha('', {}).available_settings)
        helpString += 'heuristics:\n'
        helpString += str(Heuristics('', {}).available_settings)
        helpString += 'inductive:\n'
        helpString += str(Inductive('', {}).available_settings)
        helpString += 'ILP:\n'
        helpString += str(ILP('', {}).available_settings)

        helpString += 'Variables declared:\n' \
                      ' - log\n' \
                      ' - classifier\n' \
                      ' - parameters (in case of algorithm=alpha/inductive)\n' \
                      ' - settings (in case of algorithm=ILP/heuristics)\n' \
                      ' - net_and_marking\n' \
                      ' - petrinet\n' \
                      ' - marking\n'
        print(helpString)
        return ''
    miner = None
    if algorithm == 'alpha':
        miner = Alpha(log_filename, settings)
    elif algorithm == 'heuristics':
        miner = Heuristics(log_filename, settings)
    elif algorithm == 'inductive':
        miner = Inductive(log_filename, settings)
    elif algorithm == 'ILP':
        miner = ILP(log_filename, settings)
    else:
        raise NotImplementedError()
    return miner.to_java()
