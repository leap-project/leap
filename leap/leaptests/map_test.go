package leaptests

import (
	"leap/utils"
	"testing"
)

func TestSet(t *testing.T) {
	cmap := utils.NewMap()
	cmap.Set("test", 5)
	val := cmap.Get("test")
	length := cmap.Length()
	if val != 5 {
		t.Errorf("Get was incorrect, got: %d, want: %d.", val, 5)
	}
	if length != 1 {
		t.Errorf("Length was incorrect, got: %d, want: %d.", length, 1)
	}
}

func TestContains(t *testing.T) {
	cmap := utils.NewMap()
	cmap.Set("test", 7)
	contains := cmap.Contains("test")
	length := cmap.Length()

	if contains != true {
		t.Errorf("Contains was incorrect, got: %t, want: %t.", contains, true)
	}
	if length != 1 {
		t.Errorf("Length was incorrect, got: %d, want: %d.", length, 1)
	}

	contains = cmap.Contains("blah")
	if contains != false {
		t.Errorf("Contains was incorrect, got: %t, want: %t.", contains, false)
	}
}

func TestDelete(t *testing.T) {
	cmap := utils.NewMap()
	cmap.Set("test", 7)
	cmap.Delete("test")
	contains := cmap.Contains("test")
	length := cmap.Length()

	if contains != false {
		t.Errorf("Contains was incorrect, got: %t, want: %t.", contains, false)
	}
	if length != 0 {
		t.Errorf("Length was incorrect, got: %d, want: %d.", length, 0)
	}
}
