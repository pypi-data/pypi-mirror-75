from monk.tf_keras_1.transforms.imports import *
from monk.system.imports import *

from monk.tf_keras_1.transforms.transforms import transform_color_jitter
from monk.tf_keras_1.transforms.transforms import transform_random_affine
from monk.tf_keras_1.transforms.transforms import transform_random_horizontal_flip
from monk.tf_keras_1.transforms.transforms import transform_random_rotation
from monk.tf_keras_1.transforms.transforms import transform_random_vertical_flip
from monk.tf_keras_1.transforms.transforms import transform_mean_subtraction
from monk.tf_keras_1.transforms.transforms import transform_normalize



@accepts(dict, list, post_trace=False)
#@TraceFunction(trace_args=False, trace_rv=False)
def set_transforms(system_dict, set_phases):
    '''
    Set transforms depending on the training, validation and testing phases.

    Args:
        system_dict (dict): System dictionary storing experiment state and set variables
        set_phases (list): Phases in which to apply the transforms.

    Returns:
        dict: updated system dict
    '''
    transforms_test = [];
    transforms_train = [];
    transforms_val = [];
    transformations = system_dict["dataset"]["transforms"];
    normalize = False;
    for phase in set_phases:
        tsf = transformations[phase];
        if(phase=="train"):
            train_status = True;
            val_status = False;
            test_status = False;
        elif(phase=="val"):
            train_status = False;
            val_status = True;
            test_status = False;
        else:
            train_status = False;
            val_status = False;
            test_status = True;

        for i in range(len(tsf)):
            name = list(tsf[i].keys())[0]
            input_dict = tsf[i][name];
            train = train_status;
            val = val_status;
            test = test_status;

            if(name == "ColorJitter"):
                system_dict = transform_color_jitter(
                    system_dict, 
                    input_dict["brightness"], input_dict["contrast"], input_dict["saturation"], input_dict["hue"],
                    train, val, test, retrieve=True
                    );
            elif(name == "RandomAffine"):
                system_dict = transform_random_affine(
                    system_dict, 
                    input_dict["degrees"], input_dict["translate"], input_dict["scale"], input_dict["shear"], 
                    train, val, test, retrieve=True
                    );
            elif(name == "RandomHorizontalFlip"):
                system_dict = transform_random_horizontal_flip(
                    system_dict, 
                    input_dict["p"],
                    train, val, test, retrieve=True
                    );
            elif(name == "RandomVerticalFlip"):
                system_dict = transform_random_vertical_flip(
                    system_dict, 
                    input_dict["p"],
                    train, val, test, retrieve=True
                    );
            elif(name == "RandomRotation"):
                system_dict = transform_random_rotation(
                    system_dict, 
                    input_dict["degrees"], 
                    train, val, test, retrieve=True
                    );
            elif(name == "MeanSubtraction"):
                system_dict = transform_mean_subtraction(
                    system_dict,
                    input_dict["mean"], 
                    train, val, test, retrieve=True
                    );
            elif(name == "Normalize"):
                system_dict = transform_normalize(
                    system_dict,
                    input_dict["mean"], input_dict["std"],
                    train, val, test, retrieve=True
                    );


    return system_dict;


