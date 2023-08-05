from monk.gluon.schedulers.imports import *
from monk.system.imports import *


@accepts(dict, post_trace=False)
#@TraceFunction(trace_args=False, trace_rv=False)
def load_scheduler(system_dict):
    '''
    Load schedulers for training state

    Args:
        system_dict (dict): System dictionary storing experiment state and set variables

    Returns:
        dict: updated system dict
    '''
    learning_rate_scheduler = system_dict["local"]["learning_rate_scheduler"];
    num_batches = len(system_dict["local"]["data_loaders"]["train"]);
    learning_rate = system_dict["hyper-parameters"]["learning_rate"];
    if(learning_rate_scheduler == "steplr"):
        step_size = system_dict["hyper-parameters"]["learning_rate_scheduler"]["params"]["step_size"]
        if(step_size > system_dict["hyper-parameters"]["num_epochs"]):
            msg = "Step size - {} > Num epochs - {}\n".format(step_size, system_dict["hyper-parameters"]["num_epochs"]);
            msg += "Change scheduler step size";
            raise ConstraintError(msg);

        system_dict["local"]["learning_rate_scheduler"] = mx.lr_scheduler.FactorScheduler(
            step = system_dict["hyper-parameters"]["learning_rate_scheduler"]["params"]["step_size"]*num_batches, 
            factor=system_dict["hyper-parameters"]["learning_rate_scheduler"]["params"]["gamma"], 
            base_lr=learning_rate, 
            warmup_steps=0, warmup_begin_lr=0, warmup_mode='linear', stop_factor_lr=1e-08);

    elif(learning_rate_scheduler == "multisteplr"):
        max_step_size = max(system_dict["hyper-parameters"]["learning_rate_scheduler"]["params"]["milestones"])
        if(max_step_size > system_dict["hyper-parameters"]["num_epochs"]):
            msg = "Step size - {} > Num epochs - {}\n".format(max_step_size, system_dict["hyper-parameters"]["num_epochs"]);
            msg += "Change scheduler step size";
            raise ConstraintError(msg);

        steps = system_dict["hyper-parameters"]["learning_rate_scheduler"]["params"]["milestones"];
        milestones = system_dict["hyper-parameters"]["learning_rate_scheduler"]["params"]["milestones"];
        for i in range(len(steps)):
            steps[i] = steps[i]*num_batches

        
        system_dict["local"]["learning_rate_scheduler"] = mx.lr_scheduler.MultiFactorScheduler(
            step = steps,
            factor=system_dict["hyper-parameters"]["learning_rate_scheduler"]["params"]["gamma"],
            base_lr=learning_rate);

        #to make sure milestones value is restored to original one and not the updated steps while writing to experiment state
        #for i in range(len(steps)):
        #    steps[i] = steps[i]//num_batches

    return system_dict;