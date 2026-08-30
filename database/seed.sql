USE campus_reservation;

INSERT INTO resources
(name, type, description, location, capacity, status)
VALUES
(
    'Computer Lab 1',
    'LABORATORY',
    'Computer laboratory for student practical sessions.',
    'ICT Block',
    30,
    'AVAILABLE'
),
(
    'Computer Lab 2',
    'LABORATORY',
    'Computer laboratory with networked computers.',
    'ICT Block',
    25,
    'AVAILABLE'
),
(
    'Study Room A',
    'STUDY_ROOM',
    'Quiet study room for individual and group study.',
    'Library',
    8,
    'AVAILABLE'
),
(
    'Projector 1',
    'EQUIPMENT',
    'Portable projector for academic presentations.',
    'ICT Store',
    1,
    'AVAILABLE'
);