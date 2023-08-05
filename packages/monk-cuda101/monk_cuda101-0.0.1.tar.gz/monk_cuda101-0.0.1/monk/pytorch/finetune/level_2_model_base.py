from monk.pytorch.finetune.imports import *
from monk.system.imports import *
from monk.pytorch.finetune.level_1_dataset_base import finetune_dataset


class finetune_model(finetune_dataset):
    '''
    Base class for Model setup

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
    @accepts("self", path=[bool, str, list], post_trace=False)
    #@TraceFunction(trace_args=True, trace_rv=True)
    def set_model_final(self, path=False):
        '''
        Setup model based on set parameters

        Args:
            path (str): Dummy variable

        Returns:
            None
        '''
        self.custom_print("Model Details");
        if(self.system_dict["model"]["params"]["model_path"]):
            if(os.path.isfile(self.system_dict["model"]["params"]["model_path"])):
                self.custom_print("    Loading model - {}".format(self.system_dict["model"]["params"]["model_path"]));
                self.system_dict["local"]["model"] = load_model(self.system_dict, external_path=self.system_dict["model"]["params"]["model_path"]);
                self.system_dict = model_to_device(self.system_dict);
                self.custom_print("    Model loaded!");
                self.custom_print("");

                self.system_dict = get_num_layers(self.system_dict);

                self.system_dict["local"]["params_to_update"] = []
                layer_names = [];
                for name, param in self.system_dict["local"]["model"].named_parameters():
                    if param.requires_grad == True:
                        self.system_dict["local"]["params_to_update"].append(param);
                        lname = ".".join(name.split(".")[:-1]);
                        if lname not in layer_names:
                            layer_names.append(lname);
                self.system_dict["model"]["params"]["num_params_to_update"] = len(layer_names);
                self.system_dict["model"]["status"] = True;
                
            else:
                msg = "Model not found - {}\n".format(self.system_dict["model"]["params"]["model_path"]);
                msg += "Previous Training Incomplete.";
                raise ConstraintError(msg);

        
        elif(self.system_dict["states"]["eval_infer"]):
            if(os.path.isfile(self.system_dict["model_dir_relative"] + 'final')):
                self.custom_print("    Loading model - {}".format(self.system_dict["model_dir_relative"] + 'final'));
                self.system_dict["local"]["model"] = load_model(self.system_dict, final=True);
                self.system_dict = model_to_device(self.system_dict);
                self.custom_print("    Model loaded!");
                self.custom_print("");
            else:
                msg = "Model not found - {}\n".format(self.system_dict["model_dir_relative"] + 'final');
                msg += "Previous Training Incomplete.";
                raise ConstraintError(msg);
        else:
            if(self.system_dict["states"]["resume_train"]):
                if(os.path.isfile(self.system_dict["model_dir_relative"] + 'resume_state')):
                    self.custom_print("    Loading model - {}".format(self.system_dict["model_dir_relative"] + 'resume_state'));
                    self.system_dict["local"]["model"] = load_model(self.system_dict, resume=True);
                else:
                    msg = "Model not found - \"{}\"\n".format(self.system_dict["model_dir_relative"] + 'resume_state');
                    msg += "Training not started. Cannot Run resume Mode";
                    raise ConstraintError(msg);

            elif(self.system_dict["states"]["copy_from"]):
                model_path = self.system_dict["master_systems_dir_relative"] + self.system_dict["origin"][0] + "/" + self.system_dict["origin"][1] + "/output/models/";
                if(os.path.isfile(model_path + 'final')):
                    self.custom_print("    Loading model - {}".format(model_path + 'final'));
                    self.system_dict["local"]["model"] = load_model(self.system_dict, path=model_path, final=True);
                else:
                    msg = "Model not found - {}\n".format(model_path);
                    msg += "Previous Training Incomplete.";
                    raise ConstraintError(msg);

            else:
                self.custom_print("    Loading pretrained model");
                self.system_dict = setup_model(self.system_dict);


            
            self.system_dict = model_to_device(self.system_dict);
            self.custom_print("    Model Loaded on device");


            self.system_dict = get_num_layers(self.system_dict);

            self.system_dict["local"]["params_to_update"] = []
            layer_names = [];
            for name, param in self.system_dict["local"]["model"].named_parameters():
                if param.requires_grad == True:
                    self.system_dict["local"]["params_to_update"].append(param);
                    lname = ".".join(name.split(".")[:-1]);
                    if lname not in layer_names:
                        layer_names.append(lname);
            self.system_dict["model"]["params"]["num_params_to_update"] = len(layer_names);
            self.system_dict["model"]["status"] = True;

            
            if(self.system_dict["model"]["type"] == "custom"):
                self.custom_print("        Model name:                           {}".format("Custom Model"));
            else:
                self.custom_print("        Model name:                           {}".format(self.system_dict["model"]["params"]["model_name"]));
            self.custom_print("        Num layers in model:  {}".format(self.system_dict["model"]["params"]["num_layers"]));
            self.custom_print("        Num trainable layers: {}".format(self.system_dict["model"]["params"]["num_params_to_update"]));
            self.custom_print("");
            
    ###############################################################################################################################################