from logical_formula import LogicalFormula


input_ = input("Enter expression: ").replace(' ', '')
tree = LogicalFormula()
try:
    tree.build(input_)
except ValueError as e:
    print(e)
    exit()
table = tree.truth_table()
for row in table:
    s = "\t".join(['1' if b else '0' for b in table[row]])
    print(f"{row.to_infix_form():^30}: {s}")

if fcnnf := tree.full_conjunctive_normal_numeric_form():
    s = " ,".join(map(str, fcnnf))
    print(f"({s})&")
    print(tree.full_conjunctive_normal_form())
else:
    print("No full conjunction normal form")
if fdnnf := tree.full_disjunctive_normal_numeric_form():
    s = " ,".join(map(str, fdnnf))
    print(f"({s})|")
    print(tree.full_disjunctive_normal_form())
else:
    print("No full disjunction normal form")

print(f"index: {tree.index_form()}")
