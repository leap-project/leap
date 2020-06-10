package coordinator

import (
	"context"
	"errors"
	"github.com/dgrijalva/jwt-go"
	"golang.org/x/crypto/bcrypt"
	pb "leap/proto"
	"time"
	"leap/sqlite"
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
	user := sqlite.User{Name: req.User.Username, SaltedPass: string(saltedPasswordHash), BudgetSpent: 0}
	err = c.Database.InsertUser(&user)

	if err != nil {
		return &pb.UserRegRes{Success: false}, err
	}

	c.Log.Info("User successfully registered")

	return &pb.UserRegRes{Success: true}, nil
}

func (c *Coordinator) AuthUser(ctx context.Context, req *pb.UserAuthReq) (*pb.UserAuthRes, error) {
	c.Log.Info("Received request to authenticate user")

	user := c.Database.GetUserWithUsername(req.User.Username)
	passwordHash := user.SaltedPass

	err := bcrypt.CompareHashAndPassword([]byte(passwordHash), []byte(req.User.Password))
	if err != nil {
		c.Log.Error(err)
		return &pb.UserAuthRes{Success: false}, errors.New("Wasn't able to authenticate user. Password or username incorrect.")
	}

	// Create token that lasts for 15 minutes
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"issuer": "leap",
		"sub": req.User.Username,
		"exp": time.Now().Add(15 * time.Minute),
		"iat": time.Now().UTC().Unix(),
	})

	// TODO: Generate secret key for signing instead of using testSecret
	tokenString, err := token.SignedString([]byte("testSecret"))

	checkErr(c, err)

	return &pb.UserAuthRes{Success: true, Token: tokenString}, nil
}
