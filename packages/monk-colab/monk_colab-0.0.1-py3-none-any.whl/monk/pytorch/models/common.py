from monk.pytorch.models.imports import *
from monk.system.imports import *
from monk.pytorch.models.layers import get_layer


@accepts("self", bool, post_trace=False)
#@TraceFunction(trace_args=False, trace_rv=False)
def set_parameter_requires_grad(finetune_net, freeze_base_network):
    '''
    Freeze based network as per params set

    Args:
        finetune_net (network): Model network
        freeze_base_network (bool): If True, all trainable params are freezed

    Returns:
        network: Updated Model network
    '''
    if freeze_base_network:
        for param in finetune_net.parameters():
            param.requires_grad = False
    else:
        for param in finetune_net.parameters():
            param.requires_grad = True
    return finetune_net


@accepts(list, int, int, post_trace=False)
#@TraceFunction(trace_args=True, trace_rv=False)
def set_final_layer(custom_network, num_ftrs, num_classes):
    '''
    Setup final sub-network 

    Args:
        custom_network (list): List of dicts containing details on appeded layers to base netwoek in transfer learning
        num_ftrs (int): Number of features coming from base network's last layers
        num_classes (int): Number of classes in the dataset

    Returns:
        layer: Sequential sub-network with added layers 
    '''
    modules = [];
    for i in range(len(custom_network)):
        layer, num_ftrs = get_layer(custom_network[i], num_ftrs);
        modules.append(layer);
    sequential = nn.Sequential(*modules)
    return sequential;


@accepts("self", list, int, set=int, post_trace=False)
#@TraceFunction(trace_args=False, trace_rv=False)
def create_final_layer(finetune_net, custom_network, num_classes, set=1):
    '''
    Create final sub-network 

    Args:
        finetune_net (network): Initial base network
        custom_network (list):  List of dicts containing details on appeded layers to base netwoek in transfer learning
        num_classes (int): Number of classes in the dataset
        set (int): Select the right set to find the details of outermost layer

    Returns:
        network: Updated base network with appended custom additions
    '''
    if(set == 1):
        num_ftrs = finetune_net.classifier[6].in_features;
        finetune_net.classifier = set_final_layer(custom_network, num_ftrs, num_classes);
    elif(set == 2):
        num_ftrs = finetune_net.classifier.in_features;
        finetune_net.classifier = set_final_layer(custom_network, num_ftrs, num_classes);
    elif(set == 3):
        num_ftrs = finetune_net.fc.in_features;
        finetune_net.fc = set_final_layer(custom_network, num_ftrs, num_classes);
    elif(set == 4):
        num_ftrs = finetune_net.classifier[1].in_features;
        finetune_net.classifier = set_final_layer(custom_network, num_ftrs, num_classes);
    
    return finetune_net;



@accepts(dict, post_trace=False)
#@TraceFunction(trace_args=False, trace_rv=False)
def model_to_device(system_dict):
    '''
    Load model weights on device - cpu or gpu 

    Args:
        system_dict (dict): System dict containing system state and parameters

    Returns:
        dict: Updated system dict 
    '''
    if(system_dict["model"]["params"]["use_gpu"]):
        system_dict["local"]["device"] = torch.device("cuda:0" if torch.cuda.is_available() else "cpu");
        if(torch.cuda.is_available()):
            use_gpu = True;
            system_dict["model"]["params"]["use_gpu"] = use_gpu;
        else:
            use_gpu = False;
            system_dict["model"]["params"]["use_gpu"] = use_gpu;
    else:
        system_dict["local"]["device"] = torch.device("cpu");
    
    system_dict["local"]["model"] = system_dict["local"]["model"].to(system_dict["local"]["device"]);
    return system_dict;


@accepts(dict, post_trace=False)
#@TraceFunction(trace_args=False, trace_rv=False)
def print_grad_stats(system_dict):
    '''
    Print details on which layers are trainable

    Args:
        system_dict (dict): System dict containing system state and parameters

    Returns:
        None 
    '''
    print("Model - Gradient Statistics");
    i = 1;
    for name, param in system_dict["local"]["model"].named_parameters():
        if(i%2 != 0):
            print("    {}. {} Trainable - {}".format(i//2+1, name, param.requires_grad ));
        i += 1;
    print("");



@accepts(dict, post_trace=False)
#@TraceFunction(trace_args=False, trace_rv=False)
def get_num_layers(system_dict):
    '''
    Get number of potentially trainable layers

    Args:
        system_dict (dict): System dict containing system state and parameters

    Returns:
        dict: Updated system dict 
    '''
    num_layers = 0;
    layer_names = [];
    for param in system_dict["local"]["model"].named_parameters():
        lname = ".".join(param[0].split(".")[:-1]);
        if lname not in layer_names:
            layer_names.append(lname)

    num_layers = len(layer_names);
    system_dict["model"]["params"]["num_layers"] = num_layers;
    return system_dict;



@accepts(int, dict, post_trace=False)
#@TraceFunction(trace_args=False, trace_rv=False)
def freeze_layers(num, system_dict):
    '''
    Main function responsible to freeze layers in network

    Args:
        num (int): Number of layers to freeze
        system_dict (dict): System dict containing system state and parameters

    Returns:
        dict: Updated system dict 
    '''
    system_dict = get_num_layers(system_dict);
    num_layers_in_model = system_dict["model"]["params"]["num_layers"];
    if(num > num_layers_in_model):
        msg = "Parameter num > num_layers_in_model\n";
        msg += "Freezing entire network\n";
        msg += "TIP: Total layers: {}".format(num_layers_in_model);
        raise ConstraintError(msg)

    current_num = 0;
    value = False;

    layer_names = [];
    for name,param in system_dict["local"]["model"].named_parameters():
        param.requires_grad = value;
        lname = ".".join(name.split(".")[:-1]);
        if lname not in layer_names:
            layer_names.append(lname);
            current_num += 1;
        if(current_num == num):
            value = True;

    system_dict["local"]["params_to_update"] = []
    layer_names = [];
    for name, param in system_dict["local"]["model"].named_parameters():
        if param.requires_grad == True:
            system_dict["local"]["params_to_update"].append(param);
            lname = ".".join(name.split(".")[:-1]);
            if lname not in layer_names:
                layer_names.append(lname);
    system_dict["model"]["params"]["num_params_to_update"] = len(layer_names);
    system_dict["model"]["status"] = True;

    return system_dict;


@accepts(dict, list, post_trace=False)
#@TraceFunction(trace_args=False, trace_rv=False)
def get_layer_uid(network_stack, count):
    '''
    Get a unique name for layer in custom network development

    Args:
        network_stack (list): List of list containing custom network details
        count (dict): a unique dictionary mapping number of every type of layer in the network
        system_dict (dict): System dict containing system state and parameters

    Returns:
        str: layer unique name
        dict: updated layer type mapper count
    '''
    if network_stack["uid"]:
        return network_stack["uid"], count;
    else:
        index = layer_names.index(network_stack["name"]);
        network_name = names[index] + str(count[index]);
        count[index] += 1;
        return network_name, count;