CREATE TABLE IF NOT EXISTS messages (
  id INT PRIMARY KEY,
  content VARCHAR(255) NOT NULL
);

INSERT INTO messages (id, content)
  VALUES (1, 'Hola mundo')
  ON DUPLICATE KEY UPDATE content = VALUES(content);
