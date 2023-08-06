# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.ml
#  Copyright (C) 2015-2020 Comet ML INC
#  This file can not be copied and/or distributed without the express
#  permission of Comet ML Inc.
# *******************************************************

import logging

import wrapt

from .._logging import check_module

LOGGER = logging.getLogger(__name__)
SCALE_LOSS_ORIGINAL = None


def tensor_backward(experiment, original, result, *args, **kwargs):
    # args[0] is self, the Tensor (loss):
    try:
        if experiment.curr_step is None:
            experiment.curr_step = 0
        else:
            experiment.curr_step += 1
        if experiment.log_graph and not experiment.disabled_monkey_patching:
            model = experiment._storage["torch"].get("model", None)
            if experiment.curr_step == 0 and model is not None:
                experiment._set_model_graph(model, framework="pytorch")
        if experiment.auto_metric_logging and not experiment.disabled_monkey_patching:
            ## Throttle report to every 10 batch updates:
            if experiment.curr_step % 10 == 0:
                if SCALE_LOSS_ORIGINAL is not None:
                    loss = SCALE_LOSS_ORIGINAL
                else:
                    loss = args[0]
                if len(loss.data.shape) == 0:
                    experiment._log_metric(
                        "loss",
                        loss.data.item(),
                        step=experiment.curr_step,
                        framework="pytorch",
                    )
                else:
                    experiment._log_metric(
                        "loss",
                        loss.data.mean().item(),
                        step=experiment.curr_step,
                        framework="pytorch",
                    )
    except Exception:
        LOGGER.info("Failed to run Tensor.backward logger", exc_info=True)
    return result


def model_constructor(experiment, original, *args, **kwargs):
    ## Assume the first one is the model:
    try:
        model = experiment._storage["torch"].get("model", None)
        if model is None:
            experiment._storage["torch"]["model"] = args[1]
    except Exception:
        LOGGER.info("Failed to run Module.__init__ logger", exc_info=True)


class CallableWrapper(wrapt.ObjectProxy):
    def __init__(self, wrapped, original_loss):
        super(CallableWrapper, self).__init__(wrapped)
        self.original_loss = original_loss

    def __enter__(self, *args, **kwargs):
        return_value = self.__wrapped__.__enter__(*args, **kwargs)

        global SCALE_LOSS_ORIGINAL
        SCALE_LOSS_ORIGINAL = self.original_loss

        return return_value

    def __exit__(self, *args, **kwargs):
        global SCALE_LOSS_ORIGINAL
        SCALE_LOSS_ORIGINAL = None

        return self.__wrapped__.__exit__(*args, **kwargs)


def scale_loss_hook(experiment, original, return_value, original_loss, *args, **kwargs):
    return CallableWrapper(return_value, original_loss)


def patch(module_finder):
    ## For testing:
    check_module("torch")

    ## For each backpropagation of the gradient:
    module_finder.register_after("torch.tensor", "Tensor.backward", tensor_backward)
    ## For each model constructor:
    module_finder.register_after(
        "torch.nn.modules.module", "Module.__init__", model_constructor
    )

    module_finder.register_after("apex.amp.handle", "scale_loss", scale_loss_hook)


check_module("torch")
