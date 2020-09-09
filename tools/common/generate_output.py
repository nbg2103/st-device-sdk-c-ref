#!/usr/bin/env python

import platform
import sys
import os
import time
import shutil
import subprocess

def generate_output(ref_path, bsp_name, app_name, output_file_list, debug_file_list):
    working_dir = os.getcwd()
    release_date = time.strftime("%Y%m%d", time.localtime(time.time()))

    os.chdir(ref_path)
    try:
        build_id_stdk = subprocess.check_output((['git', 'log', "--pretty=format:'%h'", "-n", "1"]))
    except:
        build_id_stdk = time.strftime("%H%M", time.localtime(time.time()))

    os.chdir(os.environ["STDK_CORE_PATH"])
    try:
        build_id_core = subprocess.check_output((['git', 'log', "--pretty=format:'%h'", "-n", "1"]))
    except:
        build_id_core = time.strftime("%H%M", time.localtime(time.time()))

    build_id = (build_id_stdk + "_" + build_id_core).replace("'", "")
    output_dir_name = "iotcore_" + app_name + "_" + release_date + "_" + build_id
    output_path = os.path.join(ref_path, "output", bsp_name, output_dir_name)

    shutil.rmtree(output_path, ignore_errors=True)
    os.makedirs(os.path.join(output_path, "debug"))

    for file in output_file_list:
        try:
            shutil.copy(file, output_path)
        except:
            print("WARN : fail to copy output file (" + file + ")")
    for file in debug_file_list:
        try:
            shutil.copy(file, os.path.join(output_path, "debug"))
        except:
            print("WARN : fail to copy output file (" + file + ")")

    build_info_file = open(os.path.join(output_path, "debug", "build_info.txt"), 'w')

    build_info_file.write(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(time.time())) + "\n")
    os.chdir(ref_path)
    build_info_file.write(ref_path + "\n")
    build_info_file.write("---------------------\n")
    build_info_file.write(subprocess.check_output(['git', 'branch', '-av']) + "\n")
    build_info_file.write("---------------------\n")
    build_info_file.write(subprocess.check_output(['git', 'status']) + "\n")
    build_info_file.write("---------------------\n")
    build_info_file.write(subprocess.check_output(['git', 'diff']) + "\n")
    build_info_file.write("---------------------\n")
    build_info_file.write(subprocess.check_output(['git', 'submodule', 'foreach', 'git', 'diff']) + "\n")
    build_info_file.close()

    print("-------------------------------------------------")
    print("binary path : " + output_path)
    print("-------------------------------------------------")
    os.chdir(working_dir)
