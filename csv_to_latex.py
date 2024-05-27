import csv

FILE_NAME = "sample_lit_map.csv"
axis1_title = "Population"
axis1_length = 7
axis2_title = "Evaluation"
axis2_length = 4
axis3_title = "Intervention"
axis3_length = 5

colour = "purple"



def print_table(row, col, row_name, col_name):
    out_file = open("files/"+row_name+col_name+".txt","w")
    ## HACKY making table
    out_file.write("""
    \\begin{table}
    \centering
""")
    out_file.write("\\textbf{"+row_name+" vs " + col_name+"}\\\\ ")
    out_file.write("\\begin{tabular}{|p{10cm}|")
    for count in range(len(col)):
        out_file.write("p{9cm}|")
    out_file.write("}")
    out_file.write("\\hline")


    #Headers
    out_file.write("\t&\n")
    h_out = ""
    for c in col:
        h_out += "\t" + c + " &\n"
    #remove the last &
    h_out = h_out[:-2]
    out_file.write(h_out)
    out_file.write("\t\\\\ \hline\n")
    for r in row:
        r_out = "\t" + r + "&\n "
        for c in col:
            result = mappings[r].intersection(mappings[c])
            result = list(result)
            result.sort()
            c_out = ""
            for paper in result:
                c_out += " \cite{" + paper + "}"
            r_out += "\t" + c_out + "&\n"
        #need to take off the last &
        r_out = r_out[:-2]
        out_file.write(r_out)
        out_file.write("\t \\\\ \hline\n")

    out_file.write("""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



    \\end{tabular}
\\end{table}""")

    out_file.close()

def print_heatmap(row, col, row_name, col_name, total_keys):
    out_file = open("files/"+row_name+col_name+"_heatmap.txt","w")
    ## HACKY making table
    out_file.write("\\newcolumntype{P}[1]{>{\centering\\arraybackslash}p{#1}}")
    out_file.write("""
    \centering
""")
    out_file.write("\\textbf{"+row_name+" vs " + col_name+"}\\\\ ")
    out_file.write("\\begin{tabular}{|p{15cm}|")
    for count in range(len(col)):
        out_file.write("P{9cm}|")
    out_file.write("}")
    out_file.write("\\hline")


    #Headers
    out_file.write("\t&\n")
    h_out = ""
    for c in col:
        h_out += "\t" + c + " &\n"
    #remove the last &
    h_out = h_out[:-2]
    out_file.write(h_out)
    out_file.write("\t\\\\ \hline\n")
    for r in row:
        r_out = "\t" + r + "&\n "
        for c in col:
            result = mappings[r].intersection(mappings[c])
            c_out = ""
            c_out += "\cellcolor{"+colour+"!"+str(int((len(result)/total_keys)*100))+"}"
            c_out += str(len(result))
            r_out += "\t" + c_out + "&\n"
        #need to take off the last &
        r_out = r_out[:-2]
        out_file.write(r_out)
        out_file.write("\t \\\\ \hline\n")

    out_file.write("""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



    \\end{tabular}
""")

    out_file.close()


in_file = open(FILE_NAME,"r")
reader = csv.DictReader(in_file)

axis1_data = reader.fieldnames[1:axis1_length]
axis2_data = reader.fieldnames[axis1_length+1:axis1_length+axis2_length+1]
axis3_data = reader.fieldnames[axis1_length+axis2_length+1:]



mappings = {}
total_keys = 0
for row in reader:
    total_keys += 1
    for heading in row:
        if(row[heading] == "X"):
            if(heading in mappings):
                mappings[heading].add(row["key"])
            else:
                mappings[heading] = {row["key"]}
print_table(axis1_data, axis2_data, axis1_title, axis2_title)
print_table(axis2_data, axis3_data, axis2_title, axis3_title)
print_table(axis1_data, axis3_data, axis1_title, axis3_title)
print_heatmap(axis1_data, axis2_data, axis1_title, axis2_title, total_keys)
print_heatmap(axis2_data, axis3_data, axis2_title, axis3_title, total_keys)
print_heatmap(axis1_data, axis3_data, axis1_title, axis3_title, total_keys)


in_file.close()




