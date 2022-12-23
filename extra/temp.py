
import helpers.csv_manipulator as manipulator

path = "output/"

csv = manipulator.read_csv("emnist-byclass-train-trimmed-letters-only.csv", path)
for record in csv:
    new_label = int(record[0]) - 10
    record[0] = new_label

print("writing new CSV file")
manipulator.write_csv("emnist-byclass-train-trimmed-letters-only2.csv", csv)
print("CSV file was created")
