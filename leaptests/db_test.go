package leaptests

import (
	"database/sql"
	"os"
	"testing"
	"leap/sqlite"
)

var db sqlite.Database

func TestMain(m *testing.M) {
	setup()
	code := m.Run()
	teardown()
	os.Exit(code)
}

func setup() {
	db = sqlite.Database{Name: "test-db"}
	database, _ := sql.Open("sqlite3", "test-db"+":mode=memory")
	db.Database = database
	db.CreateQueryTable()
	db.CreateUserTable()
}

func teardown() {
	db.Database.Close()
	os.Remove("./test-db:mode=memory")
}

func TestInsertQuery(t *testing.T) {
	err := db.InsertQuery(sqlite.Query{ReqId: 1, UserId: 2, Epsilon: 0.1, Delta: 0})

	if err != nil {
		t.Errorf(err.Error())
	}
	queries, err := db.GetQueriesFromUser(2)

	if err != nil {
		t.Errorf(err.Error())
	}

	if queries[0].ReqId != 1 {
		t.Errorf("Request id not inserted correctly")
	}

	if queries[0].UserId != 2 {
		t.Errorf("User id not inserted correctly")
	}

	if queries[0].Epsilon != 0.1 {
		t.Errorf("Epsilon not inserted correctly")
	}

	if queries[0].Delta != 0 {
		t.Errorf("Delta not inserted correctly")
	}
}

func TestMultipleInserts(t *testing.T) {

	err := db.InsertQuery(sqlite.Query{ReqId: 2, UserId: 4, Epsilon: 0.1, Delta: 0})
	if err != nil {
		t.Errorf(err.Error())
	}

	err = db.InsertQuery(sqlite.Query{ReqId: 3, UserId: 4, Epsilon: 0.2, Delta: 0.3})
	if err != nil {
		t.Errorf(err.Error())
	}

	queries, err := db.GetQueriesFromUser(4)

	if len(queries) != 2 {
		t.Errorf("Two queries not inserted")
	}

	// First query
	if queries[0].ReqId != 2 {
		t.Errorf("Request id not inserted correctly")
	}

	if queries[0].UserId != 4 {
		t.Errorf("User id not inserted correctly")
	}

	if queries[0].Epsilon != 0.1 {
		t.Errorf("Epsilon not inserted correctly")
	}

	if queries[0].Delta != 0 {
		t.Errorf("Delta not inserted correctly")
	}

	// Second query
	if queries[1].ReqId != 3 {
		t.Errorf("Request id not inserted correctly")
	}

	if queries[1].UserId != 4 {
		t.Errorf("User id not inserted correctly")
	}

	if queries[1].Epsilon != 0.2 {
		t.Errorf("Epsilon not inserted correctly")
	}

	if queries[1].Delta != 0.3 {
		t.Errorf("Delta not inserted correctly")
	}
}

func TestGetNonExistentQuery(t *testing.T) {
	queries, _ := db.GetQueriesFromUser(5)

	if len(queries) != 0 {
		t.Errorf("Length of queries returned != 0")
	}
}

func TestInsertUser(t *testing.T) {
	err := db.InsertUser(&sqlite.User{Id: 1, Name: "Bob", SaltedPass: "pass123", BudgetSpent: 0, Role: "admin"})
	if err != nil {
		t.Errorf(err.Error())
	}

	user := db.GetUserWithUsername("Bob")
	// Check user
	if user.Id != 1 {
		t.Errorf("User Id not inserted correctly")
	}

	if user.Name != "Bob" {
		t.Errorf("Username not inserted correctly")
	}

	if user.SaltedPass != "pass123" {
		t.Errorf("SaltedPass not inserted correctly")
	}

	if user.BudgetSpent != 0 {
		t.Errorf("BudgetSpent not inserted correctly")
	}

	if user.Role != "admin" {
		t.Errorf("User role not inserted correctly")
	}
}
