# Name: Kunal Mukherjee
# Personal email: kunmukh@GMAIL.COM
# Date: 6/25/21
# File name: 
# Project name:

from os import listdir
import re

base="C:\\Users\\kunmu\\Documents\\Kunal\\gitlab\\autoencoder\\data\\"
paths=[]


def main():
    all_files = [f for f in listdir(base)]

    print(all_files)

    for f in all_files:

        nd_file = [f for f in listdir(base+f) if "nd_" in f]

        r = open(base + f + "\\" + nd_file[0] + "\\" + "path_score.csv", "r")

        for x in r:
            if "Propagation-score" not in x:
                if "Average Merged Score" not in x:
                    paths.append([x.strip('\n')])

        sanitized_path = []

        for path in paths:
            sanitized_path.append([path[0].replace("<--", "")])

        with open(base + "benign-paragraph.csv", "w") as r:
            for path in sanitized_path:

                p = ' '.join(path).replace("[InetChannel]", "").replace("[Process]", "").replace("[File]", "")
                p2 = re.sub(r'\([^()]*\)', '', p)
                r.write(p2.split(",")[2] + "\n")


if __name__ == '__main__':
    main()