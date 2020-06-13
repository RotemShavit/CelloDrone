# Changing the -----


def line_change(type, status):
        with open("indication.txt", "r") as fd:
                lines = fd.readlines()
        with open("indication.txt", "w") as fd:
                for line in lines:
                        if(type in line):
                                fd.write(type + ": " + status + "\n")
                        else:
                                fd.write(line)
        fd.close()

