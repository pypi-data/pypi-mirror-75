import datetime
from copy import deepcopy
from typing import Sequence, List, Callable, Optional, Union, Dict

from graphviz import Digraph
from mixins import ReprMixin

from datacode.graph.base import GraphObject, Graphable, GraphFunction
from datacode.graph.edge import Edge
from datacode.graph.node import Node
from datacode.graph.subgraph import Subgraph
import datacode.hooks as hooks
from datacode.models.analysis import AnalysisResult
from datacode.models.links import LinkedItem
from datacode.models.pipeline.operations.operation import DataOperation, OperationOptions
from datacode.models.source import DataSource
from datacode.models.types import DataSourcesOrPipelines, DataSourceOrPipeline, ObjWithLastModified


class DataPipeline(LinkedItem, Graphable, ReprMixin):
    """
    Base class for data pipelines. Should not be used directly.
    """
    repr_cols = ['name', 'data_sources', 'operation_options']

    def __init__(self, data_sources: DataSourcesOrPipelines,
                 operation_options: Optional[Sequence[OperationOptions]],
                 name: Optional[str] = None, difficulty: float = 50):
        """

        :param data_sources:
        :param operation_options:
        :param name:
        """
        super().__init__()

        if operation_options is None:
            operation_options = []
        if data_sources is None:
            data_sources = []

        if not isinstance(data_sources, list):
            data_sources = list(data_sources)

        if not isinstance(operation_options, list):
            operation_options = list(operation_options)

        self.data_sources: List[DataSourceOrPipeline] = data_sources
        self.operation_options: List[OperationOptions] = operation_options
        self.name = name
        self.df = None
        self._operation_index = 0
        self.result = None
        self.difficulty = difficulty

    def execute(self, output: bool = True):
        hooks.on_begin_execute_pipeline(self)
        while True:
            try:
                self.next_operation()
            except LastOperationFinishedException:
                break

        self.result = self.operations[-1].result

        if output:
            self.output()

        hooks.on_end_execute_pipeline(self)
        return self.result

    def next_operation(self):
        if self._operation_index == 0:
            self._set_df_from_first_operation()

        self._do_operation()

    def reset(self, forward: bool = False):
        self.df = None
        self._operation_index = 0
        self._set_operations()
        if forward:
            for item in self.forward_links:
                item.reset(forward=True)

    def _do_operation(self):
        try:
            operation = self.operations[self._operation_index]
            print(f'Now running operation {self._operation_index + 1}: {operation}')
        except IndexError:
            raise LastOperationFinishedException

        operation.execute()

        # Set current df to result of merge
        if isinstance(operation.result, DataSource):
            # Need to check as may be analysis result, in which case df should not be changed
            self.df = operation.result.df

        self._operation_index += 1

    def _set_operations(self):
        self._operations = self._create_operations(self.data_sources, self.operation_options)

    def _create_operations(self, data_sources: DataSourcesOrPipelines, options_list: List[OperationOptions]):
        if options_list[0].op_class.num_required_sources == 0:
            operations = [options_list[0].get_operation(self, options_list[0])]
        elif options_list[0].op_class.num_required_sources == 1:
            operations = _get_operations_for_single(data_sources[0], options_list[0], self)
        elif options_list[0].op_class.num_required_sources == 2:
            operations = _get_operations_for_pair(data_sources[0], data_sources[1], options_list[0], self)
        else:
            raise ValueError('DataPipeline cannot handle operations with more than two sources')

        if len(options_list) == 1:
            return operations

        for i, options in enumerate(options_list[1:]):
            if options.op_class.num_required_sources == 0:
                operations.append(options.get_operation(self, options))
            elif options.op_class.num_required_sources == 1:
                operations += _get_operations_for_single(operations[-1].result, options, self)
            elif options.op_class.num_required_sources == 2:
                operations += _get_operations_for_pair(operations[-1].result, data_sources[i + 2], options, self)
            else:
                raise ValueError('DataPipeline cannot handle operations with more than two sources')

        return operations

    def _set_df_from_first_operation(self):
        # Need to check as may be generation pipeline which would not have a df to start from
        if hasattr(self.operations[0], 'data_sources') and self.operations[0].data_sources:
            self.df = self.operations[0].data_sources[0].df

    @property
    def operations(self) -> List[DataOperation]:
        try:
            return self._operations
        except AttributeError:
            self._set_operations()

        return self._operations

    # Following properties exist to recreate operations if data sources or merge options are overridden
    # by user

    @property
    def data_sources(self) -> List[DataSourceOrPipeline]:
        return self._data_sources

    @data_sources.setter
    def data_sources(self, data_sources: List[DataSourceOrPipeline]):
        self._data_sources = data_sources
        if data_sources is not None:
            for ds in data_sources:
                if ds is not None:
                    self._add_back_link(ds)
                    ds._add_forward_link(self)
        # only set operations if previously set. otherwise no need to worry about updating cached result
        if hasattr(self, '_operations'):
            self._set_operations()

    @property
    def operation_options(self):
        return self._operations_options

    @operation_options.setter
    def operation_options(self, options: List[OperationOptions]):
        self._operations_options = options
        # only set merges if previously set. otherwise no need to worry about updating cached result
        if hasattr(self, '_operations'):
            self._set_operations()

    def output(self):
        if self.result is None:
            return
        if isinstance(self.result, AnalysisResult):
            if not self.operation_options[-1].can_output:
                return
            self.operation_options[-1].analysis_output_func(self.result, self.operation_options[-1].out_path)
            return
        if not isinstance(self.result, DataSource):
            raise NotImplementedError(f'have not implemented pipeline output for type {type(self.result)}')
        if self.result.location is None:
            if not self.operation_options[-1].can_output:
                return
            self.result.location = self.operation_options[-1].out_path

        # By default, save calculated variables, unless user explicitly passes to not save them
        # Essentially setting the opposite default versus working directly with the DataSource since
        # usually DataSource calculations are done on loading and it is assumed if the pipeline result
        # is being saved at all then it is likely an expensive calculation which the user doesn't
        # want to repeat on every load
        if 'save_calculated' not in self.result.data_outputter_kwargs:
            extra_kwargs = dict(save_calculated=True)
        else:
            extra_kwargs = {}

        self.result.output(**extra_kwargs)

    def summary(self, *summary_args, summary_method: str=None, summary_function: Callable=None,
                             summary_attr: str=None, **summary_method_kwargs):
        for op in self.operations:
            op.summary(
                *summary_args,
                summary_method=summary_method,
                summary_function=summary_function,
                summary_attr=summary_attr,
                **summary_method_kwargs
            )

    def describe(self):
        for op in self.operations:
            op.describe()

    @property
    def last_modified(self) -> Optional[datetime.datetime]:
        # TODO [#95]: more efficient last_modified
        #
        # `last_modified` is calculated a lot and goes through the
        # entire pipeline each time. Caching the result of the
        # calculations will give a significant speed up, especially
        # in `DataExplorer.graph`. Need to handle updating the cache
        # whenever data sources or operations change, and somehow
        # also when OS modified time of file changes (fs events?).
        if any([obj.last_modified is None for obj in self.operations]):
            return None

        return max([source.last_modified for source in self._objs_with_last_modified])

    @property
    def pipeline_last_modified(self) -> Optional[datetime.datetime]:
        return self.last_modified

    @property
    def obj_last_modified(self) -> Optional[ObjWithLastModified]:
        if not self._objs_with_last_modified:
            return None
        most_recent_time = datetime.datetime(1900, 1, 1)
        most_recent_index = None
        for i, obj in enumerate(self._objs_with_last_modified):
            if obj.last_modified > most_recent_time:
                most_recent_time = obj.last_modified
                most_recent_index = i

        if most_recent_index is not None:
            return self._objs_with_last_modified[most_recent_index]

    @property
    def _objs_with_last_modified(self) -> List[ObjWithLastModified]:
        objs_with_last_modified: List[ObjWithLastModified]
        objs_with_last_modified = self.operations
        objs_with_last_modified = [obj for obj in objs_with_last_modified if obj.last_modified is not None]
        return objs_with_last_modified

    @property
    def allow_modifying_result(self) -> bool:
        return self.operation_options[-1].allow_modifying_result

    def touch(self):
        """
        Mark last_modified as now
        """
        for op in self.operations:
            # Don't mark last_modified on operations belonging to other pipelines
            if op.pipeline is self:
                op.last_modified = datetime.datetime.now()

    def copy(self):
        return deepcopy(self)

    def _graph_contents(self, include_attrs: Optional[Sequence[str]] = None,
                        func_dict: Optional[Dict[str, GraphFunction]] = None) -> List[GraphObject]:
        pn = self.primary_node(include_attrs, func_dict)
        elems = [pn]
        for source in self.data_sources:
            elems.extend(source._graph_contents(include_attrs, func_dict))
            edge = Edge(source.primary_node(include_attrs, func_dict), pn)
            elems.append(edge)
        return elems


class LastOperationFinishedException(Exception):
    pass


def _get_operations_for_single(data_source: DataSourceOrPipeline, options: OperationOptions,
                               current_pipeline: DataPipeline) -> List[DataOperation]:
    """
     Creates a list of DataOperation/subclass objects from a single DataSource or DataPipeline object
    :param data_source:
    :param options: Options for the main operation
    :return:
    """
    operations: List[DataOperation] = []
    final_operation_sources: List[DataSource] = []
    # Add any pipeline operations first, as the results from the pipeline must be ready before we can use the results
    # for other data sources or pipeline results operations
    if _is_data_pipeline(data_source):
        operations += data_source.operations  # type: ignore
        pipeline_result = data_source.operations[-1].result  # type: ignore
        # result of first pipeline will be first source in final operation
        final_operation_sources.append(pipeline_result)
    else:
        final_operation_sources.append(data_source)  # type: ignore

    # Add last (or only) operation
    operations.append(options.get_operation(current_pipeline, final_operation_sources, options))

    return operations


def _get_operations_for_pair(data_source_1: DataSourceOrPipeline, data_source_2: DataSourceOrPipeline,
                             options: OperationOptions, current_pipeline: DataPipeline) -> List[DataOperation]:
    """
    Creates a list of DataOperation/subclass objects from a paring of two DataSource objects, a DataSource and a
    DataPipeline, or two DataPipeline objects.
    :param data_source_1: DataSource or DataMergePipeline
    :param data_source_2: DataSource or DataMergePipeline
    :param options: Options for the main operation
    :return: list of DataOperation/subclass objects
    """
    operations: List[DataOperation] = []
    final_operation_sources: List[DataSource] = []
    # Add any pipeline operations first, as the results from the pipeline must be ready before we can use the results
    # for other data sources or pipeline results operations
    if _is_data_pipeline(data_source_1):
        operations += data_source_1.operations  # type: ignore
        pipeline_1_result = data_source_1.operations[-1].result  # type: ignore
        # result of first pipeline will be first source in final operation
        final_operation_sources.append(pipeline_1_result)
    else:
        final_operation_sources.append(data_source_1)  # type: ignore

    if _is_data_pipeline(data_source_2):
        operations += data_source_2.operations  # type: ignore
        # result of second pipeline will be second source in final operation
        pipeline_2_result = data_source_2.operations[-1].result # type: ignore
        final_operation_sources.append(pipeline_2_result)
    else:
        final_operation_sources.append(data_source_2)

    # Add last (or only) operation
    operations.append(options.get_operation(current_pipeline, final_operation_sources, options))

    return operations


def _is_data_pipeline(obj) -> bool:
    return hasattr(obj, 'data_sources') and hasattr(obj, 'operation_options')