import subprocess
import argparse
import pathlib



def split_pdf(pgnum_start, pgnum_stop, input_name, output_name):
    args = ["pdftk", input_name, "cat", f"{pgnum_start}-{pgnum_stop}",  
            "output", output_name]
    print(f"Running {repr(' '.join(args))}")
    return subprocess.Popen(args, stdout=subprocess.PIPE)



def split_all(pgnums, in_filename, out_filenames):
    processes = []

    for i in range(len(out_filenames)):
        start = pgnums[i]
        try:
            end = pgnums[i+1] - 1
        except IndexError:
            end = 'end'
        proc = split_pdf(start, end, in_filename, out_filenames[i])
        processes.append(proc)
        # print(start, end, out_filenames[i])


    for i, proc in enumerate(processes):
        print(i)
        out, err = proc.communicate()
        print(out, err)
        print("")

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("-F", "--outfolder", default = "./")
    parser.add_argument("-i", "--index", action="store_false")
    return parser.parse_args()


def load(filename, outfolder, use_index):
    f = pathlib.Path(filename)
    chapters_file = f.with_name(f.stem + "_chapters.txt")

    pg_nums = []
    out_filenames = []

    with open(chapters_file) as infile:
        txt = infile.read()
        lines = txt.split("\n") 
        offset = int(lines[0].split()[1])
        n = len(str(len(lines[1:-1])))

        if offset > 0:
            out_filenames.append(str(outfolder / f"{0:0>{n}}_introduction.pdf"))
            pg_nums.append(1)

        for i, line in enumerate(lines[1:-1]):
            pgnum, *name = line.split()

            
            pg_nums.append(int(pgnum) + offset)
            index = f"{i+1:0>{n}}_" if use_index else ""
            name = index + "_".join(n.lower() for n in name) + ".pdf"
            outfile = str(outfolder / name.replace(":", ""))
            out_filenames.append(outfile)

    return pg_nums, out_filenames 

def main():
    args = get_args()

    filename = args.filename
    outfolder = pathlib.Path(args.outfolder)

    pg_nums, out_filenames = load(filename, outfolder, args.index)
    split_all(pg_nums, filename, out_filenames)

if __name__ == "__main__":
    main()
