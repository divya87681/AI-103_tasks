INSERT INTO user_roles (user_id, role_name, is_active)
VALUES
    ('employee_001', 'Employee', TRUE),
    ('manager_001', 'Manager', TRUE),
    ('admin_001', 'Admin', TRUE)
ON CONFLICT (user_id) DO UPDATE
SET role_name = EXCLUDED.role_name,
    is_active = EXCLUDED.is_active;

INSERT INTO faqs (question, answer, required_role, is_active)
SELECT v.question, v.answer, v.required_role, TRUE
FROM (VALUES
    ('What are the office timings?',
     'Office hours are 9 AM to 6 PM.',
     'Employee'),
    ('What is the leave approval process?',
     'Leave requests must be submitted to the reporting manager.',
     'Manager'),
    ('How is database access managed?',
     'Database access must follow approved administrative procedures.',
     'Admin')
) AS v(question, answer, required_role)
WHERE NOT EXISTS (
    SELECT 1 FROM faqs f WHERE f.question = v.question
);
