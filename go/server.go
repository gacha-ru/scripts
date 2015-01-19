// server.go
package main

import "github.com/go-martini/martini"

func main() {
	m := martini.Classic()
	m.Get("/", top)
	m.Run()
}

func top(params martini.Params) (int, string) {
	return 200, "Hello!"
}
