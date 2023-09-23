// main.go
package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"syscall"

	"github.com/go-kit/kit/log"
	httptransport "github.com/go-kit/kit/transport/http"
	"github.com/gorilla/mux"
)

func main() {
	var (
		httpAddr = flag.String("http.addr", ":5000", "HTTP listen address")
	)
	flag.Parse()

	logger := log.NewLogfmtLogger(os.Stderr)
	logger = log.With(logger, "ts", log.DefaultTimestampUTC, "caller", log.DefaultCaller)

	var svc MyService
	svc = myService{} // Implement your service

	// Define endpoints
	endpoints := MakeEndpoints(svc)

	// Create router and HTTP handler
	r := mux.NewRouter()
	r.Methods("POST").Path("/whatsapp").Handler(httptransport.NewServer(
		endpoints.MyEndpoint,
		DecodeMyRequest,
		EncodeResponse,
	))

	http.Handle("/", r)

	errs := make(chan error, 2)
	go func() {
		c := make(chan os.Signal, 1)
		signal.Notify(c, syscall.SIGINT, syscall.SIGTERM)
		errs <- fmt.Errorf("%s", <-c)
	}()

	go func() {
		logger.Log("transport", "HTTP", "addr", *httpAddr)
		errs <- http.ListenAndServe(*httpAddr, nil)
	}()

	logger.Log("exit", <-errs)
}

// MyService represents your service interface
type MyService interface {
	MyEndpoint(context.Context, MyRequest) (MyResponse, error)
}

// myService is the implementation of MyService
type myService struct{}

func (s myService) MyEndpoint(ctx context.Context, req MyRequest) (MyResponse, error) {
	// Implement your service logic here
	return MyResponse{Message: "Hello, " + req.Name + "!"}, nil
}

// MyRequest represents the request data
type MyRequest struct {
	Name string `json:"name"`
}

// MyResponse represents the response data
type MyResponse struct {
	Message string `json:"message"`
}

// MakeEndpoints creates endpoints for your service
func MakeEndpoints(svc MyService) Endpoints {
	return Endpoints{
		MyEndpoint: MakeMyEndpoint(svc),
	}
}

// Endpoints struct holds all Go-Kit endpoints
type Endpoints struct {
	MyEndpoint endpoint.Endpoint
}

// MakeMyEndpoint creates a Go-Kit endpoint for MyEndpoint
func MakeMyEndpoint(svc MyService) endpoint.Endpoint {
	return func(ctx context.Context, request interface{}) (interface{}, error) {
		req := request.(MyRequest)
		response, err := svc.MyEndpoint(ctx, req)
		if err != nil {
			return nil, err
		}
		return response, nil
	}
}

// DecodeMyRequest decodes the HTTP request into MyRequest struct
func DecodeMyRequest(_ context.Context, r *http.Request) (interface{}, error) {
	var req MyRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		return nil, err
	}
	return req, nil
}

// EncodeResponse encodes the response as JSON
func EncodeResponse(_ context.Context, w http.ResponseWriter, response interface{}) error {
	return json.NewEncoder(w).Encode(response)
}
