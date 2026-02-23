import numpy as np
import csv

def load_all_notes(filename):
    '''Load all notes from CSV file'''
    dt = [
        ('onset', np.float32),
        ('pitch', np.int32),
        # ('mPitch', np.int32),
        ('duration', np.float32),
        ('staff', np.int32),
        ('measure', np.int32),
        ('type', '<U4')
    ] # datatype

    # Format data as structured array
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader) # skip header

        rows = []
        for row in reader:
            filtered = [x for i, x in enumerate(row) if i != 2]

            rows.append((
                float(filtered[0]),
                int(float(filtered[1])),
                float(filtered[2]),
                int(float(filtered[3])),
                int(float(filtered[4])),
                filtered[5] if len(filtered) > 5 else ''
            ))

    notes = np.array(rows, dtype=dt)

    # Get unique notes irrespective of 'staffNum'
    _, unique_indices = np.unique(notes[['onset', 'pitch']], return_index=True)
    notes = notes[unique_indices]

    notes = notes[notes['duration'] > 0]
    return np.sort(notes, order=['onset', 'pitch'])