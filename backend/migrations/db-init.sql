CREATE TABLE IF NOT EXISTS users
(
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    email           TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    role            TEXT     DEFAULT 'donor',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS campaigns
(
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    organizer_id   INTEGER NOT NULL,
    title          TEXT    NOT NULL,
    description    TEXT,
    target_amount  REAL    NOT NULL CHECK (target_amount > 0),
    current_amount REAL     DEFAULT 0,
    created_at     DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (organizer_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS transactions
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER NOT NULL,
    donor_id    INTEGER,
    amount      REAL    NOT NULL CHECK (amount > 0),
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    comment     TEXT,

    FOREIGN KEY (campaign_id) REFERENCES campaigns (id) ON DELETE CASCADE,
    FOREIGN KEY (donor_id) REFERENCES users (id) ON DELETE CASCADE
);