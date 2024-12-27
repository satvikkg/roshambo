import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split .sdf file into N entries each.")
    parser.add_argument("sdffile", help="filename you want to split")
    parser.add_argument("-n", dest="N", metavar="N", type=int, default=10000, help="the max number of entries in each splitted file. default=10000")
    parser.add_argument("-v", dest="verbose", action="store_true", help="explain what is being done")
    args = parser.parse_args()

    file = args.sdffile
    filename, file_extension = os.path.splitext(file)
    N = args.N
    
    string = ""
    mol_count = 0;
    file_count = 0;
    for line in open(file):
        string += line
        if(line.startswith("$$$$")):
            mol_count += 1
            if(mol_count % N == 0):
                file_count += 1
                output = filename+"_"+str(file_count)+".sdf"
                file = open(output, "w");
                file.write(string);
                file.close();
                if args.verbose:
                    print("output : %s" % output)
                string = "";
            
    if(string != ""):
        file_count += 1
        file = open(filename+"_"+str(file_count)+".sdf", "w");
        file.write(string);
        file.close();

    print("%d compounds are divided into %d files." % (mol_count, file_count))
