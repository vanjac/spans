import sys

def main():
    objpath = sys.argv[1]
    outpath = objpath.replace('.obj', '.is')
    with open(outpath, 'w') as outfile:
        outfile.write("\t.section\t.iwram\n")
        outfile.write("\t.align\t2\n\n")
        outfile.write("\t.global\tpoints_3d\n")
        outfile.write("points_3d:\n")
        with open(objpath) as objfile:
            num_v = 0
            while True:
                line = objfile.readline().strip()
                if line == '':
                    continue
                values = line.split(' ')
                if values[0] == 'v':
                    num_v += 1
                    x = float(values[1])
                    y = float(values[2])
                    z = float(values[3])
                    x = int(x * 256)
                    y = int(y * 256)
                    z = int(z * 256)
                    outfile.write("\t.word {0}; .word {1}; .word {2}\n"
                        .format(x, y, z))
                elif values[0] == 'f':
                    break
            outfile.write("\n\t.global\ttransformed_points\n")
            outfile.write("transformed_points:\n")
            for v in range(0, num_v):
                outfile.write("p{0}:\t.space\t8\n".format(v + 1))
            outfile.write("\n\t.global\tnum_points\n")
            outfile.write("num_points:\n")
            outfile.write("\t.word\t{0}\n\n".format(num_v))

            outfile.write("\t.global\ttriangles\n")
            outfile.write("triangles:\n")
            # start using line from previous
            while True:
                if line == '':
                    break
                values = line.split(' ')
                if values[0] == 'f':
                    a = int(values[1])
                    b = int(values[2])
                    c = int(values[3])
                    outfile.write("\t.word p{0}; .word p{1}; .word p{2}\n"
                        .format(a, b, c))
                line = objfile.readline().strip()
            outfile.write("\t.word 0\n")


if __name__ == "__main__":
    main()
