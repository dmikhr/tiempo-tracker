DROP TABLE IF EXISTS tasks;
CREATE TABLE tasks (
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE,
  description TEXT
);

DROP TABLE IF EXISTS work_blocks;
CREATE TABLE work_blocks (
  id INTEGER PRIMARY KEY,
  task_id INTEGER,
  start_time INTEGER,
  finish_time INTEGER,
  FOREIGN KEY (task_id) references tasks(id) ON DELETE CASCADE
);
