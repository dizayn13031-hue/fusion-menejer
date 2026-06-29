"""SQLite ma'lumotlar bazasi (aiosqlite)."""
import aiosqlite
from datetime import datetime
import config

_db: aiosqlite.Connection | None = None


async def init_db():
    global _db
    _db = await aiosqlite.connect(config.DB_PATH)
    _db.row_factory = aiosqlite.Row
    await _db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id     INTEGER PRIMARY KEY,
            full_name   TEXT,
            username    TEXT,
            role        TEXT DEFAULT 'employee',   -- 'admin' yoki 'employee'
            lang        TEXT DEFAULT NULL,        -- 'uz' yoki 'ru' (NULL = hali tanlanmagan)
            active      INTEGER DEFAULT 1,
            created_at  TEXT
        );

        CREATE TABLE IF NOT EXISTS tasks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            description TEXT,
            assignee_id INTEGER,
            creator_id  INTEGER,
            project_id  INTEGER,
            status      TEXT DEFAULT 'new',        -- new / in_progress / done / accepted / rejected
            deadline    TEXT,                       -- 'YYYY-MM-DD HH:MM' yoki NULL
            created_at  TEXT,
            done_at     TEXT,
            reminded    INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS reports (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER,
            text        TEXT,
            created_at  TEXT
        );

        CREATE TABLE IF NOT EXISTS issues (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            target_id   INTEGER,                    -- kimga tegishli (xodim)
            creator_id  INTEGER,                    -- admin
            project_id  INTEGER,
            text        TEXT,
            severity    TEXT DEFAULT 'normal',      -- low / normal / high
            status      TEXT DEFAULT 'open',        -- open / fixed
            created_at  TEXT,
            fixed_at    TEXT
        );

        CREATE TABLE IF NOT EXISTS attendance (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER,
            day         TEXT,                       -- 'YYYY-MM-DD'
            check_in    TEXT,
            check_out   TEXT
        );

        CREATE TABLE IF NOT EXISTS projects (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT UNIQUE,
            chat_id     INTEGER,                    -- bog'langan forum-guruh ID
            active      INTEGER DEFAULT 1,
            created_at  TEXT
        );

        CREATE TABLE IF NOT EXISTS topics (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id  INTEGER,
            kind        TEXT,                       -- tasks/issues/reports/general
            thread_id   INTEGER,                    -- forum topic message_thread_id
            title       TEXT,
            UNIQUE(project_id, kind)
        );

        -- "Design" guruhidagi MAVZU = LOYIHA biriktirish
        CREATE TABLE IF NOT EXISTS topic_projects (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id     INTEGER,
            thread_id   INTEGER,
            project_id  INTEGER,
            title       TEXT,
            UNIQUE(chat_id, thread_id)
        );

        -- Tayyor materiallar (vizual / video) jurnali
        CREATE TABLE IF NOT EXISTS deliverables (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id  INTEGER,
            user_id     INTEGER,
            user_name   TEXT,
            kind        TEXT,                       -- visual / video
            day         TEXT,
            created_at  TEXT
        );
        """
    )
    await _db.commit()


def db() -> aiosqlite.Connection:
    assert _db is not None, "init_db() chaqirilmagan"
    return _db


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


# ---------- FOYDALANUVCHILAR ----------
async def add_user(user_id, full_name, username, role="employee"):
    cur = await db().execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
    row = await cur.fetchone()
    if row:
        await db().execute(
            "UPDATE users SET full_name=?, username=? WHERE user_id=?",
            (full_name, username, user_id),
        )
    else:
        await db().execute(
            "INSERT INTO users(user_id, full_name, username, role, created_at) "
            "VALUES(?,?,?,?,?)",
            (user_id, full_name, username, role, now()),
        )
    await db().commit()


async def get_user(user_id):
    cur = await db().execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    return await cur.fetchone()


async def set_role(user_id, role):
    await db().execute("UPDATE users SET role=? WHERE user_id=?", (role, user_id))
    await db().commit()


async def set_lang(user_id, lang):
    await db().execute("UPDATE users SET lang=? WHERE user_id=?", (lang, user_id))
    await db().commit()


async def set_active(user_id, active):
    await db().execute("UPDATE users SET active=? WHERE user_id=?", (active, user_id))
    await db().commit()


async def list_employees(active_only=True):
    q = "SELECT * FROM users WHERE role='employee'"
    if active_only:
        q += " AND active=1"
    q += " ORDER BY full_name"
    cur = await db().execute(q)
    return await cur.fetchall()


async def list_all_users():
    cur = await db().execute("SELECT * FROM users ORDER BY role, full_name")
    return await cur.fetchall()


# ---------- VAZIFALAR ----------
async def create_task(title, description, assignee_id, creator_id, deadline, project_id=None):
    cur = await db().execute(
        "INSERT INTO tasks(title, description, assignee_id, creator_id, deadline, project_id, created_at) "
        "VALUES(?,?,?,?,?,?,?)",
        (title, description, assignee_id, creator_id, deadline, project_id, now()),
    )
    await db().commit()
    return cur.lastrowid


async def get_task(task_id):
    cur = await db().execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    return await cur.fetchone()


async def update_task_status(task_id, status):
    done_at = now() if status in ("done", "accepted") else None
    if done_at:
        await db().execute(
            "UPDATE tasks SET status=?, done_at=? WHERE id=?", (status, done_at, task_id)
        )
    else:
        await db().execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
    await db().commit()


async def tasks_for_user(user_id, only_open=True):
    q = "SELECT * FROM tasks WHERE assignee_id=?"
    if only_open:
        q += " AND status IN ('new','in_progress','rejected')"
    q += " ORDER BY (deadline IS NULL), deadline"
    cur = await db().execute(q, (user_id,))
    return await cur.fetchall()


async def all_open_tasks():
    cur = await db().execute(
        "SELECT * FROM tasks WHERE status IN ('new','in_progress','done','rejected') "
        "ORDER BY (deadline IS NULL), deadline"
    )
    return await cur.fetchall()


async def tasks_pending_acceptance():
    cur = await db().execute(
        "SELECT * FROM tasks WHERE status='done' ORDER BY done_at"
    )
    return await cur.fetchall()


async def due_tasks_to_remind():
    """Deadline yaqin/o'tgan va hali eslatma yuborilmagan ochiq vazifalar."""
    cur = await db().execute(
        "SELECT * FROM tasks WHERE deadline IS NOT NULL AND reminded=0 "
        "AND status IN ('new','in_progress')"
    )
    return await cur.fetchall()


async def mark_reminded(task_id):
    await db().execute("UPDATE tasks SET reminded=1 WHERE id=?", (task_id,))
    await db().commit()


# ---------- HISOBOTLAR ----------
async def add_report(user_id, text):
    await db().execute(
        "INSERT INTO reports(user_id, text, created_at) VALUES(?,?,?)",
        (user_id, text, now()),
    )
    await db().commit()


async def reports_for_day(day=None):
    day = day or today()
    cur = await db().execute(
        "SELECT r.*, u.full_name FROM reports r LEFT JOIN users u ON u.user_id=r.user_id "
        "WHERE substr(r.created_at,1,10)=? ORDER BY r.created_at",
        (day,),
    )
    return await cur.fetchall()


# ---------- XATO / KAMCHILIKLAR ----------
async def add_issue(target_id, creator_id, text, severity, project_id=None):
    cur = await db().execute(
        "INSERT INTO issues(target_id, creator_id, text, severity, project_id, created_at) "
        "VALUES(?,?,?,?,?,?)",
        (target_id, creator_id, text, severity, project_id, now()),
    )
    await db().commit()
    return cur.lastrowid


async def get_issue(issue_id):
    cur = await db().execute("SELECT * FROM issues WHERE id=?", (issue_id,))
    return await cur.fetchone()


async def fix_issue(issue_id):
    await db().execute(
        "UPDATE issues SET status='fixed', fixed_at=? WHERE id=?", (now(), issue_id)
    )
    await db().commit()


async def open_issues_for_user(user_id):
    cur = await db().execute(
        "SELECT * FROM issues WHERE target_id=? AND status='open' ORDER BY created_at",
        (user_id,),
    )
    return await cur.fetchall()


async def all_open_issues():
    cur = await db().execute(
        "SELECT i.*, u.full_name FROM issues i LEFT JOIN users u ON u.user_id=i.target_id "
        "WHERE i.status='open' ORDER BY i.created_at"
    )
    return await cur.fetchall()


# ---------- DAVOMAT ----------
async def check_in(user_id):
    day = today()
    cur = await db().execute(
        "SELECT * FROM attendance WHERE user_id=? AND day=?", (user_id, day)
    )
    row = await cur.fetchone()
    if row and row["check_in"]:
        return row["check_in"], False  # allaqachon kelgan
    if row:
        await db().execute(
            "UPDATE attendance SET check_in=? WHERE id=?", (now(), row["id"])
        )
    else:
        await db().execute(
            "INSERT INTO attendance(user_id, day, check_in) VALUES(?,?,?)",
            (user_id, day, now()),
        )
    await db().commit()
    return now(), True


async def check_out(user_id):
    day = today()
    cur = await db().execute(
        "SELECT * FROM attendance WHERE user_id=? AND day=?", (user_id, day)
    )
    row = await cur.fetchone()
    if not row or not row["check_in"]:
        return None, False  # avval check-in qilmagan
    await db().execute(
        "UPDATE attendance SET check_out=? WHERE id=?", (now(), row["id"])
    )
    await db().commit()
    return now(), True


async def attendance_for_day(day=None):
    day = day or today()
    cur = await db().execute(
        "SELECT a.*, u.full_name FROM attendance a LEFT JOIN users u ON u.user_id=a.user_id "
        "WHERE a.day=? ORDER BY a.check_in",
        (day,),
    )
    return await cur.fetchall()


# ---------- LOYIHALAR ----------
async def seed_projects(names):
    cur = await db().execute("SELECT COUNT(*) c FROM projects")
    row = await cur.fetchone()
    if row["c"] == 0:
        for n in names:
            await db().execute(
                "INSERT OR IGNORE INTO projects(name, created_at) VALUES(?,?)",
                (n, now()),
            )
        await db().commit()


async def list_projects(active_only=True):
    q = "SELECT * FROM projects"
    if active_only:
        q += " WHERE active=1"
    q += " ORDER BY name"
    cur = await db().execute(q)
    return await cur.fetchall()


async def get_project(project_id):
    cur = await db().execute("SELECT * FROM projects WHERE id=?", (project_id,))
    return await cur.fetchone()


async def get_project_by_name(name):
    cur = await db().execute(
        "SELECT * FROM projects WHERE lower(name)=lower(?)", (name.strip(),)
    )
    return await cur.fetchone()


async def get_project_by_chat(chat_id):
    cur = await db().execute("SELECT * FROM projects WHERE chat_id=?", (chat_id,))
    return await cur.fetchone()


async def add_project(name):
    cur = await db().execute(
        "INSERT OR IGNORE INTO projects(name, created_at) VALUES(?,?)", (name, now())
    )
    await db().commit()
    return cur.lastrowid


async def link_project_chat(project_id, chat_id):
    # bir guruh faqat bitta loyihaga
    await db().execute("UPDATE projects SET chat_id=NULL WHERE chat_id=?", (chat_id,))
    await db().execute("UPDATE projects SET chat_id=? WHERE id=?", (chat_id, project_id))
    await db().commit()


async def set_topic(project_id, kind, thread_id, title):
    await db().execute(
        "INSERT INTO topics(project_id, kind, thread_id, title) VALUES(?,?,?,?) "
        "ON CONFLICT(project_id, kind) DO UPDATE SET thread_id=excluded.thread_id, "
        "title=excluded.title",
        (project_id, kind, thread_id, title),
    )
    await db().commit()


async def get_topic(project_id, kind):
    cur = await db().execute(
        "SELECT * FROM topics WHERE project_id=? AND kind=?", (project_id, kind)
    )
    return await cur.fetchone()


async def topics_for_project(project_id):
    cur = await db().execute(
        "SELECT * FROM topics WHERE project_id=?", (project_id,)
    )
    return await cur.fetchall()


# ---------- DESIGN GURUHI: MAVZU = LOYIHA ----------
async def bind_topic_project(chat_id, thread_id, project_id, title):
    await db().execute(
        "INSERT INTO topic_projects(chat_id, thread_id, project_id, title) VALUES(?,?,?,?) "
        "ON CONFLICT(chat_id, thread_id) DO UPDATE SET project_id=excluded.project_id, "
        "title=excluded.title",
        (chat_id, thread_id, project_id, title),
    )
    await db().commit()


async def get_topic_project(chat_id, thread_id):
    cur = await db().execute(
        "SELECT * FROM topic_projects WHERE chat_id=? AND thread_id=?", (chat_id, thread_id)
    )
    return await cur.fetchone()


# ---------- TAYYOR MATERIALLAR ----------
async def add_deliverable(project_id, user_id, user_name, kind):
    await db().execute(
        "INSERT INTO deliverables(project_id, user_id, user_name, kind, day, created_at) "
        "VALUES(?,?,?,?,?,?)",
        (project_id, user_id, user_name, kind, today(), now()),
    )
    await db().commit()


async def deliverables_summary(day=None):
    day = day or today()
    cur = await db().execute(
        "SELECT d.project_id, p.name AS project, d.kind, COUNT(*) AS cnt "
        "FROM deliverables d LEFT JOIN projects p ON p.id=d.project_id "
        "WHERE d.day=? GROUP BY d.project_id, d.kind ORDER BY p.name",
        (day,),
    )
    return await cur.fetchall()


async def deliverables_detail(day=None):
    day = day or today()
    cur = await db().execute(
        "SELECT d.*, p.name AS project FROM deliverables d "
        "LEFT JOIN projects p ON p.id=d.project_id "
        "WHERE d.day=? ORDER BY p.name, d.created_at",
        (day,),
    )
    return await cur.fetchall()
