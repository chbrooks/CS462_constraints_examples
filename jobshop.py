import collections
from ortools.sat.python import cp_model

## assume four machines: 0: gripper 1: camera 2: laser 3: chemsensor

## job 1: gripper 3 seconds, laser 1 second, camera 1 second, chem 2
## job 2: laser 2, chem 2, camera 2, gripper 4
## job 3: camera 2, gripper 2, camera 1, laser 3
## job 4: gripper 1, chem 2, camera 2, gripper 2

jobs = [
        [(0,3),(2,1), (1, 1), (3,2)],
        [(2,2),(3,2), (1, 2), (0,4)],
        [(1,2),(0,2), (1, 1), (2,3)],
        [(0,1),(3,2), (1, 2), (0,2)]
    ]

max_possible_time = sum(item[1] for job in jobs for item in job)

# Instantiate model and solver
model = cp_model.CpModel()
solver = cp_model.CpSolver()

task_dict = {}

machine_schedule = {}

## let's use named tuples.
task_tuple = collections.namedtuple('task_tuple', 'start end interval')

## create variables
for job_id, job in enumerate(jobs):
    for task_id, task in enumerate(job):
        device = task[0]
        duration = task[1]
        suffix = '_%i_%i' % (job_id, task_id)

        start_var = model.NewIntVar(0, max_possible_time, 'start' + suffix)
        end_var = model.NewIntVar(0, max_possible_time, 'end' + suffix)
        interval_var = model.NewIntervalVar(start_var, duration, end_var,
                                            'interval' + suffix)
        task_dict[job_id,task_id] = task_tuple(start=start_var,
                                                end=end_var,
                                               interval=interval_var)
        if device in machine_schedule :
            machine_schedule[device].append(interval_var)
        else :
            machine_schedule[device] = [interval_var]

## each machine can only do one job at a time.
for machine in range(3) :
    model.AddNoOverlap(machine_schedule[machine])

## set up job precedences
for job_id, job in enumerate(jobs):
    for task_id in range(len(job) - 1):
        model.Add(task_dict[job_id][task_id + 1].start >= task_dict[job_id][task_id].end)


obj_var = model.NewIntVar(0, max_possible_time, 'makespan')
model.AddMaxEquality(obj_var, [task_dict[job_id][len(job) - 1].end
        for job_id, job in enumerate(jobs)])
status = model.Minimize(obj_var)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print('Solution:')
else :
    print(status)

