package main

import (
	"fmt"

	"github.com/flashmob/go-guerrilla"
)

func main() {
	d := guerrilla.Daemon{}
	d.AddProcessor("LdaValidator", LdaValidator)
	d.AddProcessor("LdaSaver", LdaSaver)

	if _, err := d.LoadConfig("server.conf"); err != nil {
		fmt.Println("LoadConfig failed", err)
		return
	}
	if err := d.Start(); err != nil {
		fmt.Println("Server start failed", err)
		return
	}
	fmt.Println("Server Started!")

	select {}
}
