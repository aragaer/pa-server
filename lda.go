package main

import (
	"strings"

	"github.com/flashmob/go-guerrilla/backends"
	"github.com/flashmob/go-guerrilla/mail"
)

var LdaSaver = func() backends.Decorator {
	return func(c backends.Processor) backends.Processor {
		return backends.ProcessWith(func(e *mail.Envelope, task backends.SelectTask) (backends.Result, error) {
			if task != backends.TaskSaveMail {
				return c.Process(e, task)
			}
			if err := LdaSave(e); err != nil {
				return backends.NewResult("554 Error: could not save email"), err
			}
			return c.Process(e, task)
		})
	}
}

func LdaSave(e *mail.Envelope) error {
	for _, r := range e.RcptTo {
		u := strings.ToLower(r.User)
		backends.Log().Info("Deliver to ", u)
	}
	return nil
}
