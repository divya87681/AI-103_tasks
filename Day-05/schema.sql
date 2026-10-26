CREATE TABLE IF NOT EXISTS user_roles (
    user_id VARCHAR(100) PRIMARY KEY,
    role_name VARCHAR(20) NOT NULL
        CHECK (role_name IN ('Employee', 'Manager', 'Admin')),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS faqs (
    faq_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    required_role VARCHAR(20) NOT NULL
        CHECK (required_role IN ('Employee', 'Manager', 'Admin')),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS audit_logs (
    audit_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    faq_id INTEGER,
    action VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL
        CHECK (status IN ('SUCCESS', 'DENIED', 'NOT_FOUND', 'ERROR')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_faqs_required_role
    ON faqs (required_role);

CREATE INDEX IF NOT EXISTS idx_audit_logs_user_created
    ON audit_logs (user_id, created_at DESC);
