# Search space transformations in permutation problems
 
| Problems | Transformations | Sampling |
|----------|-----------------|----------|
| QAP      | permutation     | ad-hoc-laplace |
| PFSP     | Vj              | no-restiction |
 
### Example of use
**Permutation search space and ad-hoc-laplace sampling:**

> python launcher.py -id 3 -i 400 -Pn QAP -Pp instances/QAP/tai20b.dat -Ps 200 -Sr 0.5 -s permutation -Sf ad-hoc-laplace -c True -d int8 -t 5000 -o db/QAP/ -m db/QAP/main.csv

## Dependencies
- Python3
- Matplotlib
- Numpy
