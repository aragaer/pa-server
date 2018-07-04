package main

import (
	"strings"

	"github.com/flashmob/go-guerrilla/backends"
	"github.com/flashmob/go-guerrilla/mail"
	"github.com/flashmob/go-guerrilla/response"
)

var LdaValidator = func() backends.Decorator {
	return func(c backends.Processor) backends.Processor {
		return backends.ProcessWith(func(e *mail.Envelope, task backends.SelectTask) (backends.Result, error) {
			if task != backends.TaskValidateRcpt {
				return c.Process(e, task)
			}
			if err := LdaValidate(e); err != nil {
				return backends.NewResult(response.Canned.FailRcptCmd), err
			}
			return c.Process(e, task)
		})
	}
}

func LdaValidate(e *mail.Envelope) error {
	for _, r := range e.RcptTo {
		u := strings.ToLower(r.User)
		backends.Log().Info("Mail to ", u)
	}
	return nil
}
