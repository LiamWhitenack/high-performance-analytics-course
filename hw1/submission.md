# Submission

## I. `squeue` Command

```bash
squeue -u lwhit073
```


## IV. Node Names Used

The script was executed on:
**d4-w6420b-03**


## V. Table of `srun` Results

| Srun Arguments                 | Number of Nodes Used | Total Number of Tasks Executed | Maximum Tasks per Node |
| ------------------------------ | -------------------- | ------------------------------ | ---------------------- |
| `-N1 -n2`                      | 1                    | 2                              | 2                      |
| `-N2 -n4`                      | 2                    | 4                              | 2                      |
| `-N3 -n8`                      | 3                    | 8                              | 3                      |
| `-N3 -n15 --ntasks-per-node=5` | 3                    | 15                            | 5                      |

I had to change -N3 -n16 to -N3 -n15 because of an error
