CREATE TABLE IF NOT EXISTS users
(
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    email           TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    role            TEXT     DEFAULT 'donor',
    is_active       BOOLEAN  DEFAULT TRUE,
    is_superuser    BOOLEAN  DEFAULT FALSE,
    is_verified     BOOLEAN  DEFAULT FALSE,
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

CREATE TABLE IF NOT EXISTS page_visits
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    page_url    TEXT     NOT NULL,
    user_id     INTEGER,             -- Залишаємо NULL, якщо це гість
    session_id  TEXT     NOT NULL,   -- Унікальний ідентифікатор сесії браузера (UUID)
    visited_at  DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- Якщо користувач видаляє акаунт, ми не хочемо втрачати статистику відвідувань, 
    -- тому просто скидаємо user_id в NULL (анонімізуємо візит)
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
);

-- Корисно додати індекси для швидкодії, оскільки запити до лічильників будуть частими:
CREATE INDEX idx_page_url ON page_visits(page_url);
CREATE INDEX idx_user_id ON page_visits(user_id);