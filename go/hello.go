package main

import (
	"./foobar"
	"./otaso"
	"fmt"
)

func main() {
	s := []string{"otaso", "slime"}
	otaso.Yutao(s[0])
	otaso.Yutao(s[1])
	otaso.Yuiteso(s[1])
	sum := 0

	fmt.Println(s)
	fmt.Print(s[0])

	for i := 0; i < 10; i++ {
		sum += 1
		fmt.Println(sum)
	}
	foobar.Bar()
}
