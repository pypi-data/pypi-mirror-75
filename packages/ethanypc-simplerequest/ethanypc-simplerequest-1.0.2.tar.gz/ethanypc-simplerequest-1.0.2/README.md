# ethanypc-simplerequest




A simpler API built on top of Python's http.client. 

Support for Python 3 only.


# Install  

```bash
# from pypi
pip install ethanypc-simplerequest

# from testpypi
pip install -i https://test.pypi.org/simple/ ethanypc-simplerequest
```

# Usage

```python
import simplehttp

r = simplehttp.get_json("https://httpbin.org/get")
assert r["args"] == {}  

r2 = simplehttp.get_json("https://httpbin.org/get?debug=true",
				 params={"name": "常⾒見見問題 Q&A"})
assert r2["args"] == {"debug": "true", "name": "常⾒見見問題 Q&A"}


data = {"isbn": "9789863479116", "title": u"流暢的 Python"}
r3 = simplehttp.post_json("https://httpbin.org/post",
			 params={"debug": "true"}, data=data)
assert r3["args"] == {"debug": "true"}
assert json.loads(r3["json"]) == data
```
