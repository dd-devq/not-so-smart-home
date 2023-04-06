DROP TABLE IF EXISTS user;

CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('privileged', 'unprivileged')) DEFAULT 'unprivileged'
);

DROP TABLE IF EXISTS device;

-- create table for devices
CREATE TABLE IF NOT EXISTS device (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  operating_period TEXT NOT NULL,
  state TEXT NOT NULL CHECK (state IN ('Fan', 'Light'))
);

DROP TABLE IF EXISTS fan;

-- create table for fans
CREATE TABLE IF NOT EXISTS fan (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	device_id INTEGER NOT NULL,
	rpm INTEGER NOT NULL,
	temperature INTEGER NOT NULL,
	state TEXT NOT NULL CHECK (state = 'Fan'),
	FOREIGN KEY (device_id) REFERENCES device(id) ON DELETE CASCADE,
	FOREIGN KEY (state) REFERENCES device(state) ON DELETE CASCADE
);

DROP TABLE IF EXISTS light;

-- create table for lights
CREATE TABLE IF NOT EXISTS light (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  device_id INTEGER NOT NULL,
  brightness INTEGER NOT NULL,
  color TEXT NOT NULL,
	state TEXT NOT NULL CHECK (state = 'Light'),
	FOREIGN KEY (device_id) REFERENCES device(id) ON DELETE CASCADE,
	FOREIGN KEY (state) REFERENCES device(state) ON DELETE CASCADE
);

DROP TABLE IF EXISTS user_device;

-- create table for user-device relationships
CREATE TABLE IF NOT EXISTS user_device (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  device_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
  FOREIGN KEY (device_id) REFERENCES device(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS room;

-- create table for rooms
CREATE TABLE IF NOT EXISTS room (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  roomtype TEXT NOT NULL,
  temperature INTEGER NOT NULL,
  humidity INTEGER NOT NULL,
  luminance INTEGER NOT NULL
);

DROP TABLE IF EXISTS room_device;

-- create table for room-device relationships
CREATE TABLE IF NOT EXISTS room_device (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  room_id INTEGER NOT NULL,
  device_id INTEGER NOT NULL,
  FOREIGN KEY (room_id) REFERENCES room(id) ON DELETE CASCADE,
  FOREIGN KEY (device_id) REFERENCES device(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS system_log;

-- create table for system log
CREATE TABLE IF NOT EXISTS system_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  contact TEXT NOT NULL,
  api_key TEXT NOT NULL,
  address TEXT NOT NULL
);

DROP TABLE IF EXISTS system_record;

-- create table for system record
CREATE TABLE IF NOT EXISTS system_record (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  device_id INTEGER NOT NULL,
  room_id INTEGER NOT NULL,
  system_log_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
  FOREIGN KEY (device_id) REFERENCES device(id) ON DELETE CASCADE,
  FOREIGN KEY (room_id) REFERENCES room(id) ON DELETE CASCADE,
  FOREIGN KEY (system_log_id) REFERENCES system_log(id) ON DELETE CASCADE
);
