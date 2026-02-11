# ECE158B_PA1

## Topic 2: Web Proxy Server

Note: The skeleton code is separated into multiple files to better collaborate and avoid merge conflicts. For cache to work, make sure to create a `cache` folder in the root of this repository.

### (1) (30pt) Implement the Proxy Server based on Skeleton Code. (DONE)

To test GET support:

```
curl -v -x http://localhost:8888 http://eu.httpbin.org/
```

### (2) (25pt) Adding support for POST.

To test POST support:

```
curl -v -x http://localhost:8888 \                     
  -X POST http://eu.httpbin.org/post \
  -d "test_post_support_for_my_proxy_server"
```

### (3) (45pt) Support for Web Caching.
