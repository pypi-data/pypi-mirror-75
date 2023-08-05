import os
import sys

import psutil

from monk.gluon_prototype import prototype
from monk.compare_prototype import compare
from monk.pip_unit_tests.gluon.common import print_start
from monk.pip_unit_tests.gluon.common import print_status

import mxnet as mx
import numpy as np
from monk.gluon.losses.return_loss import load_loss


def test_layer_concatenate(system_dict):
    forward = True;

    test = "test_layer_concatenate";
    system_dict["total_tests"] += 1;
    print_start(test, system_dict["total_tests"])
    if(forward):
        try:
            gtf = prototype(verbose=0);
            gtf.Prototype("sample-project-1", "sample-experiment-1");


            network = [];
            network.append(gtf.convolution(output_channels=16, uid="conv1"));
            network.append(gtf.batch_normalization(uid="bn1"));
            network.append(gtf.relu(uid="relu1"));
            network.append(gtf.max_pooling(uid="pool1"));



            subnetwork = [];
            branch1 = [];
            branch1.append(gtf.convolution(output_channels=16, uid="conv3_1_1"));
            branch1.append(gtf.batch_normalization(uid="bn3_1_1"));
            branch1.append(gtf.convolution(output_channels=16, uid="conv3_1_2"));
            branch1.append(gtf.batch_normalization(uid="bn3_1_2"));

            branch2 = [];
            branch2.append(gtf.convolution(output_channels=16, uid="conv3_2_1"));
            branch2.append(gtf.batch_normalization(uid="bn3_2_1"));

            branch3 = [];
            branch3.append(gtf.identity(uid="identity1"))

            subnetwork.append(branch1);
            subnetwork.append(branch2);
            subnetwork.append(branch3);
            subnetwork.append(gtf.concatenate(uid="concat1"))


            network.append(subnetwork);



            network.append(gtf.convolution(output_channels=16, uid="conv4"));
            network.append(gtf.batch_normalization(uid="bn4"));
            network.append(gtf.relu(uid="relu3"));
            network.append(gtf.max_pooling(uid="pool4"));

            network.append(gtf.flatten(uid="flatten1"));
            network.append(gtf.fully_connected(units=1024, uid="fc1"));
            network.append(gtf.dropout(drop_probability=0.2, uid="dp1"));
            network.append(gtf.fully_connected(units=2, uid="fc2"));


            gtf.Compile_Network(network, use_gpu=False);

            x = np.random.rand(1, 1, 64, 64);
            x = mx.nd.array(x);
            y = gtf.system_dict["local"]["model"].forward(x);          

            system_dict["successful_tests"] += 1;
            print_status("Pass");

        except Exception as e:
            system_dict["failed_tests_exceptions"].append(e);
            system_dict["failed_tests_lists"].append(test);
            forward = False;
            print_status("Fail");
    else:
        system_dict["skipped_tests_lists"].append(test);
        print_status("Skipped");

    return system_dict
