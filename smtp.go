package main

import (
	"fmt"

	"github.com/flashmob/go-guerrilla"
)

func main() {
	cfg := &guerrilla.AppConfig{}

	sc := guerrilla.ServerConfig{
		ListenInterface: ":8006",
		IsEnabled:       true,
	}
	cfg.Servers = append(cfg.Servers, sc)
	d := guerrilla.Daemon{Config: cfg}
	err := d.Start()

	if err == nil {
		fmt.Println("Server Started!")
	}
	
	select{}
}
