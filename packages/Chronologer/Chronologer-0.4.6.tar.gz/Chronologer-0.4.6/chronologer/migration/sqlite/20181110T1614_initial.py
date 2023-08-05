from yoyo import step


step(
  '''
    CREATE TABLE record (
      record_id INTEGER  PRIMARY KEY NOT NULL,
      name      TEXT     NOT NULL,  -- logger name
      ts        DATETIME NOT NULL,  -- UNIX timestamp
      level     INTEGER  NOT NULL,  -- record level
      message   TEXT,               -- record message
      logrec    JSON                -- record body
    )
  ''',
  '''
    DROP TABLE `record`
  '''
)

step(
  'CREATE INDEX level_name ON record(level, name)',
  'DROP INDEX level_name'
)

step(
  'CREATE INDEX ts ON record(ts)',
  'DROP INDEX ts'
)

