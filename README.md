# ECE158B_PA1

## Topic 2: Web Proxy Server

Note: The skeleton code is separated into multiple files to better collaborate and avoid merge conflicts.  
For cache to work, make sure to create a `cache/` folder in the root of this repository.

---

### How to run the proxy server

In one terminal (from the repo root):

```bash
mkdir -p cache
python3 ProxyServer.py <server_ip>
```

Your proxy server should listen on:

- `http://<server_ip>:8888`

---

### (1) (30pt) Implement the Proxy Server based on Skeleton Code.

To test GET support, run this command in your terminal:

```
curl -v -x http://localhost:8888 http://eu.httpbin.org/
```


### (2) (25pt) Adding support for POST.

To test POST support, run this command in your terminal:

```
curl -v -x http://localhost:8888 \
  -X POST http://eu.httpbin.org/post \
  -d "test_post_support_for_my_proxy_server"
```

### (3) (45pt) Support for Web Caching.

I implemented caching with a simple Python dict where:

- key = `filename`
- value = the path to the cached file saved under the `cache/` folder

---
### Demo video

Demo video link: ([Video](https://app.screencastify.com/watch/sboWlJitArgSINyDmzFs?checkOrg=12b78290-b232-449e-8113-4c1a1a79fb0c))
