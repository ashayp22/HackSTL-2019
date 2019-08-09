with open("/Users/skylergao/Desktop/Selfie-dataset/selfie_dataset.txt") as readFile:
    with open("/Users/skylergao/Desktop/ImageSmiling.txt", 'w') as writeFile:
        for line in readFile:
            ls = list(line.split(" "))
            writeFile.write(ls[16])
            writeFile.write("\n")
            print("Recorded smiling for image", line[0])
