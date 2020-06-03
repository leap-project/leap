package coordinator

import (
	"context"
	"errors"
	"golang.org/x/crypto/bcrypt"
	pb "leap/proto"
)

type User struct {
	Username           string
	SaltedPasswordHash string
	SiteAccess         []int64
	BudgetSpent        int64
}

// TODO: Sanitize inputs or check if sqlite3 go package does it

func (c *Coordinator) RegisterUser(ctx context.Context, req *pb.UserRegReq) (*pb.UserRegRes, error) {
	c.Log.Info("Received request to register user")

	saltedPasswordHash, err := bcrypt.GenerateFromPassword([]byte(req.User.Password), bcrypt.DefaultCost)
	checkErr(c, err)
	err = c.Database.InsertUser(req.User.Username, string(saltedPasswordHash), 0)

	if err != nil {
		return &pb.UserRegRes{Success: false}, err
	}

	c.Log.Info("User successfully registered")

	return &pb.UserRegRes{Success: true}, nil
}

func (c *Coordinator) AuthUser(ctx context.Context, req *pb.UserAuthReq) (*pb.UserAuthRes, error) {
	c.Log.Info("Received request to authenticate user")

	_, _, passwordHash, _ := c.Database.GetUserWithUsername(req.User.Username)

	err := bcrypt.CompareHashAndPassword([]byte(passwordHash), []byte(req.User.Password))
	if err != nil {
		c.Log.Error(err)
		return &pb.UserAuthRes{Success: false}, errors.New("Wasn't able to authenticate user. Password or username incorrect.")
	}
	return &pb.UserAuthRes{Success: true}, nil
}
