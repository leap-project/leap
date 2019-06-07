package Concurrent

import "sync"

// A map data structure that can be used concurrently
type Map struct {
	sync.RWMutex
	items map[interface{}]interface{}
}

// An item in the map
type Item struct {
	Key   interface{}
	Value interface{}
}

// Creates a new map that is able to safely handle concurrency.
//
// No args
func NewMap() *Map {
	m := Map{items: make(map[interface{}]interface{})}
	return &m
}

// A function that sets the given value at the given key.
// This function locks the map for writing while setting
// the key.
//
// key: A key to be associated with a value.
// value: A value to be set at the key.
func (m *Map) Set(key interface{}, value interface{}) {
	m.Lock()
	defer m.Unlock()
	m.items[key] = value
}

// A function that returns the given value at a key and returns
// whether the given value exists.
//
// key: A key in the map.
func (m *Map) Get(key interface{}) (value interface{}, ok bool) {
	m.Lock()
	defer m.Unlock()
	value, ok = m.items[key]
	return value, ok
}

// A function that deletes the value associated with the
// given key.
//
// key: The key of the value to be deleted.
func (m *Map) Delete(key interface{}) {
	m.Lock()
	defer m.Unlock()
	delete(m.items, key)
}

// Allows the builtin range keyword to be used for iterating
// over the concurrent map.
//
// No args
func (m *Map) Iter() <- chan Item {
	c := make(chan Item)
	go m.sendItemsOverChannel(&c)
	return c
}

// Each item in the map is sent over a channel, so that the
// builtin range keyword can be used.
//
// c: Channel used to send the items of the map.
func (m *Map) sendItemsOverChannel(c *chan Item) {
	m.Lock()
	defer m.Unlock()

	for k, v := range m.items {
		*c <- Item{k, v}
	}
	close(*c)
}

