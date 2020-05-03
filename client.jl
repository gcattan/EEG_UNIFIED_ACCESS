using HTTP

r = HTTP.request("GET", "http://127.0.0.1:8585/ping?please"; verbose = 3)
# r = HTTP.request("GET", "http://httpbin.org/ip"; verbose = 3)
println(r.status)
println(String(r.body))
