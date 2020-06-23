package leaptests

import (
	"database/sql"
	"leap/sqlite"
	"os"
	"testing"
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
	db.CreateSiteTable()
	db.CreateSiteAccessTable()
}

func teardown() {
	db.Database.Close()
	os.Remove("./test-db:mode=memory")
}

func TestInsertQuery(t *testing.T) {
	err := db.InsertQuery(sqlite.Query{ReqId: 1, UserId: 2, SiteId: 3, Epsilon: 0.1, Delta: 0})

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

	if queries[0].SiteId != 3 {
		t.Errorf("Site id not inserted correctly")
	}

	if queries[0].Epsilon != 0.1 {
		t.Errorf("Epsilon not inserted correctly")
	}

	if queries[0].Delta != 0 {
		t.Errorf("Delta not inserted correctly")
	}
}

func TestMultipleInserts(t *testing.T) {

	err := db.InsertQuery(sqlite.Query{ReqId: 2, UserId: 4, SiteId: 5, Epsilon: 0.1, Delta: 0})
	if err != nil {
		t.Errorf(err.Error())
	}

	err = db.InsertQuery(sqlite.Query{ReqId: 3, UserId: 4, SiteId: 6, Epsilon: 0.2, Delta: 0.3})
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

	if queries[0].SiteId != 5 {
		t.Errorf("Site id not inserted correctly")
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

	if queries[1].SiteId != 6 {
		t.Errorf("Site id not inserted correctly")
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

func TestInsertMultipleUsers(t *testing.T) {
	err := db.InsertUser(&sqlite.User{Id: 2, Name: "Sally", SaltedPass: "pass234", BudgetSpent: 1})
	if err != nil {
		t.Errorf(err.Error())
	}

	err = db.InsertUser(&sqlite.User{Id: 3, Name: "Alex", SaltedPass: "pw1234", BudgetSpent: 2})
	if err != nil {
		t.Errorf(err.Error())
	}

	user := db.GetUserWithUsername("Sally")
	// Check user
	if user.Id != 2 {
		t.Errorf("User Id not inserted correctly")
	}

	if user.Name != "Sally" {
		t.Errorf("Username not inserted correctly")
	}

	if user.SaltedPass != "pass234" {
		t.Errorf("SaltedPass not inserted correctly")
	}

	if user.BudgetSpent != 1 {
		t.Errorf("BudgetSpent not inserted correctly")
	}

	user = db.GetUserWithUsername("Alex")
	// Second user
	if user.Id != 3 {
		t.Errorf("User Id not inserted correctly")
	}

	if user.Name != "Alex" {
		t.Errorf("Username not inserted correctly")
	}

	if user.SaltedPass != "pw1234" {
		t.Errorf("SaltedPass not inserted correctly")
	}

	if user.BudgetSpent != 2 {
		t.Errorf("BudgetSpent not inserted correctly")
	}
}

func TestInsertSite(t *testing.T) {
	err := db.InsertSite(&sqlite.Site{Id: 5, EpsilonBudget: 2.5, DeltaBudget: 0.5})
	if err != nil {
		t.Errorf(err.Error())
	}

	site := db.GetSiteFromId(5)
	// Check site
	if site.Id != 5 {
		t.Errorf("Site id not inserted correctly")
	}

	if site.EpsilonBudget != 2.5 {
		t.Errorf("Site epsilon budget not inserted correctly")
	}

	if site.DeltaBudget != 0.5 {
		t.Errorf("Site delta budget not inserted correctly")
	}
}

func TestInsertMultipleSites(t *testing.T) {
	err := db.InsertSite(&sqlite.Site{Id: 1, EpsilonBudget: 0, DeltaBudget: 0.1})
	if err != nil {
		t.Errorf(err.Error())
	}

	err = db.InsertSite(&sqlite.Site{Id: 4, EpsilonBudget: 0.5, DeltaBudget: 0.75})
	if err != nil {
		t.Errorf(err.Error())
	}

	site := db.GetSiteFromId(1)
	// First site
	if site.Id != 1 {
		t.Errorf("Site id not inserted correctly")
	}

	if site.EpsilonBudget != 0 {
		t.Errorf("Site epsilon budget not inserted correctly")
	}

	if site.DeltaBudget != 0.1 {
		t.Errorf("Site delta budget not inserted correctly")
	}

	site = db.GetSiteFromId(4)
	// Second site
	if site.Id != 4 {
		t.Errorf("Site id not inserted correctly")
	}

	if site.EpsilonBudget != 0.5 {
		t.Errorf("Site epsilon budget not inserted correctly")
	}

	if site.DeltaBudget != 0.75 {
		t.Errorf("Site delta budget not inserted correctly")
	}
}

func TestInsertSiteAccess(t *testing.T) {
	err := db.InsertSiteAccess(&sqlite.SiteAccess{Id: 1, SiteId: 5, UserId: 1})
	if err != nil {
		t.Errorf(err.Error())
	}

	siteaccesses, err := db.GetSiteAccessFromUser(1)

	// Check site access
	if siteaccesses[0].Id != 1 {
		t.Errorf("Site access id not inserted correctly")
	}

	if siteaccesses[0].SiteId != 5 {
		t.Errorf("Site id not inserted correctly")
	}

	if siteaccesses[0].UserId != 1 {
		t.Errorf("User id not inserted correctly")
	}
}

func TestInsertMultipleSiteAccess(t *testing.T) {
	err := db.InsertSiteAccess(&sqlite.SiteAccess{Id: 2, SiteId: 1, UserId: 3})
	if err != nil {
		t.Errorf(err.Error())
	}

	err = db.InsertSiteAccess(&sqlite.SiteAccess{Id: 3, SiteId: 4, UserId: 3})
	if err != nil {
		t.Errorf(err.Error())
	}

	siteaccesses, err := db.GetSiteAccessFromUser(3)
	// Check site accesses
	if len(siteaccesses) != 2 {
		t.Errorf("Two site accesses not inserted")
	}

	// Check site access
	if siteaccesses[0].Id != 2 {
		t.Errorf("Site access id not inserted correctly")
	}

	if siteaccesses[0].SiteId != 1 {
		t.Errorf("Site id not inserted correctly")
	}

	if siteaccesses[0].UserId != 3 {
		t.Errorf("User id not inserted correctly")
	}


	// Second site access
	if siteaccesses[1].Id != 3 {
		t.Errorf("Site access id not inserted correctly")
	}

	if siteaccesses[1].SiteId != 4 {
		t.Errorf("Site id not inserted correctly")
	}

	if siteaccesses[1].UserId != 3 {
		t.Errorf("User id not inserted correctly")
	}
}

func TestGetSiteBudgetSpentByUser(t *testing.T) {
	// insert new site
	err := db.InsertSite(&sqlite.Site{Id: 11, EpsilonBudget: 0.5, DeltaBudget: 0.1})
	if err != nil {
		t.Errorf(err.Error())
	}
	// insert new user
	err = db.InsertUser(&sqlite.User{Id: 22, Name: "Max", SaltedPass: "pw123", BudgetSpent: 0, Role: "admin"})
	if err != nil {
		t.Errorf(err.Error())
	}
	// insert new siteaccess
	err = db.InsertSiteAccess(&sqlite.SiteAccess{Id: 5, SiteId: 11, UserId: 22})
	if err != nil {
		t.Errorf(err.Error())
	}
	// insert some queries
	err = db.InsertQuery(sqlite.Query{Id: 200, ReqId: 10, UserId: 22, SiteId: 11, Epsilon: 0, Delta: 0})
	if err != nil {
		t.Errorf(err.Error())
	}
	eps, delta := db.GetSiteBudgetSpentByUser(11, 22)
	if eps != 0 {
		t.Errorf("Epsilon for site is retrieved incorrectly")
	}
	if delta != 0 {
		t.Errorf("Delta for site is retrieved incorrectly")
	}

	err = db.InsertQuery(sqlite.Query{Id: 201, ReqId: 11, UserId: 22, SiteId: 11, Epsilon: 1.0, Delta: 0.9})
	err = db.InsertQuery(sqlite.Query{Id: 202, ReqId: 12, UserId: 22, SiteId: 11, Epsilon: 0.1, Delta: 1.3})

	// sum up epsilon & deltas
	eps, delta = db.GetSiteBudgetSpentByUser(11, 22)
	if eps != 1.1 {
		t.Errorf("Epsilon for site is retrieved incorrectly")
	}
	if delta != 2.2 {
		t.Errorf("Delta for site is retrieved incorrectly")
	}
}
