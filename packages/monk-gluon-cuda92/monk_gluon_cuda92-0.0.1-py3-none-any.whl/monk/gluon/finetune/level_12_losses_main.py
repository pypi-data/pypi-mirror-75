from monk.gluon.finetune.imports import *
from monk.system.imports import *

from monk.gluon.finetune.level_11_optimizers_main import prototype_optimizers


class prototype_losses(prototype_optimizers):
    '''
    Main class for all parameters in expert mode

    Args:
        verbose (int): Set verbosity levels
                        0 - Print Nothing
                        1 - Print desired details
    '''
    @accepts("self", verbose=int, post_trace=False)
    #@TraceFunction(trace_args=True, trace_rv=True)
    def __init__(self, verbose=1):
        super().__init__(verbose=verbose);


    ###############################################################################################################################################
    @accepts("self", weight=[list, type(np.array([1, 2, 3])), float, type(None)], batch_axis=int, post_trace=False)
    #@TraceFunction(trace_args=True, trace_rv=True)
    def loss_l1(self, weight=None, batch_axis=0):
        '''
        Select L1 Loss

        Args:
            weight (float): global scalar for weight loss
            batch_axis (int): Axis representing number of elements in the batch - N

        Returns:
            None
        '''
        self.system_dict = l1(self.system_dict, weight=weight, batch_axis=batch_axis);

        self.custom_print("Loss");
        self.custom_print("    Name:          {}".format(self.system_dict["hyper-parameters"]["loss"]["name"]));
        self.custom_print("    Params:        {}".format(self.system_dict["hyper-parameters"]["loss"]["params"]));
        self.custom_print("");
    ###############################################################################################################################################



    ###############################################################################################################################################
    @accepts("self", weight=[list, type(np.array([1, 2, 3])), float, type(None)], batch_axis=int, post_trace=False)
    #@TraceFunction(trace_args=True, trace_rv=True)
    def loss_l2(self, weight=1.0, batch_axis=0):
        '''
        Select L2 Loss

        Args:
            weight (float): global scalar for weight loss
            batch_axis (int): Axis representing number of elements in the batch - N

        Returns:
            None
        '''
        self.system_dict = l2(self.system_dict, weight=weight, batch_axis=batch_axis);

        self.custom_print("Loss");
        self.custom_print("    Name:          {}".format(self.system_dict["hyper-parameters"]["loss"]["name"]));
        self.custom_print("    Params:        {}".format(self.system_dict["hyper-parameters"]["loss"]["params"]));
        self.custom_print("");
    ###############################################################################################################################################



    ###############################################################################################################################################
    @accepts("self", weight=[list, type(np.array([1, 2, 3])), float, type(None)], batch_axis=int,
        axis_to_sum_over=int, label_as_categories=bool, label_smoothing=bool, post_trace=False)
    #@TraceFunction(trace_args=True, trace_rv=True)
    def loss_softmax_crossentropy(self, weight=None, batch_axis=0, axis_to_sum_over=-1, 
                                    label_as_categories=True, label_smoothing=False):
        '''
        Select soaftmax crossentropy Loss - Auto softmax before applying loss 

        Args:
            weight (float): global scalar for weight loss
            batch_axis (int): Axis representing number of elements in the batch - N
            axis_to_sum_over (int): Set as -1
            label_as_categories (bool): Fixed as True
            label_smoothing (bool): If True, label smoothning is applied.

        Returns:
            None
        '''
        self.system_dict = softmax_crossentropy(self.system_dict, weight=weight, batch_axis=batch_axis,
                                                axis_to_sum_over=axis_to_sum_over, label_as_categories=label_as_categories, 
                                                label_smoothing=label_smoothing);

        self.custom_print("Loss");
        self.custom_print("    Name:          {}".format(self.system_dict["hyper-parameters"]["loss"]["name"]));
        self.custom_print("    Params:        {}".format(self.system_dict["hyper-parameters"]["loss"]["params"]));
        self.custom_print("");
    ###############################################################################################################################################


    ###############################################################################################################################################
    @accepts("self", weight=[list, type(np.array([1, 2, 3])), float, type(None)], batch_axis=int,
        axis_to_sum_over=int, label_as_categories=bool, label_smoothing=bool, post_trace=False)
    #@TraceFunction(trace_args=True, trace_rv=True)
    def loss_crossentropy(self, weight=None, batch_axis=0, axis_to_sum_over=-1, 
                                    label_as_categories=True, label_smoothing=False):
        '''
        Select crossentropy Loss - Need to manually apply softmax

        Args:
            weight (float): global scalar for weight loss
            batch_axis (int): Axis representing number of elements in the batch - N
            axis_to_sum_over (int): Set as -1
            label_as_categories (bool): Fixed as True
            label_smoothing (bool): If True, label smoothning is applied.

        Returns:
            None
        '''
        self.system_dict = crossentropy(self.system_dict, weight=weight, batch_axis=batch_axis,
                                                axis_to_sum_over=axis_to_sum_over, label_as_categories=label_as_categories, 
                                                label_smoothing=label_smoothing);

        self.custom_print("Loss");
        self.custom_print("    Name:          {}".format(self.system_dict["hyper-parameters"]["loss"]["name"]));
        self.custom_print("    Params:        {}".format(self.system_dict["hyper-parameters"]["loss"]["params"]));
        self.custom_print("");
    ###############################################################################################################################################



    ###############################################################################################################################################
    @accepts("self", weight=[list, type(np.array([1, 2, 3])), float, type(None)], batch_axis=int, post_trace=False)
    #@TraceFunction(trace_args=True, trace_rv=True)
    def loss_sigmoid_binary_crossentropy(self, weight=None, batch_axis=0):
        '''
        Select sigmoid binary crossentropy Loss - Auto sigmoid before applying loss 

        Args:
            weight (float): global scalar for weight loss
            batch_axis (int): Axis representing number of elements in the batch - N

        Returns:
            None
        '''
        self.system_dict = sigmoid_binary_crossentropy(self.system_dict, weight=weight, batch_axis=batch_axis);

        self.custom_print("Loss");
        self.custom_print("    Name:          {}".format(self.system_dict["hyper-parameters"]["loss"]["name"]));
        self.custom_print("    Params:        {}".format(self.system_dict["hyper-parameters"]["loss"]["params"]));
        self.custom_print("");
    ###############################################################################################################################################



    ###############################################################################################################################################
    @accepts("self", weight=[list, type(np.array([1, 2, 3])), float, type(None)], batch_axis=int, post_trace=False)    
    #@TraceFunction(trace_args=True, trace_rv=True)
    def loss_binary_crossentropy(self, weight=None, batch_axis=0):
        '''
        Select binary crossentropy Loss - Need to manually apply sigmoid

        Args:
            weight (float): global scalar for weight loss
            batch_axis (int): Axis representing number of elements in the batch - N

        Returns:
            None
        '''
        self.system_dict = binary_crossentropy(self.system_dict, weight=weight, batch_axis=batch_axis);

        self.custom_print("Loss");
        self.custom_print("    Name:          {}".format(self.system_dict["hyper-parameters"]["loss"]["name"]));
        self.custom_print("    Params:        {}".format(self.system_dict["hyper-parameters"]["loss"]["params"]));
        self.custom_print("");
    ###############################################################################################################################################


    ###############################################################################################################################################
    @accepts("self", log_pre_applied=bool, weight=[list, type(np.array([1, 2, 3])), float, type(None)], 
        batch_axis=int, axis_to_sum_over=int, post_trace=False)
    #@TraceFunction(trace_args=True, trace_rv=True)
    def loss_kldiv(self, log_pre_applied=False, weight=None, batch_axis=0, axis_to_sum_over=-1):
        '''
        Select lkdiv Loss

        Args:
            weight (float): global scalar for weight loss
            batch_axis (int): Axis representing number of elements in the batch - N
            axis_to_sum_over (int): Set as -1
            log_pre_applied (bool): If set as False, then logarithmic function is auto applied over target variables

        Returns:
            None
        '''
        self.system_dict = kldiv(self.system_dict, weight=weight, batch_axis=batch_axis,
                                axis_to_sum_over=axis_to_sum_over, log_pre_applied=log_pre_applied);

        self.custom_print("Loss");
        self.custom_print("    Name:          {}".format(self.system_dict["hyper-parameters"]["loss"]["name"]));
        self.custom_print("    Params:        {}".format(self.system_dict["hyper-parameters"]["loss"]["params"]));
        self.custom_print("");
    ###############################################################################################################################################


    ###############################################################################################################################################
    @accepts("self", log_pre_applied=bool, weight=[list, type(np.array([1, 2, 3])), float, type(None)], 
        batch_axis=int, post_trace=False)
    #@TraceFunction(trace_args=True, trace_rv=True)
    def loss_poisson_nll(self, log_pre_applied=False, weight=None, batch_axis=0):
        '''
        Select poisson_nll Loss

        Args:
            weight (float): global scalar for weight loss
            batch_axis (int): Axis representing number of elements in the batch - N
            log_pre_applied (bool): If set as False, then logarithmic function is auto applied over target variables

        Returns:
            None
        '''
        self.system_dict = poisson_nll(self.system_dict, log_pre_applied=log_pre_applied,
                                        weight=weight, batch_axis=batch_axis);

        self.custom_print("Loss");
        self.custom_print("    Name:          {}".format(self.system_dict["hyper-parameters"]["loss"]["name"]));
        self.custom_print("    Params:        {}".format(self.system_dict["hyper-parameters"]["loss"]["params"]));
        self.custom_print("");
    ###############################################################################################################################################


    ###############################################################################################################################################
    @accepts("self", weight=[list, type(np.array([1, 2, 3])), float, type(None)], batch_axis=int,
        threshold_for_mean_estimator=[int, float], post_trace=False)
    #@TraceFunction(trace_args=True, trace_rv=True)
    def loss_huber(self, weight=None, batch_axis=0, threshold_for_mean_estimator=1):
        '''
        Select huber Loss

        Args:
            weight (float): global scalar for weight loss
            batch_axis (int): Axis representing number of elements in the batch - N
            threshold_for_mean_estimator (int): Threshold for trimmed mean estimator.

        Returns:
            None
        '''
        self.system_dict = huber(self.system_dict, threshold_for_mean_estimator=threshold_for_mean_estimator,
                                weight=weight, batch_axis=batch_axis);

        self.custom_print("Loss");
        self.custom_print("    Name:          {}".format(self.system_dict["hyper-parameters"]["loss"]["name"]));
        self.custom_print("    Params:        {}".format(self.system_dict["hyper-parameters"]["loss"]["params"]));
        self.custom_print("");
    ###############################################################################################################################################


    ###############################################################################################################################################
    @accepts("self", weight=[list, type(np.array([1, 2, 3])), float, type(None)], batch_axis=int,
        margin=[int, float], post_trace=False)
    #@TraceFunction(trace_args=True, trace_rv=True)
    def loss_hinge(self, weight=None, batch_axis=0, margin=1):
        '''
        Select hinge Loss

        Args:
            weight (float): global scalar for weight loss
            batch_axis (int): Axis representing number of elements in the batch - N
            margin (float): MArgin value.

        Returns:
            None
        '''
        self.system_dict = hinge(self.system_dict, margin=margin,
                                weight=weight, batch_axis=batch_axis);

        self.custom_print("Loss");
        self.custom_print("    Name:          {}".format(self.system_dict["hyper-parameters"]["loss"]["name"]));
        self.custom_print("    Params:        {}".format(self.system_dict["hyper-parameters"]["loss"]["params"]));
        self.custom_print("");
    ###############################################################################################################################################



    ###############################################################################################################################################
    @accepts("self", weight=[list, type(np.array([1, 2, 3])), float, type(None)], batch_axis=int,
        margin=[int, float], post_trace=False)
    #@TraceFunction(trace_args=True, trace_rv=True)
    def loss_squared_hinge(self, weight=None, batch_axis=0, margin=1):
        '''
        Select squared hinge Loss

        Args:
            weight (float): global scalar for weight loss
            batch_axis (int): Axis representing number of elements in the batch - N
            margin (float): MArgin value.

        Returns:
            None
        '''
        self.system_dict = squared_hinge(self.system_dict, margin=margin,
                                weight=weight, batch_axis=batch_axis);

        self.custom_print("Loss");
        self.custom_print("    Name:          {}".format(self.system_dict["hyper-parameters"]["loss"]["name"]));
        self.custom_print("    Params:        {}".format(self.system_dict["hyper-parameters"]["loss"]["params"]));
        self.custom_print("");
    ###############################################################################################################################################