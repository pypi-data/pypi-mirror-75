import datetime
from typing import Callable, Optional, Any, Sequence, Dict, TYPE_CHECKING
if TYPE_CHECKING:
    from datacode.models.pipeline.combine import DataCombinationPipeline

from datacode.models.logic.combine import CombineFunction, combine_sources
from datacode.models.pipeline.operations.operation import DataOperation, OperationOptions
from datacode.models.source import DataSource


class CombineOperation(DataOperation):
    """
    Data operation that combines data from two DataSources
    """
    num_required_sources = 2
    options: 'CombineOptions'
    result: 'DataSource'

    def __init__(self, pipeline: 'DataCombinationPipeline',
                 data_sources: Sequence[DataSource], options: 'CombineOptions',
                 **result_kwargs):
        super().__init__(
            pipeline,
            data_sources,
            options,
            **result_kwargs
        )
        possible_last_modified = [source.last_modified for source in self.data_sources if source.last_modified]
        if possible_last_modified:
            self.options.last_modified = max(possible_last_modified)
        else:
            self.options.last_modified = None

    def _execute(self):
        ds = self.options.func(self.data_sources, **self.options.func_kwargs)
        self.result.update_from_source(ds)
        return self.result

    def summary(self, *summary_args, summary_method: str=None, summary_function: Callable=None,
                             summary_attr: str=None, **summary_method_kwargs):
        # TODO [#73]: better summary for DataCombinationPipeline
        print(f'Combining {self.data_sources[0]} with {self.data_sources[1]} with '
              f'options {self.options}')

    def describe(self):
        return self.summary()

    def __repr__(self):
        return f'<CombinationOperation(options={self.options})>'


class CombineOptions(OperationOptions):
    """
    Class for options passed to AnalysisOperations
    """
    op_class = CombineOperation

    def __init__(self, func: CombineFunction = combine_sources,
                 out_path: Optional[str] = None,
                 result_kwargs: Optional[Dict[str, Any]] = None,
                 always_rerun: bool = False,
                 **func_kwargs):
        """

        :param func: function which combines the DataSources
        :param out_path: location for generated DataSource
        :param func_kwargs: Keyword arguments to pass to the function which generates the DataSource
        :param always_rerun: Whether to re-run operation if executed multiple times
        """
        self.func = func
        self.func_kwargs = func_kwargs
        self.out_path = out_path
        self.result_kwargs = result_kwargs
        self.always_rerun = always_rerun
