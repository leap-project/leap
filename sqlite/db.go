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

type User struct {
	Id			int64
	Name		string
	SaltedPass 	string
	BudgetSpent int64
}

// Creates an in-memory database used by the coordinator to
// retrieve and insert data
//
// dbname: Name to be given to the database
// log: Log from the coordinator.
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


// Creates a table used to hold Leap users and their login
// information.
//
// No args.
func (db *Database) CreateUserTable() {
	statement, err := db.Database.Prepare("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, username VARCHAR(64) NOT NULL , salted_hash VARCHAR NOT NULL , budget_spent BIGINT, UNIQUE(username))")
	db.checkErr(err)
	_, err = statement.Exec()
	db.checkErr(err)
}

func (db *Database) InsertUser(user *User) error {
	username := user.Name
	budgetSpent := user.BudgetSpent
	saltedHash := user.SaltedPass
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

func (db *Database) GetUserWithUsername(username string) *User {
	row := db.Database.QueryRow("SELECT * FROM user WHERE username=?", username)
	var id int64
	var name string
	var saltedpass string
	var budgetspent int64
	err := row.Scan(&id, &name, &saltedpass, &budgetspent)
	db.checkErr(err)
	user := User{id, name, saltedpass, budgetspent}
	return &user
}

// TODO: add site query was sent to
// Creates a table containing all the diff priv queries sent
// to Leap.
//
// No args.
func (db *Database) CreateQueryTable() {
	statement, err := db.Database.Prepare("CREATE TABLE IF NOT EXISTS query (id INTEGER PRIMARY KEY, req_id INTEGER, user_id INTEGER, epsilon REAL, delta REAL, FOREIGN KEY (user_id) REFERENCES user (id))")
	db.checkErr(err)
	_, err = statement.Exec()
	db.checkErr(err)
}

// Inserts a new query to the table
//
// query: Query struc containing the eps and delta values
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

// Returns all queries from the user with the given ID.
//
// userId: Id of the user to return queries
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

// Creates a table that contains the sites a user has access to.
//
// No args.
func (db *Database) CreateSiteAccessTable() {
	statement, err := db.Database.Prepare("CREATE TABLE IF NOT EXISTS site_access (id INTEGER PRIMARY KEY, site_id INTEGER, user_id INTEGER, FOREIGN KEY (user_id) REFERENCES user (id))")
	db.checkErr(err)
	_, err = statement.Exec()
	db.checkErr(err)
}

// Logs an error.
//
// err: The error to be logged.
func (db *Database) checkErr(err error) {
	if err != nil {
		db.Log.Error(err.Error())
	}
}
