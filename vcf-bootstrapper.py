#!/usr/bin/env python

"""
Generate bootstrap replicate data sets of VCF file.

usage:
    python vcf-bootstrapper.py -i data_file.vcf -n number_of_replicates
"""

import os
import random
import shutil
import argparse

def read_input_file(file):
    """read input file and split into header and data"""
    header = []
    data = []
    with open(file, "r") as input:
        for line in input:
            if line.startswith("#"):
                header.append(line)
            else:
                data.append(line)
    return header, data

def generate_bootstrap_reps(data, Nreps):
    """generate N bootstrap replicates"""
    reps = {}
    for i in range(Nreps):
        # subsample with replacement
        d = [random.choice(data) for i in range(len(data))]
        reps[i] = d
    return reps

def write_to_file(head, reps):
    """write bootstrap replicates to file"""
    for k, v in reps.items():
        with open("replicate-{0}.vcf".format(str(k)), "w") as out:
            # write vcf header info
            for h in head:
                out.write(h)

            # write data
            for line in v:
                out.write(line)

def move_files_to_folder():
    """place replicates in folder"""
    reps_path = "../replicates/"
    os.makedirs(reps_path, exist_ok = True)
    [shutil.move(f, reps_path + f) for f in os.listdir() if f.endswith(".vcf")]

def parse_arguments():
    """command line requirments for script"""
    parser = argparse.ArgumentParser(description = "Get bootstrap replicates of vcf file.")
    parser.add_argument("-i", "--infile", type = str, required = True,
                        help = "Path to vcf file.")
    parser.add_argument("-n", "--Nreps", type = int, default = 100, required = True,
                        help = "Number of bootstrap replicates.")
    return parser.parse_args()

def main():
    args = parse_arguments()
    head, data = read_input_file(args.infile)
    reps = generate_bootstrap_reps(data, args.Nreps)
    write_to_file(head, reps)
    move_files_to_folder()

if __name__ == '__main__':
    main()
