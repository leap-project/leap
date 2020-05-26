package coordinator

import (
	"context"
	"errors"
	"golang.org/x/crypto/bcrypt"
	pb "leap/proto"
)

type User struct {
	Username     string
	SaltedPasswordHash string
	SiteAccess   []int64
	BudgetSpent  int64
}

func (c *Coordinator) RegisterUser(ctx context.Context, req *pb.UserRegReq) (*pb.UserRegRes, error) {
	c.Log.Info("Received request to register user")

	if c.Users.Contains(req.User.Username) {
		c.Log.Warn("User with given username already exists: " + req.User.Username)
		return &pb.UserRegRes{Success: false}, errors.New("User with given username already exists")
	}

	saltedPasswordHash, err := bcrypt.GenerateFromPassword([]byte(req.User.Password), bcrypt.DefaultCost)
	checkErr(c, err)
	user := User{Username: req.User.Username, SaltedPasswordHash: string(saltedPasswordHash) , SiteAccess: []int64{}, BudgetSpent: 0}
	c.Users.Set(user.Username, user)

	c.Log.Info("User successfully registered")

	return &pb.UserRegRes{Success: true}, nil
}

func (c *Coordinator) AuthUser(ctx context.Context, req *pb.UserAuthReq) (*pb.UserAuthRes, error) {
	c.Log.Info("Received request to authenticate user")

	if !c.Users.Contains(req.User.Username) {
		c.Log.Warn("Wasn't able to authenticate user. Password or username incorrect.")
		return &pb.UserAuthRes{Success: false}, errors.New("Wasn't able to authenticate user. Password or username incorrect.")
	}

	item := c.Users.Get(req.User.Username)
	user := item.(User)

	err := bcrypt.CompareHashAndPassword([]byte(user.SaltedPasswordHash), []byte(req.User.Password))
	if err != nil {
		c.Log.Error(err)
		return &pb.UserAuthRes{Success: false}, errors.New("Wasn't able to authenticate user. Password or username incorrect.")
	}
	return &pb.UserAuthRes{Success: true}, nil
}
