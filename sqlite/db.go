package sqlite

import (
	"database/sql"
	"errors"
	_ "github.com/mattn/go-sqlite3"
	"github.com/sirupsen/logrus"
)

type Database struct {
	Name     string
	Database *sql.DB
	Log      *logrus.Entry
}

type Query struct {
	Id      int
	ReqId   int64
	UserId  int
	Epsilon float64
	Delta   float64
}

func CreateDatabase(dbname string, log *logrus.Entry) *Database {
	db := Database{Name: dbname, Log: log}
	database, err := sql.Open("sqlite3", dbname+":mode=memory")
	db.checkErr(err)
	db.Database = database
	db.CreateUserTable()
	db.CreateSiteAccessTable()
	db.CreateQueryTable()
	return &db
}

func (db *Database) CreateUserTable() {
	statement, err := db.Database.Prepare("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, username VARCHAR(64) NOT NULL , salted_hash VARCHAR NOT NULL , budget_spent BIGINT, UNIQUE(username))")
	db.checkErr(err)
	_, err = statement.Exec()
	db.checkErr(err)
}

func (db *Database) InsertUser(username string, saltedHash string, budgetSpent int64) error {
	statement, err := db.Database.Prepare("INSERT INTO user (username, salted_hash, budget_spent) VALUES (?, ?, ?)")
	db.checkErr(err)
	if err != nil {
		return err
	}

	_, err = statement.Exec(username, saltedHash, budgetSpent)
	db.checkErr(err)
	if err != nil {
		return err
	}
	return nil
}

func (db *Database) GetUserWithUsername(username string) (int64, string, string, int64) {
	row := db.Database.QueryRow("SELECT * FROM user WHERE username=?", username)
	var id int64
	var name string
	var saltedpass string
	var budgetspent int64
	err := row.Scan(&id, &name, &saltedpass, &budgetspent)
	db.checkErr(err)
	return id, name, saltedpass, budgetspent
}

// TODO: add site query was sent to
func (db *Database) CreateQueryTable() {
	statement, err := db.Database.Prepare("CREATE TABLE IF NOT EXISTS query (id INTEGER PRIMARY KEY, req_id INTEGER, user_id INTEGER, epsilon REAL, delta REAL, FOREIGN KEY (user_id) REFERENCES user (id))")
	db.checkErr(err)
	_, err = statement.Exec()
	db.checkErr(err)
}

func (db *Database) InsertQuery(query Query) error {
	statement, err := db.Database.Prepare("INSERT INTO query (req_id, user_id, epsilon, delta) VALUES (?, ?, ?, ?)")
	db.checkErr(err)
	if err != nil {
		return err
	}

	_, err = statement.Exec(query.ReqId, query.UserId, query.Epsilon, query.Delta)
	db.checkErr(err)
	if err != nil {
		return err
	}
	return nil
}

func (db *Database) GetQueriesFromUser(userId int) ([]Query, error) {
	rows, err := db.Database.Query("SELECT * FROM query WHERE user_id=?", userId)
	db.checkErr(err)

	if err != nil {
		return []Query{}, err
	}

	lenRows := 0
	queries := []Query{}
	for rows.Next() {
		query := Query{}
		rows.Scan(&query.Id, &query.ReqId, &query.UserId, &query.Epsilon, &query.Delta)
		queries = append(queries, query)
		lenRows++
	}

	if lenRows == 0 {
		return []Query{}, errors.New("No queries from user")
	}

	return queries, nil
}

func (db *Database) CreateSiteAccessTable() {
	statement, err := db.Database.Prepare("CREATE TABLE IF NOT EXISTS site_access (id INTEGER PRIMARY KEY, site_id INTEGER, user_id INTEGER, FOREIGN KEY (user_id) REFERENCES user (id))")
	db.checkErr(err)
	_, err = statement.Exec()
	db.checkErr(err)
}

func (db *Database) checkErr(err error) {
	if err != nil {
		db.Log.Error(err.Error())
	}
}
