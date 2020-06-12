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
	SiteId  int
	Epsilon float64
	Delta   float64
}

type User struct {
	Id          int64
	Name        string
	SaltedPass  string
	BudgetSpent int64
	Role        string
}

type Site struct {
	Id		int64
	Budget	float64
}

// Roles for users
const ADMIN = "admin"
const DP_ONLY = "dp_only"
const NON_DP = "non_dp"

type SiteAccess struct {
	Id     int
	SiteId int64
	UserId int64
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
	db.CreateSiteTable()
	db.CreateSiteAccessTable()
	db.CreateQueryTable()
	return &db
}

// Creates a table used to hold Leap users, their login
// information and their role.
//
// No args.
func (db *Database) CreateUserTable() {
	statement, err := db.Database.Prepare("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, username VARCHAR(64) NOT NULL , salted_hash VARCHAR NOT NULL, budget_spent BIGINT, role VARCHAR, UNIQUE(username))")
	db.checkErr(err)
	_, err = statement.Exec()
	db.checkErr(err)
}

// Inserts a new user to the table
//
// user: User struc containing the id, name, salted password hash, & budget spent
func (db *Database) InsertUser(user *User) error {
	username := user.Name
	budgetSpent := user.BudgetSpent
	saltedHash := user.SaltedPass
	role := user.Role
	statement, err := db.Database.Prepare("INSERT INTO user (username, salted_hash, budget_spent, role) VALUES (?, ?, ?, ?)")
	db.checkErr(err)
	if err != nil {
		return err
	}

	_, err = statement.Exec(username, saltedHash, budgetSpent, role)
	db.checkErr(err)
	if err != nil {
		return err
	}
	return nil
}

// Returns the user with the given username.
//
// username: username of the user
func (db *Database) GetUserWithUsername(username string) *User {
	row := db.Database.QueryRow("SELECT * FROM user WHERE username=?", username)
	var id int64
	var name string
	var saltedpass string
	var budgetspent int64
	var role string
	err := row.Scan(&id, &name, &saltedpass, &budgetspent, &role)
	db.checkErr(err)
	user := User{id, name, saltedpass, budgetspent, role}
	return &user
}

// TODO: add site query was sent to
// Creates a table containing all the diff priv queries sent
// to Leap.
//
// No args.
func (db *Database) CreateQueryTable() {
	statement, err := db.Database.Prepare("CREATE TABLE IF NOT EXISTS query (id INTEGER PRIMARY KEY, req_id INTEGER, user_id INTEGER, site_id INTEGER, epsilon REAL, delta REAL, FOREIGN KEY (user_id) REFERENCES user (id))")
	db.checkErr(err)
	_, err = statement.Exec()
	db.checkErr(err)
}

// Inserts a new query to the table
//
// query: Query struc containing the eps and delta values
func (db *Database) InsertQuery(query Query) error {
	statement, err := db.Database.Prepare("INSERT INTO query (req_id, user_id, site_id, epsilon, delta) VALUES (?, ?, ?, ?, ?)")
	db.checkErr(err)
	if err != nil {
		return err
	}

	_, err = statement.Exec(query.ReqId, query.UserId, query.SiteId, query.Epsilon, query.Delta)
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
		rows.Scan(&query.Id, &query.ReqId, &query.UserId, &query.SiteId, &query.Epsilon, &query.Delta)
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
	statement, err := db.Database.Prepare("CREATE TABLE IF NOT EXISTS site_access (id INTEGER PRIMARY KEY, site_id INTEGER, user_id INTEGER, FOREIGN KEY (user_id) REFERENCES user (id), FOREIGN KEY (site_id) REFERENCES site_id (id))")
	db.checkErr(err)
	_, err = statement.Exec()
	db.checkErr(err)
}

// Inserts a new site access to the table
//
// siteaccess: SiteAccess struc containing ids
func (db *Database) InsertSiteAccess(siteAccess *SiteAccess) error {
	statement, err := db.Database.Prepare("INSERT INTO site_access (id, site_id, user_id) VALUES (?, ?, ?)")
	db.checkErr(err)
	if err != nil {
		return err
	}

	_, err = statement.Exec(siteAccess.Id, siteAccess.SiteId, siteAccess.UserId)
	db.checkErr(err)
	if err != nil {
		return err
	}
	return nil
}

// Returns all sites accessible for the user with the given ID.
//
// userId: Id of the user to return sites accessible
func (db *Database) GetSiteAccessFromUser(userId int) ([]SiteAccess, error) {
	rows, err := db.Database.Query("SELECT * FROM site_access WHERE user_id=?", userId)
	db.checkErr(err)

	if err != nil {
		return []SiteAccess{}, err
	}

	lenRows := 0
	site_accesses := []SiteAccess{}
	for rows.Next() {
		siteAccess := SiteAccess{}
		rows.Scan(&siteAccess.Id, &siteAccess.SiteId, &siteAccess.UserId)
		site_accesses = append(site_accesses, siteAccess)
		lenRows++
	}

	if lenRows == 0 {
		return []SiteAccess{}, errors.New("No site access for user")
	}

	return site_accesses, nil
}

// Creates a table containing all the sites and privacy budgets
//
// No args.
func (db *Database) CreateSiteTable() {
	statement, err := db.Database.Prepare("CREATE TABLE IF NOT EXISTS site (id INTEGER PRIMARY KEY, budget REAL)")
	db.checkErr(err)
	_, err = statement.Exec()
	db.checkErr(err)
}

// Inserts a new site to the table
//
// site Site struc containing id and budget
func (db *Database) InsertSite(site *Site) error {
	statement, err := db.Database.Prepare("INSERT INTO site (id, budget) VALUES (?, ?)")
	db.checkErr(err)
	if err != nil {
		return err
	}

	_, err = statement.Exec(site.Id, site.Budget)
	db.checkErr(err)
	if err != nil {
		return err
	}
	return nil
}

// Returns the site with the given site id.
//
// siteId: id of the site
func (db *Database) GetSiteFromId(siteId int) Site {
	row := db.Database.QueryRow("SELECT * FROM site WHERE id=?", siteId)
	var id int64
	var budget float64
	err := row.Scan(&id, &budget)
	db.checkErr(err)
	site := Site{id, budget}
	return site
}

// Returns the budget spent so far by a user for a specific site
//
// siteId: id of the site that is queried
// userId: id of the user who has issued queries
func (db* Database) GetSiteBudgetSpentByUser(siteId int, userId int) (float64, float64) {
	rows, err := db.Database.Query("SELECT * FROM query WHERE user_id=? AND site_id=?", userId, siteId)
	db.checkErr(err)

	epsilonSum := float64(0)
	deltaSum := float64(0)
	for rows.Next() {
		query := Query{}
		rows.Scan(&query.Id, &query.ReqId, &query.UserId, &query.SiteId, &query.Epsilon, &query.Delta)
		epsilonSum += query.Epsilon
		deltaSum += query.Delta
	}
	return epsilonSum, deltaSum
}

// Logs an error.
//
// err: The error to be logged.
func (db *Database) checkErr(err error) {
	if err != nil {
		db.Log.Error(err.Error())
	}
}
