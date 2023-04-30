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
  dev_type TEXT NOT NULL CHECK (dev_type IN ('Fan', 'Light', 'Sensor'))
);

DROP TABLE IF EXISTS fan;

-- create table for fans
CREATE TABLE IF NOT EXISTS fan (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	device_id INTEGER NOT NULL,
	rpm INTEGER NOT NULL,
  fan_state TEXT NOT NULL,
	temperature INTEGER NOT NULL,
	dev_type TEXT NOT NULL CHECK (dev_type = 'Fan'),
	FOREIGN KEY (device_id) REFERENCES device(id) ON DELETE CASCADE,
	FOREIGN KEY (dev_type) REFERENCES device(dev_type) ON DELETE CASCADE
);

DROP TABLE IF EXISTS light;

-- create table for lights
CREATE TABLE IF NOT EXISTS light (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  device_id INTEGER NOT NULL,
  light_state TEXT NOT NULL,
  brightness INTEGER NOT NULL,
  color TEXT NOT NULL,
	dev_type TEXT NOT NULL CHECK (dev_type = 'Light'),
	FOREIGN KEY (device_id) REFERENCES device(id) ON DELETE CASCADE,
	FOREIGN KEY (dev_type) REFERENCES device(dev_type) ON DELETE CASCADE
);

DROP TABLE IF EXISTS sensor;

-- create table for sensor
CREATE TABLE IF NOT EXISTS sensor (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sensor_state TEXT NOT NULL,
  device_id INTEGER NOT NULL,
	type TEXT NOT NULL CHECK (type = 'Sensor'),
	FOREIGN KEY (device_id) REFERENCES device(id) ON DELETE CASCADE,
	FOREIGN KEY (type) REFERENCES device(type) ON DELETE CASCADE
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
  log TEXT,
  log_date DATE
);

DROP TABLE IF EXISTS system_record;

-- create table for system record
CREATE TABLE IF NOT EXISTS system_record (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  home_address TEXT NOT NULL,
  user_id INTEGER NOT NULL,
  device_id INTEGER NOT NULL,
  room_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
  FOREIGN KEY (device_id) REFERENCES device(id) ON DELETE CASCADE,
  FOREIGN KEY (room_id) REFERENCES room(id) ON DELETE CASCADE,
);
