
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
  name TEXT UNIQUE NOT NULL,
  operating_period TEXT NOT NULL,
  dev_type TEXT NOT NULL CHECK (dev_type IN ('Fan', 'Light', 'Switch'))
);


DROP TABLE IF EXISTS fan;

-- create table for fans
CREATE TABLE IF NOT EXISTS fan (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	device_id INTEGER NOT NULL,
	rpm INTEGER NOT NULL,
  fan_state TEXT NOT NULL,
	temperature INTEGER NOT NULL,
	FOREIGN KEY (device_id) REFERENCES device(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS light;


-- create table for lights
CREATE TABLE IF NOT EXISTS light (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  device_id INTEGER NOT NULL,
  light_state TEXT NOT NULL,
  brightness INTEGER NOT NULL,
  color TEXT NOT NULL,
	FOREIGN KEY (device_id) REFERENCES device(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS switch;


-- create table for switch
CREATE TABLE IF NOT EXISTS switch (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  switch_state TEXT NOT NULL,
  device_id INTEGER NOT NULL,
	FOREIGN KEY (device_id) REFERENCES device(id) ON DELETE CASCADE
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
  room_type TEXT NOT NULL,
  temperature INTEGER NOT NULL,
  humidity INTEGER NOT NULL,
  luminance INTEGER NOT NULL
);

DROP TABLE IF EXISTS room_device;


-- create table for user-device relationships
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
  log_date DATE,
  log TEXT
);

CREATE TRIGGER IF NOT EXISTS insert_fan AFTER INSERT ON device
WHEN NEW.dev_type = 'Fan'
BEGIN
  INSERT INTO fan (device_id, rpm, fan_state, temperature)
  VALUES (NEW.id, 0, 'OFF', 0);
END;


CREATE TRIGGER IF NOT EXISTS insert_light AFTER INSERT ON device
WHEN NEW.dev_type = 'Light'
BEGIN
  INSERT INTO light (device_id, brightness, light_state, color)
  VALUES (NEW.id, 00, '00', '#FFFFFF');
END;


CREATE TRIGGER IF NOT EXISTS insert_switch AFTER INSERT ON device
WHEN NEW.dev_type = 'Switch'
BEGIN
  INSERT INTO switch (device_id, switch_state)
  VALUES (NEW.id, '000');
END;